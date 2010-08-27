#!/usr/bin/env python
# encoding: utf-8
# Author: sorin sbarnea
# License: public domain
from __future__ import print_function
from __future__ import unicode_literals
import logging, sys, subprocess, types, io, time

if sys.version_info[0] == 3:
    string_types = str,
else:
    string_types = basestring,

global logger
global stdout
global stderr
global timing
global log_command

logger = None
stdout = False
stderr = False
timing = True # print execution time of each command in the log, just after the return code
log_command = True # outputs the command being executed to the log (before command output)
_sentinel = object()

def quote_command(cmd):
	""" 
	This function does assure that the command line is entirely quoted.
	This is required in order to prevent getting "The input line is too long" error message.
	"""
	import re
	re_quoted_items = re.compile(r'" \s* [^"\s] [^"]* \"', re.VERBOSE)
	woqi = re_quoted_items.sub('', cmd)
	if len(cmd) == 0 or (len(woqi) > 0 and not (woqi[0] == '"' and woqi[-1] == '"')):
		return '"' + cmd + '"'    
	else:
		return cmd

def system2(cmd, cwd=None, logger=None, stdout=None, log_command=_sentinel, timing=_sentinel):
	#def tee(cmd, cwd=None, logger=tee_logger, console=tee_console):
	""" This is a simple placement for os.system() or subprocess.Popen()
	that simulates how Unix tee() works - logging stdout/stderr using logging

	If you specify file (name or handler) it will output to this file.

	For filenames, it will open them as text for append and use UTF-8 encoding

	If logger is an instance of
	* 'string' - it will assume it is a filename, open it and log to it
	* 'handle' - it just write to it
	* 'function' - it call it using the message
	
	This method return (returncode, output_lines_as_list)
	
	"""
	t = time.clock()
	output = []
	if log_command is _sentinel: log_command = globals().get('log_command')
	if timing is _sentinel: timing = globals().get('timing')
	
	if logger is None:
		logger = globals().get('logger')
	if stdout is None:
		stdout = globals().get('stdout')

	#logging.debug("logger=%s stdout=%s" % (logger, stdout))

	f = sys.stdout
	if not f.encoding or f.encoding == 'ascii':
	# `ascii` is not a valid encoding by our standards, it's better to output to UTF-8 because it can encoding any Unicode text
		encoding = 'utf_8'
	else:
		encoding = f.encoding

	def filelogger(msg):
		try:
			msg = msg + '\n'  # we'll use the same endline on all platforms, you like it or not
			f.write(msg.encode('utf_8'))
		except Exception as e:
			import traceback
			print('        ****** ERROR: Exception: %s\nencoding = %s' % (e, encoding))
			traceback.print_exc(file=sys.stderr)
			sys.exit(-1)
		pass

	def nop(msg):
		pass

	if not logger:
		mylogger = nop
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

	cmd = quote_command(cmd) # to prevent _popen() bug
	p = subprocess.Popen(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	if(log_command):
		mylogger("Running: %s" % cmd)
	while True:
		line = p.stdout.readline().decode(encoding)
		output.append(line)
		if not line:
			break
		line = line.rstrip('\n\r')
		mylogger(line) # they are added by logging anyway
		if(stdout):
			print(line)
	returncode = p.wait()
	if(log_command):
		if(timing):
			def secondsToStr(t):
				from functools import reduce
				return "%02d:%02d:%02d" % reduce(lambda ll,b : divmod(ll[0],b) + ll[1:], [(t*1000,),1000,60,60])[:3]
			mylogger("Returned: %d (execution time %s)\n" % (returncode, secondsToStr(time.clock()-t)))
		else:
			mylogger("Returned: %d\n" % (returncode))
	return(returncode, output)	
		
def system(cmd, cwd=None, logger=None, stdout=None, log_command=_sentinel, timing=_sentinel):
	""" System does not return a tuple """
	(returncode, output) = system2(cmd, cwd=cwd, logger=logger, stdout=stdout, log_command=log_command, timing=timing)
	return(returncode)

if __name__ == '__main__':
	import colorer
	import tempfile, os

	logging.basicConfig(level=logging.NOTSET,
		format='%(message)s')
	
	# default (stdout)	
	system("python --version")

	# function/method		
	system("python --version", logger=logging.error)

	# function (this is the same as default)
	system("python --version", logger=print)

	# handler
	f = tempfile.NamedTemporaryFile(delete=False)
	system("python --version", logger=f)
	f.close()
	os.unlink(f.name)

	# test with string (filename)
	(f, fname) = tempfile.mkstemp()
	print(fname)
	system("python --version", logger=fname)

	stdout = False
	logger = None
	system("echo test")

	stdout = True
	system("echo test2")
	
		
