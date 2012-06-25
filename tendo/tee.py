#!/usr/bin/env python
# encoding: utf-8
# Author: sorin sbarnea
# License: public domain
import codecs
import functools
import logging
import os
import sys
import subprocess
import types
import time
import unittest

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
    if not (os.name == "nt" or os.name == "dos"):
        return cmd # the escaping is required only on Windows platforms, in fact it will break cmd line on others
    if '"' in cmd[1:-1]:
        cmd =  '"' + cmd + '"'
    return cmd

def system2(cmd, cwd=None, logger=_sentinel, stdout=_sentinel, log_command=_sentinel, timing=_sentinel):
    #def tee(cmd, cwd=None, logger=tee_logger, console=tee_console):
    """ Works exactly like :func:`system` but it returns both the exit code and the output as a list of lines.

    This method returns a tuple: (return_code, output_lines_as_list). The return code of 0 means success.
    """
    t = time.clock()
    output = []
    if log_command is _sentinel: log_command = globals().get('log_command')
    if timing is _sentinel: timing = globals().get('timing')

    if logger is _sentinel: # default to python native logger if logger parameter is not used
        logger = globals().get('logger')
    if stdout is _sentinel:
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
            msg += '\n'  # we'll use the same endline on all platforms, you like it or not
            try:
                f.write(msg)
            except TypeError:
                f.write(msg.encode("utf-8"))
        except Exception:
            type, e, tb = sys.exc_info()
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
        f = codecs.open(logger, "a+b", 'utf_8')
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

    if cwd is not None and not os.path.isdir(cwd):
        os.makedirs(cwd) # this throws exception if fails

    cmd = quote_command(cmd) # to prevent _popen() bug
    p = subprocess.Popen(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if log_command:
        mylogger("Running: %s" % cmd)
    while True:
        line=""
        try:
            line = p.stdout.readline()
            line = line.decode(encoding)
        except Exception:
            type, e, tb = sys.exc_info()
            logging.error(e)
            logging.error("The output of the command could not be decoded as %s\ncmd: %s\n line ignored: %s" %\
                (encoding, cmd, repr(line)))
            pass

        output.append(line)
        if not line:
            break
        line = line.rstrip('\n\r')
        mylogger(line) # they are added by logging anyway
        if stdout :
            print(line)
    returncode = p.wait()
    if log_command :
        if timing:
            def secondsToStr(t):
                return time.strftime('%H:%M:%S', time.gmtime(t))
            mylogger("Returned: %d (execution time %s)\n" % (returncode, secondsToStr(time.clock()-t)))
        else:
            mylogger("Returned: %d\n" % returncode)

    if not returncode == 0: # running a tool that returns non-zero? this deserves a warning
        logging.warning("Returned: %d from: %s\nOutput %s" % (returncode, cmd, '\n'.join(output)))

    return returncode, output

def system(cmd, cwd=None, logger=None, stdout=None, log_command=_sentinel, timing=_sentinel):
    """ This works similar to :py:func:`os.system` but add some useful optional parameters.

    * ``cmd`` - command to be executed
    * ``cwd`` - optional working directory to be set before running cmd
    * ``logger`` - None, a filename, handle or a function like print or :py:meth:`logging.Logger.warning`
    
    Returns the exit code reported by the execution of the command, 0 means success.

    >>> import os, logging
    ... import tendo.tee
    ... tee.system("echo test", logger=logging.error)  # output using python logging
    ... tee.system("echo test", logger="log.txt")  # output to a file
    ... f = open("log.txt", "w")
    ... tee.system("echo test", logger=f) # output to a filehandle
    ... tee.system("echo test", logger=print) # use the print() function for output
    """
    (returncode, output) = system2(cmd, cwd=cwd, logger=logger, stdout=stdout, log_command=log_command, timing=timing)
    return returncode

class testTee(unittest.TestCase):
    def test_1(self):
        """

                               CMD      os.system()
           1  sort /?             ok          ok
           2  "sort" /?           ok          ok
           3  sort "/?"           ok          ok
           4  "sort" "/?"         ok         [bad]
           5  ""sort /?""         ok          [bad]
           6  "sort /?"          [bad]         ok
           7  "sort "/?""        [bad]         ok
           8 ""sort" "/?""       [bad]           ok

"""

        quotes = {
            'dir >nul': 'dir >nul',
            'cd /D "C:\\Program Files\\"':'"cd /D "C:\\Program Files\\""',
            'python -c "import os" dummy':'"python -c "import os" dummy"',
            'sort':'sort',
        }

        # we fake the os name because we want to run the test on any platform
        save = os.name
        os.name = 'nt'

        for key, value in quotes.items():
            resulted_value = quote_command(key)
            self.assertEqual(value, resulted_value, "Returned <%s>, expected <%s>" % (resulted_value, value))
            #ret = os.system(resulted_value)
            #if not ret==0:
            #    print("failed")
        os.name = save

if __name__ == '__main__':
    import os
    unittest.main()
    #import pytest
    #pytest.main(['--pyargs', __name__])
    """
    import colorer
    import tempfile, os

    logging.basicConfig(level=logging.NOTSET,
        format='%(message)s')

    # default (stdout)
    print("#1")
    system("python --version")

    # function/method
    print("#2")
    system("python --version", logger=logging.error)

    # function (this is the same as default)
    print("#3")
    system("python --version", logger=print)

    # handler
    print("#4")
    f = tempfile.NamedTemporaryFile()
    system("python --version", logger=f)
    f.close()

    # test with string (filename)
    print("#5")
    (f, fname) = tempfile.mkstemp()
    system("python --version", logger=fname)
    os.close(f)
    os.unlink(fname)

    print("#6")
    stdout = False
    logger = None
    system("echo test")

    print("#7")
    stdout = True
    system("echo test2")

"""