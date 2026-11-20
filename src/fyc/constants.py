"""Named constants for the fuck-your-code analyzer.

Every scoring factor, threshold and word list lives here under a
descriptive ALL-CAPS name, so the checking code itself contains no
unexplained numeric literals. If a number matters, it has a name
and it lives in this file.
"""

# ---------------------------------------------------------------------------
# Language tables
# ---------------------------------------------------------------------------

EXT_TO_LANG = {
    ".py": "python",
    ".js": "javascript", ".mjs": "javascript", ".cjs": "javascript",
    ".jsx": "javascript", ".ts": "typescript", ".tsx": "typescript",
    ".go": "go", ".java": "java",
    ".c": "c", ".h": "c", ".cpp": "cpp", ".cc": "cpp", ".cxx": "cpp",
    ".hpp": "cpp", ".hh": "cpp",
    ".rs": "rust", ".cs": "csharp", ".php": "php", ".rb": "ruby",
    ".swift": "swift", ".kt": "kotlin", ".kts": "kotlin",
    ".sh": "shell", ".bash": "shell", ".zsh": "shell",
    ".lua": "lua", ".pl": "perl", ".pm": "perl", ".scala": "scala",
}
KNOWN_EXTS = frozenset(EXT_TO_LANG.keys())
HASH_COMMENT_LANGS = frozenset(["python", "ruby", "shell", "perl"])
INDENT_LANGS = frozenset(["python", "ruby", "shell", "perl", "lua"])
DOUBLE_QUOTE = '"'
SINGLE_QUOTE = "'"
BACKTICK = "`"
TRIPLE_LEN = 3
TAB_WIDTH = 4
PERCENT = 100.0

# ---------------------------------------------------------------------------
# The twenty checks and their weights in the Shit-Gas Index
# ---------------------------------------------------------------------------

CHECK_KEYS = [
    "complexity", "nesting", "funclen", "size", "structure",
    "duplication", "errors", "secrets", "dangerous", "deadcode",
    "globals", "params", "imports", "docs", "commented",
    "techdebt", "naming", "magic", "formatting", "debug",
]
CHECK_WEIGHTS = {
    "complexity": 0.11, "duplication": 0.09, "errors": 0.07,
    "nesting": 0.06, "secrets": 0.06, "dangerous": 0.06,
    "funclen": 0.05, "naming": 0.05, "magic": 0.05,
    "deadcode": 0.05, "size": 0.04, "structure": 0.04,
    "docs": 0.04, "globals": 0.04, "imports": 0.04,
    "techdebt": 0.03, "commented": 0.03, "params": 0.03,
    "formatting": 0.03, "debug": 0.03,
}

# ---------------------------------------------------------------------------
# Word lists used by several checks
# ---------------------------------------------------------------------------

BRANCH_WORDS = [
    "if", "elif", "else", "for", "while", "case", "catch", "except",
    "when", "switch", "foreach", "until", "match", "and", "or",
]
MEANINGLESS_NAMES = frozenset([
    "tmp", "tmp1", "tmp2", "tmp3", "temp", "temp1", "data", "data1",
    "data2", "aaa", "bbb", "xxx", "yyy", "zzz", "foo", "bar", "baz",
    "asdf", "qwerty", "test1", "test2", "var1", "var2", "obj1", "obj2",
    "thing", "stuff", "whatever", "res1", "res2", "val1",
])
DEBT_MARKERS = ["TODO", "FIXME", "HACK", "XXX", "WORKAROUND"]
CONTROL_KEYWORDS = frozenset([
    "if", "elif", "else", "for", "while", "switch", "catch", "return",
    "sizeof", "do", "try", "finally", "synchronized", "assert",
])
DEFAULT_EXCLUDE_GLOBS = [
    ".git", "*/.git/*", "node_modules", "*/node_modules/*",
    "__pycache__", "*/__pycache__/*", "dist", "*/dist/*",
    "build", "*/build/*", "vendor", "*/vendor/*",
    "*.min.js", "*.min.css", "*.map",
]

# ---------------------------------------------------------------------------
# Complexity: per-function cyclomatic complexity, McCabe style
# ---------------------------------------------------------------------------

CC_LIMIT = 10
CC_WORST_FACTOR = 6.0
CC_WORST_CAP = 60.0
CC_PCT_FACTOR = 150.0
CC_PCT_CAP = 40.0

# ---------------------------------------------------------------------------
# Nesting depth
# ---------------------------------------------------------------------------

DEEP_LIMIT = 4
DEEP_FACTOR = 15.0
DEEP_WORST_CAP = 60.0
DEEP_PCT_FACTOR = 300.0
DEEP_PCT_CAP = 40.0
DEEP_PCT_ISSUE = 0.02

# ---------------------------------------------------------------------------
# Function length
# ---------------------------------------------------------------------------

LONG_FUNCTION_LINES = 50
FUNCLEN_WORST_FACTOR = 1.5
FUNCLEN_WORST_CAP = 55.0
FUNCLEN_PCT_FACTOR = 200.0
FUNCLEN_PCT_CAP = 30.0
FUNCLEN_AVG_LIMIT = 30
FUNCLEN_AVG_FACTOR = 1.0
FUNCLEN_AVG_CAP = 15.0
FUNCLEN_MANY_ISSUE = 3

# ---------------------------------------------------------------------------
# File size and structure
# ---------------------------------------------------------------------------

