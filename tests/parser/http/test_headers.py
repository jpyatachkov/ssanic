from ssanic.parser.http import HeadersParser
import pytest


@pytest.mark.parametrize('headers,expected', [
    (
        [
            'content-Type: application/json',
            'connection: keep-alive',
            'date: Tue, 15 Nov 1994 08:12:31 GMT',
            'accept: application/json',
        ],
        [
            ['content-type', 'application/json'],
            ['connection', 'keep-alive'],
            ['date', 'Tue, 15 Nov 1994 08:12:31 GMT'],
            ['accept', 'application/json'],
        ],
    ),
    (
        ['Accept-Encoding: gzip;q=1.0, identity; q=0.5, *;q=0'],
        [['accept-encoding', 'gzip;q=1.0, identity; q=0.5, *;q=0']],
    ),
    (
        ['If-None-Match: "xyzzy"'],
        [['if-none-match', '"xyzzy"']],
    ),
    (
        ['content-type: application/json'],
        [['content-type', 'application/json']],
    )
])
def test_correct_headers(headers, expected):
    parser = HeadersParser()

    assert parser(headers) is True
    assert expected == parser.headers


@pytest.mark.parametrize('headers', [
    ('', ),
    ([], ),
    (['contentlength'], ),
    (['accept'], ),
    (['accept=application/json'], ),
    (['content-type=application/json'], ),
    (['Accept=Accept=Accept=application/json'], ),
    (['Accept=Accept: Accept: application/json'], ),
])
def test_incorrect_headers(headers):
    parser = HeadersParser()
    assert parser(headers) is False
