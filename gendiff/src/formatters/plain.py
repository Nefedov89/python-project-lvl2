import gendiff.src.constants as constants


def format_values_for_plain(value):
    if isinstance(value, dict):
        return '[complex value]'

    if isinstance(value, str):
        return '\'{value}\''.format(value=value)

    if value in [True, False]:
        return str(value).lower()

    if value is None:
        return 'null'

    return value


def build_plain_diff_dict_from_tree(diff_tree, outer_key=None):
    formatted_diff_dict = {}

    for item in diff_tree:
        key = item.get('key')
        value = item.get('value')
        children = item.get('children')
        operation = item.get('operation')

        formatted_key = '{outer_key}.{key}'.format(
            outer_key=outer_key,
            key=key
        ) if outer_key else key

        old_value = value
        updated_item = formatted_diff_dict.get(formatted_key)

        # updated
        if updated_item:
            formatted_operation = 'updated. '
            formatted_value = 'From {old_value} to {new_value}'.format(
                old_value=format_values_for_plain(
                    updated_item.get('old_value')
                ),
                new_value=format_values_for_plain(value)
            )

        # removed
        elif operation == constants.ADDED_IN_FIRST_FILE_OPERATION:
            formatted_operation = 'removed'
            formatted_value = ''

        # added
        else:
            formatted_operation = 'added with value: '
            formatted_value = format_values_for_plain(value)

        if operation != constants.NOT_CHANGED_OPERATION:
            formatted_diff_dict[formatted_key] = {
                'formatted_key': formatted_key,
                'formatted_operation': formatted_operation,
                'formatted_value': formatted_value,
                'old_value': old_value,
            }

        # handle children nodes
        if children is not None:
            children_diff = build_plain_diff_dict_from_tree(
                children,
                formatted_key
            )
            formatted_diff_dict.update(children_diff)

    return formatted_diff_dict


def format_plain(diff_tree):
    formatted_diff_dict = build_plain_diff_dict_from_tree(diff_tree)
    formatted_diff = '\n'.join(
        "Property '{key}' was {operation}{value}".format(
            key=item.get('formatted_key'),
            operation=item.get('formatted_operation'),
            value=item.get('formatted_value'),
        )
        for item in formatted_diff_dict.values()
    )

    return formatted_diff
