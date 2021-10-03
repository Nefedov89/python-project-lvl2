import json
import re
from gendiff.src.constants import\
    ADDED_IN_FIRST_FILE_OPERATION,\
    ADDED_IN_SECOND_FILE_OPERATION,\
    NOT_CHANGED_OPERATION


operations_signs_map = {
    ADDED_IN_FIRST_FILE_OPERATION: '-',
    ADDED_IN_SECOND_FILE_OPERATION: '+',
    NOT_CHANGED_OPERATION: ' ',
}


def build_diff_dict_from_tree(diff_tree):
    def get_item_value(item):
        value = item.get('value')

        return value \
            if not isinstance(value, list) \
            else build_diff_dict_from_tree(value)

    def get_key(item):
        operation = operations_signs_map.get(item.get('operation'), '')
        key = item.get('key')

        if operation:
            key = '{operation} {key}'.format(
                operation=operation,
                key=key
            )

        return key

    formatted_diff = {
        get_key(item): get_item_value(item)
        for item in diff_tree
    }

    return formatted_diff


def stylish(diff_tree, has_internal_structure=True):
    formatted_diff_dict = build_diff_dict_from_tree(diff_tree) \
        if has_internal_structure \
        else diff_tree

    formatted_diff_str = json.dumps(
        formatted_diff_dict,
        indent=4,
        separators=('', ': ')
    )
    # remove double quotes from keys
    formatted_diff_str = re.sub(r'"(.*?)"', r'\1', formatted_diff_str)

    return formatted_diff_str
