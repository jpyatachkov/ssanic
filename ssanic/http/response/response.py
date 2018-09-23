from .headers import Headers
from .status_line import StatusLine

__all__ = (
    'Response',
)


class Response:
    DEFAULT_READ_CHUNK_SIZE = 1024

    def __init__(self, status_code, header_pairs):
        self.status_line = StatusLine(status_code)
        self.headers = Headers(header_pairs)

    def __str__(self):
        return '{}\r\n{}\r\n'.format(str(self.status_line), str(self.headers))
