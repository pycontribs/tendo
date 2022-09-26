
import os
import tempfile

from tendo.execfile2 import execfile2


def exec_py_code(code, cmd=None):
    (ftmp, fname_tmp) = tempfile.mkstemp()
    f = open(fname_tmp, "w")  # encoding not specified, should use utf-8
    f.write(code)
    f.close()
    exit_code = execfile2(fname_tmp, cmd=cmd, quiet=True)
    os.close(ftmp)
    os.unlink(fname_tmp)
    return exit_code


def test_normal_execution():
    exit_code = exec_py_code("")
    assert exit_code == 0


def test_bad_code():
    exit_code = exec_py_code("bleah")
    assert exit_code == 1


def test_sys_exit_0():
    exit_code = exec_py_code("import sys; sys.exit(0)")
    assert exit_code == 0


def test_sys_exit_5():
    exit_code = exec_py_code("import sys; sys.exit(5)")
    assert exit_code == 5


def test_sys_exit_text():
    exit_code = exec_py_code("import sys; sys.exit('bleah')")
    assert exit_code == 1


def test_raised_exception():
    exit_code = exec_py_code("raise Exception('bleah')")
    assert exit_code == 1


def test_command_line():
    exit_code = exec_py_code(
        "import sys\nif len(sys.argv)==2 and sys.argv[1]=='doh!': sys.exit(-1)", cmd="doh!")
    assert exit_code == -1
