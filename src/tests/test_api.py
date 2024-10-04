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
from http.client import HTTPMessage

from k2hr3client.api import K2hr3ApiResponse

LOG = logging.getLogger(__name__)


class TestK2hr3ApiResponse(unittest.TestCase):
    """Tests the K2hr3ApiResponse class.

    Simple usage(this class only):
    $ python -m unittest tests/test_r3token.py

    Simple usage(all):
    $ python -m unittest tests
    """
    def setUp(self):
        """Sets up a test case."""

    def tearDown(self):
        """Tears down a test case."""

    def test_k2hr3apiresponse_construct(self):
        """Creates a K2hr3ApiResponse instance."""
        hdrs = HTTPMessage()
        hdrs['mime-version'] = '1.0'
        response = K2hr3ApiResponse(code=200, url="http://localhost:18080", hdrs=hdrs, body=None)
        self.assertIsInstance(response, K2hr3ApiResponse)

    def test_k2hr3apiresponse_repr(self):
        """Represent a K2hr3ApiResponse instance."""
        hdrs = HTTPMessage()
        hdrs['mime-version'] = '1.0'
        response = K2hr3ApiResponse(code=200, url="http://localhost:18080", hdrs=hdrs, body=None)
        # Note: The order of _error and _code is unknown!
        self.assertRegex(repr(response), '<K2hr3ApiResponse .*>')


#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
