========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |codecov|
    * - package
      - | |version| |wheel|
        | |supported-versions|
        | |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/pipeline-telemetry/badge/?style=flat
    :target: https://pipeline-telemetry.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/MaartendeRuyter/pipeline-telemetry.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/MaartendeRuyter/pipeline-telemetry

.. |requires| image:: https://requires.io/github/MaartendeRuyter/pipeline-telemetry/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/MaartendeRuyter/pipeline-telemetry/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/MaartendeRuyter/pipeline-telemetry/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/MaartendeRuyter/pipeline-telemetry

.. |version| image:: https://img.shields.io/pypi/v/pipeline-telemetry.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pipeline-telemetry

.. |wheel| image:: https://img.shields.io/pypi/wheel/pipeline-telemetry.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pipeline-telemetry

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pipeline-telemetry.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pipeline-telemetry

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pipeline-telemetry.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/pipeline-telemetry

.. |commits-since| image:: https://img.shields.io/github/commits-since/MaartendeRuyter/pipeline-telemetry/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/MaartendeRuyter/pipeline-telemetry/compare/v0.0.1...master


.. end-badges

Create and store data pipeline telemetry data

* Free software: GNU Lesser General Public License v3 or later (LGPLv3+)

Installing pipeline-telemetry
=============================

::

    pip install pipeline-telemetry

You can also install the in-development version with::

    pip install https://github.com/MaartendeRuyter/pipeline-telemetry/archive/master.zip


Documentation
=============


https://pipeline-telemetry.readthedocs.io/


Testing
=======

To run all the tests run::

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

