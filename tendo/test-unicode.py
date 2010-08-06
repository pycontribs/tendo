#!/usr/bin/python
import codecs, sys, types, unittest
import unicode

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
