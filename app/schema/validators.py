import re

NUMERIC_RE = re.compile(r'[0-9]+')


def is_numeric(value):
    return NUMERIC_RE.fullmatch(value) is not None
