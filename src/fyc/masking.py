"""String and comment masking for the analyzer.

Pattern-based checks should look at code, not at the contents of
string literals or comments: a detector that stores its own search
patterns as strings would otherwise flag itself. Masking replaces
string contents with spaces while preserving every quote character,
every newline and every column position, so line numbers and the
shape of the code survive intact.
"""

from fyc import constants

SLASH_COMMENT_LANGS = frozenset([
    "javascript", "typescript", "go", "java", "c", "cpp", "rust",
    "csharp", "php", "swift", "kotlin", "scala",
])
TEMPLATE_LANGS = frozenset(["javascript", "typescript"])


def mask_strings(text, lang_name):
    """Return the text with string contents blanked, comments kept."""
    return mask_text(text, lang_name, False)


def code_view(text, lang_name):
    """Return the text with strings and comments blanked out."""
    return mask_text(text, lang_name, True)


def mask_text(text, lang_name, blank_comments):
    """Blank string contents, and comments too when asked.

    The walk is a small state machine: at each position the text is
    either ordinary code, the start of a string, or the start of a
    comment, and each case is handled by one small helper.
    """
    chars = list(text)
    quotes = _quote_kinds(lang_name)
    pos = 0
    length = len(text)
    while pos < length:
        if text[pos] in quotes:
            pos = _blank_string(chars, text, pos)
        elif _is_line_comment_start(text, pos, lang_name):
            pos = _handle_span(chars, text, pos, _line_comment_end(text, pos),
                               blank_comments)
        elif _is_block_comment_start(text, pos, lang_name):
            pos = _handle_span(chars, text, pos, _block_comment_end(text, pos),
                               blank_comments)
        else:
            pos += 1
    return "".join(chars)


def _quote_kinds(lang_name):
    """Return the quote characters that start strings in a language."""
    quotes = [constants.SINGLE_QUOTE, constants.DOUBLE_QUOTE]
    if lang_name in TEMPLATE_LANGS:
        quotes.append(constants.BACKTICK)
    return quotes


def _is_line_comment_start(text, pos, lang_name):
    """Say whether a line comment starts at the given position."""
    if lang_name in constants.HASH_COMMENT_LANGS:
        return text[pos] == "#"
    marker = "--" if lang_name == "lua" else None
    if lang_name in SLASH_COMMENT_LANGS:
        marker = "//"
    return marker is not None and text.startswith(marker, pos)


def _is_block_comment_start(text, pos, lang_name):
    """Say whether a block comment starts at the given position."""
    if lang_name not in SLASH_COMMENT_LANGS:
        return False
    return text.startswith("/*", pos)


def _line_comment_end(text, pos):
    """Return the index where the line comment at pos ends."""
    found = text.find("\n", pos)
    if found == -1:
        return len(text)
    return found


def _block_comment_end(text, pos):
    """Return the index just past the block comment at pos."""
    found = text.find("*/", pos + 2)
    if found == -1:
        return len(text)
    return found + 2


def _handle_span(chars, text, start, end, blank):
    """Blank a comment span when asked, then return its end index."""
    if blank:
        _blank_range(chars, start, end)
    return end


def _blank_range(chars, start, end):
    """Replace a span of characters with spaces, keeping newlines."""
    pos = start
    while pos < end:
        if chars[pos] != "\n":
            chars[pos] = " "
        pos += 1


def _blank_string(chars, text, start):
    """Blank the contents of the string starting at the given index.

    The quote characters themselves are left in place, so code that
    assigns a literal to a suspicious name still shows its shape.
    Returns the index just past the closing quote.
    """
    quote = text[start]
    triple = text.startswith(quote * constants.TRIPLE_LEN, start)
    if triple:
        content_start = start + constants.TRIPLE_LEN
        closer_len = constants.TRIPLE_LEN
    else:
        content_start = start + 1
        closer_len = 1
    end, closed = _find_string_end(text, content_start, quote, triple)
    if closed:
        _blank_range(chars, content_start, end - closer_len)
    else:
        _blank_range(chars, content_start, end)
    return end


def _find_string_end(text, start, quote, triple):
    """Find where a string body ends, honouring backslash escapes.

    Returns a pair of the index just past the closing quote and a
    flag saying whether a closing quote was found at all.
    """
    if triple:
        return _find_triple_end(text, start, quote)
    return _find_single_end(text, start, quote)


def _find_triple_end(text, start, quote):
    """Find the end of a triple-quoted string body."""
    pos = start
    length = len(text)
    while pos < length:
        if text[pos] == "\\":
            pos += 2
        elif text.startswith(quote * constants.TRIPLE_LEN, pos):
            return pos + constants.TRIPLE_LEN, True
        else:
            pos += 1
    return len(text), False


def _find_single_end(text, start, quote):
    """Find the end of an ordinary quoted string body."""
    pos = start
    length = len(text)
    while pos < length:
        char = text[pos]
        if char == "\\":
            pos += 2
        elif char == quote:
            return pos + 1, True
        elif char == "\n" and quote != constants.BACKTICK:
            return pos, False
        else:
            pos += 1
    return length, False
