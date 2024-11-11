import filecmp
import inspect
import os
import shutil
import tempfile

import pytest

from tendo.unicode import open


@pytest.fixture
def dir():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    return os.path.dirname(inspect.getfile(inspect.currentframe()))


def test_read_utf8(dir):
    mode = "r"
    f = open(os.path.join(dir, "assets/utf8.txt"), mode)
    f.readlines()
    f.close()
    assert True


def test_read_invalid_utf8(dir):
    with pytest.raises(UnicodeDecodeError):
        mode = "r"
        f = open(os.path.join(dir, "assets/utf8-invalid.txt"), mode)
        f.readlines()
        f.close()


def test_write_on_existing_utf8(dir):
    (ftmp, fname_tmp) = tempfile.mkstemp()
    shutil.copyfile(os.path.join(dir, "assets/utf8.txt"), fname_tmp)
    f = open(fname_tmp, "a")  # encoding not specified, should use utf-8
    f.write(
        "\u0061\u0062\u0063\u0219\u021b\u005f\u1e69\u0073\u0323\u0307\u0073\u0307\u0323\u005f\u0431\u0434\u0436\u005f\u03b1\u03b2\u03ce\u005f\u0648\u062a\u005f\u05d0\u05e1\u05dc\u005f\u6c38\U0002a6a5\u9eb5\U00020000",
    )
    f.close()
    passed = filecmp.cmp(
        os.path.join(dir, "assets/utf8-after-append.txt"),
        fname_tmp,
        shallow=False,
    )
    assert passed is True
    os.close(ftmp)
    os.unlink(fname_tmp)
