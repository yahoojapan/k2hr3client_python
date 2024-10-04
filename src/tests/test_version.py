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

import logging
import unittest
from unittest.mock import patch

from k2hr3client import http as khttp
from k2hr3client import version as kversion

LOG = logging.getLogger(__name__)


class TestK2hr3Version(unittest.TestCase):
    """Tests the K2hr3ApiResponse class.

    Simple usage(this class only):
    $ python -m unittest tests/test_version.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        self.name = ""

    def tearDown(self):
        """Tears down a test case."""

    def test_k2hr3version_construct(self):
        """Creates a K2hr3ApiResponse instance."""
        myversion = kversion.K2hr3Version()
        self.assertIsInstance(myversion, kversion.K2hr3Version)

    def test_k2hr3version_repr(self):
        """Represent a K2hr3ApiResponse instance."""
        myversion = kversion.K2hr3Version()
        # Note: The order of _error and _code is unknown!
        self.assertRegex(repr(myversion), '<K2hr3Version .*>')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_k2hr3version_root_get_ok(self, mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        myversion = kversion.K2hr3Version()
        self.assertEqual(myversion.name, "")
        myversion.get()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(myversion))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/")
        # 2. assert URL params
        self.assertEqual(myversion.urlparams, None)
        # 3. assert Request header
        headers = {
            'Content-Type': 'application/json',
        }
        self.assertEqual(myversion.headers, headers)
        # 4. assert Request body
        self.assertEqual(myversion.body, None)

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_k2hr3version_root_get_v1_ok(self, mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        myversion = kversion.K2hr3Version("v1")
        self.assertEqual(myversion.name, "v1")
        myversion.get()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(myversion))

        # 1. assert URL
        self.assertEqual(httpreq.url, f"{self.base_url}/v1")
        # 2. assert URL params
        self.assertEqual(myversion.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/json',
        }
        self.assertEqual(myversion.headers, headers)
        # 4. assert Request body
        self.assertEqual(myversion.body, None)

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
