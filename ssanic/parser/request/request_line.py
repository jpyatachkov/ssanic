import re

__all__ = (
    'RequestLineParser',
)


class RequestLineParser:
    ALLOWED_SCHEMAS = (None, 'request', 'https')
    REQUEST_LINE_REGEX_PATTERN = r'^(?P<method>[A-Z]+) ((?P<scheme>\w+)://)?(?(3)[^/]*)(?P<path>/?[^\?#]*/?)?(\?[^#]*)?(\#.*)? HTTP/1.1$'

    def __init__(self):
        self._re = re.compile(self.REQUEST_LINE_REGEX_PATTERN)
        self.method = None
        self.path = None

    def __call__(self, request_line):
        if not str or not isinstance(request_line, str):
            return False

        match = self._re.match(request_line)

        if not match or match.group('scheme') not in self.ALLOWED_SCHEMAS:
            return False

        self.method = match.group('method')
        self.path = match.group('path') or '/'

        return True
