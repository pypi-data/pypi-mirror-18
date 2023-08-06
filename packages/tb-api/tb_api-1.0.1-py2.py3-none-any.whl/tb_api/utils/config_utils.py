import re

method_pattern = re.compile('^\$(\w+)\.(\w+)$')


class InvalidMethodPathError(Exception):
    pass


def parse_method_path(method_path):
    m = method_pattern.search(method_path)

    if not m:
        raise InvalidMethodPathError(method_path)

    return m.group(1), m.group(2)
