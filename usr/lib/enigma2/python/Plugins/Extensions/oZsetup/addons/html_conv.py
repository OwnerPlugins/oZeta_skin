import re
import sys
import six
import types
from six import unichr, iteritems
from six.moves import html_entities

# Python 2/3 compatibility definitions with safe fallbacks
try:
    # Try to use native Python 2 types
    basestring = basestring
    long = long
    unicode = unicode
except NameError:
    # Python 3 - define aliases for compatibility
    basestring = str
    long = int
    unicode = str

# Type definitions for cross-version compatibility
string_types = (basestring,)
integer_types = (int, long)
text_type = unicode
binary_type = bytes if sys.version_info[0] >= 3 else str

# Class types compatibility
class_types = (type,) if six.PY3 else (type, types.ClassType)
MAXSIZE = sys.maxsize  # Compatible with both versions

_UNICODE_MAP = {
    k: unichr(v) for k,
    v in iteritems(
        html_entities.name2codepoint)}
_ESCAPE_RE = re.compile("[&<>\"']")
_UNESCAPE_RE = re.compile(r"&\s*(#?)(\w+?)\s*;")
_ESCAPE_DICT = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&apos;",
}


def ensure_str(s, encoding="utf-8", errors="strict"):
    """Coerce *s* to `str`.

    - In Python 2:
      - `unicode` -> encoded to `str`
      - `str` -> `str`
    - In Python 3:
      - `str` -> `str`
      - `bytes` -> decoded to `str`
    """
    if not isinstance(s, string_types + (binary_type,)):
        raise TypeError("not expecting type '%s'" % type(s))

    if isinstance(s, text_type):
        return s.encode(encoding, errors)
    elif isinstance(s, binary_type):
        # For Python 3 bytes, or Python 2 str
        if sys.version_info[0] >= 3:
            return s.decode(encoding, errors)
        else:
            return s
    return s


def html_escape(value):
    return _ESCAPE_RE.sub(
        lambda match: _ESCAPE_DICT[match.group(0)], ensure_str(value).strip())


def html_unescape(value):
    return _UNESCAPE_RE.sub(_convert_entity, text_type(value).strip())


def _convert_entity(m):
    if m.group(1) == "#":
        try:
            return unichr(int(m.group(2)[1:], 16)) if m.group(
                2)[:1].lower() == "x" else unichr(int(m.group(2)))
        except ValueError:
            return "&#%s;" % m.group(2)
    return _UNICODE_MAP.get(m.group(2), "&%s;" % m.group(2))
