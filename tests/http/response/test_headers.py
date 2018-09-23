from ssanic.http.response import Headers


def test_one_header():
    expected_str = 'Content-Type: application/json\r\n'
    expected_repr = 'HEADERS: {}'.format(expected_str)

    h = Headers()
    h['Content-Type'] = 'application/json'

    assert expected_str == str(h)
    assert expected_repr == repr(h)


def test_several_headers():
    initial_headers = (('Content-Type', 'application/json'), ('Server', 'Ssanic'))
    expected_str = 'Content-Type: application/json\r\nServer: Ssanic\r\n'
    expected_repr = 'HEADERS: {}'.format(expected_str)

    h = Headers(initial_headers)

    for k, v in initial_headers:
        assert h[k] == v

    assert expected_str == str(h)
    assert expected_repr == repr(h)
