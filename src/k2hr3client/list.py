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
"""K2HR3 Python Client of List API.

.. code-block:: python

    # Import modules from k2hr3client package.
    from k2hr3client.token import K2hr3Token
    from k2hr3client.http import K2hr3Http
    from k2hr3client.list import K2hr3List

    iaas_project = "demo"
    iaas_token = "gAAAAA..."
    mytoken = K2hr3Token(iaas_project, iaas_token)

    # POST a request to create a token to K2HR3 Token API.
    myhttp = K2hr3Http("http://127.0.0.1:18080")
    myhttp.POST(mytoken.create())
    mytoken.token  // gAAAAA...

    # GET a request to get list from K2HR3 List API.
    mylist = K2hr3List(mytoken.token, "service")
    myhttp.GET(mylist.get())
    mylist.resp.body // {"result":true...

"""


import logging
from typing import Optional

from k2hr3client.api import K2hr3Api, K2hr3HTTPMethod
from k2hr3client.exception import K2hr3Exception

LOG = logging.getLogger(__name__)


class K2hr3List(K2hr3Api):  # pylint: disable=too-many-instance-attributes
    """Relationship with K2HR3 LIST API.

    See https://k2hr3.antpick.ax/api_list.html
    """

    __slots__ = ('_r3token', '_service', )

    def __init__(self, r3token: str, service: str) -> None:
        """Init the members."""
        super().__init__("list")
        self.r3token = r3token
        self.service = service

        # following attrs are dynamically set later.
        self.headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U={}'.format(self._r3token)
        }
        self.body = None  # type: ignore
        self.urlparams = None
        # ---
        self.expand = False

    # ---- GET ----
    # GET
    # http(s)://API SERVER:PORT/v1/list/service name
    # http(s)://API SERVER:PORT/v1/list{/service name}/resource{/root path}?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/list{/service name}/policy{/root path}?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/list{/service name}/role{/root path}?urlarg
    #
    # URL Arguments
    # expand=true or false(default)
    #
    def get(self, expand=False):
        """List K2HR3's SERVICE, RESOURCE, POLICY and ROLE in YRN form."""
        self.api_id = 1
        self.expand = expand
        return self

    # ---- HEAD ----
    # HEAD
    # http(s)://API SERVER:PORT/v1/list/service name
    # http(s)://API SERVER:PORT/v1/list{/service name}/resource{/root path}?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/list{/service name}/resource{/root path}?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/list{/service name}/policy{/root path}?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/list{/service name}/role{/root path}?urlarg
    #
    def validate(self):
        """Validate the objects."""
        self.api_id = 2
        return self

    def __repr__(self) -> str:
        """Represent the instance."""
        attrs = []
        values = ""
        for attr in [
                '_r3token', '_service'
        ]:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs])
        return '<K2hr3List ' + values + '>'

    @property  # type: ignore
    def r3token(self) -> str:
        """Return the r3token."""
        return self._r3token

    @r3token.setter
    def r3token(self, val: str):  # type: ignore # noqa: F811
        """Set the r3token."""
        if getattr(self, '_r3token', None) is None:
            self._r3token = val

    @property  # type: ignore
    def service(self) -> str:
        """Return the service."""
        return self._service

    @service.setter
    def service(self, val: str) -> None:  # type: ignore # noqa: F811
        """Set the service."""
        if isinstance(val, str) is False:
            raise K2hr3Exception(f'value type must be list, not {type(val)}')
        if getattr(self, '_service', None) is None:
            self._service = val

    #
    # abstract methos that must be implemented in subclasses
    #
    def _api_path(self, method: K2hr3HTTPMethod) -> Optional[str]:
        """Get the request url path."""
        if method == K2hr3HTTPMethod.GET:
            if self.api_id == 1:
                return f'{self.version}/{self.basepath}/{self.service}'
        if method == K2hr3HTTPMethod.HEAD:
            if self.api_id == 2:
                return f'{self.version}/{self.basepath}/{self.service}'
        return None
#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
