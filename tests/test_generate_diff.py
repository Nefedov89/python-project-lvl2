import json
from gendiff import generate_diff
from gendiff.src.decorators import string_replacer
from gendiff.src.file_parser import file_formats


FIXTURES_PATH_PREFIX = './tests/fixtures'


def setup_function(function):
    print(function)


@string_replacer(replace_from=['"', ','], replace_to='')
def get_correct_diff_as_str(file_path):
    parsed_file = json.load(open(file_path))

    return json.dumps(parsed_file, indent=4)


def _test_files_diff(test_case_fixtures_dir_name):
    for file_format in file_formats:
        files_examples_dir_path = '/'.join([
            FIXTURES_PATH_PREFIX,
            test_case_fixtures_dir_name,
            file_format,
        ])
        correct_file_path = '/'.join([
            FIXTURES_PATH_PREFIX,
            test_case_fixtures_dir_name,
            'correct_diff.json',
        ])

        correct_diff = get_correct_diff_as_str(correct_file_path)
        files_diff = generate_diff(
            '/'.join([files_examples_dir_path, 'file1.' + file_format]),
            '/'.join([files_examples_dir_path, 'file2.' + file_format])
        )

        assert correct_diff == files_diff


def test_different_files_1():
    _test_files_diff('different_files_1')


def test_different_files_2():
    _test_files_diff('different_files_2')


def test_both_empty_files():
    _test_files_diff('both_empty_files')


def test_empty_file1():
    _test_files_diff('empty_file1')


def test_empty_file2():
    _test_files_diff('empty_file2')


def test_both_identical_files():
    _test_files_diff('both_identical_files')
