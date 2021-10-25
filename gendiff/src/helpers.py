def build_internal_view_object(key, value, operation, children=None):
    return {
        'key': key,
        'value': value,
        'operation': operation,
        'children': children,
    }

