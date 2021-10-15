import json
import os.path
import gendiff.src.constants as constants
from gendiff import generate_diff
from gendiff.src.file_parser import file_formats
from gendiff.src.formatters import formats_formatters_map
from gendiff.src.formatters.stylish import dump_stylish_json_to_str


FIXTURES_PATH_PREFIX = './tests/fixtures'


def setup_function(function):
    print(function)


def get_correct_diff_as_str(test_case_fixtures_dir_name, output_format):
    formats_files_map = {
        constants.FORMAT_STYLISH: 'correct_diff.json',
        constants.FORMAT_PLAIN: 'correct_diff.txt',
        constants.FORMAT_JSON: 'correct_diff.json',
    }
    correct_file_path = '/'.join([
        FIXTURES_PATH_PREFIX,
        test_case_fixtures_dir_name,
        'correct',
        output_format,
        formats_files_map.get(output_format, '')
    ])

    if os.path.isfile(correct_file_path):
        file_pointer = open(correct_file_path, 'r')

        # stylish format
        if output_format == constants.FORMAT_STYLISH:
            diff_tree = json.load(file_pointer)

            return dump_stylish_json_to_str(diff_tree)

        # plain format
        if output_format == constants.FORMAT_PLAIN:
            return file_pointer.read()

        # json format
        if output_format == constants.FORMAT_JSON:
            diff_tree = json.load(file_pointer)

            return json.dumps(diff_tree)

    return None


def _test_files_diff(test_case_fixtures_dir_name):
    for file_format in file_formats:
        files_examples_dir_path = '/'.join([
            FIXTURES_PATH_PREFIX,
            test_case_fixtures_dir_name,
            file_format,
        ])

        for output_format, _ in formats_formatters_map.items():
            correct_diff = get_correct_diff_as_str(
                test_case_fixtures_dir_name,
                output_format
            )

            if correct_diff is not None:
                files_diff = generate_diff(
                    '/'.join([files_examples_dir_path, 'file1.' + file_format]),
                    '/'.join([files_examples_dir_path, 'file2.' + file_format]),
                    output_format
                )

                assert correct_diff == files_diff


def test_different_files_1():
    _test_files_diff('different_files_1')


def test_different_files_2():
    _test_files_diff('different_files_2')


def test_different_files_3():
    _test_files_diff('different_files_3')


def test_both_empty_files():
    _test_files_diff('both_empty_files')


def test_empty_file1():
    _test_files_diff('empty_file1')


def test_empty_file2():
    _test_files_diff('empty_file2')


def test_both_identical_files():
    _test_files_diff('both_identical_files')
