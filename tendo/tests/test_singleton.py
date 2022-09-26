import logging
from multiprocessing import Process
import sys

from tendo.singleton import SingleInstance, SingleInstanceException

logger = logging.getLogger("tendo.singleton.test")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def f(name):
    tmp = logger.level
    logger.setLevel(logging.CRITICAL)  # we do not want to see the warning
    try:
        me2 = SingleInstance(flavor_id=name)  # noqa
    except SingleInstanceException:
        sys.exit(-1)
    logger.setLevel(tmp)
    pass


def test_1():
    me = SingleInstance(flavor_id="test-1")
    del me  # now the lock should be removed
    assert True


def test_2():
    p = Process(target=f, args=("test-2",))
    p.start()
    p.join()
    # the called function should succeed
    assert p.exitcode == 0, "%s != 0" % p.exitcode


def test_3():
    me = SingleInstance(flavor_id="test-3")  # noqa -- me should still kept
    p = Process(target=f, args=("test-3",))
    p.start()
    p.join()
    # the called function should fail because we already have another
    # instance running
    assert p.exitcode != 0, "%s != 0 (2nd execution)" % p.exitcode
    # note, we return -1 but this translates to 255 meanwhile we'll
    # consider that anything different from 0 is good
    p = Process(target=f, args=("test-3",))
    p.start()
    p.join()
    # the called function should fail because we already have another
    # instance running
    assert p.exitcode != 0, "%s != 0 (3rd execution)" % p.exitcode


def test_4():
    lockfile = '/tmp/foo.lock'
    me = SingleInstance(lockfile=lockfile)
    assert me.lockfile == lockfile
