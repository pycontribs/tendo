#!/bin/bash

set -e


sudo easy_install -q nose_machineout nose_exclude yanc xtraceback
sudo easy_install-2.6 -q nose_machineout nose_exclude yanc xtraceback
sudo easy_install-2.5 -q nose_exclude yanc # xtraceback

# python python3 python3.0 python3.1 python3.2
for CMD in python2.5 python2.6 python2.7
do
    echo "using '$CMD'"
    $CMD -V >/dev/null 2>&1 || { echo "$CMD not found, skipping."; continue;};

#    if ! $CMD -m unittest discover -v -c -p '*.py' -s tendo; then
    if ! $CMD setup.py test; then
	echo "The test suite failed. Fix it!"
	exit 1
    fi

done

# pep8 tendo
