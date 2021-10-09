import json
import re
import gendiff.src.constants as constants


operations_signs_map = {
    constants.ADDED_IN_FIRST_FILE_OPERATION: '-',
    constants.ADDED_IN_SECOND_FILE_OPERATION: '+',
    constants.NOT_CHANGED_OPERATION: None,
}


def build_stylish_diff_dict_from_tree(diff_tree):
    def get_item_value(item):
        value = item.get('value')
        children = item.get('children')

        return value \
            if children is None \
            else build_stylish_diff_dict_from_tree(children)

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

    formatted_diff = {
        get_key(item): get_item_value(item)
        for item in diff_tree
    }

    return formatted_diff


def stylish(diff_tree, has_internal_structure=True):
    formatted_diff_dict = build_stylish_diff_dict_from_tree(diff_tree) \
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


formatters_handlers_map = {
    constants.FORMATTER_STYLISH: stylish
}
