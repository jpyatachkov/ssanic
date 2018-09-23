# noinspection PyProtectedMember
from ssanic.http.response.status_line import (
    StatusLine,
    _get_reason_phrase_by_code
)
import pytest


@pytest.mark.parametrize('status_code,expected', [
    (200, 'OK'),
    (400, 'Bad Request'),
    (403, 'Forbidden'),
    (404, 'Not Found'),
    (405, 'Method Not Allowed'),
    (0, '')
])
def test_get_reason_phrase_by_code(status_code, expected):
    assert expected == _get_reason_phrase_by_code(status_code)


@pytest.mark.parametrize('status_code,expected', [
    (200, ('HTTP/1.1 200 OK', 'STATUS LINE: HTTP/1.1 200 OK')),
])
def test_status_line_constructor(status_code, expected):
    expected_str, expected_repr = expected

    sl = StatusLine(status_code)

    assert expected_str == str(sl)
    assert expected_repr == repr(sl)
