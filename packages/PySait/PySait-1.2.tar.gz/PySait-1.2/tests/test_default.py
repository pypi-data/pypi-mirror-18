# -*- coding: utf-8 -*-
from io import BytesIO
import pysait as s


def test_request():
    test_1 = s.SaitRequest('GET', '/')
    assert test_1.method == 'get'
    assert test_1.path == '/'
    assert test_1.params == dict()

    test_2 = s.SaitRequest('GET', '/',
                           query={'a': '12'},
                           form={'b': '13'},
                           json_data={'c': '14'})
    assert test_2.method == 'get'
    assert test_2.path == '/'
    assert test_2.params == {'a': '12', 'b': '13', 'c': '14'}


def _unwind_response(response: s.SaitResponse):
    result = list()

    def start_response(status_code, headers):
        result.append(status_code)
        result.append(headers)

    result.append(list(response.to_wsgi(start_response)))

    return result


def test_response():
    test_1 = s.SaitResponse()
    test_1.status_code = 200
    test_1.body = 'Test 1'
    test_1.add_header('Content-Type', 'text/plain')

    assert test_1.status_code == '200 OK'
    assert test_1.body == b'Test 1'
    assert test_1.headers == [
        ('Content-Type', 'text/plain'),
    ]

    assert _unwind_response(test_1) == [
        '200 OK', [('Content-Type', 'text/plain')],
        [b'Test 1']
    ]

    test_2 = s.SaitResponse()
    test_2.status_code = 403
    test_2.body = b'Test 2'
    test_2.add_header('Content-Type', 'text/plain')

    assert test_2.status_code == '403 Forbidden'
    assert test_2.body == b'Test 2'
    assert test_2.headers == [
        ('Content-Type', 'text/plain'),
    ]

    assert _unwind_response(test_2) == [
        '403 Forbidden', [('Content-Type', 'text/plain')],
        [b'Test 2']
    ]


def test_request_build():
    input = BytesIO(b'{"some": ["stuff"]}')

    environ = {
        'wsgi.input': input,
        'wsgi.url_scheme': 'http',
        'wsgi.input_terminated': True,
        'SERVER_NAME': '127.0.0.1',
        'SERVER_PORT': '8080',
        'PATH_INFO': '/build',
        'HTTP_HOST': 'localhost:8080',
        'REMOTE_ADDR': '127.0.0.1',
        'QUERY_STRING': 'test=3',
        'CONTENT_TYPE': 'application/json',
        'RAW_URI': '/build?test=3',
        'REQUEST_METHOD': 'POST',
    }

    test_1 = s.SaitRequest.build(environ)
    assert test_1.params == {'test': '3', 'some': ['stuff']}

    input = BytesIO(b'Broken JSON')

    environ = {
        'wsgi.input': input,
        'wsgi.url_scheme': 'http',
        'wsgi.input_terminated': True,
        'SERVER_NAME': '127.0.0.1',
        'SERVER_PORT': '8080',
        'PATH_INFO': '/build',
        'HTTP_HOST': 'localhost:8080',
        'REMOTE_ADDR': '127.0.0.1',
        'QUERY_STRING': 'test=3',
        'CONTENT_TYPE': 'application/json',
        'RAW_URI': '/build?test=3',
        'REQUEST_METHOD': 'POST',
    }

    test_2 = s.SaitRequest.build(environ)
    assert test_2.params == {
        'test': '3',
        'JSON_DECODE_ERROR': 'Failed to load JSON: Expecting value: line 1 '
                             'column 1 (char 0)'
    }
