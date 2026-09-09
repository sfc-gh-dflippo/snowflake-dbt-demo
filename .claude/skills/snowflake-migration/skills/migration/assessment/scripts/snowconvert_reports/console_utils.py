"""Windows-safe console glyphs for assessment scripts.

On Windows the default console codepage (cp1252) cannot encode Unicode
check marks and similar symbols, causing UnicodeEncodeError on print().
This module exposes glyph constants that fall back to ASCII when the
terminal encoding doesn't support them.
"""
import sys


def _supports_unicode(stream=None):
    """True when the output stream can encode the glyphs we use."""
    stream = stream or sys.stdout
    encoding = getattr(stream, "encoding", None) or "ascii"
    try:
        "\u2713\u2717\u2705\u26a0".encode(encoding)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


_UNICODE = _supports_unicode()

OK = "\u2713" if _UNICODE else "[ok]"        # ✓
FAIL = "\u2717" if _UNICODE else "[FAIL]"    # ✗
DONE = "\u2705" if _UNICODE else "[done]"    # ✅
WARN = "\u26a0" if _UNICODE else "[!]"       # ⚠
