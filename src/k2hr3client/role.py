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
"""K2HR3 Python Client of Role API.

.. code-block:: python

    # Simple CUI application to create a full k2hdkc dbaas resource.
    from __future__ import (absolute_import, division, print_function,
                            unicode_literals)
    import argparse
    import json
    import os
    from pathlib import Path
    import re
    import sys
    import urllib.parse
    import urllib.request

    here = os.path.dirname(__file__)
    src_dir = os.path.join(here, '..')
    if os.path.exists(src_dir):
        sys.path.append(src_dir)

    import k2hr3client
    from k2hr3client.exception import K2hr3Exception
    from k2hr3client.http import K2hr3Http
    from k2hr3client.token import K2hr3Token
    from k2hr3client.resource import K2hr3Resource
    from k2hr3client.policy import K2hr3Policy
    from k2hr3client.role import K2hr3Role

    _MAX_LINE_LENGTH = 1024 * 8

    IDENTITY_V3_PASSWORD_AUTH_JSON_DATA = '''
    {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": "admin",
                        "domain": {
                            "name": "Default"
                        },
                        "password": "devstacker"
                    }
                } }
        }
    }
    '''

    IDENTITY_V3_TOKEN_AUTH_JSON_DATA = '''
    {
        "auth": {
            "identity": {
                "methods": [
                    "token"
                ],
                "token": {
                    "id": ""
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "id": "default"
                    },
                    "name": ""
                }
            }
        }
    }
    '''

    def get_scoped_token_id(url, user, password, project):
        # Get a scoped token id from openstack identity.
        # unscoped token-id
        # https://docs.openstack.org/api-ref/identity/v3/index.html#password-authentication-with-unscoped-authorization
        python_data = json.loads(IDENTITY_V3_PASSWORD_AUTH_JSON_DATA)
        python_data['auth']['identity']['password']['user']['name'] = user
        python_data['auth']['identity']['password']['user']['password'] = password
        headers = {
            'User-Agent': 'hiwkby-sample',
            'Content-Type': 'application/json'
        }
        req = urllib.request.Request(url,
                                     json.dumps(python_data).encode('ascii'),
                                     headers,
                                     method="POST")
        with urllib.request.urlopen(req) as res:
            unscoped_token_id = dict(res.info()).get('X-Subject-Token')
            print('unscoped_token_id:[{}]'.format(unscoped_token_id))

        # scoped token-id
        # https://docs.openstack.org/api-ref/identity/v3/index.html?expanded=#token-authentication-with-scoped-authorization
        python_data = json.loads(IDENTITY_V3_TOKEN_AUTH_JSON_DATA)
        python_data['auth']['identity']['token']['id'] = unscoped_token_id
        python_data['auth']['scope']['project']['name'] = project
        headers = {
            'User-Agent': 'hiwkby-sample',
            'Content-Type': 'application/json'
        }
        req = urllib.request.Request(url,
                                     json.dumps(python_data).encode('ascii'),
                                     headers,
                                     method="POST")
        with urllib.request.urlopen(req) as res:
            scoped_token_id = dict(res.info()).get('X-Subject-Token')
            print('scoped_token_id:[{}]'.format(scoped_token_id))
            return scoped_token_id


    def set_data(val: Path, projectname: str, clustername: str) -> str:
        # Set data.
        if val.exists() is False:
            raise K2hr3Exception(f'path must exist, not {val}')
        if val.is_file() is False:
            raise K2hr3Exception(
                f'path must be a regular file, not {val}')
        data = ""
        with val.open(encoding='utf-8') as f:  # pylint: disable=no-member
            line_len = 0
            for line in iter(f.readline, ''):
                # 3. replace TROVE_K2HDKC_CLUSTER_NAME with clustername
                line = re.sub('__TROVE_K2HDKC_CLUSTER_NAME__', clustername,
                              line)
                # 4. replace TROVE_K2HDKC_TENANT_NAME with projectname
                line = re.sub('__TROVE_K2HDKC_TENANT_NAME__', projectname,
                              line)
                line_len += len(line)
                if line_len > _MAX_LINE_LENGTH:
                    raise K2hr3Exception('data too big')
                data = "".join([data, line])  # type: ignore

        return data


    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='k2hr3 token api example')
        parser.add_argument(
            '--url',
            dest='url',
            default='http://127.0.0.1/identity/v3/auth/tokens',
            help='identity api url. ex) http://127.0.0.1/identity/v3/auth/tokens')  # noqa
        parser.add_argument('--user',
                            dest='user',
                            default='demo',
                            help='openstack user')
        parser.add_argument('--password',
                            dest='password',
                            default='password',
                            help='openstack user password')
        parser.add_argument('--project',
                            dest='project',
                            default='demo',
                            help='openstack project')
        parser.add_argument('--k2hr3_url',
                            dest='k2hr3_url',
                            default='http://localhost:18080',
                            help='k2hr3 api url')
        parser.add_argument('--resource',
                            dest='resource',
                            default='k2hdkccluster',
                            help='resource name')
        parser.add_argument('--resource_file',
                            dest='resource_file',
                            default=None,
                            help='resource file name')
        parser.add_argument('--policy',
                            dest='policy',
                            default='k2hdkccluster',
                            help='policy name')
        parser.add_argument('--role',
                            dest='role',
                            default='k2hdkccluster',
                            help='k2hr3 rolename')

        args = parser.parse_args()

        # 1. Gets a openstack token id from openstack identity server
        openstack_token = get_scoped_token_id(args.url, args.user, args.password,
                                              args.project)

        # 2. Gets a k2hr3 token from the openstack token
        k2hr3_token = K2hr3Token(args.project, openstack_token)
        http = K2hr3Http(args.k2hr3_url)
        http.POST(k2hr3_token.create())

        # 3. Makes a new k2hr3 resource
        k2hr3_resource = K2hr3Resource(k2hr3_token.token)
        resource_data = ""
        if args.resource_file:
            val = Path(args.resource_file)
            resource_data = set_data(val, projectname=args.project, clustername=args.resource)
        else:
            resource_data = args.resource

        http.POST(
            k2hr3_resource.create_conf_resource(
                name=args.resource,
                data_type='string',
                resource_data=resource_data,
                keys={
                    "cluster-name": args.resource,
                    "chmpx-server-port": "8020",
                    "chmpx-server-ctlport": "8021",
                    "chmpx-slave-ctlport": "8031"
                },
                alias=[]
            )
        )

        # 3.1. Makes a new k2hr3 resource for server
        k2hr3_resource_server = K2hr3Resource(k2hr3_token.token)
        http.POST(
            k2hr3_resource_server.create_conf_resource(
                name="/".join([args.resource, "server"]),
                data_type='string',
                resource_data="",
                keys={"chmpx-mode": "SERVER",
                      "k2hr3-init-packages": "",
                      "k2hr3-init-packagecloud-packages": "",
                      "k2hr3-init-systemd-packages": ""},
                alias=[]
            )
        )

        # 3.2. Makes a new k2hr3 resource for slave
        k2hr3_resource_slave = K2hr3Resource(k2hr3_token.token)
        http.POST(
            k2hr3_resource_slave.create_conf_resource(
                name="/".join([args.resource, "slave"]),
                data_type='string',
                resource_data="",
                keys={"chmpx-mode": "SLAVE",
                      "k2hr3-init-packages": "",
                      "k2hr3-init-packagecloud-packages": "",
                      "k2hr3-init-systemd-packages": "",
                      "k2hdkc-dbaas-add-user": 1},
                alias=[]
            )
        )

        # 4. Makes a new k2hr3 policy for the resource
        k2hr3_policy = K2hr3Policy(k2hr3_token.token)
        SERVER_RESOURCE_PATH = "yrn:yahoo:::{}:resource:{}/server".format(
            args.project, args.resource)
        SLAVE_RESOURCE_PATH = "yrn:yahoo:::{}:resource:{}/slave".format(
            args.project, args.resource)
        http.POST(
            k2hr3_policy.create(
                name=args.policy,
                effect='allow',
                action=['yrn:yahoo::::action:read'],
                resource=[SERVER_RESOURCE_PATH, SLAVE_RESOURCE_PATH],
                condition=None,
                alias=[]
            )
        )

        # 5. Makes a new k2hr3 role for the policy
        POLICY_PATH = "yrn:yahoo:::{}:policy:{}".format(args.project, args.policy)
        k2hr3_role = K2hr3Role(k2hr3_token.token)
        http.POST(
            k2hr3_role.create(
                name=args.role,
                policies=[POLICY_PATH],
                alias=[]
            )
        )
        server_role = K2hr3Role(k2hr3_token.token)
        http.POST(
            server_role.create(
                name="/".join([args.role, "server"]),
                policies=[],
                alias=[]
            )
        )
        slave_role = K2hr3Role(k2hr3_token.token)
        http.POST(
            slave_role.create(
                name="/".join([args.role, "slave"]),
                policies=[],
                alias=[]
            )
        )

        print(slave_role.resp.body)
        sys.exit(0)

"""

