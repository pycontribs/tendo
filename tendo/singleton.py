#! /usr/bin/env python

import sys, os, errno, tempfile, unittest, logging
from multiprocessing import Process

class SingleInstance:
	"""
	If you want to prevent your script from running in parallel just instantiate SingleInstance() class. If is there another instance already running it will exist the application with the message "Another instance is already running, quitting.", returning -1 error code.

	>>> import tendo
	... me = SingleInstance()

	This option is very useful if you have scripts executed by crontab at small amounts of time.

	Remember that this works by creating a lock file with a filename based on the full path to the script file.
	"""
	def __init__(self, flavor_id=""):
		import sys
		self.initialized = False
		self.lockfile = os.path.normpath(tempfile.gettempdir() + '/' +
		    os.path.splitext(os.path.abspath(sys.modules['__main__'].__file__))[0].replace("/","-").replace(":","").replace("\\","-")  + '-%s' % flavor_id +'.lock')
		logger.debug("SingleInstance lockfile: " + self.lockfile)
		if sys.platform == 'win32':
			try:
				# file already exists, we try to remove (in case previous execution was interrupted)
				if os.path.exists(self.lockfile):
					os.unlink(self.lockfile)
				self.fd =  os.open(self.lockfile, os.O_CREAT|os.O_EXCL|os.O_RDWR)
			except OSError:
				type, e, tb = sys.exc_info()
				if e.errno == 13:
					logger.error("Another instance is already running, quitting.")
					sys.exit(-1)
				print(e.errno)
				raise
		else: # non Windows
			import fcntl
			self.fp = open(self.lockfile, 'w')
			try:
				fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
			except IOError:
				logger.warning("Another instance is already running, quitting.")
				sys.exit(-1)
		self.initialized=True

	def __del__(self):
		import sys
		if not self.initialized: return
		try:
			if sys.platform == 'win32':
				if hasattr(self, 'fd'):
					os.close(self.fd)
					os.unlink(self.lockfile)
			else:
				import fcntl
				fcntl.lockf(self.fp, fcntl.LOCK_UN)
				#os.close(self.fp)
				if os.path.isfile(self.lockfile):
					os.unlink(self.lockfile)
		except Exception, e:
			logger.warning(e)
			sys.exit(-1)

def f():
	tmp = logger.level
	logger.setLevel(logging.CRITICAL) # we do not want to see the warning
	me2 = SingleInstance()
	logger.setLevel(tmp)
	pass

class testSingleton(unittest.TestCase):
	def test_1(self):
		me = SingleInstance()
		del me # now the lock should be removed
		assert True
	def test_2(self):
		p = Process(target=f)
		p.start()
		p.join()
		assert  p.exitcode == 0, "%s != 0" % p.exitcode # the called function should succeed
	def test_3(self):
		me = SingleInstance()
		p = Process(target=f)
		p.start()
		p.join()
		assert  p.exitcode != 0, "%s != 0 (2nd execution)" % p.exitcode # the called function should fail because we already have another instance running
		# note, we return -1 but this translates to 255 meanwhile we'll consider that anything different from 0 is good
		p = Process(target=f)
		p.start()
		p.join()
		assert  p.exitcode != 0, "%s != 0 (3rd execution)" % p.exitcode # the called function should fail because we already have another instance running

logger = logging.getLogger("tendo.singleton")
logger.addHandler(logging.StreamHandler())

if __name__ == "__main__":
	logger.setLevel(logging.DEBUG)
	unittest.main()

