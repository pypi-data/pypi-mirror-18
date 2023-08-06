jupyter-parser
==============

|Build Status| |codecov|

jupyter-parser is a jupyter notebook parser that attempts to gather
information about the varying ways in which a notebook may be used.
jupyter-parser has been tested on python 2.7.12 and python 3.5.2. The
current plugins written to parse notebook files are found in the
**plugins** directory and are described below...

Plugins - CellsCorrectPlugin: determines whether or not cells are in the
correct execution order - NotebookLibrariesPlugin: determines the
modules imported from the notebooks (can be local) -
NotebookSparkPlugin: uses a regular expression to search for any pyspark
variables

Plugins are included in the constructor of the main
parser(JupyterParser). This architecture is likely to be temporary as
the goal of being language/file agnostic is in the future.

This library should be used with
**`gist-dl <https://github.com/cameres/gist-dl>`__** in order to quickly
download example notebooks from
**`gist.github.com <http://gist.github.com>`__**.

Installation
------------

The project was recently added to PYPI. Feel free to submit an issue if
there are any issues with downloading via the command below...

.. code:: bash

    pip install github-dl

Installation (Development)
--------------------------

Install the project by downloading the project as a zip file or cloning
the repository. After downloading the source, run the following command
to install in the root directory of the project...

.. code:: bash

    pip install -e .

Usage
-----

jupyter-parser's functionality is currently fairly limited, but the
following functionality is supported

+--------------------------------+-------------------------------------------------+
| command line argument/option   | functionality                                   |
+================================+=================================================+
| ``--help``                     | list arguments/options for tool                 |
+--------------------------------+-------------------------------------------------+
| ``--root``                     | specify the root directory to parse for files   |
+--------------------------------+-------------------------------------------------+

.. |Build Status| image:: https://travis-ci.org/cameres/jupyter-parser.svg?branch=master
   :target: https://travis-ci.org/cameres/jupyter-parser
.. |codecov| image:: https://codecov.io/gh/cameres/jupyter-parser/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/cameres/jupyter-parser
