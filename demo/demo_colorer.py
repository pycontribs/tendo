#!/usr/bin/env python
# encoding: utf-8
# Author: sorin sbarnea
# License: public domain

from tendo import colorer

if __name__ == '__main__':
    import logging

    logging.getLogger().setLevel(logging.NOTSET)
    logging.warn("a warning")
    logging.error("some error")
    logging.info("some info")
    logging.debug("some info")
