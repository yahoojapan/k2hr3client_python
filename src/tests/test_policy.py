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
from k2hr3client import policy as kpolicy

LOG = logging.getLogger(__name__)


class TestK2hr3Policy(unittest.TestCase):
    """Tests the K2hr3Policy class.

    Simple usage(this class only):
    $ python -m unittest tests/test_resource.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        RESOURCE_PATH = "yrn:yahoo:::demo:resource:my_resource"
        self.token = "token"
        self.service = "testservice"
        self.policy_name = "testpolicy"
        self.tenant = "demo"
        self.effect = 'allow'
        self.action = ['yrn:yahoo::::action:read']
        self.resource = [RESOURCE_PATH]
        self.condition = None
        self.alias = []

    def tearDown(self):
        """Tears down a test case."""

    def test_policy_construct(self):
        """Creates a K2hr3Policy  instance."""
        mypolicy = kpolicy.K2hr3Policy(self.token)
        self.assertIsInstance(mypolicy, kpolicy.K2hr3Policy)

    def test_policy_repr(self):
        """Represent a K2hr3Policy instance."""
        mypolicy = kpolicy.K2hr3Policy(self.token)
        self.assertRegex(repr(mypolicy), '<K2hr3Policy .*>')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_policy_create_policy_using_post(self, mock_HTTP_REQUEST_METHOD):
        mypolicy = kpolicy.K2hr3Policy(self.token)
        """Get root path."""
        self.assertEqual(mypolicy.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mypolicy.headers, headers)
        mypolicy.create(
            self.policy_name, self.effect, self.action,
            self.resource, self.condition, self.alias)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.POST(mypolicy))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/policy")
        # 2. assert URL params
        self.assertEqual(mypolicy.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mypolicy.headers, headers)
        # 4. assert Request body
        import json
        python_data = json.loads(kpolicy._POLICY_API_CREATE_POLICY)
        python_data['policy']['name'] = self.policy_name
        python_data['policy']['effect'] = self.effect
        python_data['policy']['action'] = self.action
        python_data['policy']['resource'] = self.resource
        python_data['policy']['alias'] = self.alias
        body = json.dumps(python_data)
        self.assertEqual(mypolicy.body, body)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_policy_create_policy_using_put(self, mock_HTTP_REQUEST_METHOD):
        mypolicy = kpolicy.K2hr3Policy(self.token)
        """Get root path."""
        self.assertEqual(mypolicy.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mypolicy.headers, headers)
        mypolicy.create(
            self.policy_name, self.effect, self.action,
            self.resource, self.condition, self.alias)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.PUT(mypolicy))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/policy")
        # 2. assert URL params
        s_s_urlparams = {
            'name': self.policy_name,
            'effect': self.effect,
            'action': self.action,
            'resource': self.resource,
            'alias': self.alias
        }
        self.assertEqual(mypolicy.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mypolicy.headers, headers)
        # 4. assert Request body
        self.assertEqual(mypolicy.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_policy_get_using_get(self, mock_HTTP_REQUEST_METHOD):
        mypolicy = kpolicy.K2hr3Policy(self.token)
        """Get root path."""
        self.assertEqual(mypolicy.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mypolicy.headers, headers)
        mypolicy.get(self.policy_name, self.service)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(mypolicy))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/policy/{self.policy_name}") # noqa
        # 2. assert URL params
        s_s_urlparams = {
            'service': self.service
        }
        self.assertEqual(mypolicy.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mypolicy.headers, headers)
        # 4. assert Request body
        self.assertEqual(mypolicy.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_policy_validate_using_head(self, mock_HTTP_REQUEST_METHOD):
        mypolicy = kpolicy.K2hr3Policy(self.token)
        """Get root path."""
        self.assertEqual(mypolicy.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mypolicy.headers, headers)
        mypolicy.validate(
            self.policy_name, self.tenant, self.resource, self.action,
            self.service
            )

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.HEAD(mypolicy))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/policy/{self.policy_name}") # noqa
        # 2. assert URL params
        s_s_urlparams = {
            'tenant': self.tenant,
            'resource': self.resource,
            'action': self.action,
            'service': self.service
        }
        self.assertEqual(mypolicy.urlparams, json.dumps(s_s_urlparams))
        s_urlparams = urllib.parse.urlencode(s_s_urlparams)
        self.assertEqual(httpreq.urlparams, f"{s_urlparams}")
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mypolicy.headers, headers)
        # 4. assert Request body
        self.assertEqual(mypolicy.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_policy_delete_using_delete(self, mock_HTTP_REQUEST_METHOD):
        mypolicy = kpolicy.K2hr3Policy(self.token)
        """Get root path."""
        self.assertEqual(mypolicy.r3token, "token")
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mypolicy.headers, headers)
        mypolicy.delete(self.policy_name)

        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.DELETE(mypolicy))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/policy/{self.policy_name}") # noqa
        # 2. assert URL params
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mypolicy.headers, headers)
        # 4. assert Request body
        self.assertEqual(mypolicy.body, None)

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
