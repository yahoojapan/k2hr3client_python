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
"""Test Package for K2hr3 Python Client."""
import json
import logging
import unittest
from unittest.mock import patch
import urllib.parse

from k2hr3client import http as khttp
from k2hr3client import tenant as ktenant

LOG = logging.getLogger(__name__)


class TestK2hr3Tenant(unittest.TestCase):
    """Tests the K2hr3Tenant class.

    Simple usage(this class only):
    $ python -m unittest tests/test_tenant.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        self.token = "token"
        self.tenant_name = "testtenant"
        self.tenant_id = "123"
        self.users = ["demo"]
        self.desc = "test description"
        self.display = "Demone"

    def tearDown(self):
        """Tears down a test case."""

    def test_tenant_construct(self):
        """Creates a K2hr3Tenant  instance."""
        mytenant = ktenant.K2hr3Tenant(self.token)
        self.assertIsInstance(mytenant, ktenant.K2hr3Tenant)

    def test_tenant_repr(self):
        """Represent a K2hr3Tenant instance."""
        mytenant = ktenant.K2hr3Tenant(self.token)
        self.assertRegex(repr(mytenant), '<K2hr3Tenant .*>')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_tenant_create_tenant_using_post(self, mock_HTTP_REQUEST_METHOD):
        mytenant = ktenant.K2hr3Tenant(self.token)
        """Get root path."""
        self.assertEqual(mytenant.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        mytenant.create(
            self.tenant_name, self.users, self.desc, self.display)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(mytenant))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/tenant")
        # 2. assert URL params
        self.assertEqual(mytenant.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        # 4. assert Request body
        import json
        python_data = json.loads(ktenant._TENANT_API_CREATE_TENANT)
        python_data['tenant']['name'] = self.tenant_name
        python_data['tenant']['desc'] = self.desc
        python_data['tenant']['display'] = self.display
        python_data['tenant']['users'] = self.users
        body = json.dumps(python_data)
        self.assertEqual(mytenant.body, body)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_tenant_create_tenant_using_put(self, mock_HTTP_REQUEST_METHOD):
        mytenant = ktenant.K2hr3Tenant(self.token)
        """Get root path."""
        self.assertEqual(mytenant.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        mytenant.create(
            self.tenant_name, self.users, self.desc, self.display)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(mytenant))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/tenant")
        # 2. assert URL params
        s_s_urlparams = {
            'name': self.tenant_name,
            'users': self.users,
            'desc': self.desc,
            'display': self.display,
        }
        self.assertEqual(mytenant.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytenant.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_tenant_modify_tenant_using_post(self, mock_HTTP_REQUEST_METHOD):
        mytenant = ktenant.K2hr3Tenant(self.token)
        """Get root path."""
        self.assertEqual(mytenant.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        mytenant.modify(self.tenant_name, self.tenant_id, self.users,
                        self.desc, self.display)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(mytenant))

        # 1. assert URL
        self.assertEqual(httpreq.url,
                         f"{self.base_url}/v1/tenant/{self.tenant_name}")
        # 2. assert URL params
        self.assertEqual(mytenant.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        # 4. assert Request body
        import json
        python_data = json.loads(ktenant._TENANT_API_UPDATE_TENANT)
        python_data['tenant']['id'] = self.tenant_id
        python_data['tenant']['desc'] = self.desc
        python_data['tenant']['display'] = self.display
        python_data['tenant']['users'] = self.users
        body = json.dumps(python_data)
        self.assertEqual(mytenant.body, body)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_tenant_modify_tenant_using_put(self, mock_HTTP_REQUEST_METHOD):
        mytenant = ktenant.K2hr3Tenant(self.token)
        """Get root path."""
        self.assertEqual(mytenant.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        mytenant.modify(self.tenant_name, self.tenant_id, self.users,
                        self.desc, self.display)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(mytenant))

        # 1. assert URL
        self.assertEqual(httpreq.url,
                         f"{self.base_url}/v1/tenant/{self.tenant_name}")
        # 2. assert URL params
        s_s_urlparams = {
            'id': self.tenant_id,
            'users': self.users,
            'desc': self.desc,
            'display': self.display,
        }
        self.assertEqual(mytenant.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytenant.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_tenant_get_tenant_list(self, mock_HTTP_REQUEST_METHOD):
        mytenant = ktenant.K2hr3Tenant(self.token)
        """Get root path."""
        self.assertEqual(mytenant.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        mytenant.get_tenant_list()

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(mytenant))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/tenant")
        # 2. assert URL params
        s_s_urlparams = {
            'expand': False
        }
        self.assertEqual(mytenant.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytenant.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_tenant_get_tenant(self, mock_HTTP_REQUEST_METHOD):
        mytenant = ktenant.K2hr3Tenant(self.token)
        """Get root path."""
        self.assertEqual(mytenant.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        mytenant.get(self.tenant_name)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(mytenant))

        # 1. assert URL
        self.assertEqual(httpreq.url,
                         f"{self.base_url}/v1/tenant/{self.tenant_name}")
        # 2. assert URL params
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytenant.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_tenant_validate_using_head(self, mock_HTTP_REQUEST_METHOD):
        mytenant = ktenant.K2hr3Tenant(self.token)
        """Get root path."""
        self.assertEqual(mytenant.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        mytenant.validate(self.tenant_name)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.HEAD(mytenant))

        # 1. assert URL
        self.assertEqual(httpreq.url,
                         f"{self.base_url}/v1/tenant/{self.tenant_name}")
        # 2. assert URL params
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytenant.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_tenant_delete_using_delete(self, mock_HTTP_REQUEST_METHOD):
        mytenant = ktenant.K2hr3Tenant(self.token)
        """Get root path."""
        self.assertEqual(mytenant.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        mytenant.delete(self.tenant_name, self.tenant_id)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.DELETE(mytenant))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/tenant")
        # 2. assert URL params
        s_s_urlparams = {
            'tenant': self.tenant_name,
            'id': self.tenant_id
        }
        self.assertEqual(mytenant.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytenant.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_tenant_delete_user(self, mock_HTTP_REQUEST_METHOD):
        mytenant = ktenant.K2hr3Tenant(self.token)
        """Get root path."""
        self.assertEqual(mytenant.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        mytenant.delete_user(self.tenant_name, self.tenant_id)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.DELETE(mytenant))

        # 1. assert URL
        self.assertEqual(httpreq.url,
                         f"{self.base_url}/v1/tenant/{self.tenant_name}")
        # 2. assert URL params
        s_s_urlparams = {
            'id': self.tenant_id
        }
        self.assertEqual(mytenant.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mytenant.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytenant.body, None)

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
