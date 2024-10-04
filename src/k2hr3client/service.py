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
"""K2HR3 Python Client of Service API.

.. code-block:: python

    # Import modules from k2hr3client package.
    from k2hr3client.token import K2hr3Token
    from k2hr3client.http import K2hr3Http
    from k2hr3client.service import K2hr3Service

    iaas_project = "demo"
    iaas_token = "gAAAAA..."
    mytoken = K2hr3Token(iaas_project, iaas_token)

    # POST a request to create a token to K2HR3 Token API.
    myhttp = K2hr3Http("http://127.0.0.1:18080")
    myhttp.POST(mytoken.create())
    mytoken.token  // gAAAAA...

    # POST a request to create a service to K2HR3 Service API.
    myservice = K2hr3Service(mytoken.token, "test_service")
    myhttp.POST(
        myservice.create(
            verify = "http://example.com/verify_url.php"
        )
    )
    myservice.resp.body // {"result":true...

"""

import json
import logging
from typing import Optional


from k2hr3client.api import K2hr3Api, K2hr3HTTPMethod

LOG = logging.getLogger(__name__)

_SERVICE_API_CREATE_SERVICE = """
{
    "name":        "<service name>",
    "verify":      "<verify url>"
}
"""
_SERVICE_API_ADD_MEMBER = """
{
    "tenant":  "<tenant name>",
    "clear_tenant": "true/false",
    "verify":  "<verify url>"
}
"""
_SERVICE_API_MODIFY_VERIFY = """
{
    "verify":  "<verify url>"
}
"""


class K2hr3Service(K2hr3Api):  # pylint: disable=too-many-instance-attributes
    """Relationship with K2HR3 SERVICE API.

    See https://k2hr3.antpick.ax/api_service.html for details.
    """

    __slots__ = ('_r3token',)

    def __init__(self, r3token: str, service_name: str):
        """Init the members."""
        super().__init__("service")
        self.r3token = r3token
        self.name = service_name

        # following attrs are dynamically set later.
        self.headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U={}'.format(self._r3token)
        }
        self.body = None
        self.urlparams = None
        # attributes that are unique to this class
        self.verify_url = None
        self.tenant = None
        self.clear_tenant = None

    # ---- POST/PUT ----
    def create(self, verify_url: str):
        """Create services."""
        self.api_id = 1
        self.verify_url = verify_url  # type: ignore
        return self

    def add_member(self, tenant: str, clear_tenant: bool):
        """Add members to services."""
        self.api_id = 2
        self.tenant = tenant  # type: ignore
        self.clear_tenant = clear_tenant  # type: ignore
        return self

    def modify(self, verify_url: str):
        """Modify services."""
        self.api_id = 3
        self.verify_url = verify_url  # type: ignore
        return self

    # ---- GET ----
    # GET      http(s)://API SERVER:PORT/v1/service/service name
    def get(self):
        """Get services."""
        self.api_id = 4
        return self

    # ---- HEAD ----
    # HEAD     http(s)://API SERVER:PORT/v1/service/service name
    #          http(s)://API SERVER:PORT/v1/service/service name?urlarg
    #          Validate MEMBER(Optional)    tenant=tenant name
    def validate(self, tenant: Optional[str] = None):
        """Validate services."""
        self.api_id = 5
        self.tenant = tenant  # type: ignore
        return self

    # ---- DELETE ----
    # DELETE   http(s)://API SERVER:PORT/v1/service/service name
    #          http(s)://API SERVER:PORT/v1/service/service name?urlarg
    #          Delete MEMBER(Optional)        tenant=tenant name(optional)
    #
    def delete(self):
        """Delete services."""
        self.api_id = 6
        return self

    def delete_tenant(self, tenant: str):
        """Delete tenants."""
        self.api_id = 7
        self.tenant = tenant  # type: ignore
        return self

    def __repr__(self):
        """Represent the members."""
        attrs = []
        values = ""
        for attr in ['_r3token', '_name']:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs])
        return '<K2hr3Service ' + values + '>'

    @property  # type: ignore
    def r3token(self) -> str:
        """Return the r3token."""
        return self._r3token

    @r3token.setter
    def r3token(self, val: str):  # type: ignore # noqa: F811
        """Set the r3token."""
        if getattr(self, '_r3token', None) is None:
            self._r3token = val

    #
    # abstract methos that must be implemented in subclasses
    #
    def _api_path(self, method: K2hr3HTTPMethod) -> Optional[str]: # pylint: disable=too-many-branches, disable=too-many-return-statements, line-too-long # noqa
        """Get the request url path."""
        if method == K2hr3HTTPMethod.POST:
            if self.api_id == 1:
                python_data = json.loads(_SERVICE_API_CREATE_SERVICE)
                # {
                # "name":    <service name>
                # "verify":  <verify url>
                # }
                python_data['name'] = self.name
                python_data['verify'] = self.verify_url
                self.body = json.dumps(python_data)
            elif self.api_id == 2:
                python_data = json.loads(_SERVICE_API_ADD_MEMBER)
                # {
                # "tenant":  <tenant name> or [<tenant name>, ...]
                # "clear_tenant": true/false or undefined
                # "verify":  <verify url>
                # }
                python_data['tenant'] = self.tenant
                python_data['clear_tenant'] = self.clear_tenant
                self.body = json.dumps(python_data)
            elif self.api_id == 3:
                python_data = json.loads(_SERVICE_API_MODIFY_VERIFY)
                # {
                # "tenant":  <tenant name> or [<tenant name>, ...]
                # "clear_tenant": true/false or undefined
                # "verify":  <verify url>
                # }
                python_data['verify'] = self.verify_url
                self.body = json.dumps(python_data)
            return f'{self.version}/{self.basepath}'
        if method == K2hr3HTTPMethod.PUT:
            if self.api_id == 1:
                # {
                # "tenant":  <tenant name> or [<tenant name>, ...]
                # "clear_tenant": true/false or undefined
                # "verify":  <verify url>
                # }
                self.urlparams = json.dumps({
                    'name': self.name,
                    'verify': self.verify_url
                })
            elif self.api_id == 2:
                # {
                # "name":    <service name>
                # "verify":  <verify url>
                # }
                self.urlparams = json.dumps({
                    'tenant': self.tenant,
                    'clear_tenant': self.clear_tenant
                })
            elif self.api_id == 3:
                # {
                # "name":    <service name>
                # "verify":  <verify url>
                # }
                self.urlparams = json.dumps({
                    'verify': self.verify_url
                })
            return f'{self.version}/{self.basepath}'
        if method == K2hr3HTTPMethod.GET:
            if self.api_id == 4:
                return f'{self.version}/{self.basepath}/{self.name}'
        if method == K2hr3HTTPMethod.HEAD:
            if self.api_id == 5:
                return f'{self.version}/{self.basepath}/{self.name}'
        if method == K2hr3HTTPMethod.DELETE:
            if self.api_id == 6:
                return f'{self.version}/{self.basepath}/{self.name}'
            if self.api_id == 7:
                self.urlparams = json.dumps({
                    'tenant': self.tenant
                })
                return f'{self.version}/{self.basepath}/{self.name}'
        return None
#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
