"""Command line entry point for fuck-your-code.

Handles argument parsing, file collection and output plumbing.
The analysis itself lives in the analyzer module; this file only
moves code from the user's disk or clipboard into the analyzer
and moves the finished report back out.
"""

import argparse
import fnmatch
import json
import os
import sys

from fyc import VERSION
from fyc import analyzer
from fyc import constants
from fyc import i18n
from fyc import lexing
from fyc import report

SNIFF_BYTES = 4096


def load_edition_default():
    """Read the language preset shipped with this copy of the tool."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "edition.json"),
        os.path.join(here, "..", "edition.json"),
        os.path.join(here, "..", "..", "edition.json"),
        os.path.join(os.getcwd(), "edition.json"),
    ]
    for path in candidates:
        try:
            with open(path, "r", encoding="utf-8") as handle:
                preset = json.load(handle)
            if preset.get("default_lang") in ("en", "zh"):
                return preset["default_lang"]
        except (OSError, ValueError):
            continue
    return "en"


def is_excluded(rel_path, patterns):
    """Check a relative path against the exclusion globs."""
    parts = rel_path.replace("\\", "/").split("/")
    for pattern in patterns:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
        for part in parts:
            if fnmatch.fnmatch(part, pattern):
                return True
    return False


def collect_files(paths, excludes):
    """Expand file and directory arguments into source files."""
    collected = []
    for target in paths:
        if os.path.isfile(target):
            lang_name, ext = lexing.detect_lang(target)
            if ext in constants.KNOWN_EXTS:
                collected.append(target)
        elif os.path.isdir(target):
            _collect_from_dir(target, excludes, collected)
        else:
            sys.stderr.write("warning: no such path: %s\n" % target)
    return collected


def _collect_from_dir(target, excludes, collected):
    """Walk one directory tree, appending every source file found."""
    for root, dirs, names in os.walk(target):
        dirs.sort()
        for name in sorted(names):
            full = os.path.join(root, name)
            rel = os.path.relpath(full, target)
            lang_name, ext = lexing.detect_lang(full)
            if ext not in constants.KNOWN_EXTS:
                continue
            if is_excluded(rel, excludes):
                continue
            collected.append(full)


def read_text_file(path):
    """Read a file as text, skipping anything that looks binary."""
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError as exc:
        sys.stderr.write("warning: cannot read %s: %s\n" % (path, exc))
        return None
    if b"\x00" in raw[:SNIFF_BYTES]:
        return None
    for encoding in ("utf-8", "utf-8-sig", "gbk", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace")


def build_parser():
    """Build the argument parser with its subcommands."""
    parser = argparse.ArgumentParser(
        prog="fuck-your-code",
        description="Grade how shitty your code is. Fully offline.")
    parser.add_argument("--version", action="version",
                        version="fuck-your-code " + VERSION)
    parser.add_argument("--code", default=None,
                        help="analyze this code snippet directly")
    parser.add_argument("--ext", default=None, help="language hint, e.g. py, js")
    _add_common(parser)
    sub = parser.add_subparsers(dest="cmd")
    analyze_parser = sub.add_parser("analyze", help="analyze files or folders")
    analyze_parser.add_argument("paths", nargs="+",
                                help="files or folders to analyze")
    _add_common(analyze_parser)
    paste_parser = sub.add_parser("paste", help="analyze code from stdin")
    paste_parser.add_argument("--ext", default=None,
                              help="language hint, e.g. py, js")
    _add_common(paste_parser)
    return parser


def _add_common(parser):
    """Attach the options every subcommand shares."""
    parser.add_argument("--lang", choices=("en", "zh"), default=None,
                        help="report language (default: edition preset)")
    parser.add_argument("--format", choices=("console", "markdown", "json"),
                        default="console", help="output format")
    parser.add_argument("--output", help="write report to file", default=None)
    parser.add_argument("--top", type=int, default=constants.DEFAULT_TOP,
                        help="how many worst files to list")
    parser.add_argument("--exclude", action="append", default=None,
                        help="extra glob to exclude (repeatable)")


def emit(rep, fmt, output, top):
    """Render the report and send it to a file or to stdout."""
    if fmt == "json":
        text = report.render_json(rep, top)
    elif fmt == "markdown":
        text = report.render_markdown(rep, top)
    else:
        text = report.render_console(rep, top)
    if output:
        with open(output, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    else:
        sys.stdout.write(text + "\n")


def main(argv=None):
    """Entry point: parse arguments, analyze, render, report."""
    argv = list(sys.argv[1:] if argv is None else argv)
    default_lang = load_edition_default()
    known = ("analyze", "paste", "-h", "--help", "--version", "--code")
    if argv and argv[0] not in known:
        argv = ["analyze"] + argv
    parser = build_parser()
    args = parser.parse_args(argv)
    lang = args.lang or default_lang
    items = _gather_items(args, lang)
    if items is None:
        parser.print_help()
        return 2
    results = analyzer.analyze_all(items, lang)
    rep = analyzer.build_report(results, lang)
    emit(rep, args.format, args.output, args.top)
    return 0


def _gather_items(args, lang):
    """Turn parsed arguments into analyzer input triples."""
    if args.cmd == "analyze":
        return _items_from_paths(args.paths, args.exclude)
    strings = i18n.strings_for(lang)
    lang_name, _ext = lexing.detect_lang("", args.ext)
    if args.code is not None:
        return [(strings["paste_label"], args.code, lang_name)]
    if args.cmd == "paste":
        if sys.stdin.isatty():
            sys.stderr.write(strings["stdin_hint"] + "\n")
        return [(strings["paste_label"], sys.stdin.read(), lang_name)]
    return None


def _items_from_paths(paths, extra_excludes):
    """Read every collected file into an analyzer input triple."""
    excludes = list(constants.DEFAULT_EXCLUDE_GLOBS)
    excludes += list(extra_excludes or [])
    items = []
    for path in collect_files(paths, excludes):
        text = read_text_file(path)
        if text is None:
            continue
        lang_name, _ext = lexing.detect_lang(path)
        items.append((os.path.relpath(path), text, lang_name))
    return items