SIZE_START_LINES = 500
BIG_FILE_LINES = 600
GOD_FILE_LINES = 1000
SIZE_FACTOR = 0.12
SIZE_CAP = 70.0
SIZE_GOD_FACTOR = 0.15
SIZE_GOD_CAP = 30.0
MAX_FUNCS_PER_FILE = 20
TOO_MANY_FUNCS_ISSUE = 25
STRUCTURE_FUNC_FACTOR = 3.0
STRUCTURE_FUNC_CAP = 60.0
STRUCTURE_GOD_FACTOR = 0.05
STRUCTURE_GOD_CAP = 40.0

# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

ERROR_HIT_POINTS = 22.0

# ---------------------------------------------------------------------------
# Documentation ratio bands, as fractions of the nonblank lines
# ---------------------------------------------------------------------------

DOC_MIN_FILE_LINES = 20
DOC_ISSUE_MIN_LINES = 30
DOC_NEAR_ZERO = 0.02
DOC_LOW = 0.05
DOC_HIGH = 0.40
DOC_EXTREME = 0.55
DOC_SCORE_NEAR_ZERO = 70.0
DOC_SCORE_LOW = 35.0
DOC_SCORE_HIGH = 20.0
DOC_SCORE_EXTREME = 45.0

# ---------------------------------------------------------------------------
# Naming
# ---------------------------------------------------------------------------

NAMING_SINGLE_FACTOR = 4.5
NAMING_SINGLE_CAP = 40.0
NAMING_MEANINGLESS_FACTOR = 3.2
NAMING_MEANINGLESS_CAP = 40.0
NAMING_MIXED_POINTS = 26.0
NAMING_SINGLE_ISSUE = 4
NAMING_MEANINGLESS_ISSUE = 3
NAMING_MIXED_MIN = 3

# ---------------------------------------------------------------------------
# Duplication, over substantive lines only
# ---------------------------------------------------------------------------

MIN_DUP_LINE_LEN = 20
DUP_RATIO_FACTOR = 170.0
DUP_BLOCK_LINES = 5
DUP_BLOCK_FACTOR = 8.0
DUP_BLOCK_CAP = 40.0
DUP_RATIO_ISSUE = 0.10
DUP_BLOCK_ISSUE = 2

# ---------------------------------------------------------------------------
# Tech debt markers and commented-out code
# ---------------------------------------------------------------------------

DEBT_FACTOR = 22.0
DEBT_ISSUE = 2
COMMENTED_BLOCK_MIN = 3
COMMENTED_BLOCK_POINTS = 20.0
COMMENTED_LINE_POINTS = 3.0

# ---------------------------------------------------------------------------
# Magic numbers
# ---------------------------------------------------------------------------

MAGIC_FACTOR = 7.0
MAGIC_ISSUE = 4
MAGIC_ALLOWED = (0.0, 1.0, 2.0, -1.0)

# ---------------------------------------------------------------------------
# Secrets, dead code, globals, parameters, imports
# ---------------------------------------------------------------------------

SECRET_FACTOR = 45.0
DEAD_UNUSED_IMPORT_FACTOR = 6.0
DEAD_UNUSED_IMPORT_CAP = 60.0
DEAD_FUNC_FACTOR = 8.0
DEAD_FUNC_CAP = 40.0
DEAD_UNREACHABLE_FACTOR = 10.0
DEAD_UNREACHABLE_CAP = 30.0
GLOBAL_MUTABLE_POINTS = 16.0
GLOBAL_KEYWORD_POINTS = 14.0
GLOBAL_MUTABLE_DEFAULT_POINTS = 18.0
GLOBAL_ISSUE_MIN = 2
PARAM_LIMIT = 5
PARAM_FACTOR = 22.0
PARAM_CAP = 60.0
STAR_ALLOWANCE = 2
STAR_FACTOR = 10.0
STAR_CAP = 40.0
STAR_ISSUE = 4
IMPORT_FREE_COUNT = 12
IMPORT_FACTOR = 5.0
IMPORT_CAP = 50.0
IMPORT_ISSUE_COUNT = 15
STAR_IMPORT_POINTS = 25.0
MIDFILE_IMPORT_POINTS = 10.0

# ---------------------------------------------------------------------------
# Formatting and dangerous calls and debug leftovers
# ---------------------------------------------------------------------------

LONG_LINE_LIMIT = 120
FORMAT_LONG_FACTOR = 14.0
FORMAT_LONG_CAP = 60.0
FORMAT_TRAIL_FACTOR = 400.0
FORMAT_TRAIL_CAP = 25.0
FORMAT_MIXED_POINTS = 15.0
FORMAT_LONG_ISSUE = 4
DANGEROUS_FACTOR = 40.0
DEBUG_STMT_FACTOR = 16.0
DEBUG_STMT_CAP = 70.0
DEBUG_EMPTY_POINTS = 25.0
DEBUG_EMPTY_CAP = 50.0

# ---------------------------------------------------------------------------
# Report shaping
# ---------------------------------------------------------------------------

ADVICE_MIN_SCORE = 20.0
MAX_RECOMMENDATIONS = 8
DEFAULT_TOP = 10
NAME_TAIL = 41
BAR_WIDTH = 24
ISSUE_LIMIT_CONSOLE = 15
ISSUE_LIMIT_MARKDOWN = 20
NAMES_PREVIEW = 4
