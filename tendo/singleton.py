#!/usr/bin/env python -3 -t

import sys, os, errno, tempfile, unittest

class SingleInstance:
	def __init__(self):
		import sys
		self.lockfile = os.path.normpath(tempfile.gettempdir() + '/' + os.path.basename(__file__) + '.lock')
		if sys.platform == 'win32':
			try:
				# file already exists, we try to remove (in case previous execution was interrupted)
				if os.path.exists(self.lockfile):
					os.unlink(self.lockfile)
				self.fd =  os.open(self.lockfile, os.O_CREAT|os.O_EXCL|os.O_RDWR)
			except OSError as e:
				if e.errno == 13:
					print("Another instance is already running, quitting.")
					sys.exit(-1)
				print(e.errno)
				raise
		else: # non Windows
			import fcntl, sys
			self.fp = open(self.lockfile, 'w')
			try:
				fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
			except IOError:
				print("Another instance is already running, quitting.")
				sys.exit(-1)

	def __del__(self):
		import sys
		if sys.platform == 'win32':
			if hasattr(self, 'fd'):
				os.close(self.fd)
				os.unlink(self.lockfile)


class testSingleton:
	def test_1(self):
		me = SingleInstance()
		pass

if __name__ == "__main__":
	unittest.main()

