def get_type(obj):
    return obj["type"] if "type" in obj else (obj["@type"] if "@type" in obj else None)


def get_id(obj):
    return obj["id"] if "id" in obj else (obj["@id"] if "@id" in obj else None)


def enforce_list(val):
    return val if isinstance(val, list) else [val]


# Only if one level of nesting
def to_string(obj):
    if isinstance(obj, str):
        return obj
    temp = [el if not isinstance(el, list) else ", ".join(el) for el in obj]
    # the path leads to a value which is a list
    return temp[0] if len(temp) == 1 else " - ".join(temp)
    # one path leads to multiple matches (multiple objects)
