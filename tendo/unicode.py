#!/usr/bin/python
import codecs
import inspect
import logging
import os
import sys
import tempfile
import unittest

import six
"""
Author: Sorin Sbarnea

This file does add some additional Unicode support to Python, like:
* auto-detect BOM on text-file open: open(file, "r") and open(file, "rU")

"""
# we save the file function handler because we want to override it
open_old = open


def open(filename, mode='r', bufsize=-1, fallback_encoding='utf_8'):
    """This replaces Python original function with an improved version that is Unicode aware.

    The new `open()` does change behaviour only for text files, not binary.

    * mode is by default 'r' if not specified and text mode
    * negative bufsize makes it use the default system one (same as not specified)

    >>> import tendo.unicode
    ... f = open("file-with-unicode-content.txt")
    ... content = f.read() # Unicode content of the file, without BOM

    Shortly by importing unicode, you will repair code that previously was broken when the input files were Unicode.

    This will not change the behavior of  code that reads the files as binary, it has an effect on text file operations.

    Files with BOM will be read properly as Unicode and the BOM will not be part of the text.

    If you do not specify the fallback_encoding, files without BOM will be read as `UTF-8` instead of `ascii`.
    """
    # Do not assign None to bufsize or mode because calling original open will
    # fail

    # we read the first 4 bytes just to be sure we use the right encoding
    # we are interested of detecting the mode only for read text
    if "r" in mode or "a" in mode:
        try:
            f = open_old(filename, "rb")
            aBuf = bytes(f.read(4))
            f.close()
        except Exception:
            aBuf = six.b('')
        if six.binary_type(aBuf[:3]) == six.b('\xEF\xBB\xBF'):
            f = codecs.open(filename, mode, "utf_8")
            f.seek(3, 0)
            f.BOM = codecs.BOM_UTF8
        elif six.binary_type(aBuf[:2]) == six.b('\xFF\xFE'):
            f = codecs.open(filename, mode, "utf_16_le")
            f.seek(2, 0)
            f.BOM = codecs.BOM_UTF16_LE
        elif six.binary_type(aBuf[:2]) == six.b('\xFE\xFF'):
            f = codecs.open(filename, mode, "utf_16_be")
            f.seek(2, 0)
            f.BOM = codecs.BOM_UTF16_BE
        elif six.binary_type(aBuf[:4]) == six.b('\xFF\xFE\x00\x00'):
            f = codecs.open(filename, mode, "utf_32_le")
            f.seek(4, 0)
            f.BOM = codecs.BOM_UTF32_LE
        elif six.binary_type(aBuf[:4]) == six.b('\x00\x00\xFE\xFF'):
            f = codecs.open(filename, mode, "utf_32_be")
            f.seek(4, 0)
            f.BOM = codecs.BOM_UTF32_BE
        else:  # we assume that if there is no BOM, the encoding is UTF-8
            f = codecs.open(filename, mode, fallback_encoding)
            f.seek(0)
            f.BOM = None
        return f
    else:
        import traceback
        logging.warning(
            "Calling unicode.open(%s,%s,%s) that may be wrong." % (filename, mode, bufsize))
        traceback.print_exc(file=sys.stderr)

        return open_old(filename, mode, bufsize)


class testUnicode(unittest.TestCase):

    def setUp(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.dir = os.path.dirname(inspect.getfile(inspect.currentframe()))

    def test_read_utf8(self):
        try:
            f = open(os.path.join(self.dir, "tests/utf8.txt"), "rU")
            f.readlines()
            f.close()
        except Exception:
            type, e, tb = sys.exc_info()
            self.assertTrue(
                False, "Unable to properly read valid utf8 encoded file: " + e)

    def test_read_invalid_utf8(self):
        passed = False
        try:
            f = open(os.path.join(self.dir, "tests/utf8-invalid.txt"), "rU")
            f.readlines()
            f.close()
        except Exception:
            type, e, tb = sys.exc_info()
            if isinstance(e, UnicodeDecodeError):
                passed = True  # yes, we expect an exception
            pass
        self.assertTrue(passed, "Unable to detect invalid utf8 file")

    def test_write_on_existing_utf8(self):
        import filecmp
        import shutil
        (ftmp, fname_tmp) = tempfile.mkstemp()
        shutil.copyfile(os.path.join(self.dir, "tests/utf8.txt"), fname_tmp)
        f = open(fname_tmp, "a")  # encoding not specified, should use utf-8
        f.write(six.u(
            "\u0061\u0062\u0063\u0219\u021B\u005F\u1E69\u0073\u0323\u0307\u0073\u0307\u0323\u005F\u0431\u0434\u0436\u005F\u03B1\u03B2\u03CE\u005F\u0648\u062A\u005F\u05D0\u05E1\u05DC\u005F\u6C38\U0002A6A5\u9EB5\U00020000"))
        f.close()
        passed = filecmp.cmp(
            os.path.join(self.dir, "tests/utf8-after-append.txt"), fname_tmp, shallow=False)
        self.assertTrue(
            passed, "Appending to existing UTF-8 file test failed (%s)." % fname_tmp)
        os.close(ftmp)
        os.unlink(fname_tmp)


if __name__ == '__main__':
    unittest.main()
