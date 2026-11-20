"""The thirteen checks added in version two.

Nesting, function length, tech debt, commented-out code, magic
numbers, hardcoded secrets, dead code, global state, parameter
bloat, import chaos, formatting, dangerous calls and debug
leftovers. Same contract as the core checks: read the shared
file context, record issues on it, return a score from zero
to one hundred.
"""

import re

from fyc import constants
from fyc import lexing
from fyc import util

DEBT_RE = re.compile(r"\b(" + "|".join(constants.DEBT_MARKERS) + r")\b")
NUMBER_RE = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w])")
SECRET_ASSIGN_RE = re.compile(
    r"(\w*(?:password|passwd|pwd|secret|api[_-]?key|access[_-]?token|"
    r"auth[_-]?token|private[_-]?key)\w*)\s*[:=]\s*[\"']", re.IGNORECASE)
CREDENTIAL_URL_RE = re.compile(r"://[^\s/:]+:[^\s/@]+@")
IP_ADDRESS_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
PY_MUTABLE_RE = re.compile(r"^([A-Za-z_]\w*)\s*=\s*(\[|\{|dict\(|list\(|set\()")
JS_MUTABLE_RE = re.compile(r"^(?:var|let|const)\s+([A-Za-z_]\w*)\s*=\s*(\[|\{|new\s)")
GLOBAL_KEYWORD_RE = re.compile(r"^\s*global\s+\w")
TERMINATOR_RE = re.compile(r"^\s*(return|raise|break|continue|throw)\b")
EVAL_RE = re.compile(r"\beval\s*\(")
EXEC_RE = re.compile(r"\bexec\s*\(")
OS_SYSTEM_RE = re.compile(r"\bos\.system\s*\(")
SHELL_TRUE_RE = re.compile(r"\bshell\s*=\s*True\b")
PICKLE_LOADS_RE = re.compile(r"\bpickle\.loads\s*\(")
INNER_HTML_RE = re.compile(r"\.innerHTML\s*=")
DOCUMENT_WRITE_RE = re.compile(r"\bdocument\.write\s*\(")
SQL_FORMAT_RE = re.compile(r"\bexecute\s*\(\s*f[\"']")
DANGER_PATTERNS = [
    ("eval()", EVAL_RE),
    ("exec()", EXEC_RE),
    ("os.system()", OS_SYSTEM_RE),
    ("shell=True", SHELL_TRUE_RE),
    ("pickle.loads()", PICKLE_LOADS_RE),
    ("innerHTML assignment", INNER_HTML_RE),
    ("document.write()", DOCUMENT_WRITE_RE),
    ("SQL string formatting", SQL_FORMAT_RE),
]
PRINT_RE = re.compile(r"\bprint\s*\(")
CONSOLE_LOG_RE = re.compile(r"\bconsole\.log\s*\(")
SYSTEM_OUT_RE = re.compile(r"\bSystem\.out\.println\s*\(")
DEBUGGER_RE = re.compile(r"\bdebugger\s*;")
BREAKPOINT_RE = re.compile(r"\bbreakpoint\s*\(")
SET_TRACE_RE = re.compile(r"\bset_trace\s*\(")
FMT_PRINTLN_RE = re.compile(r"\bfmt\.Println\s*\(")
DEBUG_PATTERNS = [PRINT_RE, CONSOLE_LOG_RE, SYSTEM_OUT_RE, DEBUGGER_RE,
                  BREAKPOINT_RE, SET_TRACE_RE, FMT_PRINTLN_RE]
CODE_END_RE = re.compile(r"(;|\{|\})\s*$")
CODE_START_RE = re.compile(
    r"^(def|if|elif|else|for|while|return|import|from|class|"
    r"function|var|let|const|try|except|switch|case)\b")
CODE_ASSIGN_RE = re.compile(r"\w+\s*=[^=]")
CODE_CALL_RE = re.compile(r"^\w+\s*\([^)]*\)\s*;?$")
CODE_LIKE_RES = [CODE_END_RE, CODE_START_RE, CODE_ASSIGN_RE, CODE_CALL_RE]


