# -*- coding: utf-8 -*-
#
# K2HDKC DBaaS based on Trove
#
# Copyright 2020 Yahoo Japan Corporation
# Copyright 2024 LY Corporation
#
# K2HDKC DBaaS is a Database as a Service compatible with Trove which
# is DBaaS for OpenStack.
# Using K2HR3 as backend and incorporating it into Trove to provide
# DBaaS functionality. K2HDKC, K2HR3, CHMPX and K2HASH are components
# provided as AntPickax.
#
# For the full copyright and license information, please view
# the license file that was distributed with this source code.
#
# AUTHOR:   Hirotaka Wakabayashi
# CREATE:   Mon Sep 14 2020
# REVISION:
#
#
"""K2HR3 Python Client of Role API.

.. code-block:: python

    # Import modules from k2hr3client package.
    from k2hr3client.token import K2hr3Token
    from k2hr3client.http import K2hr3Http
    from k2hr3client.role import K2hr3Role

    iaas_project = "demo"
    iaas_token = "gAAAAA..."
    mytoken = K2hr3Token(iaas_project, iaas_token)

    # POST a request to create a token to K2HR3 Token API.
    myhttp = K2hr3Http("http://127.0.0.1:18080")
    myhttp.POST(mytoken.create())
    mytoken.token  // gAAAAA...

    # POST a request to create a role to K2HR3 Role API.
    myrole = K2hr3Role(mytoken.token)
    myhttp.POST(
        myrole.create(
            role_name = "test_role",
            policies = ['yrn:yahoo:::demo:policy:test_policy'],
            alias = []
        )
    )
    myrole.resp.body // {"result":true...

"""

from enum import Enum
import json
import logging
from typing import List, Optional


from k2hr3client.api import K2hr3Api, K2hr3HTTPMethod

LOG = logging.getLogger(__name__)


_ROLE_API_CREATE_ROLE = """
{
    "role":    {
        "name":        "<role name or yrn full path>",
        "policies":    [],
        "alias":       []
    }
}
"""
_ROLE_API_ADD_MEMBER = """
{
    "host":    {
        "host":            "<hostname / ip address>",
        "port":            "<port number>",
        "cuk":             "<container unique key: reserved>",
        "extra":           "<extra string data>",
        "tag":             "<tag string data>",
        "inboundip":       "<ip address>",
        "outboundip":      "<ip address>"
    },
    "clear_hostname":      "<true/false>",
    "clear_ips":           "<true/false>"
}
"""
_ROLE_API_ADD_MEMBERS = """
{
    "host":    [{
        "host":            "<hostname / ip address>",
        "port":            "<port number>",
        "cuk":             "<container unique key: reserved>",
        "extra":           "<extra string data>",
        "tag":             "<tag string data>",
        "inboundip":       "<ip address>",
        "outboundip":      "<ip address>"
    }],
    "clear_hostname":      "<true/false>",
    "clear_ips":           "<true/false>"
}
"""
_ROLE_API_ADD_MEMBER_USING_ROLETOKEN = """
{
    "host":    {
        "port":            "<port number>",
        "cuk":             "<container unique key: reserved>",
        "extra":           "<extra string data>",
        "tag":             "<tag string data>",
        "inboundip":       "<ip address>",
        "outboundip":      "<ip address>"
    }
}
"""


class K2hr3RoleHost:  # pylint disable=too-few-public-methods
    # pylint: disable=too-few-public-methods
    """Represent a host of a role.

    NOTE(hiwakaba): This class exists only for backward compatibility.
    """

    def __init__(self, host: str, port: str, cuk: str, extra: str, tag: str,
                 inboundip: str, outboundip: str):
        """Init the members."""
        self.host = host
        self.port = port
        self.cuk = cuk
        self.extra = extra
        self.tag = tag
        self.inboundip = inboundip
        self.outboundip = outboundip


class K2hr3RoleHostList:  # pylint disable=too-few-public-methods
    # pylint: disable=too-few-public-methods
    """Represent a list of hosts of a role.

    NOTE(hiwakaba): This class exists only for backward compatibility.
    """

    def __init__(self):
        """Init the members."""
        self.hostlist = []

    def add_host(self, host):
        """Add hosts to the list."""
        self.hostlist.append(host)


