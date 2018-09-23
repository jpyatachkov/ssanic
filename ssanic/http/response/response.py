from .headers import Headers
from .status_line import StatusLine

__all__ = (
    'Response',
)


class Response:
    DEFAULT_READ_CHUNK_SIZE = 1024

    def __init__(self, status_code, header_pairs, file_reader=None):
        self.status_line = StatusLine(status_code)
        self.headers = Headers(header_pairs)
        self.file_reader = file_reader

    async def write(self):
        yield str(self.status_line)
        yield str(self.headers)

        if self.file_reader is not None:
            async for line in self.file_reader.read(self.DEFAULT_READ_CHUNK_SIZE):
                if line:
                    yield line
