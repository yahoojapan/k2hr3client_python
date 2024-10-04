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
from k2hr3client import token as ktoken

LOG = logging.getLogger(__name__)


class TestK2hr3token(unittest.TestCase):
    """Tests the K2hr3token class.

    Simple usage(this class only):
    $ python -m unittest tests/test_token.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        self.iaas_project = "my_project"
        self.iaas_token = "my_iaas_token"
        self.r3token = "my_r3_token"
        self.role = "my_role"
        self.expire = 0
        self.expand = True

    def tearDown(self):
        """Tears down a test case."""

    def test_k2hr3token_construct(self):
        """Creates a K2hr3Token instance."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        self.assertIsInstance(mytoken, ktoken.K2hr3Token)

    def test_k2hr3token_repr(self):
        """Represent a K2hr3Token instance."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        # Note: The order of _error and _code is unknown!
        self.assertRegex(repr(mytoken), '<K2hr3Token .*>')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_token_create_using_post(self, mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        self.assertEqual(mytoken.iaas_project, self.iaas_project)
        self.assertEqual(mytoken.iaas_token, self.iaas_token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.iaas_token}'
        }
        self.assertEqual(mytoken.headers, headers)
        mytoken.create()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(mytoken))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/user/tokens")
        # 2. assert URL params
        self.assertEqual(mytoken.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.iaas_token}'
        }
        self.assertEqual(mytoken.headers, headers)
        # 4. assert Request body
        python_data = json.loads(ktoken._TOKEN_API_CREATE_TOKEN_TYPE2)
        python_data['auth']['tenantName'] = self.iaas_project
        body = json.dumps(python_data)
        self.assertEqual(mytoken.body, body)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_token_create_using_put(self, mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        self.assertEqual(mytoken.iaas_project, self.iaas_project)
        self.assertEqual(mytoken.iaas_token, self.iaas_token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.iaas_token}'
        }
        self.assertEqual(mytoken.headers, headers)
        mytoken.create()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(mytoken))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/user/tokens")
        # 2. assert URL params
        s_s_urlparams = {'tenantname': self.iaas_project}
        self.assertEqual(mytoken.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.iaas_token}'
        }
        self.assertEqual(mytoken.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytoken.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_token_show_credential_details_using_get(
            self, mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        self.assertEqual(mytoken.iaas_project, self.iaas_project)
        self.assertEqual(mytoken.iaas_token, self.iaas_token)
        mytoken.show()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(mytoken))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/user/tokens")
        # 2. assert URL params
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.iaas_token}'
        }
        self.assertEqual(mytoken.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytoken.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_validate(self, mock_HTTP_REQUEST_METHOD):
        mytoken = ktoken.K2hr3Token(self.iaas_project, self.iaas_token)
        """Get root path."""
        self.assertEqual(mytoken.iaas_project, self.iaas_project)
        self.assertEqual(mytoken.iaas_token, self.iaas_token)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': f'U={self.iaas_token}'
        }
        self.assertEqual(mytoken.headers, headers)

        mytoken.validate()

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.HEAD(mytoken))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/user/tokens")
        # 2. assert URL params
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        self.assertEqual(mytoken.headers, headers)
        # 4. assert Request body
        self.assertEqual(mytoken.body, None)


#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
