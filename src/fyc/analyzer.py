"""Analysis orchestration for fuck-your-code.

This module owns the per-file context every check reads, runs
the twenty checks over each file, builds the identifier corpus
that dead-code detection needs, and aggregates file results
into the project report with its verdict and recommendations.
"""

import re
from collections import Counter

from fyc import checks_core
from fyc import checks_extra
from fyc import constants
from fyc import i18n
from fyc import lexing
from fyc import masking
from fyc import recommendations
from fyc import util

IDENT_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
CHECK_RUNNERS = (
    ("complexity", checks_core.check_complexity),
    ("nesting", checks_extra.check_nesting),
    ("funclen", checks_extra.check_funclen),
    ("size", checks_core.check_size),
    ("structure", checks_core.check_structure),
    ("duplication", checks_core.check_duplication),
    ("errors", checks_core.check_errors),
    ("secrets", checks_extra.check_secrets),
    ("dangerous", checks_extra.check_dangerous),
    ("deadcode", checks_extra.check_deadcode),
    ("globals", checks_extra.check_globals),
    ("params", checks_extra.check_params),
    ("imports", checks_extra.check_imports),
    ("docs", checks_core.check_docs),
    ("commented", checks_extra.check_commented),
    ("techdebt", checks_extra.check_techdebt),
    ("naming", checks_core.check_naming),
    ("magic", checks_extra.check_magic),
    ("formatting", checks_extra.check_formatting),
    ("debug", checks_extra.check_debug),
)


class FileContext:
    """All facts gathered about one file, shared by every check."""

    def __init__(self, name, lang_name, strings):
        """Create an empty context for one file."""
        self.name = name
        self.lang_name = lang_name
        self.strings = strings
        self.lines = []
        self.masked_lines = []
        self.code_lines = []
        self.comment_lines = set()
        self.comment_text = {}
        self.docstring_lines = set()
        self.functions = []
        self.imports = []
        self.depths = []
        self.max_depth = 0
        self.deep_fraction = 0.0
        self.corpus = Counter()
        self.def_counts = Counter()
        self.issues = []

    def add(self, check, key, line, fmt):
        """Record one issue, rendering its message right away."""
        context = {"line": line, "n": 0, "name": "", "pct": 0,
                   "a": 0, "b": 0, "names": "", "kind": ""}
        if fmt:
            context.update(fmt)
        self.issues.append({
            "check": check, "file": self.name, "line": line,
            "message": self.strings[key].format(**context),
        })


def build_corpus(items):
    """Count identifier uses and function definitions across files.

    Dead-code detection needs the whole picture: a function is
    only dead when its name is used nowhere in the run at all.
    """
    corpus = Counter()
    def_counts = Counter()
    for _name, text, lang_name in items:
        viewed = masking.code_view(text, lang_name)
        corpus.update(IDENT_RE.findall(viewed))
        viewed_lines = viewed.splitlines()
        for func in lexing.find_functions(viewed_lines, lang_name):
            def_counts[func["name"]] += 1
    return corpus, def_counts


def analyze_all(items, ui_lang):
    """Analyze a list of name, text and language triples."""
    shared = build_corpus(items)
    results = []
    for name, text, lang_name in items:
        results.append(analyze_file(name, text, lang_name, ui_lang, shared))
    return results


def analyze_file(name, text, lang_name, ui_lang, shared):
    """Run all twenty checks over one file and grade it."""
    ctx = _build_context(name, text, lang_name, ui_lang)
    ctx.corpus, ctx.def_counts = shared
    checks = {}
    for key, runner in CHECK_RUNNERS:
        checks[key] = round(runner(ctx), 1)
    shit = util.clamp(sum(checks[key] * constants.CHECK_WEIGHTS[key]
                          for key in constants.CHECK_KEYS))
    return {"file": name, "language": lang_name, "lines": len(ctx.lines),
            "checks": checks, "shit_index": round(shit, 1),
            "quality": round(constants.PERCENT - shit, 1),
            "issues": ctx.issues}


def _build_context(name, text, lang_name, ui_lang):
    """Gather every lexical fact the checks will ask about."""
    ctx = FileContext(name, lang_name, i18n.strings_for(ui_lang))
    ctx.lines = text.splitlines() or [""]
    ctx.masked_lines = _padded(masking.mask_strings(text, lang_name),
                               len(ctx.lines))
    ctx.code_lines = _padded(masking.code_view(text, lang_name),
                             len(ctx.lines))
    comments = lexing.scan_comments(ctx.lines, lang_name)
    ctx.comment_lines = comments["comment_lines"]
    ctx.comment_text = comments["comment_text"]
    ctx.docstring_lines = comments["docstring_lines"]
    ctx.functions = lexing.find_functions(ctx.code_lines, lang_name)
    profile = lexing.depth_profile(ctx.code_lines, lang_name)
    ctx.depths = profile["depths"]
    ctx.max_depth = profile["max"]
    ctx.deep_fraction = profile["deep_fraction"]
    ctx.imports = lexing.parse_imports(ctx.code_lines, lang_name,
                                       ctx.docstring_lines)
    return ctx


def _padded(view_text, expected):
    """Split a masked view into lines, padding any shortfall."""
    lines = view_text.splitlines()
    while len(lines) < expected:
        lines.append("")
    return lines


def build_report(results, lang):
    """Aggregate per-file results into the project report."""
    strings = i18n.strings_for(lang)
    if not results:
        return {"lang": lang, "files": [], "overall_quality": constants.PERCENT,
                "shit_index": 0.0, "verdict": "", "roast": strings["clean_bill"],
                "checks": {}, "total_lines": 0, "worst_files": [],
                "issues": [], "recommendations": []}
    total_lines = sum(result["lines"] for result in results)
    agg = {}
    for key in constants.CHECK_KEYS:
        weighted = sum(result["checks"][key] * result["lines"]
                       for result in results)
        agg[key] = round(weighted / max(1, total_lines), 1)
    shit = sum(agg[key] * constants.CHECK_WEIGHTS[key]
               for key in constants.CHECK_KEYS)
    quality = round(constants.PERCENT - shit, 1)
    verdict, roast = i18n.tier_for(quality, lang)
    worst = sorted(results, key=lambda result: -result["shit_index"])
    all_issues = []
    for result in results:
        all_issues.extend(result["issues"])
    all_issues.sort(key=lambda issue: -constants.CHECK_WEIGHTS[issue["check"]])
    advice = recommendations.build_recommendations(
        agg, results, all_issues, strings)
    return {"lang": lang, "overall_quality": quality,
            "shit_index": round(shit, 1), "verdict": verdict,
            "roast": roast, "checks": agg, "total_lines": total_lines,
            "files": results, "worst_files": worst, "issues": all_issues,
            "recommendations": advice}
