#!/usr/bin/env python
# Licensed to PSF under a Contributor Agreement.
# See http://www.python.org/psf/license for licensing details.

__author__  = "Sorin Sbarnea"
__copyright__ = "Copyright 2010-2012, Sorin Sbarnea"
__email__   = "sorin(dot)sbarnea(at)gmail.com"
__status__  = "Development"
__version__ = "0.0.17"
__date__    = "2012-10-04"

__all__ = ['tee','colorer','unicode','execfile2','singleton','ansiterm']

"""
	Tendo is tested with Python 2.5-3.2
"""

import sys
if sys.hexversion < 0x02050000:
	sys.exit("Python 2.5 or newer is required by tendo module.")
