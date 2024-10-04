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
    from k2hr3client import version
    v = version.K2hr3Version()
    from k2hr3client import http as khttp
    httpreq = khttp.K2hr3Http('http://127.0.0.1:18080')

    # GET the K2hr Version API.
    httpreq.GET(v)
    print(v.resp)
"""

import abc
from enum import Enum
import logging
from http.client import HTTPMessage
from typing import Optional

from k2hr3client.exception import K2hr3Exception

LOG = logging.getLogger(__name__)


# NOTE(hiwakaba): we do not use 3.11's http.HTTPMethod module
# Because we need to support 3.10.
class K2hr3HTTPMethod(Enum):  # type: ignore[no-redef]
    # pylint: disable=too-few-public-methods
    """HTTPMethod."""

    CONNECT = 1
    DELETE = 2
    GET = 3
    HEAD = 4
    OPTIONS = 5
    PATCH = 6
    POST = 7
    PUT = 8
    TRACE = 9


class K2hr3ApiResponse():  # pylint: disable=too-many-instance-attributes
    """K2hr3ApiResponse stores the response of K2HR3 WebAPI.

    The members are set by setter methods only one time.
    """

    __slots__ = ('_code', '_url', '_hdrs', '_body')

    def __init__(self, code=None, url=None, hdrs=None, body=None) -> None:
        """Init the members."""
        self.code = code
        self.url = url
        self.hdrs = hdrs
        self.body = body

    def __repr__(self) -> str:
        """Represent the members."""
        attrs = []
        values = ""
        for attr in ['_hdrs', '_body', '_url', '_code']:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs]) # pylint: disable=consider-using-f-string # noqa
        return '<K2hr3ApiResponse ' + values + '>'

    @property
    def body(self) -> Optional[str]:
        """Return the body."""
        return self._body

    @body.setter
    def body(self, val: Optional[str]) -> None:
        """Set the body that may be empty."""
        if val and isinstance(val, str) is False:
            raise K2hr3Exception(f'value type must be str, not {type(val)}')
        if getattr(self, '_body', None) is None:
            self._body = val

    @property
    def hdrs(self) -> HTTPMessage:
        """Return the header."""
        return self._hdrs

    @hdrs.setter
    def hdrs(self, val: HTTPMessage) -> None:
        """Set the headers that must not be empty."""
        if isinstance(val, HTTPMessage) is False:
            raise K2hr3Exception(
                f'value type must be http.client.HTTPMessage, not {type(val)}')
        if not val:
            raise K2hr3Exception("val should not be empty")
        if getattr(self, '_hdrs', None) is None:
            self._hdrs = val

    @property
    def code(self) -> int:
        """Return the status code."""
        return self._code

    @code.setter
    def code(self, val: int) -> None:
        """Set the http status code that must not be empty."""
        if isinstance(val, int) is False:
            raise K2hr3Exception(f'val should be int, not {type(val)}')
        if not val:
            raise K2hr3Exception("val should not be empty")
        if getattr(self, '_code', None) is None:
            self._code = val

    @property
    def url(self) -> str:
        """Return the request url."""
        return self._url

    @url.setter
    def url(self, val: str) -> None:
        """Set the url code that must not be empty."""
        if isinstance(val, str) is False:
            raise K2hr3Exception("val should be str, not {type(val)")
        if not val:
            raise K2hr3Exception("val should not be empty")
        if getattr(self, '_url', None) is None:
            self._url = val


class K2hr3Api(abc.ABC):  # pylint: disable=too-many-instance-attributes
    """Base class of all K2HR3 WebAPIs."""

    DEFAULT_VERSION = "v1"

    def __init__(self, basepath: str, params: Optional[str] = None,  # pylint: disable=R0917 # noqa
                 hdrs: Optional[dict] = None, body: Optional[str] = None,
                 version: str = DEFAULT_VERSION) -> None:  # pylint: disable=W0613 # noqa
        """Init the K2hr3 API members.

        :raise K2hr3Exception: if the val is invalid.
        """
        super().__init__()
        self.basepath = basepath
        self.urlparams = params
        self.headers = hdrs
        self.body = body
        self.version = version

        # following attrs are dynamically set later.
        self.resp = None  # type: ignore
        self.api_id = 0

    def __repr__(self) -> str:
        """Represent the members."""
        attrs = []
        values = ""
        for attr in ['_basepath', '_params', '_hdrs', '_body', '_resp',
                     'api_id']:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs])
        return '<K2hr3Api ' + values + '>'

    @property
    def basepath(self) -> str:
        """Return the base url path."""
        return self._basepath

    @basepath.setter
    def basepath(self, val: str) -> None:
        """Set the base url path.

        :raise K2hr3Exception: if the val is invalid.
        """
        if isinstance(val, str) is False:
            raise K2hr3Exception("basepath should be str")
        if getattr(self, '_basepath', None) is None:
            self._basepath = val
        else:
            LOG.info("basepath has changed")
            self._basepath = val

    #
    # getters and setters
    #
    @property
    def urlparams(self) -> Optional[str]:
        """Return the url params."""
        return self._params

    @urlparams.setter
    def urlparams(self, val: Optional[str]) -> None:  # pylint: disable=arguments-differ, invalid-overridden-method # noqa
        """Set the params."""
        if getattr(self, '_params', None) is None:
            self._params = val

    @property
    def headers(self) -> Optional[dict]:
        """Return the request headers."""
        return self._hdrs

    @headers.setter
    def headers(self, val: Optional[dict]) -> None:  # pylint: disable=arguments-differ, invalid-overridden-method # noqa
        """Set the headers."""
        if getattr(self, '_hdrs', None) is None:
            self._hdrs = val

    @property
    def body(self) -> Optional[str]:
        """Return the request body."""
        return self._body

    @body.setter
    def body(self, val: Optional[str]) -> None:  # pylint: disable=arguments-differ, invalid-overridden-method # noqa
        """Set the body."""
        if getattr(self, '_body', None) is None:
            self._body = val

    @property
    def resp(self) -> K2hr3ApiResponse:
        """Return the response struct."""
        return self._resp

    @resp.setter
    def resp(self, val: K2hr3ApiResponse) -> None:
        """Set the response as is."""
        if getattr(self, '_resp', None) is None:
            self._resp = val

    @property
    def version(self) -> str:
        """Return the version string."""
        return self._version

    @version.setter
    def version(self, val: str) -> None:
        """Set the version as is."""
        self._version = val

    #
    # abstract methods that must be implemented in subclasses
    #
    @abc.abstractmethod
    def _api_path(self, method: K2hr3HTTPMethod) -> Optional[str]:
        """Sub classes should implement this method."""

    #
    # methods that are invoked from other classes
    #
    def set_response(self, code: int, url: str, headers: HTTPMessage,
                     body: Optional[str]) -> None:
        """Set the API responses in K2hr3Http class."""
        self._resp = K2hr3ApiResponse(code, url, headers, body)

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
