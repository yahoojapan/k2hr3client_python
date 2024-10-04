# -*- coding: utf-8 -*-
#
# k2hr3client - Python client for K2HR3 REST API
#
# Copyright 2020 Yahoo Japan Corporation
# Copyright 2024 LY Corporation
#
# K2HR3 is K2hdkc based Resource and Roles and policy Rules, gathers
# common management information for the cloud.
# K2HR3 can dynamically manage information as "who", "what", "operate".
# These are stored as roles, resources, policies in K2hdkc, and the
# client system can dynamically read and modify these information.
#
# For the full copyright and license information, please view
# the license file that was distributed with this source code.
#
# AUTHOR:   Hirotaka Wakabayashi
# CREATE:   Mon Sep 14 2020
# REVISION:
#
#
"""
k2hr3client - Python library for K2HR3 API.

.. code-block:: python

    # Import modules from k2hr3client package
    from k2hr3client import http as khttp
    httpreq = khttp.K2hr3Http('http://127.0.0.1:18080')

    from k2hr3client import extdata
    example = extdata.K2hr3Extdata("uripath","registerpath","ua 1.0.0")

    # GET the K2hr Extdata API.
    httpreq.GET(example.acquires_template())
    print(example.resp)
"""

from enum import Enum
import json
import logging
import re
import socket
import ssl
import time
from typing import Optional
import urllib
import urllib.parse
import urllib.request
from urllib.error import ContentTooShortError, HTTPError, URLError

from k2hr3client.api import K2hr3HTTPMethod, K2hr3Api
from k2hr3client.exception import K2hr3Exception

LOG = logging.getLogger(__name__)


class _AgentError(Enum):
    NONE = 1
    TEMP = 2
    FATAL = 3


