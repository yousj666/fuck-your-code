# Fuck Your Code

Not you — your CODE. Run it on your own code and find out how shitty it is.

A command-line shitty-code detector with a sense of humour. Point it at a
file, a whole project folder, or paste a blob of code straight in, and it
grades the mess: a per-file **Shit-Gas Index** (0–100, higher = worse) and an
overall **quality score** (0–100, higher = better), plus a verdict you can
quote at code review.

It is a joke with real measurements underneath: twenty checks look at
complexity, nesting, function length, size, structure, duplication, error
handling, hardcoded secrets, dangerous calls, dead code, global state,
parameter bloat, import chaos, documentation, commented-out code, tech
debt, naming, magic numbers, formatting and debug leftovers, across 20+
languages (Python, JavaScript/TypeScript, Go, Java, C/C++, Rust, C#, PHP,
Ruby, Swift, Kotlin, shell, Lua, Perl, Scala…).

**Fully offline.** No network, no uploads, no telemetry — your shame stays
on your machine. Pure Python 3 standard library, zero dependencies.

## Install

You need Python 3.8+ and nothing else.

```bash
unzip fuck-your-code-en.zip   # or the -zh edition
cd fuck-your-code
./fuck-your-code --help       # Windows: fuck-your-code.bat
```

This English edition defaults to English output; the Chinese edition
(`fuck-your-code-zh.zip`) defaults to Chinese. Either can be switched at
runtime with `--lang en|zh`. The default comes from `edition.json` next to
the launcher: `{"default_lang": "en"}`.

## Usage

```bash
# One file (drag-and-drop the path into your terminal works too)
./fuck-your-code analyze app.py
./fuck-your-code app.py

# A whole directory, or several paths at once
./fuck-your-code analyze src/ legacy/ tools/

# Paste code directly (ends with Ctrl-D; --ext hints the language)
./fuck-your-code paste --ext js
cat snippet.py | ./fuck-your-code paste --ext py

# Or pass a snippet inline
./fuck-your-code --code "def f(x): return x+1" --ext py
```

## Options

| Option | Meaning |
|---|---|
| `--lang en\|zh` | Report language (default: from `edition.json`) |
| `--format console\|markdown\|json` | Output format |
| `--output <file>` | Write the report to a file instead of stdout |
| `--top <n>` | How many worst files to list (default 10) |
| `--exclude <glob>` | Extra exclude glob (repeatable) |

Default excludes: `.git`, `node_modules`, `__pycache__`, `dist`, `build`,
`vendor`, `*.min.js`, and binary files are always skipped.

## How scoring works

Each file gets twenty sub-scores of shittiness (0–100). The weighted blend —
complexity 11%, duplication 9%, error handling 7%, nesting 6%, hardcoded
secrets 6%, dangerous calls 6%, function length 5%, naming 5%, magic
numbers 5%, dead code 5%, size 4%, structure 4%, documentation 4%, global
state 4%, import chaos 4%, tech debt 3%, commented-out code 3%, parameter
bloat 3%, formatting 3%, debug leftovers 3% — becomes the file's Shit-Gas
Index. Project quality is 100 minus the line-weighted Shit-Gas Index,
mapped to five verdict tiers, from "Cleaner than a surgeon's group chat"
down to "Weapon-grade code crime".

After the roasting, every report ends with a **Serious recommendations**
section: concrete, professional fixes generated from that run's actual
findings — which dimension hurt, in which file, and what to do about it.

And yes, the tool grades itself: pointed at its own source tree it scores
100.0. It got there the honest way — see `SELF_FIX_LOG.md`.

Try it on the bundled examples:

```bash
./fuck-your-code analyze examples/good.py           # the tidy one
./fuck-your-code analyze examples/shit_mountain.py  # the crime scene
./fuck-your-code analyze examples/ --lang zh        # same, in Chinese
```

## Tests

```bash
python3 tests/run_tests.py
```

## License

MIT, © Yousj. See `LICENSE`.
