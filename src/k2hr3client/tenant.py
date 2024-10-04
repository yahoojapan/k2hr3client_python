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
"""K2HR3 Python Client of Tenant API.

.. code-block:: python

    # Import modules from k2hr3client package.
    from k2hr3client.token import K2hr3Token
    from k2hr3client.http import K2hr3Http
    from k2hr3client.tenant import K2hr3Tenant

    iaas_project = "demo"
    iaas_token = "gAAAAA..."
    mytoken = K2hr3Token(iaas_project, iaas_token)

    # POST a request to create a token to K2HR3 Token API.
    myhttp = K2hr3Http("http://127.0.0.1:18080")
    myhttp.POST(mytoken.create())
    mytoken.token  // gAAAAA...

    # POST a request to create a tenant to K2HR3 Tenant API.
    mytenant = K2hr3Tenant(mytoken.token)
    myhttp.POST(
        mytenant.create(
            tenant_name = "test_tenant",
            users = ["demo"],
            desc = "test_tenant description",
            display = "test tenant display"
        )
    )
    mytenant.resp.body // {"result":true...

"""

import json
import logging
from typing import List, Optional


from k2hr3client.api import K2hr3Api, K2hr3HTTPMethod

LOG = logging.getLogger(__name__)

_TENANT_API_CREATE_TENANT = """
{
    "tenant":    {
        "name":        "<tenant name>",
        "desc":        "<tenant description>",
        "display":     "<display name>",
        "users":       "<users>"
    }
}
"""

_TENANT_API_UPDATE_TENANT = """
{
    "tenant":    {
        "id":          "<tenant id>",
        "desc":        "<tenant description>",
        "display":     "<display name>",
        "users":       "<users>"
    }
}
"""


