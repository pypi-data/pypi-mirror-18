import sys
import itertools

# -----------------------------------------------------------------------------

PY2 = int(sys.version_info[0]) == 2

# -----------------------------------------------------------------------------

if PY2:
    zip_longest = itertools.izip_longest
    basestring = basestring  # noqa
else:
    zip_longest = itertools.zip_longest
    basestring = (str, bytes)