def check_nesting(ctx):
    """Score how deep the nesting digs and how much code lives there."""
    worst_term = min(max(0, ctx.max_depth - constants.DEEP_LIMIT)
                     * constants.DEEP_FACTOR, constants.DEEP_WORST_CAP)
    pct_term = min(ctx.deep_fraction * constants.DEEP_PCT_FACTOR,
                   constants.DEEP_PCT_CAP)
    nesting_score = util.clamp(worst_term + pct_term)
    if ctx.max_depth > constants.DEEP_LIMIT:
        ctx.add("nesting", "issue_nesting", None, {"n": ctx.max_depth})
    if ctx.deep_fraction >= constants.DEEP_PCT_ISSUE:
        pct_value = int(ctx.deep_fraction * constants.PERCENT)
        ctx.add("nesting", "issue_deep_lines", None, {"pct": pct_value})
    return nesting_score


def check_funclen(ctx):
    """Score function length: the worst, the average, the crowd."""
    if not ctx.functions:
        return 0.0
    lengths = [func["length"] for func in ctx.functions]
    longest = max(lengths)
    average = sum(lengths) / len(lengths)
    over = sum(1 for length in lengths
               if length > constants.LONG_FUNCTION_LINES)
    worst_term = min(max(0, longest - constants.LONG_FUNCTION_LINES)
                     * constants.FUNCLEN_WORST_FACTOR,
                     constants.FUNCLEN_WORST_CAP)
    pct_term = min(over / len(lengths) * constants.FUNCLEN_PCT_FACTOR,
                   constants.FUNCLEN_PCT_CAP)
    avg_term = min(max(0.0, average - constants.FUNCLEN_AVG_LIMIT)
                   * constants.FUNCLEN_AVG_FACTOR, constants.FUNCLEN_AVG_CAP)
    funclen_score = util.clamp(worst_term + pct_term + avg_term)
    if longest > constants.LONG_FUNCTION_LINES:
        longest_func = max(ctx.functions, key=lambda func: func["length"])
        ctx.add("funclen", "issue_long_function", longest_func["line"],
                {"name": longest_func["name"], "n": longest})
    if over >= constants.FUNCLEN_MANY_ISSUE:
        ctx.add("funclen", "issue_many_long_functions", None, {"n": over})
    return funclen_score


def check_techdebt(ctx):
    """Score the debt markers sprinkled through comments and code.

    The scan runs on the string-masked view, so the marker words
    stored as data by this very tool never count as findings.
    """
    markers = sum(len(DEBT_RE.findall(raw)) for raw in ctx.masked_lines)
    debt_score = util.clamp(markers * constants.DEBT_FACTOR)
    if markers >= constants.DEBT_ISSUE:
        ctx.add("techdebt", "issue_todo", None, {"n": markers})
    return debt_score


def check_commented(ctx):
    """Score blocks of code that were commented out instead of deleted."""
    blocks = 0
    block_lines = 0
    run = 0
    previous = -2
    for index in sorted(ctx.comment_text):
        body = ctx.comment_text[index]
        if index == previous + 1 and _looks_like_code(body):
            run += 1
        elif _looks_like_code(body):
            run = 1
        else:
            run = 0
        if run == constants.COMMENTED_BLOCK_MIN:
            blocks += 1
            block_lines += run
        elif run > constants.COMMENTED_BLOCK_MIN:
            block_lines += 1
        previous = index
    commented_score = util.clamp(blocks * constants.COMMENTED_BLOCK_POINTS
                                 + block_lines * constants.COMMENTED_LINE_POINTS)
    if blocks >= 1:
        ctx.add("commented", "issue_commented_code", None, {"n": block_lines})
    return commented_score


def _looks_like_code(body):
    """Say whether a comment line reads like code, not prose."""
    text = body.strip()
    if not text:
        return False
    for pattern in CODE_LIKE_RES:
        if pattern.search(text):
            return True
    return False


