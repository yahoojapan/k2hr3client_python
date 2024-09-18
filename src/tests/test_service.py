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
"""Test Package for K2hr3 Python Client."""

import json
import logging
import unittest
from unittest.mock import patch
import urllib.parse

from k2hr3client import http as khttp
from k2hr3client import service as kservice

LOG = logging.getLogger(__name__)


class TestK2hr3Service(unittest.TestCase):
    """Tests the K2hr3Service class.

    Simple usage(this class only):
    $ python -m unittest tests/test_service.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        self.name = "testservice"
        self.verify = '[{"name":"testresource2","type":"string","data":"testresource_str2","keys":{}}]' # noqa

    def tearDown(self):
        """Tears down a test case."""

    def test_k2hr3role_construct(self):
        """Creates a K2hr3Service  instance."""
        myservice = kservice.K2hr3Service("token", self.name)
        self.assertIsInstance(myservice, kservice.K2hr3Service)

    def test_k2hr3role_repr(self):
        """Represent a K2hr3Service instance."""
        myservice = kservice.K2hr3Service("token", self.name)
        self.assertRegex(repr(myservice), '<K2hr3Service .*>')

    #
    # TestCases using POST Requests
    #
    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_service_create_service_using_post(self, mock_HTTP_REQUEST_METHOD):
        myservice = kservice.K2hr3Service("token", service_name=self.name)
        """Get root path."""
        self.assertEqual(myservice.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        verify = '[{"name":"testresource2","type":"string","data":"testresource_str2","keys":{}}]' # noqa
        myservice.create(verify_url=verify)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(myservice))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/service")
        # 2. assert URL params
        self.assertEqual(myservice.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        # 4. assert Request body
        python_data = json.loads(kservice._SERVICE_API_CREATE_SERVICE)
        python_data['name'] = self.name
        python_data['verify'] = self.verify
        body = json.dumps(python_data)
        self.assertEqual(myservice.body, body)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_service_add_member_using_post(self, mock_HTTP_REQUEST_METHOD):
        myservice = kservice.K2hr3Service("token", service_name=self.name)
        """Get root path."""
        tenant = "mytenant"
        clear_tenant = False
        myservice.add_member(tenant=tenant, clear_tenant=clear_tenant)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(myservice))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/service")
        # 2. assert URL params
        self.assertEqual(myservice.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        # 4. assert Request body
        python_data = json.loads(kservice._SERVICE_API_ADD_MEMBER)
        python_data['tenant'] = tenant
        python_data['clear_tenant'] = False
        body = json.dumps(python_data)
        self.assertEqual(myservice.body, body)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_service_modify_using_post(self, mock_HTTP_REQUEST_METHOD):
        myservice = kservice.K2hr3Service("token",service_name=self.name)
        """Get root path."""
        self.assertEqual(myservice.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        verify = '[{"name":"testresource2","type":"string","data":"testresource_str2","keys":{}}]' # noqa
        myservice.modify(verify)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(myservice))
        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/service")
        # 2. assert URL params
        self.assertEqual(myservice.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        # 4. assert Request body
        python_data = json.loads(kservice._SERVICE_API_MODIFY_VERIFY)
        python_data['verify'] = self.verify
        body = json.dumps(python_data)
        self.assertEqual(myservice.body, body)

    #
    # TestCases using PUT Requests
    #
    # Create SERVICE
    # 	PUT	http(s)://API SERVER:PORT/v1/service?name=service name&verify=verify url # noqa
    #
    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_service_create_service_using_put(self, mock_HTTP_REQUEST_METHOD):
        myservice = kservice.K2hr3Service("token",service_name=self.name)
        """Get root path."""
        self.assertEqual(myservice.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        verify = '[{"name":"testresource2","type":"string","data":"testresource_str2","keys":{}}]' # noqa
        myservice.create(verify_url=verify)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(myservice))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/service")
        # 2. assert URL params
        s_s_urlparams = {
            'name': self.name,
            'verify': verify
        }
        self.assertEqual(myservice.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        # 4. assert Request body
        self.assertEqual(myservice.body, None)

    #
    # TestCases using PUT Requests
    #
    # Add MEMBER to SERVICE
    # 	PUT	http(s)://API SERVER:PORT/v1/service/service name?tenant=tenant name
    #
    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_service_add_member_using_put(self, mock_HTTP_REQUEST_METHOD):
        myservice = kservice.K2hr3Service("token",service_name=self.name)
        """Get root path."""
        self.assertEqual(myservice.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        tenant = "mytenant"
        clear_tenant = False
        myservice.add_member(tenant=tenant, clear_tenant=clear_tenant)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(myservice))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/service")
        # 2. assert URL params
        s_s_urlparams = {
            'tenant': tenant,
            'clear_tenant': clear_tenant
        }
        self.assertEqual(myservice.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        # 4. assert Request body
        self.assertEqual(myservice.body, None)

    #
    # TestCases using PUT Requests
    #
    # Modify VERIFY URL
    # 	PUT http(s)://API SERVER:PORT/v1/service?name=service name&verify=verify url # noqa
    #
    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_service_modify_using_put(self, mock_HTTP_REQUEST_METHOD):
        myservice = kservice.K2hr3Service("token",service_name=self.name)
        """Get root path."""
        self.assertEqual(myservice.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        verify = '[{"name":"testresource2","type":"string","data":"testresource_str2","keys":{}}]' # noqa
        myservice.modify(verify_url=verify)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(myservice))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/service")
        # 2. assert URL params
        s_s_urlparams = {
            'verify': verify
        }
        self.assertEqual(myservice.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        # 4. assert Request body
        self.assertEqual(myservice.body, None)

    #
    # TestCases using PUT Requests
    #
    # GET	http(s)://API SERVER:PORT/v1/service/service name
    #
    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_service_get_service_using_get(self, mock_HTTP_REQUEST_METHOD):
        myservice = kservice.K2hr3Service("token",service_name=self.name)
        """Get root path."""
        self.assertEqual(myservice.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        myservice.get()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(myservice))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/service/{self.name}")  # noqa
        # 2. assert URL params
        self.assertEqual(myservice.urlparams, None)
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        # 4. assert Request body
        self.assertEqual(myservice.body, None)

    #
    # TestCases using PUT Requests
    #
    # HEAD	http(s)://API SERVER:PORT/v1/service/service name http(s)://API SERVER:PORT/v1/service/service name?urlarg # noqa
    #
    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_service_validate_service_using_head(self,
                                                 mock_HTTP_REQUEST_METHOD):
        myservice = kservice.K2hr3Service("token",service_name=self.name)
        """Get root path."""
        self.assertEqual(myservice.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        myservice.validate()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.HEAD(myservice))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/service/{self.name}")  # noqa
        # 2. assert URL params
        self.assertEqual(myservice.urlparams, None)
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        # 4. assert Request body
        self.assertEqual(myservice.body, None)

    #
    # TestCases using PUT Requests
    #
    # DELETE	http(s)://API SERVER:PORT/v1/service/service name http(s)://API SERVER:PORT/v1/service/service name?urlarg # noqa
    #
    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_service_delete_service_using_delete(self,
                                                 mock_HTTP_REQUEST_METHOD):
        myservice = kservice.K2hr3Service("token",service_name=self.name)
        """Get root path."""
        self.assertEqual(myservice.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        myservice.delete()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.DELETE(myservice))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/service/{self.name}")  # noqa
        # 2. assert URL params
        self.assertEqual(myservice.urlparams, None)
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        # 4. assert Request body
        self.assertEqual(myservice.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_service_delete_service_using_delete_tenant(
            self, mock_HTTP_REQUEST_METHOD):
        myservice = kservice.K2hr3Service("token",service_name=self.name)
        """Get root path."""
        self.assertEqual(myservice.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        tenant = "mytenant"
        myservice.delete_tenant(tenant)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.DELETE(myservice))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/service/{self.name}")  # noqa
        # 2. assert URL params
        s_s_urlparams = {
            'tenant': tenant
        }
        self.assertEqual(myservice.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myservice.headers, headers)
        # 4. assert Request body
        self.assertEqual(myservice.body, None)

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
