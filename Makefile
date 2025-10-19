.PHONY: install test run lint

install:
	pip install -r requirements.txt

test:
	pytest -q

run:
	python -m app.cli --help

