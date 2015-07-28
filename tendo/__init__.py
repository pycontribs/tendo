#!/usr/bin/env python
# Licensed to PSF under a Contributor Agreement.
# See http://www.python.org/psf/license for licensing details.
from __future__ import absolute_import

__author__ = "Sorin Sbarnea"
__copyright__ = "Copyright 2010-2013, Sorin Sbarnea"
__email__ = "sorin(dot)sbarnea(at)gmail.com"
__status__ = "Production"
from .version import __version__
import sys
__date__ = "2015-07-28"

__all__ = ['tee', 'colorer', 'unicode',
           'execfile2', 'singleton', 'ansiterm', 'version']

"""
Tendo is tested with Python 2.5-3.3
"""

if sys.hexversion < 0x02050000:
    sys.exit("Python 2.5 or newer is required by tendo module.")
