def string_replacer(replace_from, replace_to):
    def wrapper(fn):
        def inner(*args):
            result = fn(*args)

            if not isinstance(result, str):
                return result

            return result.replace(replace_from, replace_to)

        return inner

    return wrapper
