def gen_dict_extract(key, var):
    """
    :type keys: object
    """
    try:
        g = var.items()
    except AttributeError:
        print('error')
        pass
    else:
        for k, v in g:
            if k == key:
                yield v
            if isinstance(v, dict):
                yield from gen_dict_extract(key, v)
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result
