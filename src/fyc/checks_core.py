"""The original seven checks of fuck-your-code.

Complexity, duplication, size, structure, error handling,
documentation and naming. Each check receives the shared file
context, records its findings as issues on that context, and
returns a shittiness score between zero and one hundred where
zero means nothing to complain about.
"""

import re
from collections import Counter

from fyc import constants
from fyc import util

BRANCH_RE = re.compile(r"\b(" + "|".join(constants.BRANCH_WORDS) + r")\b")
BARE_EXCEPT_RE = re.compile(r"except\s*:|except\s*\(\s*\)\s*:")
EXCEPT_PASS_RE = re.compile(r"except[^:]*:\s*pass\b")
EMPTY_CATCH_RE = re.compile(r"catch\s*\([^)]*\)\s*\{\s*\}")
EMPTY_CATCH_BARE_RE = re.compile(r"catch\s*\{\s*\}")
ERROR_CHECKS = (
    ("issue_bare_except", BARE_EXCEPT_RE),
    ("issue_except_pass", EXCEPT_PASS_RE),
    ("issue_empty_catch", EMPTY_CATCH_RE),
    ("issue_empty_catch", EMPTY_CATCH_BARE_RE),
)
SINGLE_LETTER_RE = re.compile(r"(?:^|\s)(?:var|let|const)?\s*([a-z])\s*=(?!=)",
                              re.M)
IDENT_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
SNAKE_RE = re.compile(r"[a-z]+(_[a-z0-9]+)+")
CAMEL_RE = re.compile(r"[a-z]+[a-z0-9]*([A-Z][a-z0-9]*)+")


def check_complexity(ctx):
    """Score the worst per-function cyclomatic complexity.

    Every function gets a McCabe-style count of its branch words,
    boolean operators and ternaries, plus one for the entry point.
    Only functions past the agreed limit hurt the score.
    """
    worst = 0
    worst_func = None
    over = 0
    for func in ctx.functions:
        complexity = _function_complexity(ctx, func)
        if complexity > worst:
            worst = complexity
            worst_func = func
        if complexity > constants.CC_LIMIT:
            over += 1
    total = max(1, len(ctx.functions))
    worst_term = min(max(0, worst - constants.CC_LIMIT)
                     * constants.CC_WORST_FACTOR, constants.CC_WORST_CAP)
    pct_term = min(over / total * constants.CC_PCT_FACTOR,
                   constants.CC_PCT_CAP)
    complexity_score = util.clamp(worst_term + pct_term)
    if worst_func is not None and worst > constants.CC_LIMIT:
        ctx.add("complexity", "issue_complex_function", worst_func["line"],
                {"name": worst_func["name"], "n": worst})
    return complexity_score


def _function_complexity(ctx, func):
    """Count the branch points inside one function span."""
    total = 1
    for raw in ctx.code_lines[func["start"]:func["end"]]:
        total += len(BRANCH_RE.findall(raw))
        total += raw.count("&&") + raw.count("||") + raw.count("?")
    return total


def check_duplication(ctx):
    """Score copy-paste duplication over substantive lines.

    Only lines long enough to carry meaning take part, so repeated
    braces and closing brackets never inflate the result.
    """
    substantive = []
    for raw in ctx.code_lines:
        normalized = re.sub(r"\s+", " ", raw.strip())
        if len(normalized) >= constants.MIN_DUP_LINE_LEN:
            if any(char.isalnum() for char in normalized):
                substantive.append(normalized)
    total = max(1, len(substantive))
    counts = Counter(substantive)
    repeated = sum(count - 1 for count in counts.values() if count > 1)
    ratio = repeated / total
    blocks = _repeated_blocks(substantive)
    block_term = min(blocks * constants.DUP_BLOCK_FACTOR,
                     constants.DUP_BLOCK_CAP)
    dup_score = util.clamp(ratio * constants.DUP_RATIO_FACTOR + block_term)
    if ratio >= constants.DUP_RATIO_ISSUE:
        pct_value = int(ratio * constants.PERCENT)
        ctx.add("duplication", "issue_dup_lines", None, {"pct": pct_value})
    if blocks >= constants.DUP_BLOCK_ISSUE:
        ctx.add("duplication", "issue_dup_blocks", None, {"n": blocks})
    return dup_score


def _repeated_blocks(substantive):
    """Count repeated windows of consecutive substantive lines."""
    seen = set()
    blocks = 0
    window = constants.DUP_BLOCK_LINES
    for index in range(len(substantive) - window + 1):
        block = "\n".join(substantive[index:index + window])
        if block in seen:
            blocks += 1
        else:
            seen.add(block)
    return blocks


def check_size(ctx):
    """Score raw file length, gently at first, then with feeling."""
    total = len(ctx.lines)
    base_term = min(max(0, total - constants.SIZE_START_LINES)
                    * constants.SIZE_FACTOR, constants.SIZE_CAP)
    god_term = min(max(0, total - constants.GOD_FILE_LINES)
                   * constants.SIZE_GOD_FACTOR, constants.SIZE_GOD_CAP)
    size_score = util.clamp(base_term + god_term)
    if total >= constants.GOD_FILE_LINES:
        ctx.add("size", "issue_god_file", None, {"n": total})
    elif total >= constants.BIG_FILE_LINES:
        big_fmt = {"n": total}
        ctx.add("size", "issue_big_file", None, big_fmt)
    return size_score


