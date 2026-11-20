"""Serious recommendations, generated from the actual findings.

The jokes come first in every report, but a roast alone does not
fix anything. This module ranks the checks that scored badly in
the current run and attaches matching professional advice.
Nothing here is a static list: no bad score, no advice.
"""

from fyc import constants


def build_recommendations(agg_checks, results, issues, strings):
    """Build the advice list for one finished analysis run.

    Dimensions are ranked by their aggregated shittiness, the
    worst ones first, and each one names the file that scored
    worst on it. When nothing crosses the advice threshold but
    issues exist, the dimension of the worst single issue still
    earns a mention.
    """
    ranked = sorted(agg_checks.items(), key=lambda item: -item[1])
    picked = []
    for key, score in ranked:
        if score < constants.ADVICE_MIN_SCORE:
            continue
        if len(picked) >= constants.MAX_RECOMMENDATIONS:
            break
        target = _worst_file_for(results, key)
        if target is not None:
            picked.append(_entry(key, target, strings))
    if not picked and issues:
        key = issues[0]["check"]
        target = _worst_file_for(results, key) or issues[0]["file"]
        return [_entry(key, target, strings)]
    return picked


def _entry(key, target, strings):
    """Build one recommendation record for a check and a file."""
    return {"check": key, "file": target,
            "advice": strings["advice_" + key].format(file=target)}


def _worst_file_for(results, key):
    """Return the name of the file with the worst score on a check."""
    best_name = None
    best_score = -1.0
    for result in results:
        if result["checks"][key] > best_score:
            best_score = result["checks"][key]
            best_name = result["file"]
    return best_name
