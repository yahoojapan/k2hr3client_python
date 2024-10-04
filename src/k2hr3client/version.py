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
#
"""K2HR3 Python Client of Version API.

.. code-block:: python

    # Import modules from k2hr3client package
    from k2hr3client import version
    v = version.K2hr3Version()
    from k2hr3client import http as khttp
    httpreq = khttp.K2hr3Http('http://127.0.0.1:18080')

    # GET the K2hr Version API.
    httpreq.GET(v)
    print(v.resp)

"""

import logging
from typing import Optional


from k2hr3client.api import K2hr3Api, K2hr3HTTPMethod

LOG = logging.getLogger(__name__)


class K2hr3Version(K2hr3Api):  # pylint: disable=too-many-instance-attributes
    """Relationship with K2HR3 VERSION API.

    See https://k2hr3.antpick.ax/api_version.html for details.
    """

    __slots__ = ('_name',)

    def __init__(self, version=""):
        """Init the members."""
        super().__init__("", version=version)
        self.name = version

        # following attrs are dynamically set later.
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.body = None
        self.urlparams = None

    # ---- GET ----
    #
    # GET http(s)://API SERVER:PORT/
    # GET http(s)://API SERVER:PORT/v1
    #
    def get(self):
        """Get the version."""
        self.api_id = 1

    def __repr__(self):
        """Represent the members."""
        attrs = []
        values = ""
        for attr in [
                'name'
        ]:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs])
        return '<K2hr3Version ' + values + '>'

    #
    # abstract methos that must be implemented in subclasses
    #
    def _api_path(self, method: K2hr3HTTPMethod) -> Optional[str]:
        """Get the request url path."""
        if method == K2hr3HTTPMethod.GET:
            if self.api_id == 1:
                return f'{self.version}'
        return None
#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
