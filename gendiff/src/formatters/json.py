import json
import gendiff.src.constants as constants


operations_words_map = {
    constants.ADDED_IN_FIRST_FILE_OPERATION: 'removed',
    constants.ADDED_IN_SECOND_FILE_OPERATION: 'added',
    constants.BOTH_FILES_UPDATED_OPERATION: 'updated',
    constants.NOT_CHANGED_OPERATION: None,
}


def get_item_value(tree_node, outer_key, formatted_diff_dict):
    value = tree_node.get('value')
    existing_formatted_value = formatted_diff_dict.get(outer_key)

    operation = tree_node.get('operation')
    children = tree_node.get('children')

    formatted_value = []

    # updated
    if existing_formatted_value:
        formatted_value = [
            operations_words_map.get(
                constants.BOTH_FILES_UPDATED_OPERATION
            ),
            existing_formatted_value.pop(),
            value,
        ]

    # removed
    elif operation == constants.ADDED_IN_FIRST_FILE_OPERATION:
        formatted_value = [
            operations_words_map.get(
                constants.ADDED_IN_FIRST_FILE_OPERATION
            ),
            value,
        ]

    # added
    elif operation == constants.ADDED_IN_SECOND_FILE_OPERATION:
        formatted_value = [
            operations_words_map.get(
                constants.ADDED_IN_SECOND_FILE_OPERATION
            ),
            value,
        ]

    # not changed
    elif operation == constants.NOT_CHANGED_OPERATION:
        formatted_value = value

    return formatted_value \
        if children is None \
        else build_json_diff_dict_from_tree(children)


def build_json_diff_dict_from_tree(diff_tree):
    formatted_diff_dict = {}

    for item in diff_tree:
        formatted_diff_dict[item.get('key')] = get_item_value(
            item,
            item.get('key'),
            formatted_diff_dict
        )

    return formatted_diff_dict


def format_json(diff_tree):
    formatted_diff_dict = build_json_diff_dict_from_tree(diff_tree)

    return json.dumps(formatted_diff_dict)