def check_structure(ctx):
    """Score how much unrelated machinery shares one file."""
    func_count = len(ctx.functions)
    line_total = len(ctx.lines)
    func_term = min(max(0, func_count - constants.MAX_FUNCS_PER_FILE)
                    * constants.STRUCTURE_FUNC_FACTOR,
                    constants.STRUCTURE_FUNC_CAP)
    god_penalty = min(max(0, line_total - constants.GOD_FILE_LINES)
                      * constants.STRUCTURE_GOD_FACTOR,
                      constants.STRUCTURE_GOD_CAP)
    structure_score = util.clamp(func_term + god_penalty)
    if func_count > constants.TOO_MANY_FUNCS_ISSUE:
        ctx.add("structure", "issue_too_many_funcs", None, {"n": func_count})
    return structure_score


def check_errors(ctx):
    """Score error handling that swallows failures in silence."""
    hits = 0
    total = len(ctx.code_lines)
    for index, raw in enumerate(ctx.code_lines):
        stripped = raw.strip()
        for key, pattern in ERROR_CHECKS:
            if pattern.search(raw):
                hits += 1
                ctx.add("errors", key, index + 1, None)
        if _is_swallowed(ctx, index, stripped):
            hits += 1
            ctx.add("errors", "issue_except_pass", index + 1, None)
    joined = "\n".join(ctx.code_lines)
    if re.search(r"catch\s*\([^)]*\)\s*\{\s*\n\s*\}", joined):
        hits += 1
    if total == 0:
        return 0.0
    return util.clamp(hits * constants.ERROR_HIT_POINTS)


def _is_swallowed(ctx, index, stripped):
    """Say whether an except header is followed by a silent pass."""
    if "except" not in stripped:
        return False
    following = index + 1
    if following < len(ctx.code_lines):
        return ctx.code_lines[following].strip() == "pass"
    return False


def check_docs(ctx):
    """Score the documentation ratio against a healthy band.

    Too few comments starve the reader, too many bury the code.
    Files too small to judge are left alone entirely.
    """
    total_lines = len(ctx.lines)
    if total_lines < constants.DOC_MIN_FILE_LINES:
        return 0.0
    nonblank = sum(1 for raw in ctx.lines if raw.strip())
    ratio = len(ctx.comment_lines) / max(1, nonblank)
    docs_score = _docs_band(ratio)
    if ratio < constants.DOC_LOW and total_lines >= constants.DOC_ISSUE_MIN_LINES:
        ctx.add("docs", "issue_no_comments", None, None)
    if docs_score == constants.DOC_SCORE_EXTREME:
        doc_pct = int(ratio * constants.PERCENT)
        ctx.add("docs", "issue_too_many_comments", None, {"pct": doc_pct})
    return docs_score


def _docs_band(ratio):
    """Map a documentation ratio onto its penalty score."""
    if ratio < constants.DOC_NEAR_ZERO:
        return constants.DOC_SCORE_NEAR_ZERO
    if ratio < constants.DOC_LOW:
        return constants.DOC_SCORE_LOW
    if ratio > constants.DOC_EXTREME:
        return constants.DOC_SCORE_EXTREME
    if ratio > constants.DOC_HIGH:
        return constants.DOC_SCORE_HIGH
    return 0.0


def check_naming(ctx):
    """Score naming taste on the masked code view.

    Single-letter assignments, placeholder names doing real work,
    and two naming conventions fighting in one file all count.
    String contents never reach this check, so a detector can
    store its own word lists without convicting itself.
    """
    code_text = "\n".join(ctx.code_lines)
    single_count, meaningless, snake, camel = _naming_counts(code_text)
    mixed = (len(snake) >= constants.NAMING_MIXED_MIN
             and len(camel) >= constants.NAMING_MIXED_MIN)
    single_term = min(single_count * constants.NAMING_SINGLE_FACTOR,
                      constants.NAMING_SINGLE_CAP)
    meaning_term = min(len(meaningless) * constants.NAMING_MEANINGLESS_FACTOR,
                       constants.NAMING_MEANINGLESS_CAP)
    naming_score = util.clamp(single_term + meaning_term
                              + (constants.NAMING_MIXED_POINTS if mixed else 0.0))
    if single_count >= constants.NAMING_SINGLE_ISSUE:
        ctx.add("naming", "issue_single_letter", None, {"n": single_count})
    if len(meaningless) >= constants.NAMING_MEANINGLESS_ISSUE:
        ctx.add("naming", "issue_meaningless", None, {"n": len(meaningless)})
    if mixed:
        ctx.add("naming", "issue_mixed_case", None,
                {"a": len(snake), "b": len(camel)})
    return naming_score


def _naming_counts(code_text):
    """Collect the raw naming evidence of one file.

    Returns the single-letter assignment count, the list of
    placeholder names in use, and the snake_case and camelCase
    identifier sets whose coexistence signals a style war.
    """
    single_count = len(SINGLE_LETTER_RE.findall(code_text))
    idents = IDENT_RE.findall(code_text)
    meaningless = [word for word in idents
                   if word in constants.MEANINGLESS_NAMES]
    snake = [word for word in set(idents) if SNAKE_RE.fullmatch(word)]
    camel = [word for word in set(idents) if CAMEL_RE.fullmatch(word)]
    return single_count, meaningless, snake, camel
