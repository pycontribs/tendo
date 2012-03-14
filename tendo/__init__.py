#!/usr/bin/env python -3 -t
# Licensed to PSF under a Contributor Agreement.
# See http://www.python.org/psf/license for licensing details.

__author__  = "Sorin Sbarnea"
__copyright__ = "Copyright 2010-2011, Sorin Sbarnea"
__email__   = "sorindotsbarnea@gmail.com"
__status__  = "Development"
__version__ = "0.0.10"
__date__    = "2012-03-14"

__all__ = ['tee','colorer','unicode','execfile2','singleton']

"""
	Tendo is tested with Python 2.5-3.2
"""

import sys
if sys.hexversion < 0x02050000:
	sys.exit("Python 2.5 or newer is required by tendo module.")