class K2hr3Tenant(K2hr3Api):  # pylint: disable=too-many-instance-attributes
    """Relationship with K2HR3 TENANT API.

    See https://k2hr3.antpick.ax/api_tenant.html for details.
    """

    __slots__ = ('_r3token',)

    def __init__(self, r3token: str):
        """Init the members."""
        super().__init__("tenant")
        self.r3token = r3token

        # following attrs are dynamically set later.
        self.headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U={}'.format(self._r3token)
        }
        self.body = None
        self.urlparams = None
        # attributes that are unique to this class
        self.tenant_name = None
        self.users = None
        self.desc = None
        self.display = None
        self.tenant_id = None
        self.expand = None

    # POST(create)    http(s)://API SERVER:PORT/v1/tenant
    # {
    #     tenant:    {
    #         name:     <tenant name>
    #         desc:     <description for tenant>
    #         display:  <display name for tenant>
    #         users:    [<user name>, ...]
    #     }
    # }
    # PUT(Create)    http(s)://API SERVER:PORT/v1/tenant?name=tenant name&… # noqa
    def create(self, tenant_name: str, users: Optional[List[str]],
               desc: Optional[str], display: Optional[str]):
        """Create a new K2HR3 cluster Local Tenant(TENANT)."""
        self.api_id = 1
        self.tenant_name = tenant_name  # type: ignore
        self.users = users  # type: ignore
        self.desc = desc  # type: ignore
        self.display = display  # type: ignore
        return self

    # POST (Update)    http(s)://API SERVER:PORT/v1/tenant/tenant name
    # {
    #     tenant:    {
    #         id:       <tenant id>
    #         desc:     <description for tenant>
    #         display:  <display name for tenant>
    #         users:    [<user name>, ...]
    #     }
    # }
    # PUT (Update)    http(s)://API SERVER:PORT/v1/tenant/tenant name?id=tenant id # noqa
    def modify(self, tenant_name: str, tenant_id: int,  # pylint: disable=R0917
               users: Optional[List[str]], desc: Optional[str],
               display: Optional[str]):
        """Update the K2HR3 cluster Local Tenant(TENANT)."""
        self.api_id = 3
        self.tenant_name = tenant_name  # type: ignore
        self.tenant_id = tenant_id  # type: ignore
        self.users = users  # type: ignore
        self.desc = desc  # type: ignore
        self.display = display  # type: ignore
        return self

    # GET (List)    http(s)://API SERVER:PORT/v1/tenant?expand=true or false
    def get_tenant_list(self, expand: bool = False):
        """List the K2HR3 cluster Local Tenant(TENANT)."""
        self.api_id = 5
        self.expand = expand  # type: ignore
        return self

    # GET (Tenant)    http(s)://API SERVER:PORT/v1/tenant/tenant name
    def get(self, tenant_name: str):
        """Get the K2HR3 cluster Local Tenant(TENANT) information."""
        self.api_id = 6
        self.tenant_name = tenant_name  # type: ignore
        return self

    # HEAD            http(s)://API SERVER:PORT/v1/tenant/tenant name
    def validate(self, tenant_name: str):
        """Check the existence of the K2HR3 cluster Local Tenant(TENANT)."""
        self.api_id = 7
        self.tenant_name = tenant_name  # type: ignore
        return self

    # DELETE (Tenant)    http(s)://API SERVER:PORT/v1/tenant?tenant=tenant name?id=tenant id # noqa
    def delete(self, tenant_name: str, tenant_id: int):
        """Completely delete the Local Tenant(TENANT)."""
        self.api_id = 8
        self.tenant_name = tenant_name  # type: ignore
        self.tenant_id = tenant_id  # type: ignore
        return self

    # DELETE (User)    http(s)://API SERVER:PORT/v1/tenant/tenant name?id=tenant id # noqa
    def delete_user(self, tenant_name: str, tenant_id: int):
        """Make the USER unavailable to the K2HR3 cluster Local Tenant(TENANT)."""  # noqa
        self.api_id = 9
        self.tenant_name = tenant_name  # type: ignore
        self.tenant_id = tenant_id  # type: ignore
        return self

    def __repr__(self) -> str:
        """Represent the members."""
        attrs = []
        values = ""
        for attr in ['_r3token']:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs])
        return '<K2hr3Tenant ' + values + '>'

    @property  # type: ignore
    def r3token(self) -> str:
        """Return the r3token."""
        return self._r3token

    @r3token.setter
    def r3token(self, val: str) -> None:  # type: ignore # noqa: F811
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
                python_data = json.loads(_TENANT_API_CREATE_TENANT)
                python_data['tenant']['name'] = self.tenant_name
                python_data['tenant']['users'] = self.users
                python_data['tenant']['desc'] = self.desc
                python_data['tenant']['display'] = self.display
                self.body = json.dumps(python_data)
                return f'{self.version}/{self.basepath}'
            if self.api_id == 3:
                python_data = json.loads(_TENANT_API_UPDATE_TENANT)
                python_data['tenant']['id'] = self.tenant_id
                python_data['tenant']['users'] = self.users
                python_data['tenant']['desc'] = self.desc
                python_data['tenant']['display'] = self.display
                self.body = json.dumps(python_data)
                return f'{self.version}/{self.basepath}/{self.tenant_name}'

        if method == K2hr3HTTPMethod.PUT:
            if self.api_id == 1:
                python_data = json.loads(_TENANT_API_CREATE_TENANT)
                self.urlparams = json.dumps({
                    'name': self.tenant_name,
                    'users': self.users,
                    'desc': self.desc,
                    'display': self.display
                })
                return f'{self.version}/{self.basepath}'
            if self.api_id == 3:
                python_data = json.loads(_TENANT_API_UPDATE_TENANT)
                self.urlparams = json.dumps({
                    'id': self.tenant_id,
                    'users': self.users,
                    'desc': self.desc,
                    'display': self.display
                })
                return f'{self.version}/{self.basepath}/{self.tenant_name}'

        if method == K2hr3HTTPMethod.GET:
            if self.api_id == 5:
                self.urlparams = json.dumps({
                    'expand': self.expand
                })
                return f'{self.version}/{self.basepath}'
            if self.api_id == 6:
                return f'{self.version}/{self.basepath}/{self.tenant_name}'

        if method == K2hr3HTTPMethod.HEAD:
            if self.api_id == 7:
                return f'{self.version}/{self.basepath}/{self.tenant_name}'

        if method == K2hr3HTTPMethod.DELETE:
            if self.api_id == 8:
                self.urlparams = json.dumps({
                    'tenant': self.tenant_name,
                    'id': self.tenant_id
                })
                return f'{self.version}/{self.basepath}'
            if self.api_id == 9:
                self.urlparams = json.dumps({
                    'id': self.tenant_id
                })
                return f'{self.version}/{self.basepath}/{self.tenant_name}'
        return None
#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
