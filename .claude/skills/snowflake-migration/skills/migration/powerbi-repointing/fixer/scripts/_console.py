"""Windows-safe console glyphs for PowerBI repointing scripts."""
import sys


def _supports_unicode():
    encoding = getattr(sys.stdout, "encoding", None) or "ascii"
    try:
        "\u2713\u2717".encode(encoding)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


_UNICODE = _supports_unicode()

OK = "\u2713" if _UNICODE else "[ok]"
FAIL = "\u2717" if _UNICODE else "[FAIL]"