class K2hr3Http():  # pylint: disable=too-many-instance-attributes
    """K2hr3Http sends a http/https request to the K2hr3 WebAPI.

    Most of the members are set by setter methods only one time.
    """

    __slots__ = ('_baseurl', '_hdrs', '_timeout_seconds',
                 '_url', '_urlparams',
                 '_retry_interval_seconds', '_retries',
                 '_allow_self_signed_cert')

    def __init__(self, baseurl: str) -> None:
        """Init the members."""
        self._set_baseurl(baseurl)
        self._timeout_seconds = 30
        self._url = None  # type: Optional[str]
        self._urlparams = None  # type: Optional[str]
        self._retry_interval_seconds = 60  # type: int
        self._retries = 3  # type: int
        self._allow_self_signed_cert = True  # type: bool

    def __repr__(self) -> str:
        """Represent the members."""
        attrs = []
        values = ""
        for attr in ['_baseurl', '_hdrs', '_timeout_seconds',
                     '_retry_interval_seconds', '_retries',
                     '_allow_self_signed_cert']:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs]) # pylint: disable=consider-using-f-string # noqa
        return '<K2hr3Http ' + values + '>'

    @property
    def baseurl(self) -> Optional[str]:
        """Returns the url."""
        return self._baseurl

    def _set_baseurl(self, value: Optional[str]) -> None:
        """Set the baseurl.

        :raise K2hr3Exception: if the val is invalid.
        """
        if isinstance(value, str) is False:
            raise K2hr3Exception("value should be str, not {type(value)}")
        # scheme
        try:
            scheme, url_string = value.split('://', maxsplit=2)  # type: ignore
        except ValueError as verr:
            raise K2hr3Exception(
                f'scheme should contain ://, not {value}') from verr
        if scheme not in ('http', 'https'):
            raise K2hr3Exception(
                f'scheme should be http or http, not {scheme}')
        matches = re.match(
            r'(?P<domain>[\w|\.]+)?(?P<port>:\d{2,5})?(?P<path>[\w|/]*)?',
            url_string)
        if matches is None:
            raise K2hr3Exception(
                f'the argument seems not to be a url string, {value}')

        # domain must be resolved.
        domain = matches.group('domain')
        if domain is None:
            raise K2hr3Exception(
                f'url contains no domain, {value}')
        try:
            # https://github.com/python/cpython/blob/master/Modules/socketmodule.c#L5729
            ipaddress = socket.gethostbyname(domain)
        except OSError as error:  # resolve failed
            raise K2hr3Exception(
                f'unresolved domain, {domain} {error}') from error
        LOG.debug('%s resolved %s', domain, ipaddress)

        # path(optional)
        if matches.group('path') is None:
            raise K2hr3Exception(
                f'url contains no path, {value}')
        path = matches.group('path')
        # port(optional)
        port = matches.group('port')
        LOG.debug('url=%s domain=%s port=%s path=%s', value, domain, port,
                  path)
        if getattr(self, '_baseurl', None) is None:
            self._baseurl = value

    @property
    def headers(self) -> dict:
        """Return the request headers."""
        return self._hdrs  # type: ignore

    @headers.deleter
    def headers(self) -> None:
        """Delete the request headers."""
        self._hdrs = None

    @headers.setter
    def headers(self, val: dict) -> None:  # pylint: disable=arguments-differ, invalid-overridden-method # noqa
        """Set the headers."""
        if getattr(self, '_hdrs', None) is None:
            self._hdrs = val  # type: ignore

    @property
    def url(self) -> Optional[str]:
        """Returns the url."""
        return self._url  # type: ignore

    @url.deleter
    def url(self) -> None:
        """Delete the request url."""
        self._url = None

    @url.setter
    def url(self, val: Optional[str]) -> None:  # type: ignore # noqa: F811
        """Set the url."""
        if isinstance(val, str) is False:
            raise K2hr3Exception("basepath should be str")
        if getattr(self, '_url', None) is None:
            self._url = val
        else:
            LOG.info("url has changed")
            self._url = val

    @property
    def urlparams(self) -> Optional[str]:
        """Returns the urlparams."""
        return self._urlparams

    @urlparams.deleter
    def urlparams(self) -> None:
        """Delete the urlparams headers."""
        self._urlparams = None

    @urlparams.setter
    def urlparams(self, val: Optional[str]) -> None:  # type: ignore # noqa
        """Set the urlparams."""
        if getattr(self, '_urlparams', None) is None:
            self._urlparams = val

    def _init_request(self) -> None:
        """Init the headers and params."""
        del self.headers
        self.headers = {'User-Agent': 'K2hr3Http'}
        del self.url
        del self.urlparams

    def _HTTP_REQUEST_METHOD(self, r3api: K2hr3Api, req: urllib.request.Request) -> bool:   # pylint: disable=invalid-name # noqa
        agent_error = _AgentError.NONE
        try:
            ctx = None
            if req.type == 'https':
                # https://docs.python.jp/3/library/ssl.html#ssl.create_default_context
                ctx = ssl.create_default_context()
                if self._allow_self_signed_cert:
                    # https://github.com/python/cpython/blob/master/Lib/ssl.py#L567
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=self._timeout_seconds,
                                        context=ctx) as res:
                r3api.set_response(code=res.getcode(),
                                   url=res.geturl(),
                                   headers=res.info(),
                                   body=res.read().decode('utf-8'))
                return True
        except HTTPError as error:
            LOG.error(
                'Could not complete the request. code %s reason %s headers %s',
                error.code, error.reason, error.headers)
            agent_error = _AgentError.FATAL
        except (ContentTooShortError, URLError) as error:
            # https://github.com/python/cpython/blob/master/Lib/urllib/error.py#L73
            LOG.error('Could not read the server. reason %s', error.reason)
            agent_error = _AgentError.FATAL
        except (socket.timeout, OSError) as error:  # temporary error
            LOG.error('error(OSError, socket) %s', error)
            agent_error = _AgentError.TEMP
        finally:
            if agent_error == _AgentError.TEMP:
                self._retries -= 1  # decrement the retries value.
                if self._retries >= 0:
                    LOG.warning('sleeping for %s. remaining retries=%s',
                                self._retry_interval_seconds,
                                self._retries)
                    time.sleep(self._retry_interval_seconds)
                    self.GET(r3api)
                else:
                    LOG.error("reached the max retry count.")
                    agent_error = _AgentError.FATAL

        if agent_error == _AgentError.NONE:
            LOG.debug('no problem.')
            return True
        LOG.debug('problem. See the error log.')
        return False

    def POST(self, r3api: K2hr3Api) -> bool:  # pylint: disable=invalid-name # noqa
        """Send requests by using POST Method."""
        self._init_request()
        # 1. Constructs request url using K2hr3Api.path property.
        r3api_path = r3api._api_path(K2hr3HTTPMethod.POST)  # type: ignore # pylint: disable=protected-access # noqa
        self.url = f"{self._baseurl}/{r3api_path}"

        # 2. Constructs url parameters using K2hr3Api.urlparams property.
        if r3api.headers:
            content_type = r3api.headers.get('Content-Type')
        if content_type == "application/json":
            query = r3api.body
            if query:
                query = query.encode('ascii')  # type: ignore
        else:
            query = urllib.parse.urlencode(r3api.urlparams)  # type: ignore
            if query:
                query = query.encode('ascii')  # type: ignore
        self.urlparams = query

        # 3. Constructs headers using K2hr3Api.headers property.
        if self._hdrs:
            self._hdrs.update(r3api.headers)

        # 4. Sends a request.
        req = urllib.request.Request(self.url, data=query,  # type: ignore
                                     headers=self._hdrs,    # type: ignore  # noqa
                                     method="POST")
        if req.type not in ('http', 'https'):
            LOG.error('http or https, not %s', req.type)
            return False
        return self._HTTP_REQUEST_METHOD(r3api, req)

    def PUT(self, r3api: K2hr3Api) -> bool:  # pylint: disable=invalid-name # noqa
        """Send requests by using PUT Method."""
        self._init_request()
        # 1. Constructs request url using K2hr3Api.path property.
        r3api_path = r3api._api_path(K2hr3HTTPMethod.PUT)  # type: ignore # pylint: disable=protected-access # noqa
        self.url = f"{self._baseurl}/{r3api_path}"

        # 2. Constructs url parameters using K2hr3Api.urlparams property.
        query = urllib.parse.urlencode(json.loads(r3api.urlparams))  # type: ignore  # noqa
        self.urlparams = query

        # 3. Constructs headers using K2hr3Api.headers property.
        if self._hdrs:
            self._hdrs.update(r3api.headers)

        # 5. Sends a request.
        req = urllib.request.Request("?".join([self.url, self.urlparams]),
                                     data=None, headers=self._hdrs,  # type: ignore  # noqa
                                     method="PUT")
        if req.type not in ('http', 'https'):
            LOG.error('http or https, not %s', req.type)
            return False
        return self._HTTP_REQUEST_METHOD(r3api, req)

    def GET(self, r3api: K2hr3Api) -> bool:   # pylint: disable=invalid-name # noqa
        """Send requests by using GET Method."""
        self._init_request()
        # 1. Constructs request url using K2hr3Api.path property.
        r3api_path = r3api._api_path(K2hr3HTTPMethod.GET)  # type: ignore # pylint: disable=protected-access # noqa
        self.url = f"{self._baseurl}/{r3api_path}"

        # 2. Constructs url parameters using K2hr3Api.params property.
        if r3api.urlparams:
            if isinstance(r3api.urlparams, dict):
                query = urllib.parse.urlencode(r3api.urlparams)
            else:
                query = urllib.parse.urlencode(json.loads(r3api.urlparams))
            self.urlparams = query
        url = self.url
        if self.urlparams:
            url = "?".join([self.url, self.urlparams])

        # 3. Constructs headers using K2hr3Api.headers property.
        if self._hdrs:
            self._hdrs.update(r3api.headers)

        # 4. Sends a request.
        req = urllib.request.Request(url, headers=self._hdrs, method="GET")  # type: ignore  # noqa
        if req.type not in ('http', 'https'):
            LOG.error('http or https, not %s', req.type)
            return False
        return self._HTTP_REQUEST_METHOD(r3api, req)

    def HEAD(self, r3api: K2hr3Api) -> bool:   # pylint: disable=invalid-name # noqa
        """Send requests by using GET Method."""
        self._init_request()
        # 1. Constructs request url using K2hr3Api.path property.
        r3api_path = r3api._api_path(K2hr3HTTPMethod.HEAD)  # type: ignore # pylint: disable=protected-access # noqa
        self.url = f"{self._baseurl}/{r3api_path}"

        # 2. Constructs url parameters using K2hr3Api.params property.
        if r3api.urlparams:
            if isinstance(r3api.urlparams, dict):
                query = urllib.parse.urlencode(r3api.urlparams)
            else:
                query = urllib.parse.urlencode(json.loads(r3api.urlparams))
            self.urlparams = query
        url = self.url
        if self.urlparams:
            url = "?".join([self.url, self.urlparams])

        # 3. Constructs headers using K2hr3Api.headers property.
        if self._hdrs:
            self._hdrs.update(r3api.headers)  # type: ignore

        # 4. Sends a request.
        # NOTE: headers is expected "MutableMapping[str, str]"
        req = urllib.request.Request(url, headers=self._hdrs, method="HEAD")  # type: ignore # noqa
        if req.type not in ('http', 'https'):
            LOG.error('http or https, not %s', req.type)
            return False
        return self._HTTP_REQUEST_METHOD(r3api, req)

    def DELETE(self, r3api: K2hr3Api) -> bool:   # pylint: disable=invalid-name # noqa
        """Send requests by using DELETE Method."""
        self._init_request()
        # 1. Constructs request url using K2hr3Api.path property.
        r3api_path = r3api._api_path(K2hr3HTTPMethod.DELETE)  # type: ignore # pylint: disable=protected-access # noqa
        self.url = f"{self._baseurl}/{r3api_path}"

        # 2. Constructs url parameters using K2hr3Api.params property.
        if r3api.urlparams:
            if isinstance(r3api.urlparams, dict):
                query = urllib.parse.urlencode(r3api.urlparams)
            else:
                query = urllib.parse.urlencode(json.loads(r3api.urlparams))
            self.urlparams = query
        url = self.url
        if self.urlparams:
            url = "?".join([self.url, self.urlparams])

        # 3. Constructs headers using K2hr3Api.headers property.
        if self._hdrs:
            self._hdrs.update(r3api.headers)  # type: ignore

        # 4. Sends a request.
        # NOTE: headers is expected "MutableMapping[str, str]"
        req = urllib.request.Request(url, headers=self._hdrs, method="HEAD")  # type: ignore # noqa
        if req.type not in ('http', 'https'):
            LOG.error('http or https, not %s', req.type)
            return False
        return self._HTTP_REQUEST_METHOD(r3api, req)

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
