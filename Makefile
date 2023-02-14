
FORMAT=stylish
FILE_FORMAT=json
test_simple:
	poetry run gendiff ./tests/fixtures/file1.$(FILE_FORMAT) ./tests/fixtures/file2.$(FILE_FORMAT) --format $(FORMAT)

test_nested:
	poetry run gendiff ./tests/fixtures/file_nested1.$(FILE_FORMAT) ./tests/fixtures/file_nested2.$(FILE_FORMAT) --format $(FORMAT) > ./tests/fixtures/diff_$(FILE_FORMAT)_$(FORMAT).fixture

test:
	poetry run pytest ./tests/

lint:
	flake8
