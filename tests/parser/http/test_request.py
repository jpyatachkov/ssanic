import pytest

from ssanic.parser.http import RequestParser


class TestRequestParser:

    @pytest.mark.parametrize('raw_request', [
        r'GET /home/file1.txt/\r\n\r\n',
        r'GET index.html HTTP/1.1\r\nContent-Type=application/json\r\n\r\n',
        r'PUT / HTTP/1.1\r\nContent-Type=application/json\r\n\r\nname=value1',
    ])
    def test_calls_parse_head_if_request_has_2_delimiters(self, raw_request, mocker):
        parser = RequestParser()

        mocked_parse_head = mocker.patch.object(parser,
                                                '_parse_head',
                                                return_value=True)

        assert parser(raw_request) is True
        mocked_parse_head.assert_called_once_with(raw_request.split(RequestParser.DELIMITER * 2)[0])

    @pytest.mark.parametrize('raw_request', [
        '',
        b'df',
        [],
        r'HEAD / HTTP/1.1\r\n',
        r'GET index.html HTTP/1.1\r\nContent-Type=application/json\r\n',
        r'GET index.html HTTP/1.1\r\nContent-Type=application/json\r\n\r',
    ])
    def test_returns_false_if_request_has_not_2_delimiters(self, raw_request, mocker):
        parser = RequestParser()

        mocked_parse_head = mocker.patch.object(parser,
                                                '_parse_head',
                                                return_value=True)

        assert parser(raw_request) is False
        mocked_parse_head.assert_not_called()

    @pytest.mark.parametrize('raw_request, request_line_correct,headers_correct', [
        (r'GET index.html HTTP/1.1\r\nContent-Type=application/json\r\n\r\n', True, True),
        (r'GET index.html HTTP/1.1\r\nContent-Type=application/json\r\n\r\n', True, False),
        (r'GET index.html HTTP/1.1\r\nContent-Type=application/json\r\n\r\n', False, True),
        (r'GET index.html HTTP/1.1\r\nContent-Type=application/json\r\n\r\n', False, False),
    ])
    def test_ands_request_line_and_header_parsing_results(self, raw_request,
                                                          request_line_correct, headers_correct, mocker):
        parser = RequestParser()

        mocked_request_line = mocker.patch('ssanic.parser.http.request_line.RequestLineParser.__call__',
                                           return_value=request_line_correct)
        mocked_headers = mocker.patch('ssanic.parser.http.headers.HeadersParser.__call__',
                                      return_value=headers_correct)

        assert parser(raw_request) == (request_line_correct and headers_correct)

        mocked_request_line.assert_called_once()

        if request_line_correct:
            mocked_headers.assert_called_once()