def check_magic(ctx):
    """Score unexplained numeric literals in the logic.

    Numbers inside module-level constant assignments, numbers in
    function signatures, and the small counting values are all
    exempt; what remains is numbers with no name and no story.
    """
    regions = lexing.const_regions(ctx.code_lines)
    func_starts = {func["start"] for func in ctx.functions}
    import_lines = {entry["line"] - 1 for entry in ctx.imports}
    exempt = regions | func_starts | import_lines
    count = 0
    for index, raw in enumerate(ctx.code_lines):
        if index in exempt:
            continue
        for found in NUMBER_RE.finditer(raw):
            if float(found.group(0)) not in constants.MAGIC_ALLOWED:
                count += 1
    magic_score = util.clamp(count * constants.MAGIC_FACTOR)
    if count >= constants.MAGIC_ISSUE:
        ctx.add("magic", "issue_magic_numbers", None, {"n": count})
    return magic_score


def check_secrets(ctx):
    """Score secrets that were hardcoded into the source.

    Runs on the string-masked view: the assignment shape and the
    opening quote survive masking, the secret value itself is
    never read, stored or printed.
    """
    hits = 0
    ip_count = 0
    for index, raw in enumerate(ctx.masked_lines):
        found = SECRET_ASSIGN_RE.search(raw)
        if found:
            hits += 1
            ctx.add("secrets", "issue_secret_assignment", index + 1,
                    {"name": found.group(1)})
        if CREDENTIAL_URL_RE.search(raw):
            hits += 1
            ctx.add("secrets", "issue_credential_url", index + 1, None)
        ip_count += len(IP_ADDRESS_RE.findall(raw))
    if ip_count >= 1:
        hits += ip_count
        ctx.add("secrets", "issue_hardcoded_ip", None, {"n": ip_count})
    return util.clamp(hits * constants.SECRET_FACTOR)


def check_deadcode(ctx):
    """Score imports nobody uses, functions nobody calls, lost lines."""
    unused = _unused_imports(ctx)
    dead = _dead_functions(ctx)
    unreachable = _unreachable_count(ctx)
    import_term = min(len(unused) * constants.DEAD_UNUSED_IMPORT_FACTOR,
                      constants.DEAD_UNUSED_IMPORT_CAP)
    func_term = min(len(dead) * constants.DEAD_FUNC_FACTOR,
                    constants.DEAD_FUNC_CAP)
    reach_term = min(unreachable * constants.DEAD_UNREACHABLE_FACTOR,
                     constants.DEAD_UNREACHABLE_CAP)
    dead_score = util.clamp(import_term + func_term + reach_term)
    if unused:
        unused_names = ", ".join(unused[:constants.NAMES_PREVIEW])
        ctx.add("deadcode", "issue_unused_imports", None,
                {"n": len(unused), "names": unused_names})
    if dead:
        dead_names = ", ".join(dead[:constants.NAMES_PREVIEW])
        ctx.add("deadcode", "issue_dead_functions", None, {"n": len(dead), "names": dead_names})
    if unreachable >= 1:
        ctx.add("deadcode", "issue_unreachable", None, {"n": unreachable})
    return dead_score


def _unused_imports(ctx):
    """Return the imported names that never appear again in the file."""
    excluded = {entry["line"] - 1 for entry in ctx.imports}
    searchable = "\n".join(raw for index, raw in enumerate(ctx.code_lines)
                           if index not in excluded)
    unused = []
    for entry in ctx.imports:
        for name in entry["names"]:
            if not re.search(r"\b" + re.escape(name) + r"\b", searchable):
                unused.append(name)
    return unused


def _dead_functions(ctx):
    """Return functions whose name is never used outside definitions."""
    dead = []
    for func in ctx.functions:
        name = func["name"]
        if name.startswith("__") and name.endswith("__"):
            continue
        used = ctx.corpus.get(name, 0) - ctx.def_counts.get(name, 0)
        if used <= 0:
            dead.append(name)
    return dead


