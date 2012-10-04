#!/usr/bin/env python
# Setuptools is required for the use_2to3 option below. You should install it
# from the Distribute home page, http://packages.python.org/distribute/
import inspect
import logging
import os
import sys

from setuptools import setup, Command
from setuptools.command.test import test as TestCommand

#from distutils.core import setup, Command

from tendo import __version__

# Hack to prevent stupid "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when running `python
# setup.py test` (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing
except ImportError:
    pass

test_requirements=['pep8>=0.6','py','pytest','six','sphinx'] #'nosexcover']
test_suite="py.test"
if sys.hexversion >= 0x02060000:
    #requirements.extend(['nose-machineout'])
    test_suite="py.test"

# handle python 3
if sys.version_info >= (3,):
    use_2to3 = True
else:
    use_2to3 = False

options = {}

#class PyTest(Command):
#    user_options = []
#    def initialize_options(self):
#        pass
#    def finalize_options(self):
#        pass
#    def run(self):
#        import sys,subprocess
#        errno = subprocess.call([sys.executable, 'tox'])
#        raise SystemExit(errno)

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)

setup(
	name = 'tendo',
	py_modules = ['tendo.colorer', 'tendo.execfile2', 'tendo.singleton', 'tendo.tee', 'tendo.unicode'],
	packages = ['tendo'],
	version = __version__,
	zip_safe = False,
	description = 'A Python library that extends some core functionality',
	author = 'Sorin Sbarnea',
	author_email = 'sorin.sbarnea@gmail.com',
	url = 'https://github.com/pycontribs/tendo',
	download_url = 'https://github.com/pycontribs/tendo/archives/master',
	keywords = ['tendo', 'tee', 'unicode', 'colorer', 'singleton'],
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.5',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Development Status :: 4 - Beta',
		'Environment :: Other Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Internet',
	],
	long_description = open('README.txt').read(),
	setup_requires=['six'], #,'nosexcover'],
	tests_require=test_requirements, # autopep8 removed because it does not install on python2.5
	test_suite=test_suite,
	cmdclass={'test':PyTest},
#	use_2to3 = use_2to3,
        **options
)
