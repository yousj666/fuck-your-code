"""Report rendering for fuck-your-code.

The analysis produces one plain data structure; this module
turns it into terminal text, Markdown or JSON. Every renderer
shows the same story in the same order: the score, the verdict,
the twenty check bars, the hall of shame, the worst offences,
and finally the serious recommendations.
"""

import json

from fyc import VERSION
from fyc import constants
from fyc import i18n

RULE_WIDTH = 68
FILE_COL = 44
CONSOLE_FORMATS = ("%s: %.1f / 100", "%s: %s", ">> ", "%s: %d    %s: %d")
MARKDOWN_FORMATS = ("**%s: %.1f / 100**", "**%s:** %s", "> ",
                    "%s: %d | %s: %d")


def render_bar(score, width=constants.BAR_WIDTH):
    """Render a score as a fixed-width ASCII bar."""
    filled = int(round(score / constants.PERCENT * width))
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def _join(lines):
    """Join report lines into one document of text."""
    return "\n".join(lines)


def _section(title):
    """Start a console section: a blank line, then its heading."""
    return ["", title]


def _md_section(title):
    """Start a Markdown section with a level-two heading."""
    return ["", "## " + title, ""]


def _summary_lines(rep, strings, formats, spacer):
    """Build the score, verdict, roast and size lines of a report.

    The spacer is inserted between the lines when it is not None,
    which is how the Markdown renderer gets its blank lines while
    the console renderer stays compact.
    """
    score_fmt, verdict_fmt, roast_prefix, counts_fmt = formats
    score_line = score_fmt % (strings["overall_quality"], rep["overall_quality"])
    verdict_line = verdict_fmt % (strings["verdict"], rep["verdict"])
    roast_line = roast_prefix + rep["roast"]
    counts_line = counts_fmt % (strings["files_analyzed"], len(rep["files"]),
                                strings["total_lines"], rep["total_lines"])
    lines = []
    for part in (score_line, verdict_line, roast_line, counts_line):
        lines.append(part)
        if spacer is not None:
            lines.append(spacer)
    return lines


def _check_lines(rep, strings, template):
    """Build one formatted line per check, bars included."""
    lines = []
    for key in constants.CHECK_KEYS:
        value = rep["checks"][key]
        lines.append(template % (strings["checks"][key],
                                 render_bar(value), value))
    return lines


def _issue_location(issue):
    """Render where an issue lives, with its line when known."""
    location = issue["file"]
    if issue.get("line"):
        location += ":%s" % issue["line"]
    return location


def _advice_entries(rep, bullet):
    """Format each recommendation with the section's bullet."""
    return [bullet + entry["advice"] for entry in rep["recommendations"]]


def render_console(rep, top):
    """Render the report as plain terminal text."""
    strings = i18n.strings_for(rep["lang"])
    rule = "=" * RULE_WIDTH
    lines = [rule, strings["app_tagline"], strings["report_title"], rule]
    if not rep["files"]:
        lines.append(strings["no_files"])
        return _join(lines)
    lines.extend(_summary_lines(rep, strings, CONSOLE_FORMATS, None))
    checks = _section(strings["check_breakdown"])
    checks.extend(_check_lines(rep, strings, "  %-22s %s %5.1f"))
    lines.extend(checks)
    lines.extend(_console_worst(rep, strings, top))
    lines.extend(_console_issues(rep, strings))
    lines.extend(_console_advice(rep, strings))
    return _join(lines)


def _console_worst(rep, strings, top):
    """Build the hall of shame table of the report."""
    lines = _section(strings["worst_files"])
    header = "  %-*s %8s %8s %6s" % (
        FILE_COL, strings["col_file"], strings["col_score"],
        strings["col_quality"], strings["col_lines"])
    lines.append(header)
    for result in rep["worst_files"][:top]:
        name = result["file"]
        if len(name) > FILE_COL:
            name = "..." + name[-constants.NAME_TAIL:]
        row = "  %-*s %8.1f %8.1f %6d" % (
            FILE_COL, name, result["shit_index"],
            result["quality"], result["lines"])
        lines.append(row)
    return lines


def _console_issues(rep, strings):
    """Build the worst offences list of the report."""
    lines = ["", strings["top_issues"]]
    if not rep["issues"]:
        lines.append("  " + strings["clean_bill"])
        return lines
    for issue in rep["issues"][:constants.ISSUE_LIMIT_CONSOLE]:
        check_name = strings["checks"][issue["check"]]
        entry = "  - [%s] %s -- %s" % (check_name, _issue_location(issue),
                                       issue["message"])
        lines.append(entry)
    return lines


def _console_advice(rep, strings):
    """Build the serious recommendations section, when present."""
    if not rep["recommendations"]:
        return []
    lines = []
    lines.extend(_section(strings["recommendations_title"]))
    lines.extend(_advice_entries(rep, "  - "))
    return lines


def render_markdown(rep, top):
    """Render the report as Markdown."""
    labels = i18n.strings_for(rep["lang"])
    lines = ["# " + labels["report_title"], "", labels["app_tagline"], ""]
    if not rep["files"]:
        lines.append(labels["no_files"])
        return _join(lines)
    lines.extend(_summary_lines(rep, labels, MARKDOWN_FORMATS, ""))
    lines.append("## " + labels["check_breakdown"])
    lines.append("")
    lines.extend(_check_lines(rep, labels, "- %s: `%s` %.1f"))
    lines.extend(_markdown_worst(rep, labels, top))
    lines.extend(_markdown_issues(rep, labels))
    lines.extend(_markdown_advice(rep, labels))
    return _join(lines)


def _markdown_worst(rep, strings, top):
    """Build the Markdown hall of shame table."""
    table = _md_section(strings["worst_files"])
    columns = (strings["col_file"], strings["col_lang"],
               strings["col_score"], strings["col_quality"],
               strings["col_lines"])
    table.append("| %s | %s | %s | %s | %s |" % columns)
    table.append("|---|---|---:|---:|---:|")
    for entry in rep["worst_files"][:top]:
        row = "| %s | %s | %.1f | %.1f | %d |" % (
            entry["file"], entry["language"], entry["shit_index"],
            entry["quality"], entry["lines"])
        table.append(row)
    return table


def _markdown_issues(rep, strings):
    """Build the Markdown worst offences list."""
    items = _md_section(strings["top_issues"])
    if not rep["issues"]:
        items.append(strings["clean_bill"])
        return items
    for issue in rep["issues"][:constants.ISSUE_LIMIT_MARKDOWN]:
        entry = "- **%s** `%s` -- %s" % (
            strings["checks"][issue["check"]], _issue_location(issue),
            issue["message"])
        items.append(entry)
    return items


def _markdown_advice(rep, strings):
    """Build the Markdown serious recommendations section."""
    if not rep["recommendations"]:
        return []
    section = _md_section(strings["recommendations_title"])
    section.extend(_advice_entries(rep, "- "))
    return section


def render_json(rep, top):
    """Render the report as a JSON document."""
    payload = {"tool": "fuck-your-code", "version": VERSION,
               "lang": rep["lang"]}
    copied = ("overall_quality", "shit_index", "verdict", "roast",
              "checks", "total_lines")
    for key in copied:
        payload[key] = rep.get(key)
    payload["files"] = rep["files"]
    payload["worst_files"] = [result["file"]
                              for result in rep.get("worst_files", [])[:top]]
    payload["issues"] = rep.get("issues", [])
    payload["recommendations"] = rep.get("recommendations") or []
    return json.dumps(payload, ensure_ascii=False, indent=2)
