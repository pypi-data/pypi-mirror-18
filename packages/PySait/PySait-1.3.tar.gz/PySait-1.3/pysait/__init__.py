# -*- coding: utf-8 -*-

import json
from typing import Dict, Any, TypeVar, List

from werkzeug import wsgi as ww
from werkzeug.datastructures import Headers, FileStorage, \
    Authorization
from werkzeug.formparser import parse_form_data
from werkzeug.http import HTTP_STATUS_CODES, parse_authorization_header, \
    dump_cookie, parse_cookie
from werkzeug.urls import iri_to_uri, url_parse
from werkzeug.utils import secure_filename

AnyStr = TypeVar('AnyStr', str, bytes)
FileOrFiles = TypeVar('AnyFile', 'SaitFileStorage', List['SaitFileStorage'])


class SaitRequest(object):
    def __init__(self, method: str, path: str,
                 query: Dict[str, Any] = None,
                 form: Dict[str, Any] = None,
                 files: Dict[str, FileOrFiles] = None,
                 json_data: Dict[str, Any] = None,
                 cookies: Dict[str, str] = None,

                 host: str = 'localhost', scheme: str = 'http',

                 accept_type: str = 'text/json',
                 accept_language: str = '',
                 content_type: str = 'x-www-form-urlencoded',

                 remote_addr: str = None,
                 auth: Authorization = None):
        self.method = method.lower()
        self.path = path
        self.query = query or dict()
        self.form = form or dict()
        self.files = files or dict()
        self.json_data = json_data
        self.cookies = cookies or dict()
        self.host = host
        self.scheme = scheme
        self.accept_type = accept_type
        self.accept_language = accept_language
        self.content_type = content_type
        self.remote_addr = remote_addr
        self.auth = auth

        self.params = dict()  # type: Dict[str, Any]
        self.params.update(self.query)
        self.params.update(self.form)
        self.params.update(self.files)
        if self.json_data:
            self.params.update(self.json_data)

    @classmethod
    def build(cls, environ: Dict[str, Any]) -> 'SaitRequest':
        uri = iri_to_uri(ww.get_current_url(environ))
        stream, form, files = parse_form_data(environ)

        url = url_parse(uri)
        """:type: werkzeug.urls.URL"""

        host = url.host
        scheme = url.scheme

        auth = parse_authorization_header(
            environ.get('HTTP_AUTHORIZATION'))

        method = environ.get('REQUEST_METHOD', 'get').lower()
        path = url.path

        query = flatten_multidict(url.decode_query())
        form = flatten_multidict(form)
        files = flatten_multidict(files,
                                  lambda v: len(v.filename),
                                  SaitFileStorage.rebuild)

        cookies = parse_cookie(environ)

        params = dict()
        params.update(query)
        params.update(form)
        params.update(files)

        remote_addr = environ.get('REMOTE_ADDR')

        accept_type = environ.get('HTTP_ACCEPT', '')
        accept_language = environ.get('HTTP_ACCEPT_LANGUAGE', '')

        content_type = environ.get('CONTENT_TYPE', '')

        json_data = None
        if 'application/json' in content_type:
            try:
                json_data = json.loads(stream.read().decode('utf-8'))
                assert isinstance(json_data, dict)
            except json.decoder.JSONDecodeError as exc:
                json_data = {
                    'JSON_DECODE_ERROR': 'Failed to load JSON: %s' % str(exc)
                }

        return cls(method, path,
                   query=query, form=form, files=files,
                   json_data=json_data,
                   cookies=cookies,
                   host=host, scheme=scheme,
                   accept_type=accept_type,
                   accept_language=accept_language,
                   content_type=content_type,
                   remote_addr=remote_addr, auth=auth)

    def get_cookie(self, name, default=None):
        """Retrieve cookie from the request.

        This matches with the api of `poort.Response`, this provides
        `response.set_cookie` and `response.del_cookie`.

        :param name: Name of the cookie.
        :param default: Default when the cookie is not set.

        :type name: str
        :type default: str | None

        :rtype: str | None
        """
        return self.cookies.get(name, default)


class SaitResponse(object):
    def __init__(self):
        self._status_code = 200
        self._headers = Headers()
        self._body = b''

    @property
    def status_code(self):
        sc = self._status_code
        return '%d %s' % (sc, HTTP_STATUS_CODES[sc])

    @status_code.setter
    def status_code(self, value: int):
        self._status_code = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value: AnyStr):
        if isinstance(value, str):
            self._body = value.encode('utf-8')
        else:
            self._body = value

    @property
    def headers(self):
        return self._headers.to_wsgi_list()

    def add_header(self, name, value, **kw):
        self._headers.add(name, value, **kw)

    def set_cookie(self, name: str, value: str = '', max_age: int = None,
                   path: str = '/', domain: str = None, secure: bool = False,
                   httponly: bool = True):
        cookie = dump_cookie(
            name, value=str(value), max_age=max_age,
            path=path, domain=domain,
            secure=secure, httponly=httponly,
            charset='utf-8', sync_expires=True)

        self.add_header('Set-Cookie', cookie)

    def del_cookie(self, name: str, path: str = '/', domain: str = None,
                   secure: bool = False, httponly: bool = True):
        self.set_cookie(name, max_age=0, path=path, domain=domain,
                        secure=secure, httponly=httponly)

    def to_wsgi(self, start_response):
        start_response(self.status_code, self.headers)
        return iter([self.body])


def flatten_multidict(data, validate=None, wrap=None):
    r"""Flatten a `werkzeug` MultiDict into a simple dict.

    **Parameters**

    :param data: MultiDict to flatten.
    :param validate: Only append values that match this validator.
    :type data: werkzeug.datastructures.MultiDict
    :type validate: mixed for filter
    :rtype: dict

    """
    result = {}
    for key, values in data.lists():
        if validate is not None:
            values = filter(validate, values)
        if wrap is not None:
            values = list(map(wrap, values))
        result[key] = values[0] if len(values) == 1 else values
    return result


class SaitFileStorage(FileStorage):
    @classmethod
    def rebuild(cls, original):
        return cls(stream=original.stream, filename=original.filename,
                   name=original.name, content_type=original.content_type,
                   content_length=original.content_length,
                   headers=original.headers)

    @property
    def secure_filename(self):
        return secure_filename(self.filename)
