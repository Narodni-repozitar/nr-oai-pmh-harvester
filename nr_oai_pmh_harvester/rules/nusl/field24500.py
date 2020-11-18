import pycountry


def title(el, **kwargs):
    return get_title(el, kwargs)


def get_title(el, kwargs, field="title", first_lang_field="a", second_lang_field="b"):
    # record = kwargs["record"]
    # lang = record["04107"]["a"]
    # py_lang = pycountry.languages.get(alpha_3=lang) or pycountry.languages.get(bibliographic=lang)
    # res = {
    #     field: {
    #         py_lang.alpha_2: el[first_lang_field]
    #     }
    # }
    res = {
        field: get_title_dict(kwargs, el[first_lang_field])
    }
    if lang2 := el.get(second_lang_field):
        res[field]["en"] = lang2
    return res


def get_title_dict(kwargs, value):
    record = kwargs["record"]
    lang = record["04107"]["a"]
    py_lang = pycountry.languages.get(alpha_3=lang) or pycountry.languages.get(
        bibliographic=lang)
    return {py_lang.alpha_2: value}