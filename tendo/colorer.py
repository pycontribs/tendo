#!/usr/bin/env python
# encoding: utf-8
# Author: sorin sbarnea
# License: public domain

"""
Colorer does enable colored logging messages by using `ANSI escape sequences <http://en.wikipedia.org/wiki/ANSI_escape_code>`_.

Under Windows, where the escapes are not supported it does use the Windows API.

The colored output is generated only when the console is a terminal supporting it, so if you redirect the output to a log file you will not see the escape codes in the file.

>>> import colorer, logging
... logging.error("red line")
... logging.warn("yellow line")
... logging.info("gray line")
... logging.debug("magenta line")
"""
import logging, sys, os

if (hasattr(sys.stderr, "isatty") and sys.stderr.isatty()) or \
        ('TERM' in os.environ.keys() and os.environ['TERM'] in ['linux'] ) or \
        ('PYCHARM_HOSTED' in os.environ.keys()):

	# Why stderr and not stdout? - because python logging module does output to stderr by default and not stdout.
	# now we patch Python code to add color support to logging.StreamHandler
	def add_coloring_to_emit_windows(fn):
			# add methods we need to the class
		def _out_handle(self):
			import ctypes
			return ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)

		def _set_color(self, code):
			import ctypes
			# Constants from the Windows API
			self.STD_OUTPUT_HANDLE = -11
			hdl = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
			ctypes.windll.kernel32.SetConsoleTextAttribute(hdl, code)

		setattr(logging.StreamHandler, '_set_color', _set_color)

		def new(*args):
			FOREGROUND_BLUE      = 0x0001 # text color contains blue.
			FOREGROUND_GREEN     = 0x0002 # text color contains green.
			FOREGROUND_RED       = 0x0004 # text color contains red.
			FOREGROUND_INTENSITY = 0x0008 # text color is intensified.
			FOREGROUND_WHITE     = FOREGROUND_BLUE|FOREGROUND_GREEN |FOREGROUND_RED
			# winbase.h
			STD_INPUT_HANDLE = -10
			STD_OUTPUT_HANDLE = -11
			STD_ERROR_HANDLE = -12

			# wincon.h
			FOREGROUND_BLACK     = 0x0000
			FOREGROUND_BLUE      = 0x0001
			FOREGROUND_GREEN     = 0x0002
			FOREGROUND_CYAN      = 0x0003
			FOREGROUND_RED       = 0x0004
			FOREGROUND_MAGENTA   = 0x0005
			FOREGROUND_YELLOW    = 0x0006
			FOREGROUND_GREY      = 0x0007
			FOREGROUND_INTENSITY = 0x0008 # foreground color is intensified.

			BACKGROUND_BLACK     = 0x0000
			BACKGROUND_BLUE      = 0x0010
			BACKGROUND_GREEN     = 0x0020
			BACKGROUND_CYAN      = 0x0030
			BACKGROUND_RED       = 0x0040
			BACKGROUND_MAGENTA   = 0x0050
			BACKGROUND_YELLOW    = 0x0060
			BACKGROUND_GREY      = 0x0070
			BACKGROUND_INTENSITY = 0x0080 # background color is intensified.     

			levelno = args[1].levelno
			if levelno>=50:
				color = BACKGROUND_YELLOW | FOREGROUND_RED | FOREGROUND_INTENSITY | BACKGROUND_INTENSITY 
			elif levelno>=40:
				color = FOREGROUND_RED | FOREGROUND_INTENSITY
			elif levelno>=30:
				color = FOREGROUND_YELLOW | FOREGROUND_INTENSITY
			elif levelno>=20:
				color = FOREGROUND_GREEN
			elif levelno>=10:
				color = FOREGROUND_MAGENTA
			else:
				color =  FOREGROUND_WHITE
			args[0]._set_color(color)

			ret = fn(*args)
			args[0]._set_color( FOREGROUND_WHITE )
			#print "after"
			return ret
		return new

	def add_coloring_to_emit_ansi(fn):
		# add methods we need to the class
		def new(*args):
			levelno = args[1].levelno
			if levelno>=50:
				color = '\x1b[31m' # red
			elif levelno>=40 :
				color = '\x1b[31m' # red
			elif levelno>=30 :
				color = '\x1b[33m' # yellow
			elif levelno>=20 :
				color = '\x1b[32m' # green 
			elif levelno>=10:
				color = '\x1b[35m' # pink
			else:
				color = '\x1b[0m' # normal
			args[1].msg = color + str(args[1].msg) +  '\x1b[0m'  # normal
			#print "after"
			return fn(*args)
		return new

	import platform
	if platform.system()=='Windows':
		# Windows does not support ANSI escapes and we are using API calls to set the console color
		logging.StreamHandler.emit = add_coloring_to_emit_windows(logging.StreamHandler.emit)
	else:
		# all non-Windows platforms are supporting ANSI escapes so we use them
		logging.StreamHandler.emit = add_coloring_to_emit_ansi(logging.StreamHandler.emit)
		#log = logging.getLogger()
		#log.addFilter(log_filter())
		#//hdlr = logging.StreamHandler()
		#//hdlr.setFormatter(formatter())

if __name__ == '__main__':
	import logging
	# import colorer
	# remember that logging outputs to stderr and not stdout (just in case you'll wonder)

	for param in os.environ.keys():
		print("%25s %s" % (param,os.environ[param]))

	isatty = None
	if hasattr(sys.stderr, "isatty"):
		isatty = sys.stderr.isatty()
	print("sys.stderr.isatty = %s" % isatty)

	isatty = None
	if hasattr(sys.stdout, "isatty"):
		isatty = sys.stdout.isatty()
	print("sys.stdout.isatty = %s" % isatty)

	logging.getLogger().setLevel(logging.NOTSET)
	logging.warn("a warning")
	logging.error("some error")
	logging.info("some info")
	logging.debug("some info")
