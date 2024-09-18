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
from k2hr3client import extdata as kextdata

LOG = logging.getLogger(__name__)


class TestK2hr3Extdata(unittest.TestCase):
    """Tests the K2hr3ApiResponse class.

    Simple usage(this class only):
    $ python -m unittest tests/test_extdata.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""
        self.base_url = "http://127.0.0.1:18080"
        self.extapi_name = "uripath"
        self.register_path = "registerpath"
        self.user_agent = "allowed_useragent 1.0.0"

    def tearDown(self):
        """Tears down a test case."""

    def test_extdata_construct(self):
        """Creates a K2hr3ApiResponse instance."""
        myextdata = kextdata.K2hr3Extdata(self.extapi_name, self.register_path,
                                          self.user_agent)
        self.assertIsInstance(myextdata, kextdata.K2hr3Extdata)

    def test_extdata_repr(self):
        """Represent a K2hr3ApiResponse instance."""
        myextdata = kextdata.K2hr3Extdata(self.extapi_name, self.register_path,
                                          self.user_agent)
        # Note: The order of _error and _code is unknown!
        self.assertRegex(repr(myextdata), '<K2hr3Extdata .*>')

    @patch('k2hr3client.http.K2hr3Http._HTTP_REQUEST_METHOD')
    def test_extdata_acquries_template_using_get(self,
                                                 mock_HTTP_REQUEST_METHOD):
        """Get root path."""
        myextdata = kextdata.K2hr3Extdata(self.extapi_name, self.register_path,
                                          self.user_agent)
        myextdata.acquires_template()
        httpreq = khttp.K2hr3Http(self.base_url)
        self.assertTrue(httpreq.GET(myextdata))

        # 1. assert URL
        self.assertEqual(httpreq.url,
                         f"{self.base_url}/v1/extdata/{self.extapi_name}/{self.register_path}") # noqa
        # 2. assert URL params
        self.assertEqual(myextdata.urlparams, None)
        self.assertEqual(httpreq.urlparams, None)
        # 3. assert Request headers
        headers = {
            'Content-Type': 'application/octet-stream',
            'User-Agent': f"{self.user_agent}",
            'Accept-Encoding': 'gzip',
        }
        self.assertEqual(myextdata.headers, headers)
        # 4. assert Request body
        self.assertEqual(myextdata.body, None)

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
