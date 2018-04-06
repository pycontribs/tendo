#!/usr/bin/env python
# Licensed to PSF under a Contributor Agreement.
# See http://www.python.org/psf/license for licensing details.
from __future__ import absolute_import
import sys

from pbr.version import VersionInfo


_v = VersionInfo('tendo').semantic_version()
__version__ = _v.release_string()
version_info = _v.version_tuple()

__author__ = "Sorin Sbarnea"
__copyright__ = "Copyright 2010-2018, Sorin Sbarnea"
__email__ = "sorin.sbarnea@gmail.com"
__status__ = "Production"
__all__ = ('tee', 'colorer', 'unicode',
           'execfile2', 'singleton', 'ansiterm', '__version__')


if sys.hexversion < 0x02050000:
    sys.exit("Python 2.5 or newer is required by tendo module.")
