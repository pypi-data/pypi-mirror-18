========
Shellman
========



Write doc in your shell scripts.

Shellman is a Python script that read files, search for special comment lines
(documentation) and output formatted documentation
as text, markdown or man page.

License
=======

Software licensed under `MPL 2.0`_ license.

.. _`MPL 2.0`: https://www.mozilla.org/en-US/MPL/2.0/

Installation
============

::

    pip install shellman

Documentation
=============

https://github.com/Pawamoy/shellman/wiki

Development
===========

To run all the tests: ``tox``

Usage
=====

.. code:: bash

    shellman FILE
    # equivalent to...
    SHELLMAN_FORMAT=text shellman FILE
    # also available:
    SHELLMAN_FORMAT=man shellman FILE
    SHELLMAN_FORMAT=markdown shellman FILE


*The script does not currently handle arguments, except for the file name.*

In a script, for automatic help text:

.. code:: bash

    #!/bin/bash

    ## \brief Just a demo
    ## \desc This script actually does nothing.

    main() {
      case "$1" in
        ## \option -h, --help
        ## Print this help and exit.
        -h|--help) shellman.py "$0"; exit 0 ;;
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

=========
Changelog
=========

0.1.0 (2016-11-30)
==================

* Alpha release on PyPI.


