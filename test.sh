#!/bin/bash

#if ! python ./testsuite.py && [ "$IGNORE_TEST" != "yes" ]; then
if ! python -m unittest discover -v -c -p '*.py' -s tendo; then
	echo "The test suite failed. Fix it!"
	exit 1
fi

# pep8 tendo
