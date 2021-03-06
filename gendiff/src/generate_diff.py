from gendiff.src.file_parser import parse_file
import gendiff.src.constants as constants
from gendiff.src.formatters import formats_formatters_map
from gendiff.src.helpers import build_internal_view_object


def build_diff_tree(parsed_file1_dict, parsed_file2_dict):
    diff = []

    for key1, value1 in parsed_file1_dict.items():
        value2 = parsed_file2_dict.get(key1)

        if value2 is not None:
            # check if both are dicts
            if isinstance(value1, dict) and isinstance(value2, dict):
                diff.append(
                    build_internal_view_object(
                        key1,
                        None,
                        constants.NOT_CHANGED_OPERATION,
                        build_diff_tree(value1, value2),
                    )
                )
            else:
                # item was not changed
                if value1 == value2:
                    diff.append(
                        build_internal_view_object(
                            key1,
                            value1,
                            constants.NOT_CHANGED_OPERATION,
                        )
                    )
                else:
                    # item was changed
                    diff.append(
                        build_internal_view_object(
                            key1,
                            value1,
                            constants.ADDED_IN_FIRST_FILE_OPERATION,
                        )
                    )
                    diff.append(
                        build_internal_view_object(
                            key1,
                            value2,
                            constants.ADDED_IN_SECOND_FILE_OPERATION,
                        )
                    )

            # pop key1 item form file 2 as already seen
            parsed_file2_dict.pop(key1)
        # item is present in file1 and isn't present in file 2
        else:
            diff.append(
                build_internal_view_object(
                    key1,
                    value1,
                    constants.ADDED_IN_FIRST_FILE_OPERATION,
                )
            )

    # left items in file 2 we assume as added
    added_items_in_file_2 = [
        build_internal_view_object(
            key2,
            value2,
            constants.ADDED_IN_SECOND_FILE_OPERATION
        )
        for key2, value2 in parsed_file2_dict.items()
    ]
    diff.extend(added_items_in_file_2)

    # sorted by alphabet
    diff = sorted(diff, key=lambda x: x.get('key'))

    return diff


def generate_diff(file1, file2, output_format=constants.FORMAT_STYLISH):
    parsed_file1_dict = parse_file(file1)
    parsed_file2_dict = parse_file(file2)
    formatter = formats_formatters_map.get(output_format)

    diff_tree = build_diff_tree(parsed_file1_dict, parsed_file2_dict)

    return formatter(diff_tree)
