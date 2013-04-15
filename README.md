======
tendo
======

Tendo is a python module that adds basic functionality that is 
not (yet) provided by Python. 

[![Build Status](https://drone.io/github.com/pycontribs/tendo/status.png)](https://drone.io/github.com/pycontribs/tendo/latest)

* [transparent Unicode support for text file operations (BOM detection)](https://tendo.readthedocs.org/en/latest/#module-tendo.singleton)
* [console logging coloring](https://tendo.readthedocs.org/en/latest/#module-tendo.colorer)
* enable you to use symlinks under windows
* [python tee implementation](https://tendo.readthedocs.org/en/latest/#module-tendo.colorer) for executing extenal programs and redirecting their output to both console/file)
* [improved execfile](https://tendo.readthedocs.org/en/latest/#module-tendo.execfile2)
 
Documentation
------------------------------
Check:
* http://packages.python.org/tendo/
* https://tendo.readthedocs.org/en/latest/

Requirements and compatibility
------------------------------
* python 2.5-3.2
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
* implement all PEP8 recomandations

