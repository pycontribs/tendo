import logging
import sys
import tempfile


def test_colorer():
    isatty = None
    if hasattr(sys.stderr, "isatty"):
        isatty = sys.stderr.isatty()
    print("sys.stderr.isatty = %s" % isatty)

    isatty = None
    if hasattr(sys.stdout, "isatty"):
        isatty = sys.stdout.isatty()
    print("sys.stdout.isatty = %s" % isatty)

    logging.getLogger().setLevel(logging.NOTSET)
    tmp_file = tempfile.NamedTemporaryFile(suffix='_colorer.log').name
    fh = logging.FileHandler(tmp_file)
    fh.setLevel(logging.NOTSET)
    ch = logging.StreamHandler()
    ch.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)
    logging.getLogger().addHandler(fh)

    logging.warning("a warning")
    logging.error("some error")
    logging.info("some info")
    logging.debug("some info")
    expected_lines = ['WARNING: a warning\n', 'ERROR: some error\n', 'INFO: some info\n', 'DEBUG: some info\n']
    line_no = 0
    for line in open(tmp_file).readlines():
        assert(line == expected_lines[line_no])
        line_no += 1