from enum import Enum
import json
import logging
from typing import List, Optional
import warnings


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

    def __init__(self, host: str, port: str, cuk: str, extra: str, tag: str,  # pylint: disable=R0917 # noqa
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
        self.name = None
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
    def create(self, name: str, policies: List[str], alias: List[str],
               role_name: Optional[str] = None):
        """Create tokens."""
        self.api_id = 1
        self.name = name  # type: ignore
        self.policies = policies  # type: ignore
        self.alias = alias  # type: ignore
        if name is None and role_name is not None:
            warnings.warn(
                "The 'role_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = role_name
        return self

    # POST(Add HOST to ROLE)
    # http(s)://API SERVER:PORT/v1/role/role path
    # http(s)://API SERVER:PORT/v1/role/yrn full path to role
    def add_member(self, name: str, host: str,  # pylint: disable=R0917
                   clear_hostname: bool, clear_ips: str,
                   role_name: Optional[str] = None):
        """Add a member to the role."""
        self.api_id = 3
        self.name = name  # type: ignore
        self.host = host  # type: ignore
        self.clear_hostname = clear_hostname  # type: ignore
        self.clear_ips = clear_ips  # type: ignore
        if name is None and role_name is not None:
            warnings.warn(
                "The 'role_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = role_name
        return self

    def add_members(self, name: str, hosts: str,  # pylint: disable=R0917
                    clear_hostname: bool, clear_ips: str,
                    role_name: Optional[str] = None):
        """Add members to the role."""
        self.api_id = 4
        self.name = name  # type: ignore
        self.hosts = hosts  # type: ignore
        self.clear_hostname = clear_hostname  # type: ignore
        self.clear_ips = clear_ips  # type: ignore
        if name is None and role_name is not None:
            warnings.warn(
                "The 'role_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = role_name
        return self

    # PUT(Add HOST to ROLE)
    # http(s)://API SERVER:PORT/v1/role/role path?urlarg
    # http(s)://API SERVER:PORT/v1/role/yrn full path to role?urlarg
    def add_member_with_roletoken(self, name: str, port: str, cuk: str,  # pylint: disable=R0917 # noqa
                                  extra: str, tag: str,
                                  inboundip: str, outboundip: str,
                                  role_name: Optional[str] = None):
        """Add members to the role without roletoken."""
        self.api_id = 5
        self.name = name  # type: ignore
        self.port = port  # type: ignore
        self.cuk = cuk  # type: ignore
        self.extra = extra  # type: ignore
        self.tag = tag  # type: ignore
        self.inboundip = inboundip  # type: ignore
        self.outboundip = outboundip  # type: ignore
        if name is None and role_name is not None:
            warnings.warn(
                "The 'role_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = role_name
        return self

    # GET(Create ROLE Token)
    # TODO(hiwakaba)

    # GET(Show ROLE details)
    # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path?urlarg
    def get(self, name: str, expand: bool = True,
            role_name: Optional[str] = None):
        """Show role details."""
        self.api_id = 6
        self.name = name  # type: ignore
        self.expand = expand  # type: ignore
        if name is None and role_name is not None:
            warnings.warn(
                "The 'role_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = role_name
        return self

    # GET (Role Token List)
    # http(s)://APISERVER:PORT/v1/role/token/list/role path or yrn full role path # noqa
    def get_token_list(self, name: str, expand: bool = True,
                       role_name: Optional[str] = None):
        """Show token list."""
        self.api_id = 7
        self.name = name  # type: ignore
        self.expand = expand  # type: ignore
        if name is None and role_name is not None:
            warnings.warn(
                "The 'role_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = role_name
        return self

    # HEAD(Validate ROLE)
    # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path
    def validate_role(self, name: str, role_name: Optional[str] = None):
        """Validate role."""
        self.api_id = 8
        self.name = name  # type: ignore
        if name is None and role_name is not None:
            warnings.warn(
                "The 'role_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = role_name
        return self

    # DELETE(Delete ROLE)
    # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path?urlarg
    def delete(self, name: str, role_name: Optional[str] = None):
        """Delete role."""
        self.api_id = 9
        self.name = name  # type: ignore
        if name is None and role_name is not None:
            warnings.warn(
                "The 'role_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = role_name
        return self

    # DELETE(Hostname/IP address deletion-role specification)
    # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path
    def delete_member(self, name: str, host: str, port: str, cuk: str,  # pylint: disable=R0917 # noqa
                      role_name: Optional[str] = None):
        """Delete host."""
        self.api_id = 10
        self.name = name  # type: ignore
        self.host = host  # type: ignore
        self.port = port  # type: ignore
        self.cuk = cuk  # type: ignore
        if name is None and role_name is not None:
            warnings.warn(
                "The 'role_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = role_name
        return self

    # DELETE(Hostname/IP address deletion - Role not specified)
    def delete_member_wo_roletoken(self, cuk: str):
        """Delete host without roletoken."""
        self.api_id = 11
        self.cuk = cuk  # type: ignore
        return self

    # DELETE (RoleToken deletion - Role specified)
    # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path
    def delete_roletoken(self, name: str, port: str, cuk: str,
                         role_name: Optional[str] = None):
        """Delete roletoken."""
        self.api_id = 12
        self.name = name  # type: ignore
        self.port = port  # type: ignore
        self.cuk = cuk  # type: ignore
        if name is None and role_name is not None:
            warnings.warn(
                "The 'role_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = role_name
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
                python_data['role']['name'] = self.name
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
                return f'{self.version}/{self.basepath}/{self.name}'
            # elif (self.api_id == 4):
            #     python_data = json.loads(_ROLE_API_ADD_MEMBERS)
            #     # TODO(hiwakaba) Not implemented
            #     self.body = json.dumps(python_data)
            #     # http(s)://API SERVER:PORT/v1/role/role path
            #     return f'{self.basepath}/{self.name}'
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
                return f'{self.version}/{self.basepath}/{self.name}'
        if method == K2hr3HTTPMethod.PUT:
            if self.api_id == 1:
                self.urlparams = json.dumps({
                    'name': self.name,
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
                return f'{self.version}/{self.basepath}/{self.name}'
            if self.api_id == 4:
                # TODO(hiwakaba) Not implemented
                self.urlparams = json.dumps({
                })
                # http(s)://API SERVER:PORT/v1/role/role path
                return f'{self.version}/{self.basepath}/{self.name}'
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
                return f'{self.version}/{self.basepath}/{self.name}'
        if method == K2hr3HTTPMethod.GET:
            if self.api_id == 6:
                self.urlparams = json.dumps({
                    'expand': self.expand
                })
                # GET(Show ROLE details)
                # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path?urlarg # noqa
                return f'{self.version}/{self.basepath}/{self.name}'
            if self.api_id == 7:
                self.urlparams = json.dumps({
                    'expand': self.expand
                })
                # http(s)://APISERVER:PORT/v1/role/token/list/role path or yrn full role path # noqa
                return f'{self.version}/{self.basepath}/token/list/' \
                       f'{self.name}'

        if method == K2hr3HTTPMethod.HEAD:
            if self.api_id == 8:
                # HEAD(Validate ROLE)
                # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path # noqa
                return f'{self.version}/{self.basepath}/{self.name}'

        if method == K2hr3HTTPMethod.DELETE:
            if self.api_id == 9:
                # DELETE(Delete ROLE)
                # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path?urlarg # noqa
                return f'{self.version}/{self.basepath}/{self.name}'
            if self.api_id == 10:
                # DELETE(Hostname/IP address deletion-role specification)
                # http(s)://API SERVER:PORT/v1/role/role path or yrn full role path # noqa
                self.urlparams = json.dumps({
                    'host': self.host,
                    'port': self.port,
                    'cuk': self.cuk
                })
                return f'{self.version}/{self.basepath}/{self.name}'
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
                return f'{self.version}/{self.basepath}/{self.name}'
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
