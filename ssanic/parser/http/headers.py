__all__ = (
    'HeadersParser',
)


class HeadersParser:
    DELIMITER = ': '

    def __init__(self):
        self.headers = None

    def __call__(self, raw_headers):
        if not raw_headers or not isinstance(raw_headers, list):
            return False

        self.headers = []
        for raw_header in raw_headers:
            pair = [x for x in raw_header.split(self.DELIMITER) if x]

            if len(pair) != 2:
                return False

            key, value = pair
            self.headers.append([key.lower(), value])

        return True
