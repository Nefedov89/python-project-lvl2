def string_replacer(replace_from, replace_to):
    def wrapper(fn):
        def inner(*args):
            result = fn(*args)

            if isinstance(replace_from, str):
                result = result.replace(replace_from, replace_to)

            if isinstance(replace_from, list):
                for replace_from_char in replace_from:
                    result = result.replace(replace_from_char, replace_to)

            return result

        return inner

    return wrapper
