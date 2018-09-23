from .headers import HeadersParser
from .request_line import RequestLineParser

__all__ = (
    'RequestParser',
)


class RequestParser:
    DELIMITER = r'\r\n'

    def __init__(self):
        self.request_line = RequestLineParser()
        self.headers = HeadersParser()

    def __call__(self, http_request):
        if not http_request or not isinstance(http_request, str):
            return False

        split = http_request.split(self.DELIMITER * 2)

        if len(split) == 2:
            head, body = split
            return self._parse_head(head)
        else:
            return False

    def _parse_head(self, raw_head):
        head = raw_head.split(self.DELIMITER)

        if len(head) > 1:
            request_line, *headers = head
            return self.request_line(request_line) and self.headers(headers)
        elif len(head) == 1:
            return self.request_line(*head)
        else:
            return False
