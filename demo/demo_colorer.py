#!/usr/bin/env python
# encoding: utf-8

from tendo import colorer   # noqa

if __name__ == '__main__':
    import logging

    logging.getLogger().setLevel(logging.NOTSET)
    logging.warn("a warning")
    logging.error("some error")
    logging.info("some info")
    logging.debug("some info")
