import re

# This regex is not going to catch every possible ansi escape sequence, but should suffice for
# our purposes.
ansi_regex = re.compile(r"\x1b[^m]*?m")
