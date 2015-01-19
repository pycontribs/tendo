#!/usr/bin/env python
# Setuptools is required for the use_2to3 option below. You should install it
# from the Distribute home page, http://packages.python.org/distribute/
from __future__ import absolute_import

import inspect
import logging
import os
import sys

from setuptools import setup, Command
from setuptools.command.test import test as TestCommand

NAME = "tendo"

from tendo.version import __version__

# Hack to prevent stupid "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when running `python
# setup.py test` (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing
except ImportError:
    pass


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

        FORMAT = '%(levelname)-10s %(message)s'
        logging.basicConfig(format=FORMAT)
        logging.getLogger().setLevel(logging.INFO)

        # if we have pytest-cache module we enable the test failures first mode
        try:
            import pytest_cache
            self.pytest_args.append("--ff")
        except ImportError:
            pass

        # try:
        #     import pytest_instafail
        #     self.pytest_args.append("--instafail")
        # except ImportError:
        #     pass
        self.pytest_args.append("-s")

        if sys.stdout.isatty():
            # when run manually we enable fail fast
            self.pytest_args.append("--maxfail=2")

        try:
            import coveralls
            self.pytest_args.append("--cov=%s" % NAME)
            self.pytest_args.extend(["--cov-report", "xml"])

        except ImportError:
            pass

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # before running tests we need to run autopep8
        r = os.system(
            "python -m autopep8 -r --in-place %s/ examples/" % NAME)
        if r:
            raise Exception("autopep8 failed")

        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class Release(Command):
    user_options = []

    def initialize_options(self):
        # Command.initialize_options(self)
        pass

    def finalize_options(self):
        # Command.finalize_options(self)
        pass

    def run(self):
        import json
        try:
            from urllib.request import urlopen
        except ImportError:
            from urllib2 import urlopen
        response = urlopen(
            "http://pypi.python.org/pypi/%s/json" % NAME).read().decode('utf-8')
        data = json.loads(response)
        released_version = data['info']['version']
        if released_version == __version__:
            raise RuntimeError(
                "This version was already released, remove it from PyPi if you want to release it again or increase the version number. http://pypi.python.org/pypi/%s/" % NAME)
        elif released_version > __version__:
            raise RuntimeError("Cannot release a version (%s) smaller than the PyPI current release (%s)." % (
                __version__, released_version))

        sys.exit()

setup(
    name=NAME,
    py_modules=['tendo.colorer', 'tendo.execfile2', 'tendo.singleton',
                'tendo.tee', 'tendo.unicode', 'tendo.version'],
    version=__version__,
    cmdclass={'test': PyTest, 'release': Release},
    packages=[NAME],

    zip_safe=False,
    setup_requires=['six'],
    tests_require=['pep8>=0.6', 'py>=1.4.15', 'pytest', 'six', 'sphinx'],
    test_suite="py.test",
    maintainer='Sorin Sbarnea',
    maintainer_email='sorin.sbarnea@gmail.com',
    license='Python',
    description='A Python library that extends some core functionality',

    long_description=open("README.rst").read(),
    author='Sorin Sbarnea',
    author_email='sorin.sbarnea@gmail.com',
    platforms=['any'],
    url='https://github.com/pycontribs/tendo',
    download_url='https://github.com/pycontribs/tendo/archives/master',
    bugtrack_url='https://github.com/pycontribs/tendo/issues',
        home_page='https://github.com/pycontribs/tendo',
    keywords=['tendo', 'tee', 'unicode', 'colorer', 'singleton'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
    ],
)
