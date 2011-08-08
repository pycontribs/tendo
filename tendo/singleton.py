#! /usr/bin/env python -3 -t

import sys, os, errno, tempfile, unittest, logging
from multiprocessing import Process

class SingleInstance:
	"""
	If you want to prevent your script from running in parallel just instantiate SingleInstance() class. If is there another instance already running it will exist the application with the message "Another instance is already running, quitting.", returning -1 error code.

	>>> import tendo
	>>> me = SingleInstance()

	This option is very useful if you have scripts executed by crontab at small amounts of time.

	Remember that this works by creating a lock file with a filename based on the full path to the script file.
	"""
	def __init__(self):
		import sys
		self.lockfile = os.path.normpath(tempfile.gettempdir() + '/' +
		    os.path.splitext(os.path.abspath(__file__))[0].replace("/","-").replace(":","").replace("\\","-")  + '.lock')
		logging.debug("SingleInstance lockfile: " + self.lockfile)
		if sys.platform == 'win32':
			try:
				# file already exists, we try to remove (in case previous execution was interrupted)
				if os.path.exists(self.lockfile):
					os.unlink(self.lockfile)
				self.fd =  os.open(self.lockfile, os.O_CREAT|os.O_EXCL|os.O_RDWR)
			except OSError as e:
				if e.errno == 13:
					logging.error("Another instance is already running, quitting.")
					sys.exit(-1)
				print(e.errno)
				raise
		else: # non Windows
			import fcntl, sys
			self.fp = open(self.lockfile, 'w')
			try:
				fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
			except IOError:
				logging.warning("Another instance is already running, quitting.")
				sys.exit(-1)

	def __del__(self):
		import sys
		if sys.platform == 'win32':
			if hasattr(self, 'fd'):
				os.close(self.fd)
				os.unlink(self.lockfile)

def f():
	tmp = logging.getLogger().level
	logging.getLogger().setLevel(logging.CRITICAL) # we do not want to see the warning
	me2 = SingleInstance()
	logging.getLogger().setLevel(tmp)
	pass

class testSingleton(unittest.TestCase):
	def test_1(self):
		me = SingleInstance()
		pass
	def test_2(self):
		me = SingleInstance()
		p = Process(target=f)
		p.start()
		p.join()
		assert(not p.exitcode == 0) # the called function should fail because we already have another instance running
		# note, we return -1 but this translates to 255 meanwhile we'll consider that anything different from 0 is good

if __name__ == "__main__":
	logging.getLogger().setLevel(logging.DEBUG)
	unittest.main()

