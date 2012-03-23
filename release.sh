#!/bin/bash
echo "Please don't run this as a user. This generates a new release for PyPI. Press ^C to exit or Enter to continue."
read

#if ! python ./testsuite.py && [ "$IGNORE_TEST" != "yes" ]; then
if ! python -m unittest discover -v -c -p '*.py' -s tendo; then
	echo "The test suite failed. Fix it!"
	exit 1
fi

# pep8 tendo

# Clear old distutils stuff
rm -rf build dist MANIFEST &> /dev/null

# Build installers, etc. and upload to PyPI
# python setup.py register sdist bdist_wininst upload

#python setup.py register sdist build_sphinx upload upload_sphinx
python setup.py register sdist upload

