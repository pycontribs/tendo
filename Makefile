all: test

prepare:
	pip install --user -r requirements-dev.txt
	pip install --user -r requirements.txt

test: prepare
	python setup.py --version
	python setup.py --name
	python -m tox -e lint
	python setup.py test
