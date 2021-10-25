import json
import re
import gendiff.src.constants as constants
from gendiff.src.helpers import build_internal_view_object


operations_signs_map = {
    constants.ADDED_IN_FIRST_FILE_OPERATION: '- ',
    constants.ADDED_IN_SECOND_FILE_OPERATION: '+ ',
    constants.NOT_CHANGED_OPERATION: constants.TWO_SPACES_INDENT,
}


def dump_stylish_json_to_str(formatted_diff_dict):
    formatted_diff_str = json.dumps(
        formatted_diff_dict,
        indent=4,
        separators=('', ': ')
    )
    # remove double quotes from keys
    formatted_diff_str = re.sub(r'"(.*?)"', r'\1', formatted_diff_str)
    back_braces_count = formatted_diff_str.count(constants.BACK_BRACE_SIGN)

    formatted_diff_str = formatted_diff_str.replace(
        constants.BACK_BRACE_SIGN,
        constants.TWO_SPACES_INDENT + constants.BACK_BRACE_SIGN,
        back_braces_count - 1
    )

    return formatted_diff_str


def build_stylish_diff_dict_from_tree(diff_tree):
    formatted_diff_dict = {}

    for tree_node in diff_tree:
        operation = tree_node.get('operation')
        operation_sign = operations_signs_map.get(operation)
        children = tree_node.get('children')
        key = tree_node.get('key')
        value = tree_node.get('value')

        formatted_key = '{operation_sign}{key}'.format(
            operation_sign=operation_sign,
            key=key
        )

        if children is not None:
            formatted_value = build_stylish_diff_dict_from_tree(
                children
            )
        elif children is None and isinstance(value, dict):
            children = [
                build_internal_view_object(key, value, 'was_not_changed')
                for key, value in value.items()
            ]
            formatted_value = build_stylish_diff_dict_from_tree(
                children
            )
        else:
            formatted_value = value

        formatted_diff_dict[formatted_key] = formatted_value

    return formatted_diff_dict


def format_stylish(diff_tree):
    formatted_diff_dict = build_stylish_diff_dict_from_tree(diff_tree)

    return dump_stylish_json_to_str(formatted_diff_dict)
