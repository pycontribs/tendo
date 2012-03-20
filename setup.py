#!/usr/bin/env python
# Setuptools is required for the use_2to3 option below. You should install it
# from the Distribute home page, http://packages.python.org/distribute/
import sys
from setuptools import setup
from tendo import __version__


options = {}

setup(
	name = 'tendo',
	py_modules = ['tendo.colorer', 'tendo.execfile2', 'tendo.singleton', 'tendo.tee', 'tendo.unicode'],
	version = __version__,
	description = 'A Python library that extends some core functionality',
	author = 'Sorin Sbarnea',
	author_email = 'sorin.sbarnea@gmail.com',
	url = 'https://github.com/ssbarnea/tendo',
	download_url = 'https://github.com/ssbarnea/tendo/archives/master',
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
        **options
)
  