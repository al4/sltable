REPO?="testpypi"

default: dist

setup:
	python3 -m pip install --upgrade build tox twine

test: setup
	tox

dist: setup test
	python3 -m build

upload: dist
	python3 -m twine upload --repository $(REPO) dist/*

PHONY: test setup upload
