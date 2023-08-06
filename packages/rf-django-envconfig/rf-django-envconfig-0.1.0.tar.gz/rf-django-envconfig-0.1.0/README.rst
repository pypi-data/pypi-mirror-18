========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/rf-django-envconfig/badge/?style=flat
    :target: https://readthedocs.org/projects/rf-django-envconfig
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/rfleschenberg/rf-django-envconfig.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/rfleschenberg/rf-django-envconfig

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/rfleschenberg/rf-django-envconfig?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/rfleschenberg/rf-django-envconfig

.. |requires| image:: https://requires.io/github/rfleschenberg/rf-django-envconfig/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/rfleschenberg/rf-django-envconfig/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/rfleschenberg/rf-django-envconfig/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/rfleschenberg/rf-django-envconfig

.. |version| image:: https://img.shields.io/pypi/v/rf-django-envconfig.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/rf-django-envconfig

.. |downloads| image:: https://img.shields.io/pypi/dm/rf-django-envconfig.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/rf-django-envconfig

.. |wheel| image:: https://img.shields.io/pypi/wheel/rf-django-envconfig.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/rf-django-envconfig

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/rf-django-envconfig.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/rf-django-envconfig

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/rf-django-envconfig.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/rf-django-envconfig


.. end-badges

Helpers to configure Django settings by environment variables

The goal of this package is to help making your Django settings configurable
via environment variables, while keeping everything as simple and decoupled as
possible.


Related work
------------
* https://12factor.net/
* https://github.com/doismellburning/django12factor
* https://github.com/joke2k/django-environ


Installation
============

::

    pip install rf-django-envconfig

Documentation
=============

https://rf-django-envconfig.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
