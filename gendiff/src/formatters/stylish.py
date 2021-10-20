import json
import re
import gendiff.src.constants as constants


operations_signs_map = {
    constants.ADDED_IN_FIRST_FILE_OPERATION: '- ',
    constants.ADDED_IN_SECOND_FILE_OPERATION: '+ ',
    constants.NOT_CHANGED_OPERATION: '  ',
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


def get_item_key(tree_node):
    operation = tree_node.get('operation')
    operation_sign = operations_signs_map.get(operation, '')
    original_key = tree_node.get('key')
    children = tree_node.get('children')

    if children is not None:
        operation_sign = ''

    key = '{operation_sign}{original_key}'.format(
        operation_sign=operation_sign,
        original_key=original_key
    )

    return key


def get_item_value(tree_node):
    value = tree_node.get('value')
    children = tree_node.get('children')

    return value \
        if children is None \
        else build_stylish_diff_dict_from_tree(children)


def build_stylish_diff_dict_from_tree(diff_tree):
    formatted_diff_dict = {}

    for item in diff_tree:
        formatted_key = get_item_key(item)
        formatted_value = get_item_value(item)

        formatted_diff_dict[formatted_key] = formatted_value

    return formatted_diff_dict


def format_stylish(diff_tree):
    formatted_diff_dict = build_stylish_diff_dict_from_tree(diff_tree)

    return dump_stylish_json_to_str(formatted_diff_dict)
