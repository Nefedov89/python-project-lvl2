import os
import json
import yaml


file_formats = [
    'json',
    'yaml',
    'yml',
]


""" Tries to parse file and return it json representation as a dictionary """


def parse_file(file_path):
    if os.path.getsize(file_path) == 0:
        return {}

    file_extension = get_file_extension(file_path)
    file_parser = get_file_parser(file_extension)

    if not file_parser:
        return {}

    return file_parser(file_path)


def get_file_extension(file_path):
    return os.path.splitext(file_path)[1][1:]


def get_file_parser(file_extension):
    def json_parser(file_path):
        return json.load(open(file_path))

    def yaml_parser(file_path):
        return yaml.load(open(file_path), Loader=yaml.FullLoader)

    parsers_map = {
        'json': json_parser,
        'yaml': yaml_parser,
        'yml': yaml_parser,
    }

    return parsers_map.get(file_extension)
