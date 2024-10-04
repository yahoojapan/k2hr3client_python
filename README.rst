==================
k2hr3client_python
==================

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
        :target: https://github.com/yahoojapan/k2hr3client_python/blob/master/LICENSE
.. image:: https://img.shields.io/pypi/pyversions/k2hr3client.svg
        :target: https://pypi.python.org/pypi/k2hr3client
.. image:: https://img.shields.io/github/forks/yahoojapan/k2hr3client_python.svg
        :target: https://github.com/yahoojapan/k2hr3client_python/network
.. image:: https://img.shields.io/github/stars/yahoojapan/k2hr3client_python.svg
        :target: https://github.com/yahoojapan/k2hr3client_python/stargazers
.. image:: https://img.shields.io/github/issues/yahoojapan/k2hr3client_python.svg
        :target: https://github.com/yahoojapan/k2hr3client_python/issues
.. image:: https://github.com/yahoojapan/k2hr3client_python/workflows/Python%20package/badge.svg
        :target: https://github.com/yahoojapan/k2hr3client_python/actions
.. image:: https://readthedocs.org/projects/k2hr3client-python/badge/?version=latest
        :target: https://k2hr3client-python.readthedocs.io/en/latest/?badge=latest
.. image:: https://img.shields.io/pypi/v/k2hr3client
        :target: https://pypi.org/project/k2hr3client/



Overview
---------

k2hr3client_python is an official Python WebAPI client for `k2hr3`_.

.. _`k2hr3`: https://k2hr3.antpick.ax/

.. image:: https://k2hr3.antpick.ax/images/top_k2hr3.png


Install
--------

Let's install k2hr3client_python using pip::

    pip install k2hr3client


Usage
------

Let's try to get a token and create a resource.::

    >>> from k2hr3client.token import K2hr3Token
    >>> iaas_user = "demo"
    >>> iaas_project = "demo"
    >>> iaas_token_url = "http://172.24.4.1/identity/v3/auth/tokens"
    >>> iaas_token = K2hr3Token.get_openstack_token(
    ...     iaas_token_url, iaas_user, "password", iaas_project
    ... )
    >>> mytoken = K2hr3Token(iaas_project, iaas_token)
    >>>
    >>> from k2hr3client.http import K2hr3Http
    >>> k2hr3_token_url = "http://127.0.0.1:18080"
    >>> myhttp = K2hr3Http(k2hr3_token_url)
    >>> myhttp.POST(mytoken.create())
    >>> mytoken.token  // k2hr3 token
    >>>
    >>> from k2hr3client.resource import K2hr3Resource
    >>> k2hr3_resource_name = "test_resource"
    >>> myresource = K2hr3Resource(mytoken.token)
    >>> myhttp.POST(
    ... myresource.create_conf_resource(
    ...     name=k2hr3_resource_name,
    ...     data_type="string",
    ...     data="testresourcedata",
    ...     keys={
    ...         "cluster-name": "test-cluster",
    ...         "chmpx-server-port": "8020",
    ...         "chmpx-server-ctrlport": "8021",
    ...         "chmpx-slave-ctrlport": "8031"},
    ...     alias=[])
    ... )
    >>> myresource.resp.body // {"result":true...

Development
------------

Clone this repository and go into the directory, then run the following command::

    $ make init
    $ pipenv shell
    $ make lint test docs build


Documents
----------

Here are documents including other components.

`Document top page`_

`About K2HR3`_

`About AntPickax`_

.. _`Document top page`: https://k2hr3client-python.readthedocs.io/
.. _`About K2HR3`: https://k2hr3.antpick.ax/
.. _`About AntPickax`: https://antpick.ax


Packages
--------

Here are packages including other components.

`k2hr3client(python packages)`_

.. _`k2hr3client(python packages)`:  https://pypi.org/project/k2hr3client/


License
--------

MIT License. See the LICENSE file.


AntPickax
---------

**k2hr3client_python** is a project by AntPickax_, which is an open source team in `LY Corporation`_.

.. _AntPickax: https://antpick.ax/
.. _`LY Corporation`: https://www.lycorp.co.jp/en/company/overview/

