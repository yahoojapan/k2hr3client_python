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
from k2hr3client import acr as kacr

LOG = logging.getLogger(__name__)


class TestK2hr3Acr(unittest.TestCase):
    """Tests the K2hr3ApiResponse class.

    Simple usage(this class only):
    $ python -m unittest tests/test_acr.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        self.service = "testservicez"
        self.newtenant = "newtenant"

    def tearDown(self):
        """Tears down a test case."""

    def test_acr_construct(self):
        """Creates a K2hr3ApiResponse instance."""
        acr = kacr.K2hr3Acr("token", service=self.service)
        self.assertIsInstance(acr, kacr.K2hr3Acr)

    def test_acr_repr(self):
        """Represent a K2hr3ApiResponse instance."""
        myacr = kacr.K2hr3Acr("token", self.service)
        # Note: The order of _error and _code is unknown!
        self.assertRegex(repr(myacr), '<K2hr3Acr .*>')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_acr_add_member_using_post(self, mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        myacr = kacr.K2hr3Acr("token", self.service)
        self.assertEqual(myacr.r3token, "token")
        self.assertEqual(myacr.service, self.service)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myacr.headers, headers)
        myacr.add_member(self.newtenant)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(myacr))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/acr/{self.service}")
        # 2. assert URL params
        self.assertEqual(myacr.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myacr.headers, headers)
        # 4. assert Request body
        python_data = json.loads(kacr._ACR_API_ADD_MEMBER)
        python_data['tenant'] = self.newtenant
        body = json.dumps(python_data)
        self.assertEqual(myacr.body, body)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_acr_add_member_using_put(self, mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        myacr = kacr.K2hr3Acr("token", self.service)
        self.assertEqual(myacr.r3token, "token")
        self.assertEqual(myacr.service, self.service)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myacr.headers, headers)
        myacr.add_member(self.newtenant)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(myacr))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/acr/{self.service}")
        # 2. assert URL params
        s_s_urlparams = {'tenant': self.newtenant}
        self.assertEqual(myacr.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myacr.headers, headers)
        # 4. assert Request body
        self.assertEqual(myacr.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_acr_show_credential_details_using_get(self,
                                                   mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        myacr = kacr.K2hr3Acr("token", self.service)
        self.assertEqual(myacr.r3token, "token")
        self.assertEqual(myacr.service, self.service)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myacr.headers, headers)
        myacr.show_credential_details()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(myacr))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/acr/{self.service}")
        # 2. assert URL params
        self.assertEqual(myacr.urlparams, None)
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myacr.headers, headers)
        # 4. assert Request body
        self.assertEqual(myacr.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_acr_get_available_resources_using_get(self,
                                                   mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        myacr = kacr.K2hr3Acr("token", self.service)
        self.assertEqual(myacr.r3token, "token")
        self.assertEqual(myacr.service, self.service)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myacr.headers, headers)
        s_s_urlparams = {
            'cip': 'mycip',
            'cport': 'mycport',
            'crole': 'mycrole',
            'ccuk': 'myccuk',
            'sport': 'mysport',
            'srole': 'mysrole',
            'scuk': 'myscuk',
        }
        myacr.get_available_resources(
            s_s_urlparams['cip'],
            s_s_urlparams['cport'],
            s_s_urlparams['crole'],
            s_s_urlparams['ccuk'],
            s_s_urlparams['sport'],
            s_s_urlparams['srole'],
            s_s_urlparams['scuk'])
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(myacr))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/acr/{self.service}")
        # 2. assert URL params
        self.assertEqual(myacr.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myacr.headers, headers)
        # 4. assert Request body
        self.assertEqual(myacr.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_acr_delete_member_using_get(self, mock_HTTP_REQUEST_METHOD):
        myacr = kacr.K2hr3Acr("token", self.service)
        self.assertEqual(myacr.r3token, "token")
        self.assertEqual(myacr.service, self.service)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myacr.headers, headers)
        myacr.delete_member(self.newtenant)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.DELETE(myacr))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/acr/{self.service}")
        # 2. assert URL params
        s_s_urlparams = {'tenant': self.newtenant}
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(myacr.urlparams, json.dumps(s_s_urlparams))
        self.assertEqual(httpreq.urlparams, s_urlparams)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myacr.headers, headers)
        # 4. assert Request body
        self.assertEqual(myacr.body, None)


#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