class K2hr3TokenType(Enum):  # pylint disable=too-few-public-methods
    # pylint: disable=too-few-public-methods
    """Represent a type of token."""

    SCOPED_TOKEN = 1
    ROLE_TOKEN = 2
    NO_TOKEN = 3


class K2hr3Role(K2hr3Api):  # pylint: disable=too-many-instance-attributes
    """Relationship with K2HR3 ROLE API.

    See https://k2hr3.antpick.ax/api_role.html
    """

    __slots__ = ('_r3token',)

    def __init__(self, r3token: str, token_type=K2hr3TokenType.SCOPED_TOKEN):
        """Init the members."""
        super().__init__("role")
        self.r3token = r3token

        # following attrs are dynamically set later.
        if token_type == K2hr3TokenType.SCOPED_TOKEN:
            self.headers = {
                'Content-Type': 'application/json',
                'x-auth-token': 'U={}'.format(self._r3token)
            }
        elif token_type == K2hr3TokenType.ROLE_TOKEN:
            self.headers = {
                'Content-Type': 'application/json',
                'x-auth-token': 'R={}'.format(self._r3token)
            }
        elif token_type == K2hr3TokenType.NO_TOKEN:
            self.headers = {
                'Content-Type': 'application/json'
            }
        self.body = None
        self.urlparams = None
        # attributes that are unique to this class
        self.role_name = None
        self.policies = None
        self.alias = None
        self.host = None
        self.clear_hostname = None
        self.clear_ips = None
        self.hosts = None
        self.port = None
        self.cuk = None
        self.extra = None
        self.tag = None
        self.inboundip = None
        self.outboundip = None
        self.expand = None
        self.role_token_string = None

    # POST http(s)://API SERVER:PORT/v1/role
    # PUT http(s)://API SERVER:PORT/v1/role?urlarg
    def create(self, role_name: str, policies: List[str], alias: List[str]):
        """Create tokens."""
        self.api_id = 1
        self.role_name = role_name  # type: ignore
        self.policies = policies  # type: ignore
        self.alias = alias  # type: ignore
        return self

    # POST(Add HOST to ROLE)
    # http(s)://API SERVER:PORT/v1/role/role path
    # http(s)://API SERVER:PORT/v1/role/yrn full path to role
    def add_member(self, role_name: str, host: str,
                   clear_hostname: bool, clear_ips: str):
        """Add a member to the role."""
        self.api_id = 3
        self.role_name = role_name  # type: ignore
        self.host = host  # type: ignore
        self.clear_hostname = clear_hostname  # type: ignore
        self.clear_ips = clear_ips  # type: ignore
        return self

    def add_members(self, role_name: str, hosts: str,
                    clear_hostname: bool, clear_ips: str):
        """Add members to the role."""
        self.api_id = 4
        self.role_name = role_name  # type: ignore
        self.hosts = hosts  # type: ignore
        self.clear_hostname = clear_hostname  # type: ignore
        self.clear_ips = clear_ips  # type: ignore
        return self

    # PUT(Add HOST to ROLE)
    # http(s)://API SERVER:PORT/v1/role/role path?urlarg
    # http(s)://API SERVER:PORT/v1/role/yrn full path to role?urlarg
    def add_member_with_roletoken(self, role_name: str, port: str, cuk: str,
                                  extra: str, tag: str,
                                  inboundip: str, outboundip: str):
        """Add members to the role without roletoken."""
        self.api_id = 5
        self.role_name = role_name  # type: ignore
        self.port = port  # type: ignore
        self.cuk = cuk  # type: ignore
        self.extra = extra  # type: ignore
        self.tag = tag  # type: ignore
        self.inboundip = inboundip  # type: ignore
        self.outboundip = outboundip  # type: ignore
        return self

    # GET(Create ROLE Token)
    # TODO(hiwakaba)

    # GET(Show ROLE details)
    # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path?urlarg
    def get(self, role_name: str, expand: bool = True):
        """Show role details."""
        self.api_id = 6
        self.role_name = role_name  # type: ignore
        self.expand = expand  # type: ignore
        return self

    # GET (Role Token List)
    # http(s)://APISERVER:PORT/v1/role/token/list/role path or yrn full role path # noqa
    def get_token_list(self, role_name: str, expand: bool = True):
        """Show token list."""
        self.api_id = 7
        self.role_name = role_name  # type: ignore
        self.expand = expand  # type: ignore
        return self

    # HEAD(Validate ROLE)
    # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path
    def validate_role(self, role_name: str):
        """Validate role."""
        self.api_id = 8
        self.role_name = role_name  # type: ignore
        return self

    # DELETE(Delete ROLE)
    # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path?urlarg
    def delete(self, role_name: str):
        """Delete role."""
        self.api_id = 9
        self.role_name = role_name  # type: ignore
        return self

    # DELETE(Hostname/IP address deletion-role specification)
    # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path
    def delete_member(self, role_name: str, host: str, port: str, cuk: str):
        """Delete host."""
        self.api_id = 10
        self.role_name = role_name  # type: ignore
        self.host = host  # type: ignore
        self.port = port  # type: ignore
        self.cuk = cuk  # type: ignore
        return self

    # DELETE(Hostname/IP address deletion - Role not specified)
    def delete_member_wo_roletoken(self, cuk: str):
        """Delete host without roletoken."""
        self.api_id = 11
        self.cuk = cuk  # type: ignore
        return self

    # DELETE (RoleToken deletion - Role specified)
    # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path
    def delete_roletoken(self, role_name: str, port: str, cuk: str):
        """Delete roletoken."""
        self.api_id = 12
        self.role_name = role_name  # type: ignore
        self.port = port  # type: ignore
        self.cuk = cuk  # type: ignore
        return self

    # DELETE(Delete RoleToken - Role not specified)
    def delete_roletoken_with_string(self, role_token_string: str):
        """Delete roletoken without role."""
        self.api_id = 13
        self.role_token_string = role_token_string  # type: ignore
        return self

    def __repr__(self) -> str:
        """Represent the instance."""
        attrs = []
        values = ""
        for attr in ['_r3token']:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs])
        return '<K2hr3Role ' + values + '>'

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
    def _api_path(self, method: K2hr3HTTPMethod) -> Optional[str]: # pylint: disable=too-many-branches, disable=too-many-return-statements, too-many-statements, line-too-long # noqa
        """Get the request url path."""
        if method == K2hr3HTTPMethod.POST:
            if self.api_id == 1:
                python_data = json.loads(_ROLE_API_CREATE_ROLE)
                python_data['role']['name'] = self.role_name
                python_data['role']['policies'] = self.policies
                python_data['role']['alias'] = self.alias
                self.body = json.dumps(python_data)
                # POST http(s)://API SERVER:PORT/v1/role
                return f'{self.version}/{self.basepath}'
            if self.api_id == 3:
                python_data = json.loads(_ROLE_API_ADD_MEMBER)
                python_data['host']['host'] = self.host.host  # type: ignore[attr-defined]  # noqa
                python_data['host']['port'] = self.host.port  # type: ignore[attr-defined]  # noqa
                python_data['host']['cuk'] = self.host.cuk  # type: ignore[attr-defined]  # noqa
                python_data['host']['extra'] = self.host.extra  # type: ignore[attr-defined]  # noqa
                python_data['host']['tag'] = self.host.tag  # type: ignore[attr-defined]  # noqa
                python_data['host']['inboundip'] = self.host.inboundip  # type: ignore[attr-defined]  # noqa # pylint: disable=line-too-long
                python_data['host']['outboundip'] = self.host.outboundip  # type: ignore[attr-defined]  # noqa # pylint: disable=line-too-long
                self.body = json.dumps(python_data)
                # http(s)://API SERVER:PORT/v1/role/role path
                return f'{self.version}/{self.basepath}/{self.role_name}'
            # elif (self.api_id == 4):
            #     python_data = json.loads(_ROLE_API_ADD_MEMBERS)
            #     # TODO(hiwakaba) Not implemented
            #     self.body = json.dumps(python_data)
            #     # http(s)://API SERVER:PORT/v1/role/role path
            #     return f'{self.basepath}/{self.role_name}'
            if self.api_id == 5:
                python_data = json.loads(_ROLE_API_ADD_MEMBER_USING_ROLETOKEN)
                python_data['host']['port'] = self.host.port  # type: ignore[attr-defined]  # noqa
                python_data['host']['cuk'] = self.host.cuk  # type: ignore[attr-defined]  # noqa
                python_data['host']['extra'] = self.host.extra  # type: ignore[attr-defined]  # noqa
                python_data['host']['tag'] = self.host.tag  # type: ignore[attr-defined]  # noqa
                python_data['host']['inboundip'] = self.host.inboundip  # type: ignore[attr-defined]  # noqa # pylint: disable=line-too-long
                python_data['host']['outboundip'] = self.host.outboundip  # type: ignore[attr-defined]  # noqa # pylint: disable=line-too-long
                self.body = json.dumps(python_data)
                # http(s)://API SERVER:PORT/v1/role/role path
                return f'{self.version}/{self.basepath}/{self.role_name}'
        if method == K2hr3HTTPMethod.PUT:
            if self.api_id == 1:
                self.urlparams = json.dumps({
                    'name': self.role_name,
                    'policies': self.policies,
                    'alias': self.alias
                })
                # POST http(s)://API SERVER:PORT/v1/role
                return f'{self.version}/{self.basepath}'
            if self.api_id == 3:
                self.urlparams = json.dumps({
                    'host': self.host.host,  # type: ignore[attr-defined]
                    'port': self.host.port,  # type: ignore[attr-defined]
                    'cuk': self.host.cuk,  # type: ignore[attr-defined]
                    'extra': self.host.extra,  # type: ignore[attr-defined]
                    'tag': self.host.tag,  # type: ignore[attr-defined]
                    'inboundip': self.host.inboundip,  # type: ignore[attr-defined]  # noqa
                    'outboundip': self.host.outboundip  # type: ignore[attr-defined]  # noqa
                })
                # http(s)://API SERVER:PORT/v1/role/role path
                return f'{self.version}/{self.basepath}/{self.role_name}'
            if self.api_id == 4:
                # TODO(hiwakaba) Not implemented
                self.urlparams = json.dumps({
                })
                # http(s)://API SERVER:PORT/v1/role/role path
                return f'{self.version}/{self.basepath}/{self.role_name}'
            if self.api_id == 5:
                self.urlparams = json.dumps({
                    'port': self.port,
                    'cuk': self.cuk,
                    'extra': self.extra,
                    'tag': self.tag,
                    'inboundip': self.inboundip,
                    'outboundip': self.outboundip
                })
                # http(s)://API SERVER:PORT/v1/role/role path
                return f'{self.version}/{self.basepath}/{self.role_name}'
        if method == K2hr3HTTPMethod.GET:
            if self.api_id == 6:
                self.urlparams = json.dumps({
                    'expand': self.expand
                })
                # GET(Show ROLE details)
                # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path?urlarg # noqa
                return f'{self.version}/{self.basepath}/{self.role_name}'
            if self.api_id == 7:
                self.urlparams = json.dumps({
                    'expand': self.expand
                })
                # http(s)://APISERVER:PORT/v1/role/token/list/role path or yrn full role path # noqa
                return f'{self.version}/{self.basepath}/token/list/' \
                       f'{self.role_name}'

        if method == K2hr3HTTPMethod.HEAD:
            if self.api_id == 8:
                # HEAD(Validate ROLE)
                # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path # noqa
                return f'{self.version}/{self.basepath}/{self.role_name}'

        if method == K2hr3HTTPMethod.DELETE:
            if self.api_id == 9:
                # DELETE(Delete ROLE)
                # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path?urlarg # noqa
                return f'{self.version}/{self.basepath}/{self.role_name}'
            if self.api_id == 10:
                # DELETE(Hostname/IP address deletion-role specification)
                # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path # noqa
                self.urlparams = json.dumps({
                    'host': self.host,
                    'port': self.port,
                    'cuk': self.cuk
                })
                return f'{self.version}/{self.basepath}/{self.role_name}'
            if self.api_id == 11:
                # DELETE(Hostname/IP address deletion-role specification)
                # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path # noqa
                self.urlparams = json.dumps({
                    'cuk': self.cuk
                })
                return f'{self.version}/{self.basepath}'
            if self.api_id == 12:
                # DELETE (RoleToken deletion - Role specified)
                # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path # noqa
                self.urlparams = json.dumps({
                    'port': self.port,
                    'cuk': self.cuk
                })
                return f'{self.version}/{self.basepath}/{self.role_name}'
            if self.api_id == 13:
                # DELETE(Delete RoleToken - Role not specified)
                # http(s)://API SERVER:PORT/v1/role/token/role token string
                return f'{self.version}/{self.basepath}/token/{self.role_token_string}' # noqa
        return None
#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
