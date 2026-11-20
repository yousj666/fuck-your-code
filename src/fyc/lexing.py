"""Lexical facts about source files.

This module answers the humble questions every check depends on:
which language is this, which lines are comments or docstrings,
where does each function start and end, how deep does the nesting
go, what gets imported, and which lines belong to module-level
constant assignments. Everything here is approximate on purpose;
the tool grades mess, it does not compile anything.
"""

import os
import re

from fyc import constants

PY_FUNC_RE = re.compile(r"^\s*(?:async\s+)?def\s+(\w+)\s*\(")
JS_FUNC_RE = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(")
JS_METHOD_RE = re.compile(r"^\s*(?:public\s+|private\s+|protected\s+|static\s+)*"
                          r"function\s+(\w+)\s*\(")
JS_ARROW_RE = re.compile(r"^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(")
GO_FUNC_RE = re.compile(r"^\s*func\s+(?:\([^)]*\)\s*)?(\w+)\s*\(")
RUST_FUNC_RE = re.compile(r"^\s*(?:pub\s+)?(?:async\s+)?fn\s+(\w+)\s*\(")
RUBY_FUNC_RE = re.compile(r"^\s*def\s+(\w+)")
SCALA_FUNC_RE = re.compile(r"^\s*(?:private\s+|protected\s+|override\s+)*"
                           r"def\s+(\w+)")
KOTLIN_FUNC_RE = re.compile(r"^\s*(?:public\s+|private\s+|protected\s+|"
                            r"internal\s+|open\s+|final\s+)*fun\s+(\w+)\s*\(")
SWIFT_FUNC_RE = re.compile(r"^\s*(?:public\s+|private\s+|internal\s+|open\s+|"
                           r"final\s+|static\s+)*func\s+(\w+)\s*\(")
SHELL_FUNC_RE = re.compile(r"^\s*(\w+)\s*\(\)\s*\{?")
JAVA_FUNC_RE = re.compile(r"^\s*(?:[\w<>\[\]\.,]|\s)+?\s(\w+)\s*\([^;]*\)"
                          r"\s*(?:\{|throws\b[^{]*)?\s*$")
GENERIC_FUNC_RE = re.compile(r"^\s*(?:def|function|fn|func)\s+(\w+)\s*\(")
FUNC_PATTERNS = {
    "python": [PY_FUNC_RE],
    "javascript": [JS_FUNC_RE, JS_METHOD_RE, JS_ARROW_RE],
    "go": [GO_FUNC_RE],
    "rust": [RUST_FUNC_RE],
    "ruby": [RUBY_FUNC_RE],
    "scala": [SCALA_FUNC_RE],
    "kotlin": [KOTLIN_FUNC_RE],
    "swift": [SWIFT_FUNC_RE],
    "shell": [SHELL_FUNC_RE],
    "java": [JAVA_FUNC_RE],
}


def detect_lang(path, ext_hint=None):
    """Return the language name and extension for a path or hint."""
    if ext_hint:
        ext = ext_hint if ext_hint.startswith(".") else "." + ext_hint
        return constants.EXT_TO_LANG.get(ext.lower(), "text"), ext.lower()
    ext = os.path.splitext(path)[1].lower()
    return constants.EXT_TO_LANG.get(ext, "text"), ext


def is_comment(line, lang_name, in_block, stripped):
    """Say whether a line is a comment, tracking block state."""
    if in_block:
        if "*/" in stripped:
            return True, False
        return True, True
    if lang_name in constants.HASH_COMMENT_LANGS:
        return stripped.startswith("#"), False
    if stripped[:2] == "//":
        return True, False
    if stripped.startswith("/*"):
        return True, ("*/" not in stripped[2:])
    if stripped.startswith("*") and lang_name not in constants.HASH_COMMENT_LANGS:
        return True, False
    if lang_name == "lua" and stripped[:2] == "--":
        return True, False
    return False, False


def scan_comments(lines, lang_name):
    """Collect comment lines, real comment text and docstring lines.

    The returned mapping keeps three sets apart: every line that
    counts as documentation, the text of genuine comments only,
    and the lines belonging to Python docstrings.
    """
    comment_lines = set()
    comment_text = {}
    docstring_lines = set()
    in_block = False
    in_docstring = False
    for index, raw in enumerate(lines):
        stripped = raw.strip()
        is_doc = False
        python_based = lang_name == "python"
        if python_based:
            in_docstring, is_doc = _docstring_state(stripped, in_docstring)
        if is_doc:
            docstring_lines.add(index)
        found = is_doc
        if not found:
            found, in_block = is_comment(raw, lang_name, in_block, stripped)
        if not found:
            continue
        comment_lines.add(index)
        if is_doc:
            continue
        comment_text[index] = _comment_body(stripped)
    return {"comment_lines": comment_lines, "comment_text": comment_text,
            "docstring_lines": docstring_lines}


def _comment_body(text):
    """Strip the comment markers off a comment line, leaving prose."""
    if text.startswith("#"):
        return text.lstrip("#").strip()
    if text[:2] == "//":
        return text[2:].strip()
    body = text
    if body.startswith("/*"):
        body = body[2:]
    if body.endswith("*/"):
        body = body[:-2]
    return body.lstrip("*").strip()


def _docstring_state(stripped, in_docstring):
    """Advance docstring tracking over one Python line.

    Returns the new in-docstring state together with a flag
    saying whether this line belongs to a docstring at all.
    """
    triple_double = constants.DOUBLE_QUOTE * constants.TRIPLE_LEN
    triple_single = constants.SINGLE_QUOTE * constants.TRIPLE_LEN
    quotes = stripped.count(triple_double) + stripped.count(triple_single)
    if in_docstring:
        return quotes == 0, True
    starts = stripped.startswith(triple_double) or stripped.startswith(triple_single)
    if quotes == 1 and starts:
        return True, True
    if quotes >= 2 and len(stripped) > constants.TRIPLE_LEN * 2:
        return False, True
    return False, False


def find_functions(code_lines, lang_name):
    """Approximate the function spans in a file.

    Each result carries the function name, its start index, its
    length in lines, its parameter count and a flag for variadic
    signatures. Spans are measured on the masked code view, so
    parentheses inside strings never confuse the counting.
    """
    patterns = _func_patterns(lang_name)
    starts = []
    for line_no, raw in enumerate(code_lines):
        for pattern in patterns:
            found = pattern.search(raw)
            if found and found.group(1) not in constants.CONTROL_KEYWORDS:
                starts.append((line_no, found.group(1)))
                break
    functions = []
    for order, (start, name) in enumerate(starts):
        if order + 1 < len(starts):
            next_start = starts[order + 1][0]
        else:
            next_start = len(code_lines)
        end = _span_end(code_lines, start, next_start, lang_name)
        params, star = _params_of(code_lines, start, end)
        functions.append({"name": name, "start": start, "line": start + 1,
                          "length": end - start, "end": end,
                          "params": params, "star": star})
    return functions


def _func_patterns(lang_name):
    """Return the function-start patterns for one language family."""
    family = lang_name
    if lang_name in ("typescript", "php"):
        family = "javascript"
    if lang_name in ("csharp", "c", "cpp"):
        family = "java"
    return FUNC_PATTERNS.get(family, [GENERIC_FUNC_RE])


def _span_end(code_lines, start, next_start, lang_name):
    """Return the exclusive end index of a function span."""
    indent_based = lang_name in constants.INDENT_LANGS
    if indent_based:
        def_line = code_lines[start]
        def_indent = len(def_line) - len(def_line.lstrip(" "))
        end = next_start
        pos = start + 1
        while pos < next_start:
            raw = code_lines[pos]
            line_indent = len(raw) - len(raw.lstrip(" "))
            if raw.strip() and line_indent <= def_indent:
                end = pos
                break
            pos += 1
    else:
        end = _brace_span_end(code_lines, start, next_start)
    while end > start + 1 and not code_lines[end - 1].strip():
        end -= 1
    return end


def _brace_span_end(code_lines, start, next_start):
    """End a brace-based span where the brace balance closes."""
    balance = 0
    seen_open = False
    cursor = start
    while cursor < next_start:
        raw = code_lines[cursor]
        balance += raw.count("{") - raw.count("}")
        if "{" in raw:
            seen_open = True
        cursor += 1
        if seen_open and balance <= 0:
            return cursor
    if not seen_open:
        return start + 1
    return next_start


def _params_of(code_lines, start, end):
    """Extract the parameter count and variadic flag of a function."""
    text = "\n".join(code_lines[start:end])
    open_index = text.find("(")
    if open_index == -1:
        return 0, False
    balance = 0
    close_index = len(text)
    for index in range(open_index, len(text)):
        char = text[index]
        if char == "(":
            balance += 1
        elif char == ")" and balance == 1:
            close_index = index
            break
        elif char == ")":
            balance -= 1
    return _count_params(text[open_index + 1:close_index])


def _count_params(text):
    """Count top-level parameters in a signature fragment."""
    parts = []
    depth = 0
    current = ""
    for char in text:
        depth += "([{".count(char) - ")]}".count(char)
        if char == "," and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += char
    parts += [current]
    names = [part.strip() for part in parts if part.strip()]
    star = any(name.startswith("*") for name in names)
    real = [name for name in names
            if name.split("=")[0].split(":")[0].strip() not in ("self", "cls")]
    return len(real), star


def depth_profile(code_lines, lang_name):
    """Measure nesting depth across a whole file.

    Returns the maximum depth and the fraction of code lines that
    sit deeper than the comfortable limit. Lines that continue a
    statement wrapped in unclosed brackets inherit the depth of
    the statement's first line, because a wrapped call is not an
    extra level of logic nesting.
    """
    depths = []
    if lang_name in constants.INDENT_LANGS:
        balance = 0
        previous = 0
        for raw in code_lines:
            if not raw.strip():
                depths.append(0)
                continue
            depth_here = previous
            if balance == 0:
                expanded = raw.expandtabs(constants.TAB_WIDTH)
                indent = len(expanded) - len(expanded.lstrip(" "))
                depth_here = indent // constants.TAB_WIDTH
                previous = depth_here
            depths.append(depth_here)
            balance = max(0, balance + _bracket_delta(raw))
    else:
        depths = _brace_depths(code_lines)
    solid_count = 0
    deep_count = 0
    worst_depth = 0
    for raw, depth in zip(code_lines, depths):
        if raw.strip():
            solid_count += 1
            worst_depth = max(worst_depth, depth)
            if depth > constants.DEEP_LIMIT:
                deep_count += 1
    if not solid_count:
        return {"max": 0, "deep_fraction": 0.0, "depths": depths}
    return {"max": worst_depth, "deep_fraction": deep_count / solid_count,
            "depths": depths}


def _brace_depths(code_lines):
    """Return the brace depth in effect at the start of each line.

    Lines that merely continue a call or an argument list spanning
    several lines inherit the depth of the statement they belong
    to: a wrapped argument is not an extra level of nesting.
    """
    depths = []
    balance = 0
    parens = 0
    previous = 0
    for line in code_lines:
        text = line.strip()
        if parens > 0:
            depths.append(previous)
        else:
            depth = balance
            if text and "{" in line and not text.startswith("}"):
                depth = balance + 1
            previous = depth
            depths.append(depth)
        balance = max(0, balance + line.count("{") - line.count("}"))
        parens = max(0, parens + line.count("(") + line.count("[")
                     - line.count(")") - line.count("]"))
    return depths


def parse_imports(code_lines, lang_name, docstring_lines):
    """Collect the import statements of a file.

    Each entry names the symbols it brings in, where it sits, and
    whether it hides in the middle of the file instead of the top.
    """
    entries = []
    first_code = len(code_lines)
    for index, raw in enumerate(code_lines):
        if not raw.strip() or index in docstring_lines:
            continue
        if _import_on_line(raw, lang_name) is not None:
            continue
        first_code = index
        break
    for pos, raw in enumerate(code_lines):
        parsed = _import_on_line(raw, lang_name)
        if parsed is None:
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        parsed["line"] = pos + 1
        parsed["midfile"] = pos > first_code or indent > 0
        entries.append(parsed)
    return entries


def _import_on_line(raw, lang_name):
    """Parse one line as an import statement, or return None."""
    if lang_name == "python":
        return _python_import(raw)
    if lang_name == "javascript" or lang_name == "typescript":
        return _js_import(raw)
    generic = re.match(r"^\s*(import|use|using|#include|require)\b", raw)
    if generic:
        return {"star": False, "names": []}
    return None


def _python_import(raw):
    """Parse a Python import line into the names it binds."""
    plain = re.match(r"^\s*import\s+(.+)$", raw)
    if plain:
        return {"names": _bind_names(plain.group(1), True), "star": False}
    from_match = re.match(r"^\s*from\s+[\w\.]+\s+import\s+(.+)$", raw)
    if from_match:
        body = from_match.group(1).strip().strip("()")
        if "*" in body:
            return {"names": [], "star": True}
        return {"names": _bind_names(body, False), "star": False}
    return None


def _bind_names(body, dotted):
    """Collect the names bound by a comma-separated import list.

    An alias after "as" wins; a dotted path binds its first part
    for plain imports and the written name for from-imports.
    """
    names = []
    for part in body.split(","):
        tokens = part.strip().split()
        if not tokens:
            continue
        if "as" in tokens:
            names.append(tokens[tokens.index("as") + 1])
        elif dotted:
            names.append(tokens[0].split(".")[0])
        else:
            names.append(tokens[0])
    return names


def _js_import(raw):
    """Parse a JavaScript import or require line."""
    default = re.match(r"^\s*import\s+(\w+)\s+from", raw)
    if default:
        return {"names": [default.group(1)], "star": False}
    named = re.match(r"^\s*import\s*\{([^}]*)\}\s*from", raw)
    if named:
        return {"names": _bind_names(named.group(1), False), "star": False}
    require = re.search(r"(?:const|let|var)\s+(\w+)\s*=\s*require\s*\(", raw)
    if require:
        return {"names": [require.group(1)], "star": False}
    if re.match(r"^\s*import\b", raw):
        return {"names": [], "star": False}
    return None


def const_regions(code_lines):
    """Return the line indexes of module-level constant assignments.

    A region starts at an ALL-CAPS assignment in column zero and
    runs until its brackets balance out again. Numbers inside such
    regions are configuration, not magic.
    """
    regions = set()
    balance = 0
    active = False
    for row_no, raw in enumerate(code_lines):
        if not active and re.match(r"^[A-Z][A-Z0-9_]*\s*=[^=]", raw):
            active = True
            balance = 0
        if not active:
            continue
        regions.add(row_no)
        balance += _bracket_delta(raw)
        if balance <= 0:
            active = False
    return regions


def _bracket_delta(raw):
    """Return how much a line opens minus how much it closes."""
    opens = raw.count("(") + raw.count("[") + raw.count("{")
    closes = raw.count(")") + raw.count("]") + raw.count("}")
    return opens - closes
