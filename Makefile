FORMAT=stylish
FILE_FORMAT=json


.PHONY=check

test_simple:
	poetry run gendiff ./tests/fixtures/file1.$(FILE_FORMAT) ./tests/fixtures/file2.$(FILE_FORMAT) --format $(FORMAT)

test_nested:
	poetry run gendiff ./tests/fixtures/file_nested1.$(FILE_FORMAT) ./tests/fixtures/file_nested2.$(FILE_FORMAT) --format $(FORMAT) > ./tests/fixtures/diff_$(FILE_FORMAT)_$(FORMAT).fixture
	cat ./tests/fixtures/diff_$(FILE_FORMAT)_$(FORMAT).fixture

test:
	poetry run pytest ./tests/

test-coverage:
	poetry run pytest --cov --cov-report=xml ./tests/

lint:
	poetry run flake8

build:
	poetry build

check: test lint

install:
	poetry install

install-gendiff:
	pip install --force-reinstall ./dist/hexlet_code-0.1.0-py3-none-any.whl
