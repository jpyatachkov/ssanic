import re

__all__ = (
    'RequestLineParser',
)


class RequestLineParser:
    ALLOWED_SCHEMAS = (None, 'http', 'https')
    INDEX_FILE_NAME = 'index.html'
    REQUEST_LINE_REGEX_PATTERN = r'^(?P<method>[A-Z]+) ((?P<scheme>\w+)://)?(?(3)[^/]*)/?(?P<path>[^\?#]*/?)?(\?[^#]*)?(\#.*)? HTTP/1.[0|1]$'

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

        if match.group('path') == '/':
            self.path = self.INDEX_FILE_NAME
        else:
            self.path = match.group('path') or self.INDEX_FILE_NAME

        return True
