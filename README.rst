======
tendo
======

Tendo is a python module that adds basic functionality that is
not (yet) provided by Python.

.. image:: https://img.shields.io/pypi/v/tendo.svg?colorB=green
        :target: https://pypi.python.org/pypi/tendo/

.. image:: https://img.shields.io/pypi/l/tendo.svg?colorB=green
        :target: https://pypi.python.org/pypi/tendo/

.. image:: https://img.shields.io/pypi/wheel/tendo.svg
        :target: https://pypi.python.org/pypi/tendo/

.. image:: https://img.shields.io/codecov/c/github/pycontribs/tendo/master.svg
        :target: https://codecov.io/gh/pycontribs/tendo

------------

.. image:: https://readthedocs.org/projects/tendo/badge/?version=latest
        :target: http://tendo.readthedocs.io

.. image:: https://api.travis-ci.com/pycontribs/tendo.svg?branch=master
        :target: https://travis-ci.com/pycontribs/tendo

.. image:: https://requires.io/github/pycontribs/tendo/requirements.svg?branch=master
        :target: https://requires.io/github/pycontribs/tendo/requirements/?branch=master
        :alt: Requirements Status


* [transparent Unicode support for text file operations (BOM detection)](https://tendo.readthedocs.org/en/latest/#module-tendo.singleton)
* [console logging coloring](https://tendo.readthedocs.org/en/latest/#module-tendo.colorer)
* enable you to use symlinks under windows
* [python tee implementation](https://tendo.readthedocs.org/en/latest/#module-tendo.colorer) for executing external programs and redirecting their output to both console/file)
* [improved execfile](https://tendo.readthedocs.org/en/latest/#module-tendo.execfile2)

Documentation
------------------------------
Check:
* http://packages.python.org/tendo/
* https://tendo.readthedocs.org/en/latest/

Requirements and compatibility
------------------------------
* python 2.7-3.6
* distribute (for installation)
* tox for running tests

Related project and packages
----------------------------
* six - helps you write code that works with both py2 and py3
* jaraco - http://pypi.python.org/pypi/jaraco.util
* pexpect (maybe)


TODO
----
* implement testing, see test frameworks http://pycheesecake.org/wiki/PythonTestingToolsTaxonomy
* implement all PEP8 recommendations
