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
"""Test Package for K2hr3 Python Client.

This file is needed to run tests simply like:
$ python -m unittest discover

All of the test files must be a package importable from the top-level directory of the project.
https://docs.python.org/3.6/library/unittest.html#test-discovery
"""
__author__ = 'Hirotaka Wakabayashi <hiwakaba@lycorp.co.jp>'
__version__ = '1.0.0'

# Disables the k2hr3client library logs by failure assetion tests.
import logging
logging.getLogger('k2hr3client').addHandler(logging.NullHandler())

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
