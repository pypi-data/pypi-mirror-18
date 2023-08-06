========
Overview
========



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


Changelog
=========

0.1.0 (2016-12-15)
-----------------------------------------

* First release on PyPI.


