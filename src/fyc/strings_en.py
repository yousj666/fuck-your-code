"""English strings for fuck-your-code.

Every label, check name, verdict, insult and piece of serious
advice the tool can print in English lives in this one table.
Keeping the words in a data module means the checking code never
has to mix logic with copy, and translators get exactly one
file to look at per language.
"""

STRINGS_EN = {
    # Report labels and column headers
    "app_tagline": "fuck-your-code -- how shitty is your code, really?",
    "report_title": "SHITTY CODE REPORT",
    "overall_quality": "Overall quality score",
    "shit_index": "Shit-Gas Index",
    "verdict": "Verdict",
    "files_analyzed": "Files analyzed",
    "total_lines": "Total lines",
    "check_breakdown": "Breakdown by check (longer bar = shittier)",
    "worst_files": "Hall of Shame -- worst files",
    "top_issues": "Worst offences",
    "recommendations_title": "Serious recommendations",
    "no_files": "No analysable files found. Did you point me at thin air?",
    "col_file": "File",
    "col_score": "Shit-Gas",
    "col_quality": "Quality",
    "col_lines": "Lines",
    "col_lang": "Lang",
    "clean_bill": "Nothing embarrassing found. Suspiciously clean.",
    "paste_label": "(pasted code)",
    "stdin_hint": ("Reading code from stdin... paste it, then Ctrl-D "
                   "(Ctrl-Z + Enter on Windows)."),

    # The twenty check names
    "checks": {
        "complexity": "Complexity",
        "nesting": "Nesting",
        "funclen": "Function Length",
        "size": "Size & Bloat",
        "structure": "Structure",
        "duplication": "Duplication",
        "errors": "Error Handling",
        "secrets": "Hardcoded Secrets",
        "dangerous": "Dangerous Calls",
        "deadcode": "Dead Code",
        "globals": "Global State",
        "params": "Parameter Bloat",
        "imports": "Import Chaos",
        "docs": "Comments & Docs",
        "commented": "Commented-Out Code",
        "techdebt": "Tech Debt",
        "naming": "Naming",
        "magic": "Magic Numbers",
        "formatting": "Formatting",
        "debug": "Debug Leftovers",
    },

    # Verdict tiers: threshold, label, roast
    "tiers": [
        (90, "Cleaner than a surgeon's group chat",
         "I brought my finest insults and I am leaving with all of them. "
         "This code is so clean it squeaks when you scroll it."),
        (75, "Respectably human",
         "A couple of crumbs on the counter, but nobody is calling pest "
         "control. Ship it and sleep fine."),
        (55, "Mid, but make it compile",
         "The code equivalent of a shrug emoji. It works, technically, "
         "the way a shopping cart with one bad wheel works."),
        (35, "Shit mountain with a gift shop",
         "Tourists are taking photos. Somewhere in there is a function "
         "held together by hope and a semicolon."),
        (0, "Weapon-grade code crime",
         "Archaeologists will dig this up in 3,000 years and conclude "
         "our civilisation deserved it. Delete, deny, relocate."),
    ],

    # Issue messages, one per offence the checks can find
    "issue_complex_function": (
        "Function {name} runs a cyclomatic complexity of about {n} -- "
        "a choose-your-own-adventure novel"),
    "issue_nesting": (
        "Nesting digs {n} levels down -- pack a rope, a headlamp and a will"),
    "issue_deep_lines": (
        "{pct}% of the lines live deeper than four levels of nesting"),
    "issue_long_function": (
        "Function {name} runs {n} lines without coming up for air "
        "(line {line})"),
    "issue_many_long_functions": (
        "{n} functions are over fifty lines long -- a crowd of marathons"),
    "issue_god_file": "God file: {n} lines doing every job in the building",
    "issue_big_file": "File is {n} lines -- not illegal, just exhausting",
    "issue_too_many_funcs": (
        "{n} functions crammed into one file -- a crowd, not a module"),
    "issue_bare_except": (
        "Bare except swallowing every error whole, line {line}"),
    "issue_except_pass": (
        "except, then pass -- errors check in, silence checks out, "
        "line {line}"),
    "issue_empty_catch": (
        "Empty catch block: the error was seen, judged and ignored, "
        "line {line}"),
    "issue_no_comments": (
        "Basically zero comments -- future you is going to have QUESTIONS"),
    "issue_too_many_comments": (
        "Comments are staging a coup ({pct}% of the file)"),
    "issue_single_letter": (
        "Single-letter variables everywhere ({n}) -- code, not algebra "
        "homework"),
    "issue_meaningless": (
        "Soul-less names like tmp and data1 doing real jobs ({n} found)"),
    "issue_mixed_case": (
        "snake_case and camelCase are brawling in one file ({a} vs {b})"),
    "issue_dup_lines": "{pct}% of lines are copy-paste repeats",
    "issue_dup_blocks": (
        "{n} repeated five-line blocks -- Ctrl+C, Ctrl+V, Ctrl+Shame"),
    "issue_todo": (
        "{n} debt markers buried for the next poor soul to step on"),
    "issue_commented_code": (
        "{n} lines of code are parked in comments -- not alive, not "
        "deleted, just haunting the file"),
    "issue_magic_numbers": (
        "{n} magic numbers roam the logic with no name tag"),
    "issue_secret_assignment": (
        "A secret-looking literal is assigned to {name}, line {line} -- "
        "secrets do not belong in source code"),
    "issue_credential_url": (
        "A URL with credentials baked into it, line {line}"),
    "issue_hardcoded_ip": (
        "Hardcoded IP addresses in the code ({n} found)"),
    "issue_unused_imports": "{n} imports are never used: {names}",
    "issue_dead_functions": (
        "{n} functions are defined but never called anywhere: {names}"),
    "issue_unreachable": (
        "{n} statements sit after a return or raise and can never run"),
    "issue_globals": (
        "{n} chunks of module-level mutable state, shared with "
        "everyone, trusted by no one"),
    "issue_global_keyword": (
        "{n} global statements -- spooky action at a distance"),
    "issue_mutable_default": (
        "Function {name} has a mutable default argument -- it remembers "
        "every previous call"),
    "issue_too_many_params": (
        "Function {name} takes {n} parameters -- a family reunion, "
        "not a function"),
    "issue_star_args": (
        "{n} functions hide behind variadic catch-all parameters"),
    "issue_import_chaos": (
        "{n} imports crowd the top of the file -- a flea market of "
        "dependencies"),
    "issue_star_import": (
        "Star import on line {line} -- nobody knows which names live "
        "here anymore"),
    "issue_midfile_imports": (
        "{n} imports are hiding in the middle of the file"),
    "issue_long_lines": (
        "{n} lines exceed the length limit -- horizontal scrolling is "
        "not a feature"),
    "issue_trailing_ws": "{n} lines trail whitespace behind them",
    "issue_mixed_indent": "Tabs and spaces are mixed -- pick a side, any side",
    "issue_dangerous_call": "Dangerous call: {kind} on line {line}",
    "issue_debug_statements": (
        "{n} debug print or log statements never left the building"),
    "issue_empty_function": (
        "Function {name} is an empty shell (line {line})"),

    # Serious advice, one entry per check, written for the worst file
    "advice_complexity": (
        "In {file}: split the most complex function into smaller "
        "single-purpose helpers, and replace nested branches with "
        "early returns. Keep cyclomatic complexity at or below ten "
        "per function."),
    "advice_nesting": (
        "In {file}: flatten deep nesting with guard clauses and "
        "early returns, and extract inner blocks into named "
        "functions. Aim for at most three to four levels."),
    "advice_funclen": (
        "In {file}: break functions longer than about fifty lines "
        "into named steps such as parse, validate, compute and "
        "render. A function should do one thing."),
    "advice_size": (
        "In {file}: the file is doing too many jobs. Move cohesive "
        "groups of functions into their own modules, named after "
        "the thing they own."),
    "advice_structure": (
        "In {file}: too many functions share one file. Group them "
        "by responsibility into separate modules with a small, "
        "clear public surface."),
    "advice_duplication": (
        "In {file}: extract the repeated blocks into one shared "
        "function and call it from each site, so duplicated logic "
        "only ever needs fixing in one place."),
    "advice_errors": (
        "In {file}: catch specific exception types instead of bare "
        "handlers, log the error with context, and never swallow "
        "a failure with an empty block."),
    "advice_docs": (
        "In {file}: add a short module docstring and one-line "
        "docstrings for public functions that explain intent, "
        "not mechanics."),
    "advice_naming": (
        "In {file}: rename single-letter and placeholder variables "
        "to words that carry meaning, and pick one naming "
        "convention per file and keep it."),
    "advice_techdebt": (
        "In {file}: turn every debt marker into a tracked issue "
        "with an owner, then delete the marker. Stale markers are "
        "how known bugs become surprises."),
    "advice_commented": (
        "In {file}: delete commented-out code. Version control "
        "already remembers it. If a block must stay, say why in "
        "prose and give it an expiry date."),
    "advice_magic": (
        "In {file}: give every unexplained numeric literal a "
        "named constant, so each value has a meaning and a single "
        "place where it can change."),
    "advice_secrets": (
        "In {file}: move secrets out of the source into "
        "environment variables or a secrets manager, and rotate "
        "any credential that was ever committed."),
    "advice_deadcode": (
        "In {file}: delete unused imports and unreferenced "
        "functions. Dead code still gets read, reviewed and "
        "maintained, so make the codebase mean everything it says."),
    "advice_globals": (
        "In {file}: replace module-level mutable state with "
        "parameters, return values or a small explicit state "
        "object, and avoid mutable default arguments."),
    "advice_params": (
        "In {file}: functions with many parameters usually want "
        "a small config object or dataclass. Group the related "
        "arguments and give the group a name."),
    "advice_imports": (
        "In {file}: remove star imports, keep every import at "
        "the top of the file, and drop dependencies the module "
        "does not actually use."),
    "advice_formatting": (
        "In {file}: run a formatter, cap lines at the agreed "
        "length, strip trailing whitespace, and use exactly one "
        "indentation style per file."),
    "advice_dangerous": (
        "In {file}: replace dynamic evaluation and shell string "
        "execution with structured APIs, parameterise database "
        "queries, and never unpickle untrusted data."),
    "advice_debug": (
        "In {file}: remove leftover debug output and empty "
        "placeholder functions. Use a logging module with levels "
        "for anything genuinely worth keeping."),
}
