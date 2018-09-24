__all__ = (
    'StatusLine',
)


def _get_reason_phrase_by_code(status_code):
    if status_code == 200:
        return 'OK'
    elif status_code == 400:
        # Из-за строчки (proto, code, status) = statusline.split(" "); в httptest.py
        return 'Bad_Request'
    elif status_code == 403:
        return 'Forbidden'
    elif status_code == 404:
        return 'Not Found'
    elif status_code == 405:
        return 'Method Not Allowed'
    else:
        return ''


class StatusLine:
    HTTP_VERSION = '1.1'

    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        reason_phrase = _get_reason_phrase_by_code(self.status_code)
        return 'HTTP/{} {} {}'.format(self.HTTP_VERSION, self.status_code, reason_phrase)

    def __repr__(self):
        reason_phrase = _get_reason_phrase_by_code(self.status_code)
        return 'STATUS LINE: HTTP/{} {} {}'.format(self.HTTP_VERSION, self.status_code, reason_phrase)
