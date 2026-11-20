#!/usr/bin/env python3
"""Self-tests for fuck-your-code. Run: python3 tests/run_tests.py"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "src", "fuck_your_code.py")
EX = os.path.join(ROOT, "examples")
SRC = os.path.join(ROOT, "src")

NEW_DIMENSIONS = ("nesting", "funclen", "techdebt", "commented", "magic",
                  "secrets", "deadcode", "globals", "params", "imports",
                  "formatting", "dangerous", "debug")


def run(*args):
    proc = subprocess.run(
        [sys.executable, TOOL] + list(args),
        capture_output=True, text=True, cwd=ROOT)
    if proc.returncode != 0:
        raise AssertionError("command failed: %s\n%s" % (args, proc.stderr))
    return proc.stdout


def quality_of(path, lang="en"):
    out = run("analyze", path, "--lang", lang, "--format", "json")
    data = json.loads(out)  # also proves JSON parses
    return data["files"][0]["quality"], data


def main():
    good_q, _ = quality_of(os.path.join(EX, "good.py"))
    shit_q, shit_data = quality_of(os.path.join(EX, "shit_mountain.py"))
    gap = good_q - shit_q
    print("good.py quality:          %.1f" % good_q)
    print("shit_mountain.py quality: %.1f" % shit_q)
    print("gap:                      %.1f (need >= 25)" % gap)
    assert gap >= 25, "quality gap too small: %.1f" % gap
    assert good_q >= 70, "good.py should score well, got %.1f" % good_q
    assert shit_q < 50, "shit_mountain.py should score badly, got %.1f" % shit_q

    js_q, js_data = quality_of(os.path.join(EX, "shit_mountain.js"))
    print("shit_mountain.js quality: %.1f" % js_q)
    assert js_q < good_q, "bad JS should lose to good.py"
    assert js_q < 55, "shit_mountain.js should score badly, got %.1f" % js_q

    # exactly twenty dimensions, in the aggregate and per file
    assert len(shit_data["checks"]) == 20, "aggregate must have 20 checks"
    assert len(shit_data["files"][0]["checks"]) == 20, "file must have 20 checks"
    for key in NEW_DIMENSIONS:
        assert key in shit_data["checks"], "missing dimension: %s" % key
    print("twenty dimensions: OK")

    # the new dimensions demonstrably fire on the shit samples
    fired = {issue["check"] for issue in shit_data["issues"]}
    for key in ("magic", "secrets", "dangerous", "techdebt", "commented",
                "debug", "params", "deadcode", "globals", "imports",
                "nesting", "funclen"):
        assert key in fired, "dimension never fired on shit_mountain.py: %s" % key
    js_fired = {issue["check"] for issue in js_data["issues"]}
    assert "formatting" in js_fired, "formatting never fired on the JS sample"
    print("new dimensions fire on shit samples: OK")

    # serious recommendations: generated, present in every format
    assert shit_data["recommendations"], "recommendations must not be empty"
    for entry in shit_data["recommendations"]:
        assert entry["file"] and entry["advice"], "recommendation lacks detail"
    en_console = run("analyze", os.path.join(EX, "shit_mountain.py"),
                     "--lang", "en")
    assert "Serious recommendations" in en_console, "EN advice section missing"
    zh_console = run("analyze", os.path.join(EX, "shit_mountain.py"),
                     "--lang", "zh")
    assert "正经建议" in zh_console, "ZH advice section missing"
    md = run("analyze", os.path.join(EX, "shit_mountain.py"),
             "--format", "markdown", "--lang", "en")
    assert "Serious recommendations" in md, "markdown advice section missing"
    print("serious recommendations: OK (%d entries)"
          % len(shit_data["recommendations"]))

    # both languages produce a console report
    en = run("analyze", os.path.join(EX, "good.py"), "--lang", "en")
    zh = run("analyze", os.path.join(EX, "good.py"), "--lang", "zh")
    assert "SHITTY CODE REPORT" in en, "EN report title missing"
    assert "屎山代码检测报告" in zh, "ZH report title missing"
    print("en + zh console reports: OK")

    # markdown + paste + --code paths
    assert md.startswith("#"), "markdown report should start with a title"
    proc = subprocess.run(
        [sys.executable, TOOL, "paste", "--ext", "py", "--format", "json"],
        input="x=1\n", capture_output=True, text=True, cwd=ROOT)
    assert proc.returncode == 0 and json.loads(proc.stdout), "paste failed"
    out = run("--code", "def f(a):\n    return a+1\n", "--ext", "py",
              "--format", "json")
    assert json.loads(out)["files"], "--code failed"
    print("markdown / paste / --code: OK")

    # whole examples directory runs
    data = json.loads(run("analyze", EX, "--format", "json"))
    assert len(data["files"]) == 3, "expected 3 example files"
    print("directory scan: OK (3 files)")

    # self-scan smoke test: the tool survives its own source tree
    data = json.loads(run("analyze", SRC, "--format", "json"))
    assert len(data["files"]) >= 8, "self-scan should cover the package"
    assert len(data["checks"]) == 20, "self-scan must have 20 checks"
    print("self-scan smoke test: OK (%d files, quality %.1f)"
          % (len(data["files"]), data["overall_quality"]))
    print("ALL TESTS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
