#!/usr/bin/env python
# encoding: utf-8
# Author: sorin sbarnea
# License: public domain
from __future__ import print_function
from __future__ import unicode_literals
import logging, sys, subprocess, types, io

if sys.version_info[0] == 3:
    string_types = str,
else:
    string_types = basestring,

def tee(cmd, cwd=None, logger=None, console=True):
	""" This is a simple placement for os.system() or subprocess.Popen()
	that simulates how Unix tee() works - logging stdout/stderr using logging

	If you specify file (name or handler) it will output to this file.

	For filenames, it will open them as text for append and use UTF-8 encoding

	If logger is an instance of
	* 'string' - it will assume it is a filename, open it and log to it
	* 'handle' - it just write to it
	* 'function' - it call it using the message
	
	"""
	f = sys.stdout
	if not f.encoding:
		encoding = 'utf_8'
	else:
		encoding = f.encoding

	def filelogger(msg):
		f.write(msg + '\n') # we'll use the same endline on all platforms, you like it or not
		pass

	if not logger:
		mylogger = print
	elif isinstance(logger, string_types):
		f = open(logger, "at+")
		mylogger = filelogger
	elif isinstance(logger, (types.FunctionType, types.MethodType, types.BuiltinFunctionType)):
		mylogger = logger
	else:
		method_write = getattr(logger, "write", None)
		# if we can call write() we'll aceppt it :D
		if hasattr(method_write,'__call__'): # this should work for filehandles
			f = logger
			mylogger = filelogger
		else:
			sys.exit("tee() does not support this type of logger=%s" % type(logger))

	p = subprocess.Popen(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	while True:
		line = p.stdout.readline().decode(encoding)
		if not line:
			break
		line = line.rstrip('\n\r')
		mylogger(line) # they are added by logging anyway
		if(console):
			print(line)
	return p.wait()


if __name__ == '__main__':
	import colorer
	import tempfile, os

	logging.basicConfig(level=logging.NOTSET,
		format='%(message)s')
	
	# default (console)	
	tee("python --version")

	# function/method		
	tee("python --version", logger=logging.error)

	# function (this is the same as default)
	tee("python --version", logger=print)

	# handler
	f = tempfile.NamedTemporaryFile(delete=False)
	tee("python --version", logger=f)
	f.close()
	os.unlink(f.name)

	# test with string (filename)
	(f, fname) = tempfile.mkstemp()
	print(fname)
	tee("python --version", logger=fname)
	
	
