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
from k2hr3client import resource as kresource

LOG = logging.getLogger(__name__)


class TestK2hr3Resource(unittest.TestCase):
    """Tests the K2hr3Resource class.

    Simple usage(this class only):
    $ python -m unittest tests/test_resource.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        self.resource_path = "test_resource_path"
        self.name = "test_resource"
        self.data_type = 'string'
        self.resource_data = "testresourcedata"
        self.keys = {
            "cluster-name": "testcluster",
            "chmpx-server-port": "8020",
            "chmpx-server-ctrlport": "8021",
            "chmpx-slave-ctrlport": "8031"
        }
        self.expand = True
        self.service = 'test_service'
        self.alias = []

        self.port = 3000
        self.cuk = "testcuk"
        self.role = "testrole"
        self.data_type = "test_datatype"

    def tearDown(self):
        """Tears down a test case."""

    def test_k2hr3resource_construct(self):
        """Creates a K2hr3Resoiurce  instance."""
        resource = kresource.K2hr3Resource("token")
        self.assertIsInstance(resource, kresource.K2hr3Resource)

    def test_k2hr3resource_repr(self):
        """Represent a K2hr3Resource instance."""
        resource = kresource.K2hr3Resource("token")
        # Note: The order of _error and _code is unknown!
        self.assertRegex(repr(resource), '<K2hr3Resource .*>')

    #
    # TestCases using PUT Requests
    #
    # PUT
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/yrn full resource path?urlarg
    #
    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_resource_create_resource_using_put(self,
                                                mock_HTTP_REQUEST_METHOD):
        myresource = kresource.K2hr3Resource("token")
        self.assertEqual(myresource.r3token, "token")
        """ root path."""
        myresource.create_conf_resource(
            name = self.name,
            data_type = self.data_type,
            resource_data = self.resource_data,
            keys = self.keys,
            alias = self.alias)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(myresource))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/resource")
        # 2. assert URL params
        s_s_urlparams = {
            'name': self.name,
            'type': self.data_type,
            'data': self.resource_data,
            'keys': self.keys,
            'alias': self.alias
        }
        self.assertEqual(myresource.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myresource.headers, headers)
        # 4. assert Request body
        self.assertEqual(myresource.body, None)

    #
    # TestCases using GET Requests
    #
    # GET
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/yrn full resource path?urlarg
    #
    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_resource_get_resource_using_get(self, mock_HTTP_REQUEST_METHOD):
        myresource = kresource.K2hr3Resource("token",
                                             resource_path=self.resource_path)
        self.assertEqual(myresource.r3token, "token")
        """Get root path."""
        myresource.get(self.expand, self.service)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(myresource))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/resource/{self.resource_path}") # noqa
        # 2. assert URL params
        s_s_urlparams = {
            'expand': self.expand,
            'service': self.service
        }
        self.assertEqual(myresource.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myresource.headers, headers)
        # 4. assert Request body
        self.assertEqual(myresource.body, None)

    #
    # TestCases using GET Requests
    #
    # GET
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/yrn full resource path?urlarg
    #
    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_resource_get_resource_with_roletoken_using_get(
            self, mock_HTTP_REQUEST_METHOD):
        myresource = kresource.K2hr3Resource(roletoken="token",
                                             resource_path=self.resource_path)
        self.assertEqual(myresource.roletoken, "token")
        """Get root path."""
        myresource.get_with_roletoken(self.data_type, self.keys, self.service)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(myresource))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/resource/{self.resource_path}") # noqa
        # 2. assert URL params
        s_s_urlparams = {
            'type': self.data_type,
            'keys': self.keys,
            'service': self.service
        }
        self.assertEqual(myresource.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'R=token'
        }
        self.assertEqual(myresource.headers, headers)
        # 4. assert Request body
        self.assertEqual(myresource.body, None)

    #
    # TestCases using HEAD Requests
    #
    # HEAD
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/resource path or yrn full resource path?urlarg # noqa
    # http(s)://API SERVER:PORT/v1/resource/yrn full resource path?urlarg
    #
    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_resource_validate_resource_using_head(self,
                                                   mock_HTTP_REQUEST_METHOD):
        myresource = kresource.K2hr3Resource("token",
                                             resource_path=self.resource_path)
        """Get root path."""
        self.assertEqual(myresource.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myresource.headers, headers)
        myresource.validate(self.data_type, self.keys, self.service)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.HEAD(myresource))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/resource/{self.resource_path}") # noqa
        # 2. assert URL params
        s_s_urlparams = {
            'type': self.data_type,
            'keys': self.keys,
            'service': self.service
        }
        self.assertEqual(myresource.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(myresource.headers, headers)
        # 4. assert Request body
        self.assertEqual(myresource.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_resource_validate_resource_without_token_using_head(
            self, mock_HTTP_REQUEST_METHOD):
        myresource = kresource.K2hr3Resource(resource_path=self.resource_path)
        """Get root path."""
        self.assertEqual(myresource.r3token, None)
        headers = {
            'Content-Type': 'application/json',
        }
        self.assertEqual(myresource.headers, headers)
        myresource.validate_with_notoken(
            self.port,
            self.cuk,
            self.role,
            self.data_type,
            self.keys,
            self.service)
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.HEAD(myresource))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/resource/{self.resource_path}") # noqa
        # 2. assert URL params
        s_s_urlparams = {
            'port': self.port,
            'cuk': self.cuk,
            'role': self.role,
            'type': self.data_type,
            'keys': self.keys,
            'service': self.service
        }
        self.assertEqual(myresource.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
        }
        self.assertEqual(myresource.headers, headers)
        # 4. assert Request body
        self.assertEqual(myresource.body, None)

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
