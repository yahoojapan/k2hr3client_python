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
"""K2HR3 Python Client of Resource API."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import argparse
import json
import os
import sys
from pathlib import Path
import urllib.parse
import urllib.request

here = os.path.dirname(__file__)
src_dir = os.path.join(here, '..')
if os.path.exists(src_dir):
    sys.path.append(src_dir)

import k2hr3client # type: ignore # pylint: disable=import-error, wrong-import-position # noqa
from k2hr3client.http import K2hr3Http  # type: ignore # pylint: disable=import-error, wrong-import-position # noqa
from k2hr3client.token import K2hr3Token  # type: ignore # pylint: disable=import-error, wrong-import-position # noqa
from k2hr3client.resource import K2hr3Resource  # type: ignore # pylint: disable=import-error, wrong-import-position # noqa
from k2hr3client.policy import K2hr3Policy  # type: ignore # pylint: disable=import-error, wrong-import-position # noqa
from k2hr3client.role import K2hr3Role  # type: ignore # pylint: disable=import-error, wrong-import-position # noqa

IDENTITY_V3_PASSWORD_AUTH_JSON_DATA = """
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
"""

IDENTITY_V3_TOKEN_AUTH_JSON_DATA = """
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
"""


def get_scoped_token_id(url, user, password, project):
    """Get a scoped token id from openstack identity."""
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='k2hr3 token api example')
    parser.add_argument(
        '--url',
        dest='url',
        default='http://127.0.0.1/identity/v3/auth/tokens',
        help='identity api url. ex) http://127.0.0.1/identity/v3/auth/tokens')
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
    init_py = Path(k2hr3client.__file__)
    txt_file = init_py.parent.joinpath('examples',
                                       'example_resource.txt')
    http.POST(
        k2hr3_resource.create_conf_resource(
            name=args.resource,
            data_type='string',
            data=Path(txt_file),
            tenant=args.project,
            cluster_name=args.resource,
            keys={
                "cluster-name": args.resource,
                "chmpx-server-port": "8020",
                "chmpx-server-ctlport": "8021",
                "chmpx-slave-ctlport": "8031"
            },
            alias=[]
        )
    )

    # debug
    # print(k2hr3_resource.resp.body)
    # sys.exit(0)

    # 3.1. Makes a new k2hr3 resource for server
    k2hr3_resource_server = K2hr3Resource(k2hr3_token.token)
    http.POST(
        k2hr3_resource_server.create_conf_resource(
            tenant=args.project,
            cluster_name=args.resource,
            name="/".join([args.resource, "server"]),
            data_type='string',
            data="",
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
            tenant=args.project,
            cluster_name=args.resource,
            name="/".join([args.resource, "slave"]),
            data_type='string',
            data="",
            keys={"chmpx-mode": "SLAVE",
                  "k2hr3-init-packages": "",
                  "k2hr3-init-packagecloud-packages": "",
                  "k2hr3-init-systemd-packages": "",
                  "k2hdkc-dbaas-add-user": 1},
            alias=[]
        )
    )

    # debug
    # print(k2hr3_resource_slave.resp.body)
    # sys.exit(0)

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

    # debug
    # print(k2hr3_policy.resp.body)
    # sys.exit(0)

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

    # debug
    # print(slave_role.resp.body)
    # sys.exit(0)

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
