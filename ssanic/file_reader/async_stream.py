__all__ = (
    'AsyncStreamFileReader',
)


class AsyncStreamFileReader:

    def __init__(self, file_path):
        self.fp = open(file_path, 'rb')

    async def read(self, size):
        while True:
            chunk = self.fp.read(size)

            if not chunk:
                self.fp.close()
                break

            yield chunk
