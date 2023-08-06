========
Overview
========



Bootstrap your project to use behave bdd

* Free software: BSD license

Installation
============

::

    pip install behave-generator

Documentation
=============

https://behave-generator.readthedocs.io/

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

0.1.0 (2016-11-06)
-----------------------------------------

* First release on PyPI.


