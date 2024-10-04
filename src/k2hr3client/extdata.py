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
k2hr3client - Python library for k2hr3 Extdata API.

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

import logging
from typing import Optional

from k2hr3client.api import K2hr3Api, K2hr3HTTPMethod
from k2hr3client.exception import K2hr3Exception

LOG = logging.getLogger(__name__)


# curl -v \
#  http://127.0.0.1:18080/v1/extdata/test -H 'User-Agent: cloud-init 0.7.9'
#
#
class K2hr3Extdata(K2hr3Api):  # pylint: disable=too-many-instance-attributes
    """Relationship with K2HR3 EXTDATA API.

    See https://k2hr3.antpick.ax/api_extdata.html for details.
    """

    __slots__ = ('_extapi_name', '_register_path', '_user_agent',)

    def __init__(self, extapi_name: str, register_path: str,
                 user_agent: str) -> None:
        """Init the members."""
        super().__init__("extdata")
        self.extapi_name = extapi_name
        self.register_path = register_path
        self.user_agent = user_agent

        # following attrs are dynamically set later.
        self.headers = {

            'Content-Type': 'application/octet-stream',
            'User-Agent': f"{user_agent}",
            'Accept-Encoding': 'gzip',
        }
        self.body = None  # type: ignore
        self.urlparams = None  # type: ignore

    # ---- GET ----
    # GET（Extdata）    http(s)://API SERVER:PORT/v1/extdata/uripath/registerpath
    def acquires_template(self) -> None:
        """Set a request to acquire a template."""
        self.api_id = 1

    def __repr__(self) -> str:
        """Represent the members."""
        attrs = []
        values = ""
        for attr in ['_extapi_name', '_register_path', '_user_agent']:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs])
        return '<K2hr3Extdata ' + values + '>'

    @property  # type: ignore
    def extapi_name(self) -> str:
        """Return the tenant."""
        return self._extapi_name

    @extapi_name.setter
    def extapi_name(self, val: str) -> None:  # type: ignore # noqa: F811
        """Set the extapi_name."""
        if isinstance(val, str) is False:
            raise K2hr3Exception(f'value type must be str, not {type(val)}')
        if getattr(self, '_extapi_name', None) is None:
            self._extapi_name = val

    @property  # type: ignore
    def register_path(self) -> str:
        """Return the tenant."""
        return self._register_path

    @register_path.setter
    def register_path(self, val: str) -> None:  # type: ignore # noqa: F811
        """Set the extapi_name."""
        if isinstance(val, str) is False:
            raise K2hr3Exception(f'value type must be str, not {type(val)}')
        if getattr(self, '_register_path', None) is None:
            self._register_path = val

    @property  # type: ignore
    def user_agent(self) -> str:
        """Return the tenant."""
        return self._user_agent

    @user_agent.setter
    def user_agent(self, val: str) -> None:  # type: ignore # noqa: F811
        """Set the extapi_name."""
        if isinstance(val, str) is False:
            raise K2hr3Exception(f'value type must be str, not {type(val)}')
        if getattr(self, '_user_agent', None) is None:
            self._user_agent = val

    #
    # abstract methos that must be implemented in subclasses
    #
    def _api_path(self, method: K2hr3HTTPMethod) -> Optional[str]:
        """Get the request url path."""
        if method == K2hr3HTTPMethod.GET:
            if self.api_id == 1:
                return f'{self.version}/{self.basepath}/{self.extapi_name}' \
                       f'/{self.register_path}'
        return None
#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
