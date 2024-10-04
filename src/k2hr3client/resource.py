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
"""K2HR3 Python Client of Resource API.

.. code-block:: python

    # Import modules from k2hr3client package.
    from k2hr3client.token import K2hr3Token
    from k2hr3client.http import K2hr3Http
    from k2hr3client.resource import K2hr3Resource

    iaas_project = "demo"
    iaas_token = "gAAAAA..."
    mytoken = K2hr3Token(iaas_project, iaas_token)

    # POST a request to create a token to K2HR3 Token API.
    myhttp = K2hr3Http("http://127.0.0.1:18080")
    myhttp.POST(mytoken.create())
    mytoken.token  // gAAAAA...

    # POST a request to create a K2HDKC resource.
    myresource = K2hr3Resource(mytoken.token)
    myhttp.POST(
        myresource.create_conf_resource(
            name="test_resource",
            data_type="string",
            resource_data="testresourcedata",
            keys={
                "cluster-name": "test-cluster",
                "chmpx-server-port": "8020",
                "chmpx-server-ctrlport": "8021",
                "chmpx-slave-ctrlport": "8031"},
            alias=[])
        )
    myresource.resp.body // {"result":true...

"""

import json
import logging
from typing import Optional

from k2hr3client.api import K2hr3Api, K2hr3HTTPMethod

LOG = logging.getLogger(__name__)

_MAX_LINE_LENGTH = 1024 * 8
_RESOURCE_API_CREATE_RESOURCE = """
{
    "resource":    {
        "name":    "<resource name>",
        "type":    "<data type>",
        "data":    "<resource data>",
        "keys":    {},
        "alias":    []
    }
}
"""
_RESOURCE_API_CREATE_RESOURCE_WITH_ROLE_TOKEN = """
{
    "resource":    {
        "type":    "<data type>",
        "data":    "<resource data>",
        "keys":    {},
    }
}
"""
_RESOURCE_API_CREATE_RESOURCE_WITH_NO_TOKEN = """
{
    "resource":    {
        "port":    "<port number>",
        "cuk":     "<container unique key>",
        "role":    "<role full yrn>",
        "type":    "<data type>",
        "data":    "<resource data>",
        "keys":    {},
    }
}
"""


