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
"""K2HR3 Python Client of Policy API.

.. code-block:: python

    # Import modules from k2hr3client package.
    from k2hr3client.token import K2hr3Token
    from k2hr3client.http import K2hr3Http
    from k2hr3client.policy import K2hr3Policy

    iaas_project = "demo"
    iaas_token = "gAAAAA..."
    mytoken = K2hr3Token(iaas_project, iaas_token)

    # POST a request to create a token to K2HR3 Token API.
    myhttp = K2hr3Http("http://127.0.0.1:18080")
    myhttp.POST(mytoken.create())
    mytoken.token  // gAAAAA...

    # POST request to get a K2HR3 Policy API.
    mypolicy = K2hr3Policy(mytoken.token)
    RESOURCE_PATH = "yrn:yahoo:::demo:resource:test_resource"
    myhttp.POST(
        mypolicy.create(
            name="test_policy",
            effect="allow",
            action=['yrn:yahoo::::action:read'],
            resource=[RESOURCE_PATH],
            condition=None,
            alias=[]
            )
        )
    mypolicy.resp.body // {"result":true...

"""

import json
import logging
from typing import List, Optional
import warnings


from k2hr3client.api import K2hr3Api, K2hr3HTTPMethod

LOG = logging.getLogger(__name__)

_POLICY_API_CREATE_POLICY = """
{
    "policy":    {
        "name":      "<policy name>",
        "effect":    "<allow or deny>",
        "action":    [],
        "resource":  [],
        "condition": null,
        "alias":     []
    }
}
"""


class K2hr3Policy(K2hr3Api):  # pylint: disable=too-many-instance-attributes
    """Relationship with K2HR3 POLICY API.

    See https://k2hr3.antpick.ax/api_policy.html for details.
    """

    __slots__ = ('_r3token',)

    def __init__(self, r3token: str) -> None:
        """Init the members."""
        super().__init__("policy")
        self.r3token = r3token

        # following attrs are dynamically set later.
        if r3token:
            self.headers = {
                'Content-Type': 'application/json',
                'x-auth-token': 'U={}'.format(self._r3token)
            }
        else:
            self.headers = {
                'Content-Type': 'application/json',
            }
        self.body = None
        self.urlparams = None
        # attributes that are unique to this class
        self.name = None
        self.effect = None
        self.action = None
        self.resource = None
        self.condition = None
        self.alias = None
        self.service = None
        self.tenant = None

    # ---- POST/PUT ----
    # POST   http(s)://API SERVER:PORT/v1/policy
    # PUT    http(s)://API SERVER:PORT/v1/policy?urlarg
    def create(self, name: str, effect: str,  # pylint: disable=R0917
               action: Optional[List[str]],
               resource: Optional[List[str]] = None,
               condition: Optional[str] = None,
               alias: Optional[List[str]] = None,
               policy_name: Optional[str] = None):
        """Create policies."""
        self.api_id = 1
        # must to process a request further
        self.name = name  # type: ignore
        self.effect = effect  # type: ignore
        self.action = action  # type: ignore
        # optionals
        self.resource = resource  # type: ignore
        self.condition = condition  # type: ignore
        self.alias = alias  # type: ignore
        if name is None and policy_name is not None:
            warnings.warn(
                "The 'policy_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = policy_name
        return self

    # ---- GET ----
    # GET    http(s)://API SERVER:PORT/v1/policy/\
    #            policy path or yrn full policy path{?service=service name} # noqa
    def get(self, name: str, service: str, policy_name: Optional[str] = None):
        """Get policies."""
        self.api_id = 3
        self.name = name   # type: ignore
        self.service = service  # type: ignore
        if name is None and policy_name is not None:
            warnings.warn(
                "The 'policy_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = policy_name
        return self

    # ---- HEAD ----
    # HEAD   http(s)://API SERVER:PORT/v1/policy/yrn full policy path?urlarg
    def validate(self, name: str, tenant: str, resource: str,  # pylint: disable=R0917 # noqa
                 action: str, service: Optional[str] = None,
                 policy_name: Optional[str] = None):
        """Validate policies."""
        self.api_id = 4
        self.name = name  # type: ignore
        self.tenant = tenant  # type: ignore
        self.resource = resource  # type: ignore
        self.action = action  # type: ignore
        # optionals
        self.service = service  # type: ignore
        if name is None and policy_name is not None:
            warnings.warn(
                "The 'policy_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = policy_name
        return self

    # ---- DELETE ----
    # DELETE http(s)://API SERVER:PORT/v1/policy/policy path or yrn full policy path # noqa
    def delete(self, name: str, policy_name: Optional[str] = None):
        """Delete policies."""
        self.api_id = 5
        self.name = name  # type: ignore
        if name is None and policy_name is not None:
            warnings.warn(
                "The 'policy_name' parameter to 'create' "
                "is deprecated and slated for removal in "
                "k2hr3client-1.1.0",
                DeprecationWarning,
                stacklevel=1)
            self.name = policy_name
        return self

    def __repr__(self) -> str:
        """Represent the instance."""
        attrs = []
        values = ""
        for attr in [
                '_r3token'
        ]:
            val = getattr(self, attr, None)
            if val:
                attrs.append((attr, repr(val)))
                values = ', '.join(['%s=%s' % i for i in attrs])
        return '<K2hr3Policy ' + values + '>'

    @property  # type: ignore
    def r3token(self) -> str:
        """Return the r3token."""
        return self._r3token

    @r3token.setter
    def r3token(self, val: str) -> None:  # type: ignore # noqa: F811
        """Set the r3token."""
        if getattr(self, '_r3token', None) is None:
            self._r3token = val

    #
    # abstract methos that must be implemented in subclasses
    #
    def _api_path(self, method: K2hr3HTTPMethod) -> Optional[str]:
        """Get the request url path."""
        if method == K2hr3HTTPMethod.POST:
            if self.api_id == 1:
                python_data = json.loads(_POLICY_API_CREATE_POLICY)
                python_data['policy']['name'] = self.name
                python_data['policy']['effect'] = self.effect
                python_data['policy']['action'] = self.action
                python_data['policy']['resource'] = self.resource
                python_data['policy']['alias'] = self.alias
                self.body = json.dumps(python_data)
                return f'{self.version}/{self.basepath}'
        if method == K2hr3HTTPMethod.PUT:
            if self.api_id == 1:
                self.urlparams = json.dumps({
                    'name': self.name,
                    'effect': self.effect,
                    'action': self.action,
                    'resource': self.resource,
                    'alias': self.alias
                })
                return f'{self.version}/{self.basepath}'
        if method == K2hr3HTTPMethod.GET:
            if self.api_id == 3:
                self.urlparams = json.dumps({
                    'service': self.service
                })
                return f'{self.version}/{self.basepath}/{self.name}'
        if method == K2hr3HTTPMethod.HEAD:
            if self.api_id == 4:
                self.urlparams = json.dumps({
                    'tenant': self.tenant,
                    'resource': self.resource,
                    'action': self.action,
                    'service': self.service
                })
                return f'{self.version}/{self.basepath}/{self.name}'
        if method == K2hr3HTTPMethod.DELETE:
            if self.api_id == 5:
                return f'{self.version}/{self.basepath}/{self.name}'
        return None

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
