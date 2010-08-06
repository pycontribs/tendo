#!/usr/bin/python
import codecs, sys, types, unittest

# Author: Sorin Sbarnea <ssbarnea@adobe.com>

# This file does add some additional Unicode support to Python, like:
# * auto-detect BOM on text-file open: open(file, "r") and open(file, "rU")

# we save the file function handler because we want to override it
open_old = open

def open(filename, mode=None, bufsize=None, fallback_encoding='utf_8'):
	#try:
		# we read the first 4 bytes just to be sure we use the right encoding
		if(mode == "r" or mode == "rU"): # we are interested of detecting the mode only for read text
			f = open_old(filename, "rb")
			aBuf = f.read(4)
			if aBuf[:3] ==   b'\xEF\xBB\xBF' :
				f = codecs.open(filename, mode, "utf_8")
				f.seek(3,0)
				f.BOM = codecs.BOM_UTF8
			elif aBuf[:2] == b'\xFF\xFE':
				f = codecs.open(filename, mode, "utf_16_le")
				f.seek(2,0)
				f.BOM = codecs.BOM_UTF16_LE
			elif aBuf[:2] == b'\xFE\xFF':
				f = codecs.open(filename, mode, "utf_16_be")
				f.seek(2,0)
				f.BOM = codecs.BOM_UTF16_BE
			elif aBuf[:4] == b'\xFF\xFE\x00\x00':
				f = codecs.open(filename, mode, "utf_32_le")
				f.seek(4,0)
				f.BOM = codecs.BOM_UTF32_LE
			elif aBuf[:4] == b'\x00\x00\xFE\xFF': 
				f = codecs.open(filename, mode, "utf_32_be")
				f.seek(4,0)
				f.BOM = codecs.BOM_UTF32_BE
			else:  # we assume that if there is no BOM, the encoding is UTF-8
				f.close()
				f = codecs.open(filename, mode, fallback_encoding)
				f.seek(0)
				f.BOM = None
			return f
		else:
			return open_old(filename, mode, bufsize)

class testUnicode(unittest.TestCase):
	def test_read_utf8(self):
		try:
			f = open("tests/utf8.txt","rU")
			r = f.readlines()
			f.close()
		except Exception as e:
			self.assertTrue(False, "Unable to properly read valid utf8 encoded file.")
	def test_read_invalid_utf8(self):
		passed = False
		try:
			f = open("tests/utf8-invalid.txt","rU")
			r = f.readlines()
			f.close()
		except Exception as e:
			if isinstance(e, UnicodeDecodeError):
				passed = True # yes, we expect an exception
			pass
		self.assertTrue(passed, "Unable to detect invalid utf8 file")		

if __name__ == '__main__':
	unittest.main()

	#lines = open("test/utf8.txt","rU")
	
	#for line in lines:
	#	print(line)