class K2hr3Resource(K2hr3Api):  # pylint: disable=too-many-instance-attributes
    """Relationship with K2HR3 RESOURCE API.

    See https://k2hr3.antpick.ax/api_resource.html for details.
    """

    __slots__ = ('_r3token', '_roletoken', '_resource_path', )

    def __init__(self, r3token: Optional[str] = None,
                 roletoken: Optional[str] = None,
                 resource_path: Optional[str] = None) -> None:
        """Init the members."""
        super().__init__("resource")
        self.r3token = r3token
        self.roletoken = roletoken
        self.resource_path = resource_path

        # following attrs are dynamically set later.
        if r3token:
            self.headers = {
                'Content-Type': 'application/json',
                'x-auth-token': 'U={}'.format(self._r3token)
            }
        elif roletoken:
            self.headers = {
                'Content-Type': 'application/json',
                'x-auth-token': 'R={}'.format(self._roletoken)
            }
        else:
            self.headers = {
                'Content-Type': 'application/json',
            }
        self.body = None
        self.urlparams = None
        # attributes that are unique to this class
        self.resource_data = None
        self.name = None
        self.data_type = None
        self.keys = None
        self.alias = None
        self.expand = None
        self.service = None
        self.port = None
        self.cuk = None
        self.role = None

    # ---- POST/PUT ----
    # POST http(s)://API SERVER:PORT/v1/resource
    # POST http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path # noqa
    # POST http(s)://API SERVER:PORT/v1/resource/yrn full resource path
    #
    # PUT
    # http(s)://API SERVER:PORT/v1/resource?urlarg
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/yrn full resource path?urlarg
    #
    # name=resource name
    # type=data type
    # data=resource data
    # keys=json key value object
    # alias=json alias array
    # type=data type
    # data=resource data
    # keys=json key value object
    #
    # port=port number
    # cuk=container unique key
    # role=yrn full role path
    # type=data type
    # data=resource data
    # keys=json key value object
    #
    def create_conf_resource(self, name: str, data_type: str, resource_data: str,  # pylint: disable=R0917 # noqa
                             keys: Optional[dict] = None,
                             alias: Optional[list] = None):
        """Create the resource."""
        self.api_id = 1
        self.name = name  # type: ignore
        self.resource_data = resource_data  # type: ignore
        self.data_type = data_type  # type: ignore
        self.keys = keys  # type: ignore
        self.alias = alias  # type: ignore
        return self

    # ---- GET ----
    # GET http(s)://API SERVER:PORT/v1/resource/\
    #    resource path or yrn full resource path?urlarg # noqa
    # GET http(s)://API SERVER:PORT/v1/resource/\
    #    resource path or yrn full resource path?urlarg # noqa
    # GET http(s)://API SERVER:PORT/v1/resource/yrn full resource path?urlarg
    #     expand=true or false
    #     service=service name
    #
    # If a role token request header is specified
    #     type=data type
    #     keyname=key name
    #     service=service name
    #
    # No token specified in the request headers
    #     port=port number
    #     cuk=container unique key
    #     role=yrn full role path
    #     type=data type
    #     keyname=key name
    #     service=service name
    #
    def get(self, expand: bool = False,
            service: Optional[str] = None):
        """Get the resource."""
        self.api_id = 3
        self.expand = expand  # type: ignore
        self.service = service  # type: ignore
        return self

    def get_with_roletoken(self, data_type: str, keys: Optional[dict],
                           service: Optional[str] = None):
        """Get the resource with roletoken."""
        self.api_id = 4
        self.data_type = data_type  # type: ignore
        self.keys = keys  # type: ignore
        self.service = service  # type: ignore
        return self

    # ---- HEAD ----
    # HEAD
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/yrn full resource path?urlarg
    #
    # type=data type
    # keyname=key name
    # service=service name
    #
    # port=port number
    # cuk=container unique key
    # role=yrn full role path
    # type=data type
    # keyname=_key name
    # service=service name
    #
    def validate(self, data_type: str, keys: Optional[dict],
                 service: Optional[str] = None):
        """Validate the resource."""
        self.api_id = 5
        self.data_type = data_type  # type: ignore
        self.keys = keys  # type: ignore
        self.service = service  # type: ignore
        return self

    def validate_with_notoken(self, port: str, cuk: str, role: str,  # pylint: disable=R0917 # noqa
                              data_type: str, keys: Optional[dict],
                              service: Optional[str] = None):
        """Validate the resource without tokens."""
        self.api_id = 6
        self.port = port  # type: ignore
        self.cuk = cuk  # type: ignore
        self.role = role  # type: ignore
        self.data_type = data_type  # type: ignore
        self.keys = keys  # type: ignore
        self.service = service  # type: ignore
        return self

    # DELETE
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/yrn full resource path?urlarg
    #   Scoped User Token
    #     type=data type
    #     keynames=key name
    #     aliases=json alias array
    #   Role Token
    #     type=data type
    #     keynames=key name
    #   No Token
    #     port=port number
    #     cuk=container unique key
    #     role=yrn full role path
    #     type=data type
    #     keyname=_key name
    def delete_with_scopedtoken(self, data_type: str,
                                keys: Optional[dict],
                                alias: Optional[list] = None):
        """Delete the resource with scoped token."""
        self.api_id = 7
        self.data_type = data_type  # type: ignore
        self.keys = keys  # type: ignore
        self.alias = alias   # type: ignore
        return self

    def delete_with_roletoken(self, data_type: str,
                              keys: Optional[dict]):
        """Delete the resource with role token."""
        self.api_id = 8
        self.data_type = data_type  # type: ignore
        self.keys = keys  # type: ignore
        return self

    def delete_with_notoken(self, port: str, cuk: str, role: str,  # pylint: disable=R0917 # noqa
                            data_type: str, keys: Optional[dict]):
        """Delete the resource without token."""
        self.api_id = 9
        self.port = port  # type: ignore
        self.cuk = cuk  # type: ignore
        self.role = role  # type: ignore
        self.data_type = data_type  # type: ignore
        self.keys = keys  # type: ignore
        return self

    def __repr__(self) -> str:
        """Represent instance."""
        attrs = []
        values = ""
        for attr in ['_r3token', '_resource_name', '_resource_path']:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs])
        return '<K2hr3Resource ' + values + '>'

    @property  # type: ignore
    def r3token(self):
        """Return the r3token."""
        return self._r3token

    @r3token.setter
    def r3token(self, val):  # type: ignore # noqa: F811
        """Set the r3token."""
        if getattr(self, '_r3token', None) is None:
            self._r3token = val

    @property  # type: ignore
    def roletoken(self):
        """Return the roletoken."""
        return self._roletoken

    @roletoken.setter
    def roletoken(self, val):  # type: ignore # noqa: F811
        """Set the roletoken."""
        if getattr(self, '_roletoken', None) is None:
            self._roletoken = val

    @property  # type: ignore
    def resource_path(self):
        """Return the resource_path."""
        return self._resource_path

    @resource_path.setter
    def resource_path(self, val):  # type: ignore # noqa: F811
        """Set the resource path."""
        if getattr(self, '_resource_path', None) is None:
            self._resource_path = val

    #
    # abstract methos that must be implemented in subclasses
    #
    def _api_path(self, method: K2hr3HTTPMethod) -> Optional[str]: # pylint: disable=too-many-branches, too-many-return-statements, line-too-long # noqa
        """Get the request url path."""
        if method == K2hr3HTTPMethod.POST:
            if self.api_id == 1:
                python_data = json.loads(_RESOURCE_API_CREATE_RESOURCE)
                python_data['resource']['name'] = self.name
                python_data['resource']['type'] = self.data_type
                python_data['resource']['data'] = self.resource_data
                python_data['resource']['keys'] = self.keys
                python_data['resource']['alias'] = self.alias
                self.body = json.dumps(python_data)
                if self.r3token:
                    return f'{self.version}/{self.basepath}'
                return f'{self.version}/{self.basepath}/{self.resource_path}'
        if method == K2hr3HTTPMethod.PUT:
            if self.api_id == 1:
                self.urlparams = json.dumps({
                    'name': self.name,
                    'type': self.data_type,
                    'data': self.resource_data,
                    'keys': self.keys,
                    'alias': self.alias
                })
                if self.r3token:
                    return f'{self.version}/{self.basepath}'
                return f'{self.version}/{self.basepath}/{self.resource_path}'
        if method == K2hr3HTTPMethod.GET:
            if self.api_id == 3:
                self.urlparams = json.dumps({
                    'expand': self.expand,
                    'service': self.service
                })
                return f'{self.version}/{self.basepath}/{self.resource_path}'
            if self.api_id == 4:
                self.urlparams = json.dumps({
                    'type': self.data_type,
                    'keys': self.keys,
                    'service': self.service
                })
                return f'{self.version}/{self.basepath}/{self.resource_path}'
        if method == K2hr3HTTPMethod.HEAD:
            if self.api_id == 5:
                self.urlparams = json.dumps({
                    'type': self.data_type,
                    'keys': self.keys,
                    'service': self.service
                })
                return f'{self.version}/{self.basepath}/{self.resource_path}'
            if self.api_id == 6:
                self.urlparams = json.dumps({
                    'port': self.port,
                    'cuk': self.cuk,
                    'role': self.role,
                    'type': self.data_type,
                    'keys': self.keys,
                    'service': self.service
                })
                return f'{self.version}/{self.basepath}/{self.resource_path}'
        if method == K2hr3HTTPMethod.DELETE:
            if self.api_id == 7:
                self.urlparams = json.dumps({
                    'type': self.data_type,
                    'keynames': self.keys,
                    'alias': self.alias
                })
                return f'{self.version}/{self.basepath}/{self.resource_path}'
            if self.api_id == 8:
                self.urlparams = json.dumps({
                    'type': self.data_type,
                    'keynames': self.keys,
                })
                return f'{self.version}/{self.basepath}/{self.resource_path}'
            if self.api_id == 9:
                self.urlparams = json.dumps({
                    'port': self.port,
                    'cuk': self.cuk,
                    'role': self.role,
                    'type': self.data_type,
                    'keynames': self.keys,
                })
                return f'{self.version}/{self.basepath}/{self.resource_path}'
        return None
#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
