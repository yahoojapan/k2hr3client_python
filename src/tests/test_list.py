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

import logging
import unittest
from unittest.mock import patch

from k2hr3client import http as khttp
from k2hr3client import list as klist

LOG = logging.getLogger(__name__)


class TestK2hr3List(unittest.TestCase):
    """Tests the K2hr3ApiResponse class.

    Simple usage(this class only):
    $ python -m unittest tests/test_list.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        self.service = "testservice"

    def tearDown(self):
        """Tears down a test case."""

    def test_k2hr3list_construct(self):
        """Creates a K2hr3ApiResponse instance."""
        mylist = klist.K2hr3List("token", self.service)
        self.assertIsInstance(mylist, klist.K2hr3List)

    def test_k2hr3list_repr(self):
        """Represent a K2hr3ApiResponse instance."""
        mylist = klist.K2hr3List("token", self.service)
        # Note: The order of _error and _code is unknown!
        self.assertRegex(repr(mylist), '<K2hr3List .*>')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_k2hr3list_service_get_ok(self, mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        mylist = klist.K2hr3List("token", self.service)
        self.assertEqual(mylist.r3token, "token")
        self.assertEqual(mylist.service, self.service)
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mylist.headers, headers)
        mylist.get()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(mylist))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1/list/{self.service}")
        # 2. assert URL params
        self.assertEqual(mylist.urlparams, None)
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
            'x-auth-token': 'U=token'
        }
        self.assertEqual(mylist.headers, headers)
        # 4. assert Request body
        self.assertEqual(mylist.body, None)


#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
