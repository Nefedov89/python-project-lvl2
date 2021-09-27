import json
from gendiff.src.decorators import string_replacer


ADDED_IN_FIRST_FILE_SIGN = '-'
ADDED_IN_SECOND_FILE_SIGN = '+'


@string_replacer(replace_from=['"', ','], replace_to='')
def generate_diff(file_path1, file_path2):
    diff = []
    parsed_file1_dict = json.load(open(file_path1))
    parsed_file2_dict = json.load(open(file_path2))

    for key1, value1 in parsed_file1_dict.items():
        value2 = parsed_file2_dict.get(key1)

        if value2:
            # item was not changed
            if value1 == value2:
                diff.append({'key': key1, 'value': value1, 'sign': ' '})
            else:
                # item was changed
                diff.append({
                    'key': key1,
                    'value': value1,
                    'sign': ADDED_IN_FIRST_FILE_SIGN,
                })
                diff.append({
                    'key': key1,
                    'value': value2,
                    'sign': ADDED_IN_SECOND_FILE_SIGN,
                })

            # pop key1 item form file 2 as already seen
            parsed_file2_dict.pop(key1)
        # item is present in file1 and isn't present in file 2
        else:
            diff.append({
                'key': key1,
                'value': value1,
                'sign': ADDED_IN_FIRST_FILE_SIGN,
            })

    # left items in file 2 we assume as added
    added_items_in_file_2 = [
        {
            'key': k2,
            'value': v2,
            'sign': ADDED_IN_SECOND_FILE_SIGN,
        }
        for k2, v2 in parsed_file2_dict.items()
    ]
    diff.extend(added_items_in_file_2)

    # sorted by alphabet
    diff = sorted(diff, key=lambda x: x.get('key'))

    # formatted diff
    diff = {
        '{} {}'.format(
            item.get('sign'),
            item.get('key')
        ): item.get('value')
        for item in diff
    }

    return json.dumps(diff, indent=4)