def _unreachable_count(ctx):
    """Count statements stranded right after a block terminator."""
    count = 0
    for index, line in enumerate(ctx.code_lines):
        if not TERMINATOR_RE.search(line):
            continue
        following = index + 1
        while following < len(ctx.code_lines) and not ctx.code_lines[following].strip():
            following += 1
        if following < len(ctx.code_lines) and _is_stranded(ctx, index, following):
            count += 1
    return count


def _is_stranded(ctx, index, following):
    """Say whether the line after a terminator can never run.

    In indentation-based languages the stranded line must sit at
    the same indent as the terminator without opening a new
    definition; in brace languages it must sit at the same depth
    without closing the block.
    """
    next_raw = ctx.code_lines[following]
    if ctx.lang_name in constants.INDENT_LANGS:
        term_raw = ctx.code_lines[index]
        next_indent = len(next_raw) - len(next_raw.lstrip(" "))
        term_indent = len(term_raw) - len(term_raw.lstrip(" "))
        opens = next_raw.strip().startswith(("def ", "class "))
        return next_indent == term_indent and not opens
    if ctx.depths[following] != ctx.depths[index]:
        return False
    return not next_raw.strip().startswith("}")


def check_globals(ctx):
    """Score shared mutable state and its spooky action at a distance."""
    mutables = 0
    for raw in ctx.code_lines:
        found = PY_MUTABLE_RE.search(raw) or JS_MUTABLE_RE.search(raw)
        if found and found.group(1) != found.group(1).upper():
            mutables += 1
    keyword_hits = sum(1 for raw in ctx.code_lines
                       if GLOBAL_KEYWORD_RE.search(raw))
    defaults = _mutable_defaults(ctx)
    global_score = util.clamp(
        mutables * constants.GLOBAL_MUTABLE_POINTS
        + keyword_hits * constants.GLOBAL_KEYWORD_POINTS
        + len(defaults) * constants.GLOBAL_MUTABLE_DEFAULT_POINTS)
    if mutables >= constants.GLOBAL_ISSUE_MIN:
        ctx.add("globals", "issue_globals", None, {"n": mutables})
    if keyword_hits >= 1:
        ctx.add("globals", "issue_global_keyword", None, {"n": keyword_hits})
    if defaults:
        ctx.add("globals", "issue_mutable_default", defaults[0]["line"],
                {"name": defaults[0]["name"]})
    return global_score


def _mutable_defaults(ctx):
    """Return the functions whose signature hides a mutable default."""
    found = []
    for candidate in ctx.functions:
        if re.search(r"=\s*[\[{]", ctx.code_lines[candidate["start"]]):
            found.append(candidate)
    return found


def check_params(ctx):
    """Score parameter lists that grew into family reunions."""
    if len(ctx.functions) == 0:
        return 0.0
    worst_func = max(ctx.functions, key=lambda func: func["params"])
    star_count = sum(1 for func in ctx.functions if func["star"])
    worst_term = min(max(0, worst_func["params"] - constants.PARAM_LIMIT)
                     * constants.PARAM_FACTOR, constants.PARAM_CAP)
    star_term = min(max(0, star_count - constants.STAR_ALLOWANCE)
                    * constants.STAR_FACTOR, constants.STAR_CAP)
    params_score = util.clamp(worst_term + star_term)
    if worst_func["params"] > constants.PARAM_LIMIT:
        ctx.add("params", "issue_too_many_params", worst_func["line"],
                {"name": worst_func["name"], "n": worst_func["params"]})
    if star_count >= constants.STAR_ISSUE:
        ctx.add("params", "issue_star_args", None, {"n": star_count})
    return params_score


