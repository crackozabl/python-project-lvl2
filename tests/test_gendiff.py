import pytest
import gendiff


@pytest.fixture()
def path1():
    return "tests/fixtures/file_nested1.yml"


@pytest.fixture()
def path2():
    return "tests/fixtures/file_nested2.yml"


def get_fixture_content(name):
    with open(f'tests/fixtures/{name}.fixture', 'r') as f:
        return f.read()


@pytest.fixture()
def diff_simple_stylish():
    return get_fixture_content('diff_file1_json_file2_json_stylish')


@pytest.mark.parametrize(
    'path1, path2, format_, diff_fixture',
    [
        ("path1", "path2", "json", 'diff_yml_json'),
        ("path1", "path2", "stylish", 'diff_yml_stylish'),
        ("path1", "path2", "plain", 'diff_yml_plain')
    ],
    indirect=["path1", "path2"])
def test_gendiff(path1, path2, format_, diff_fixture):
    diff = get_fixture_content(diff_fixture)
    assert gendiff.generate_diff(path1, path2, format_) == diff
