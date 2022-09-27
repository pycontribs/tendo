import inspect
import pytest
import tempfile
import six
import os
import filecmp
import shutil


@pytest.fixture
def dir():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    return os.path.dirname(inspect.getfile(inspect.currentframe()))


def test_read_utf8(dir):
    if six.PY2:
        mode = "rU"
    else:
        mode = "r"
    f = open(os.path.join(dir, "assets/utf8.txt"), mode)
    f.readlines()
    f.close()
    assert True


def test_read_invalid_utf8(dir):
    with pytest.raises(UnicodeDecodeError):
        if six.PY2:
            mode = "rU"
        else:
            mode = "r"
        f = open(os.path.join(dir, "assets/utf8-invalid.txt"), mode)
        f.readlines()
        f.close()


def test_write_on_existing_utf8(dir):
    (ftmp, fname_tmp) = tempfile.mkstemp()
    shutil.copyfile(os.path.join(dir, "assets/utf8.txt"), fname_tmp)
    f = open(fname_tmp, "a")  # encoding not specified, should use utf-8
    f.write(six.u(
        "\u0061\u0062\u0063\u0219\u021B\u005F\u1E69\u0073\u0323\u0307\u0073\u0307\u0323\u005F\u0431\u0434\u0436\u005F\u03B1\u03B2\u03CE\u005F\u0648\u062A\u005F\u05D0\u05E1\u05DC\u005F\u6C38\U0002A6A5\u9EB5\U00020000"))
    f.close()
    passed = filecmp.cmp(
        os.path.join(dir, "assets/utf8-after-append.txt"), fname_tmp, shallow=False)
    assert passed is True
    os.close(ftmp)
    os.unlink(fname_tmp)
