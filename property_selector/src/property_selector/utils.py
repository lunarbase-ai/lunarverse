def get_nested_value_from_dict(d: dict, keys: list) -> any:
    for key in keys:
        d = d[key]
    return d