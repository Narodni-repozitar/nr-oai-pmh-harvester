from dojson.utils import GroupableOrderedDict


def transform_to_dict(source):
    if isinstance(source, (dict, GroupableOrderedDict)):
        target = {}
        for k, v in source.items():
            if k.startswith("__"):
                continue
            target[k] = transform_to_dict(v)
    elif isinstance(source, (list, tuple)):
        target = []
        for _ in source:
            target.append(transform_to_dict(_))
    else:
        target = source
    return target
