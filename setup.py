# -*- coding: utf-8 -*-
#
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
"""K2HR3 Python Client."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

__author__ = 'Hirotaka Wakabayashi <hiwakaba@lycorp.co.jp>'
__copyright__ = """

MIT License

Copyright (c) 2020 Yahoo Japan Corporation

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice (including the next
paragraph) shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

# Always prefer setuptools over distutils
from setuptools import setup


def get_version():
    """Returns the package version from __ini__.py."""
    from pathlib import Path
    from os import path, sep
    import re

    here = path.abspath(path.dirname(__file__))
    init_py = Path(sep.join([here, 'src', 'k2hr3client', '__init__.py'])).resolve()

    with init_py.open() as fp:
        for line in fp:
            version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                                      line.strip(), re.M)
            if version_match:
                return version_match.group(1)
    raise RuntimeError('version expected, but no version found.')


setup(
    version=get_version(),
)

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
