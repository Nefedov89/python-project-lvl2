import json
import re
import gendiff.src.constants as constants

operations_signs_map = {
    constants.ADDED_IN_FIRST_FILE_OPERATION: '-',
    constants.ADDED_IN_SECOND_FILE_OPERATION: '+',
    constants.NOT_CHANGED_OPERATION: None,
}


def dump_stylish_json_to_str(formatted_diff_dict):
    formatted_diff_str = json.dumps(
        formatted_diff_dict,
        indent=4,
        separators=('', ': ')
    )
    # remove double quotes from keys
    formatted_diff_str = re.sub(r'"(.*?)"', r'\1', formatted_diff_str)

    return formatted_diff_str


def build_stylish_diff_dict_from_tree(diff_tree):
    def get_key(item):
        operation = operations_signs_map.get(item.get('operation'), '')
        key = item.get('key')
        children = item.get('children')

        if operation is not None:
            key = '{operation} {key}'.format(
                operation=operation,
                key=key
            )
        else:
            not_changed_operation_prefix = '' \
                if children is not None \
                else '  '
            key = '{not_changed_operation_prefix}{key}'.format(
                not_changed_operation_prefix=not_changed_operation_prefix,
                key=key
            )

        return key

    def get_value(item):
        value = item.get('value')
        children = item.get('children')

        return value \
            if children is None \
            else build_stylish_diff_dict_from_tree(children)

    formatted_diff = {
        get_key(item): get_value(item)
        for item in diff_tree
    }

    return formatted_diff


def stylish(diff_tree):
    formatted_diff_dict = build_stylish_diff_dict_from_tree(diff_tree)

    return dump_stylish_json_to_str(formatted_diff_dict)


def build_plain_diff_dict_from_tree(diff_tree):
    def get_key(item):
        return 2

    def get_value(item):
        return 1

    def get_operation(item):
        return 3

    formatted_diff = ''

    for item in diff_tree:
        formatted_diff += "\nProperty '{key}' was {operation}{value}".format(
            key=get_key(item),
            operation=get_operation(item),
            value=get_value(item)
        )

    return formatted_diff


def plain(diff_tree):
    formatted_diff_dict = build_plain_diff_dict_from_tree(diff_tree)

    return formatted_diff_dict


formats_formatters_map = {
    constants.FORMAT_STYLISH: stylish,
    # constants.FORMAT_PLAIN: plain,
}
