Unix: |Unix Build Status| Windows: |Windows Build Status|\ Metrics:
|Coverage Status| |Scrutinizer Code Quality|\ Usage: |PyPI Version|
|PyPI Downloads|

Overview
========

Verchew is an embeddable Python script to check the versions of your
project's system dependencies. Its only external dependency is a Python
interpreter, available on macOS and most linux-based operating systems.

Setup
=====

Requirements
------------

-  Python 2.7+ or Python 3.3+

Installation
------------

Install verchew with pip:

.. code:: sh

    $ pip install verchew

or directly from the source code:

.. code:: sh

    $ git clone https://github.com/jacebrowning/verchew.git
    $ cd verchew
    $ python setup.py install

Usage
=====

Create a configuration file (``.verchew``) with your project's system
dependencies:

.. code:: ini

    [Working Program]

    cli = working-program
    version = 1.2.

    [Newer Working Program]

    cli = working-program
    version =  4.

    [Broken Program]

    cli = broken-program
    version = 1.2.3

    [Missing Program]

    cli = missing-program
    version = 1.2.3

Run ``verchew`` to see if you have the right versions installed:

.. code:: sh

    $ verchew

    Checking for Working Program...

    $ working-program --version
    1.2.3
    ✔ MATCHED: 1.2.

    Checking for Newer Working Program...

    $ working-program --version
    1.2.3
    ✘ EXPECTED: 4.

    Checking for Broken Program...

    $ broken-program --version
    An error occurred.
    ✘ EXPECTED: 1.2.3

    Checking for Missing Program...

    $ missing-program --version
    sh: command not found: missing-program
    ✘ EXPECTED: 1.2.3

    Results: ✔ ✘ ✘ ✘

.. |Unix Build Status| image:: https://img.shields.io/travis/jacebrowning/verchew/develop.svg
   :target: https://travis-ci.org/jacebrowning/verchew
.. |Windows Build Status| image:: https://img.shields.io/appveyor/ci/jacebrowning/verchew/develop.svg
   :target: https://ci.appveyor.com/project/jacebrowning/verchew
.. |Coverage Status| image:: https://img.shields.io/coveralls/jacebrowning/verchew/develop.svg
   :target: https://coveralls.io/r/jacebrowning/verchew
.. |Scrutinizer Code Quality| image:: https://img.shields.io/scrutinizer/g/jacebrowning/verchew.svg
   :target: https://scrutinizer-ci.com/g/jacebrowning/verchew/?branch=develop
.. |PyPI Version| image:: https://img.shields.io/pypi/v/verchew.svg
   :target: https://pypi.python.org/pypi/verchew
.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/verchew.svg
   :target: https://pypi.python.org/pypi/verchew

Revision History
================

0.5 (unreleased)
----------------

-  Added ``--exit-code`` option to return non-zero exit codes on
   failure.

0.4 (2016/10/20)
----------------

-  Added support for custom version arguments.
-  Fixed handling of internal versions matches.

0.3 (2016/10/18)
----------------

-  Added support for detecting missing and broken programs.

0.2.1 (2016/10/18)
------------------

-  Now stripping whitespace after calling ``--version`` on a program.

0.2 (2016/10/17)
----------------

-  Added ``--version`` command.

0.1 (2016/10/17)
----------------

-  Initial release.


