#!/bin/bash
set -e
if ! python setup.py test; then
	echo "The test suite failed. Fix it!"
	exit 1
fi

echo "Please don't run this as a user. This generates a new release for PyPI. Press ^C to exit or Enter to continue."
read

# pep8 tendo

# Clear old distutils stuff
rm -rf build dist MANIFEST &> /dev/null

# Build installers, etc. and upload to PyPI
# python setup.py register sdist bdist_wininst upload

#python setup.py register sdist build_sphinx upload upload_sphinx
python setup.py register -r http://testpypi.python.org/pypi
python setup.py sdist upload -r http://testpypi.python.org/pypi




