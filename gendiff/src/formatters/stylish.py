import gendiff.src.constants as constants
from gendiff.src.helpers import build_internal_view_object


operations_signs_map = {
    constants.ADDED_IN_FIRST_FILE_OPERATION: '- ',
    constants.ADDED_IN_SECOND_FILE_OPERATION: '+ ',
    constants.NOT_CHANGED_OPERATION: constants.TWO_SPACES_INDENT,
}


def format_values_for_plain(value):
    if isinstance(value, str):
        return value.strip()

    if value in [True, False]:
        return str(value).lower()

    if value is None:
        return 'null'

    return value


def stringify_diff_tree(diff_tree, depth=2):
    lines = []

    for tree_node in diff_tree:
        operation = tree_node.get('operation')
        operation_sign = operations_signs_map.get(operation)
        children = tree_node.get('children')
        key = tree_node.get('key')
        value = tree_node.get('value')

        if children is None and isinstance(value, dict):
            children = [
                build_internal_view_object(
                    key,
                    value,
                    constants.NOT_CHANGED_OPERATION
                )
                for key, value in value.items()
            ]

        formatted_value = format_values_for_plain(value)\
            if children is None\
            else '{{\n{value}\n{close_brace}'.format(
                value=stringify_diff_tree(children, depth + 4),
                close_brace=constants.ONE_SPACE_INDENT * (depth + 2) + '}'
        )

        line = '{indent}{operation_sign}{key}:{space}{value}'.format(
            indent=constants.ONE_SPACE_INDENT * depth,
            operation_sign=operation_sign,
            key=key,
            space=constants.ONE_SPACE_INDENT if value != '' else '',
            value=formatted_value,
        )
        lines.append(line)

    return '\n'.join(lines)


def format_stylish(diff_tree):
    formatted_str = stringify_diff_tree(diff_tree)

    return '{{\n{inner_str}\n}}'.format(inner_str=formatted_str)
