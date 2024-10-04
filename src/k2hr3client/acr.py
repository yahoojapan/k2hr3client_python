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

"""K2HR3 Python Client of ACR API.

.. code-block:: python

    # Import modules from k2hr3client package.
    from k2hr3client.token import K2hr3Token
    from k2hr3client.http import K2hr3Http
    from k2hr3client.acr import K2hr3Acr

    iaas_project = "demo"
    iaas_token = "gAAAAA..."
    mytoken = K2hr3Token(iaas_project, iaas_token)

    # POST a request to create a token to K2HR3 Token API.
    myhttp = K2hr3Http("http://127.0.0.1:18080")
    myhttp.POST(mytoken.create())
    mytoken.token  // gAAAAA...

    # POST a request to add member to K2HR3 ACR API.
    myacr = K2hr3Acr(mytoken.token, "service")
    myhttp.POST(myacr.add_member("mytenant"))

"""


import json
from typing import Optional

from k2hr3client.api import K2hr3Api, K2hr3HTTPMethod
from k2hr3client.exception import K2hr3Exception

_ACR_API_ADD_MEMBER = """
{
    "tenant":    "<tenant name>"
}
"""


class K2hr3Acr(K2hr3Api):  # pylint: disable=too-many-instance-attributes
    """Relationship with K2HR3 ACR API.

    See https://k2hr3.antpick.ax/api_acr.html
    """

    __slots__ = ('_r3token', '_service')

    def __init__(self, r3token: str, service: str):
        """Init the members."""
        super().__init__("acr")
        self.r3token = r3token
        self.service = service

        # following attrs are dynamically set later.
        self.headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U={}'.format(self._r3token)
        }
        self.body = None
        self.urlparams = None
        # attributes that are unique to this class
        self.tenant = None  # type: Optional[str]
        self.cip = None  # type: Optional[str]
        self.cport = None  # type: Optional[str]
        self.ccuk = None  # type: Optional[str]
        self.crole = None  # type: Optional[str]
        self.sport = None  # type: Optional[str]
        self.srole = None  # type: Optional[str]
        self.scuk = None  # type: Optional[str]

    # ---- POST/PUT ----
    # POST    http(s)://API SERVER:PORT/v1/acr/service name
    # PUT     http(s)://API SERVER:PORT/v1/acr/service name
    #         http(s)://API SERVER:PORT/v1/acr/service name?urlarg
    #                   urlargs    tenant=tenant name
    def add_member(self, tenant: Optional[str]):
        """Add the members."""
        self.api_id = 1
        self.tenant = tenant
        return self

    # ---- GET ----
    # GET    http(s)://API SERVER:PORT/v1/acr/service name
    #         http(s)://API SERVER:PORT/v1/acr/service name?urlarg
    #            cip=client ip address
    #            cport=client port(optional)
    #            crole=client role yrn path
    #            ccuk=client container unique key
    #            sport=service port(optional)
    #            srole=service role yrn path
    #            scuk=service container unique key
    def show_credential_details(self):
        """Show the credential details."""
        self.api_id = 2
        return self

    def get_available_resources(self,  # pylint: disable=R0917
                                cip: Optional[str] = None,
                                cport: Optional[str] = None,
                                crole: Optional[str] = None,
                                ccuk: Optional[str] = None,
                                sport: Optional[str] = None,
                                srole: Optional[str] = None,
                                scuk: Optional[str] = None):
        """Show the available resources."""
        self.api_id = 3
        self.cip = cip
        self.cport = cport
        self.crole = crole
        self.ccuk = ccuk
        self.sport = sport
        self.srole = srole
        self.scuk = scuk
        return self

    # ---- DELETE ----
    #
    # DELETE    http(s)://API SERVER:PORT/v1/acr/service name
    def delete_member(self, tenant: str):
        """Delete the members."""
        self.api_id = 4
        self.tenant = tenant
        return self

    def __repr__(self) -> str:
        """Represent the instance."""
        attrs = []
        values = ""
        for attr in ['_r3token', '_tenant']:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs])
        return '<K2hr3Acr ' + values + '>'

    @property  # type: ignore
    def r3token(self) -> str:
        """Return the r3token."""
        return self._r3token

    @r3token.setter
    def r3token(self, val: str) -> None:  # type: ignore # noqa: F811
        """Set the r3token."""
        if getattr(self, '_r3token', None) is None:
            self._r3token = val

    @property  # type: ignore
    def service(self) -> str:
        """Return the tenant."""
        return self._service

    @service.setter
    def service(self, val: str):  # type: ignore # noqa: F811
        """Set the service."""
        if isinstance(val, str) is False:
            raise K2hr3Exception(f'value type must be str, not {type(val)}')
        if getattr(self, '_service', None) is None:
            self._service = val

    #
    # abstract methos that must be implemented in subclasses
    #
    def _api_path(self, method: K2hr3HTTPMethod) -> Optional[str]:
        """Get the request url path."""
        if method == K2hr3HTTPMethod.POST:
            # Creating the request body
            if self.api_id == 1:
                python_data = json.loads(_ACR_API_ADD_MEMBER)
                python_data['tenant'] = self.tenant
                self.body = json.dumps(python_data)
                return f'{self.version}/{self.basepath}/{self.service}'
        if method == K2hr3HTTPMethod.PUT:
            if self.api_id == 1:
                self.urlparams = json.dumps({
                    'tenant': self.tenant
                })
                return f'{self.version}/{self.basepath}/{self.service}'
        if method == K2hr3HTTPMethod.GET:
            if self.api_id == 2:
                return f'{self.version}/{self.basepath}/{self.service}'
            if self.api_id == 3:
                self.urlparams = json.dumps({
                    'cip': self.cip,
                    'cport': self.cport,
                    'crole': self.crole,
                    'ccuk': self.ccuk,
                    'sport': self.sport,
                    'srole': self.srole,
                    'scuk': self.scuk,
                })
                return f'{self.version}/{self.basepath}/{self.service}'
        if method == K2hr3HTTPMethod.DELETE:
            if self.api_id == 4:
                self.urlparams = json.dumps({
                    'tenant': self.tenant
                })
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