def check_imports(ctx):
    """Score import sections that sprawl, hide, or import the world."""
    total = len(ctx.imports)
    stars = [entry for entry in ctx.imports if entry["star"]]
    midfile = sum(1 for entry in ctx.imports if entry["midfile"])
    base_term = min(max(0, total - constants.IMPORT_FREE_COUNT)
                    * constants.IMPORT_FACTOR, constants.IMPORT_CAP)
    mid_term = midfile * constants.MIDFILE_IMPORT_POINTS
    import_score = util.clamp(base_term + mid_term
                              + len(stars) * constants.STAR_IMPORT_POINTS)
    if total > constants.IMPORT_ISSUE_COUNT:
        ctx.add("imports", "issue_import_chaos", None, {"n": total})
    for entry in stars:
        ctx.add("imports", "issue_star_import", entry["line"], None)
    if midfile >= 1:
        ctx.add("imports", "issue_midfile_imports", None, {"n": midfile})
    return import_score


def check_formatting(ctx):
    """Score the surface hygiene: line length, trailing space, tabs."""
    long_lines = 0
    trailing = 0
    nonblank = 0
    tabbed = False
    spaced = False
    for raw in ctx.lines:
        nonblank += bool(raw.strip())
        long_lines += bool(len(raw) > constants.LONG_LINE_LIMIT)
        trailing += bool(raw.strip() and raw != raw.rstrip())
        tabbed = tabbed or raw.startswith("\t")
        spaced = spaced or raw.startswith(" ")
    mixed = tabbed and spaced
    long_term = min(long_lines * constants.FORMAT_LONG_FACTOR,
                    constants.FORMAT_LONG_CAP)
    trail_term = min(trailing / max(1, nonblank) * constants.FORMAT_TRAIL_FACTOR,
                     constants.FORMAT_TRAIL_CAP)
    mixed_term = constants.FORMAT_MIXED_POINTS * int(mixed)
    formatting_score = util.clamp(long_term + trail_term + mixed_term)
    if long_lines >= constants.FORMAT_LONG_ISSUE:
        ctx.add("formatting", "issue_long_lines", None, {"n": long_lines})
    if trailing >= 1:
        ctx.add("formatting", "issue_trailing_ws", None, {"n": trailing})
    if mixed:
        ctx.add("formatting", "issue_mixed_indent", None, None)
    return formatting_score


def check_dangerous(ctx):
    """Score calls that hand the keys to strangers or to chaos."""
    hits = 0
    seen = set()
    for line_no, raw in enumerate(ctx.code_lines):
        for kind, pattern in DANGER_PATTERNS:
            if not pattern.search(raw):
                continue
            hits += 1
            if kind in seen:
                continue
            seen.add(kind)
            ctx.add("dangerous", "issue_dangerous_call", line_no + 1, {"kind": kind})
    return util.clamp(hits * constants.DANGEROUS_FACTOR)


def check_debug(ctx):
    """Score debug output and placeholder bodies left in the code."""
    statements = 0
    for line in ctx.code_lines:
        for pattern in DEBUG_PATTERNS:
            statements += len(pattern.findall(line))
    empties = _empty_functions(ctx)
    stmt_term = min(statements * constants.DEBUG_STMT_FACTOR,
                    constants.DEBUG_STMT_CAP)
    empty_term = min(len(empties) * constants.DEBUG_EMPTY_POINTS,
                     constants.DEBUG_EMPTY_CAP)
    debug_score = util.clamp(stmt_term + empty_term)
    if statements >= 1:
        ctx.add("debug", "issue_debug_statements", None, {"n": statements})
    for func in empties:
        ctx.add("debug", "issue_empty_function", func["line"],
                {"name": func["name"]})
    return debug_score


def _empty_functions(ctx):
    """Return functions whose body is empty or a lone placeholder."""
    found = []
    for entry in ctx.functions:
        body = ctx.code_lines[entry["start"] + 1:entry["end"]]
        solid = [raw.strip() for raw in body if raw.strip()]
        if not solid:
            found.append(entry)
            continue
        if all(text == "pass" for text in solid):
            found.append(entry)
            continue
        raw_indexes = range(entry["start"] + 1, entry["end"])
        if all(index in ctx.docstring_lines or not ctx.lines[index].strip()
               for index in raw_indexes):
            found.append(entry)
    return found
