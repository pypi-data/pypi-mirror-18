wobble
======

Deployment tool for deploying to Marathon running in DCOS, easily pluggable for servers requiring authentication and custom confirmation logic.

This is a deployment solution for deployments to Marathon orchestrated clusters running in DCOS. If what you
need is a *fire-and-forget* deployment, you should probably use `dcos/dcos-cli`_.

.. _usage:
Usage
-----

Current support is only for a cluster that is protected with Auth0_, however this will be abstracted into a :ref:`Plugin <plugins>` shortly.

.. code-block::

    pip install wobble
    wobble --help

Most options listed will respect an environmental variable, where the leading hyphens are stripped and the remaining characters are capitalized and converted to snake case:

.. code-block::

    dcos-url -> DCOS_URL
    auth0-url -> AUTH0_URL

.. _plugins:
Plugins
-------

TODO: This system is not currently defined

Developing
==========

    # Run all the tests
    python setup.py test

    # Develop
    pip install -e .

.. _dcos/dcos-cli: https://github.com/dcos/dcos-cli
.. _Auth0: https://auth0.com/