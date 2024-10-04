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
"""K2HR3 Python Client of Userdata API.

.. code-block:: python

    # Import modules from k2hr3client package.
    from k2hr3client.token import K2hr3Token
    from k2hr3client.http import K2hr3Http
    from k2hr3client.userdata import K2hr3Userdata

    # GET a userdatascript from K2HR3 Userdata API.
    userdata_path = "testpath"
    myuserdata = K2hr3Userdata(userdata_path)
    myhttp.GET(
        myuserdata.provides_userdata_script()
    )
    myuserdata.resp.body // {"result":true...

"""
import logging
from typing import Optional


from k2hr3client.api import K2hr3Api, K2hr3HTTPMethod
from k2hr3client.exception import K2hr3Exception

LOG = logging.getLogger(__name__)


class K2hr3Userdata(K2hr3Api):  # pylint: disable=too-many-instance-attributes # noqa
    """Relationship with K2HR3 USERDATA API.

    See https://k2hr3.antpick.ax/api_userdata.html for details.

    """

    __slots__ = ('_userdatapath',)

    def __init__(self, userdatapath: str):
        """Init the members."""
        super().__init__("userdata")
        self.userdatapath = userdatapath

        # following attrs are dynamically set later.
        self.headers = {
            'Content-Type': 'application/octet-stream',
            'User-Agent': 'Cloud-Init 0.7.9',
        }
        self.body = None
        self.urlparams = None

    # ---- GET ----
    # GET（Userdata）    http(s)://API SERVER:PORT/v1/userdata/userdata_path
    def provides_userdata_script(self):
        """Get userdata."""
        self.api_id = 1
        return self

    def __repr__(self) -> str:
        """Represent the instance."""
        attrs = []
        values = ""
        for attr in ['_userdatapath']:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs])
        return '<K2hr3Userdata ' + values + '>'

    @property  # type: ignore
    def userdatapath(self) -> str:
        """Return the tenant."""
        return self._userdatapath

    @userdatapath.setter
    def userdatapath(self, val) -> None:  # type: ignore # noqa: F811
        """Set the userdatapath."""
        if isinstance(val, str) is False:
            raise K2hr3Exception(f'value type must be str, not {type(val)}')
        if getattr(self, '_userdatapath', None) is None:
            self._userdatapath = val

    #
    # abstract methos that must be implemented in subclasses
    #
    def _api_path(self, method: K2hr3HTTPMethod) -> Optional[str]:
        """Get the request url path."""
        if method == K2hr3HTTPMethod.GET:
            if self.api_id == 1:
                return f'{self.version}/{self.basepath}/{self.userdatapath}'
        return None
#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
