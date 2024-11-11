#!/usr/bin/env python
# Licensed to PSF under a Contributor Agreement.
# See http://www.python.org/psf/license for licensing details.
import sys

from ._version import __version__

__author__ = "Sorin Sbarnea"
__copyright__ = "Copyright 2010-2024, Sorin Sbarnea"
__email__ = "sorin.sbarnea@gmail.com"
__status__ = "Production"
__all__ = (
    "tee",
    "unicode",
    "execfile2",
    "singleton",
    "__version__",
)


if sys.hexversion < 0x030A0000:
    sys.exit("Python 3.10 or newer is required by tendo module.")
