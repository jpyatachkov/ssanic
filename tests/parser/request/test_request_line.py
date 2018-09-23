import pytest

from ssanic.parser.request import RequestLineParser


@pytest.mark.parametrize('request_line,expected', [
    # ('GET * HTTP/1.1', ('GET', '*')),
    ('GET file.html HTTP/1.1', ('GET', 'file.html')),
    ('GET /file.html HTTP/1.1', ('GET', '/file.html')),
    ('GET file.html/ HTTP/1.1', ('GET', 'file.html/')),
    ('GET / HTTP/1.1', ('GET', '/')),
    ('MY / HTTP/1.1', ('MY', '/')),
    ('GET /home/my/ HTTP/1.1', ('GET', '/home/my/')),
    ('GET /home/my HTTP/1.1', ('GET', '/home/my')),
    ('GET /home/../../../../../../file.html HTTP/1.1', ('GET', '/home/../../../../../../file.html')),
    ('GET /home/my/file.html HTTP/1.1', ('GET', '/home/my/file.html')),
    ('GET request://example.com HTTP/1.1', ('GET', '/')),
    ('GET request://example.com#anchor HTTP/1.1', ('GET', '/')),
    ('GET request://example.com?key=value HTTP/1.1', ('GET', '/')),
    ('GET request://example.com?key=value&key=value&key=value,value,value HTTP/1.1', ('GET', '/')),
    ('GET request://example.com?key=value#anchor HTTP/1.1', ('GET', '/')),
    ('GET request://example.com/page HTTP/1.1', ('GET', '/page')),
    ('GET request://example.com/page?key=value HTTP/1.1', ('GET', '/page')),
    ('GET request://example.com/page#anchor HTTP/1.1', ('GET', '/page')),
    ('GET request://example.com/page.html HTTP/1.1', ('GET', '/page.html')),
    ('GET request://example.com/page.html?key=value HTTP/1.1', ('GET', '/page.html')),
    ('GET request://example.com/page.html#anchor HTTP/1.1', ('GET', '/page.html')),
    ('GET %70%61%67%65%2e%68%74%6d%6c HTTP/1.1', ('GET', '%70%61%67%65%2e%68%74%6d%6c')),
    ('GET /%70%61%67%65%2e%68%74%6d%6c HTTP/1.1', ('GET', '/%70%61%67%65%2e%68%74%6d%6c')),
    ('GET file...txt HTTP/1.1', ('GET', 'file...txt')),
])
def test_correct_request_line(request_line, expected):
    method, path = expected

    parser = RequestLineParser()

    assert parser(request_line) is True
    assert method == parser.method
    assert path == parser.path


@pytest.mark.parametrize('request_line', [
    b'skm',
    [],
    '',
    'GET/HTTP/1.1',
    'GET file:///myfile.txt HTTP/1.1',
    'get / HTTP/1.1',
    'GET / HTTP/1.0',
    'GET / request/1.1',
    'GET / HTTP/1.1;sflg',
    'GET / HTTP/1.0\\r',
    'GET / HTTP/1.0',
    'GET / HTTP/1.1\\r',
])
def test_incorrect_request_line(request_line):
    parser = RequestLineParser()
    assert parser(request_line) is False
