def form_encode(data):
    exploded_data = {}
    for k, v in data.items():
        items = _explode_enumerable(k, v)
        for new_key, new_val in items:
            exploded_data[new_key] = new_val
    return exploded_data


def _explode_enumerable(k, v):
    exploded_items = []
    if isinstance(v, list) or isinstance(v, tuple):
        if len(v) == 0:
            exploded_items.append((k, v))
        else:
            for idx, item in enumerate(v):
                current_key = '{}[{}]'.format(k, idx)
                exploded_items.extend(_explode_enumerable(current_key, item))
    elif isinstance(v, dict):
        if len(v) == 0:
            exploded_items.append((k, v))
        else:
            for idx, item in v.items():
                current_key = '{}[{}]'.format(k, idx)
                exploded_items.extend(_explode_enumerable(current_key, item))
    else:
        exploded_items.append((k, v))
    return exploded_items
