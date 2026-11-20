"""Language lookup for the analyzer.

The two string tables live in their own modules as plain data;
this module wraps them so callers can fetch the active table
and the verdict tier for a score without knowing that.
"""

from types import MappingProxyType

from fyc import strings_en
from fyc import strings_zh

_TABLES = MappingProxyType({"en": strings_en.STRINGS_EN,
                            "zh": strings_zh.STRINGS_ZH})


def strings_for(lang):
    """Return the string table for a language code."""
    return _TABLES.get(lang, _TABLES["en"])


def tier_for(quality, lang):
    """Return the verdict label and roast for a quality score."""
    tiers = _TABLES.get(lang, _TABLES["en"])["tiers"]
    for threshold, name, roast in tiers:
        if quality >= threshold:
            return name, roast
    return tiers[-1][1], tiers[-1][2]
