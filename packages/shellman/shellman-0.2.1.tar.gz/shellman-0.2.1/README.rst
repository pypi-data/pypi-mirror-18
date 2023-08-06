========
Shellman
========

.. start-badges


|travis|
|codecov|
|landscape|
|version|
|wheel|
|pyup|
|gitter|


.. |travis| image:: https://travis-ci.org/Pawamoy/shellman.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Pawamoy/shellman/

.. |codecov| image:: https://codecov.io/github/Pawamoy/shellman/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Pawamoy/shellman/

.. |landscape| image:: https://landscape.io/github/Pawamoy/shellman/master/landscape.svg?style=flat
    :target: https://landscape.io/github/Pawamoy/shellman/
    :alt: Code Quality Status

.. |pyup| image:: https://pyup.io/repos/github/pawamoy/shellman/shield.svg
    :target: https://pyup.io/repos/github/pawamoy/shellman/
    :alt: Updates

.. |gitter| image:: https://badges.gitter.im/Pawamoy/shellman.svg
    :alt: Join the chat at https://gitter.im/Pawamoy/shellman
    :target: https://gitter.im/Pawamoy/shellman?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. |version| image:: https://img.shields.io/pypi/v/shellman.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/shellman/

.. |wheel| image:: https://img.shields.io/pypi/wheel/shellman.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/shellman/


.. end-badges

Write doc in your shell scripts.

Shellman is a Python package that read files, search for special comment lines
(documentation) and output formatted documentation as text, markdown or man page.

License
=======

Software licensed under `MPL 2.0`_ license.

.. _`MPL 2.0`: https://www.mozilla.org/en-US/MPL/2.0/

Installation
============

::

    pip install [--user] shellman

Documentation
=============

https://github.com/Pawamoy/shellman/wiki

Development
===========

To run all the tests: ``tox``

Usage
=====

To render the doc on stdout:

.. code:: bash

    shellman FILE
    # equivalent to...
    shellman --format=text FILE
    # other available formats:
    shellman --format=man FILE
    shellman --format=markdown FILE

You can pass the ``-o``, ``--output`` option to specify a file to write to, instead of stdout.

To check if the documentation within a script is correct:

.. code:: bash

    shellman --check --warn FILE         # CI test
    shellman --check --failfast FILE     # quick CI test with no output
    shellman --check --warn --nice FILE  # always passing test with output

In a script, for automatic help text:

.. code:: bash

    #!/bin/bash

    ## \brief Just a demo
    ## \desc This script actually does nothing.

    main() {
      case "$1" in
        ## \option -h, --help
        ## Print this help and exit.
        -h|--help) shellman "$0"; exit 0 ;;
      esac
    }

    ## \usage demo [-h]
    main "$@"


Output when calling ``./demo -h``:

.. code::

    Usage: demo [-h]

    This script actually does nothing.

    Options:
      -h, --help
        Print this help and exit.
