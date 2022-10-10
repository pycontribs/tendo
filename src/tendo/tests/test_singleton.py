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
        with SingleInstance(flavor_id=name):
            pass
    except SingleInstanceException:
        sys.exit(-1)
    logger.setLevel(tmp)


def test_singleton_from_script():
    with SingleInstance(flavor_id="test-1"):
        pass
    # now the lock should be removed
    assert True


def test_singleton_from_process():
    p = Process(target=f, args=("test-2",))
    p.start()
    p.join()
    # the called function should succeed
    assert p.exitcode == 0, "%s != 0" % p.exitcode


def test_multiple_singletons_from_process():
    with SingleInstance(flavor_id="test-3"):
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


def test_singleton_lock_file():
    lockfile = '/tmp/foo.lock'
    with SingleInstance(lockfile=lockfile) as me:
        print(me)
        assert me.lockfile == lockfile
