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
#
"""K2HR3 Python Client of Token API."""

__author__ = 'Hirotaka Wakabayashi <hiwakaba@lycorp.co.jp>'
__version__ = '1.0.0'

import sys

if sys.platform.startswith('win'):
    raise ImportError(r'Currently we do not test well on windows')


def get_version() -> str:
    """Return a version of the package.

    :returns: version
    :rtype: str
    """
    return __version__


#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
