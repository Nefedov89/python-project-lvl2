import json
from gendiff import generate_diff
from gendiff.src.decorators import string_replacer


FIXTURES_PATH_PREFIX = 'tests/fixtures/'


def setup_function(function):
    print(function)


@string_replacer(replace_from=['"', ','], replace_to='')
def get_correct_diff_as_str(file_path):
    parsed_file = json.load(open(file_path))

    return json.dumps(parsed_file, indent=4)


def _test_files_diff(test_case_fixtures_dir_name):
    files_dir_path = FIXTURES_PATH_PREFIX + test_case_fixtures_dir_name

    correct_diff = get_correct_diff_as_str(
        files_dir_path + '/correct_diff.json'
    )
    files_diff = generate_diff(
        files_dir_path + '/file1.json',
        files_dir_path + '/file2.json'
    )

    assert correct_diff == files_diff


def test_different_files_1():
    _test_files_diff('different_files_1')


def test_different_files_2():
    _test_files_diff('different_files_2')
