import pycountry
from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "marcxml", "/24500", phase="pre")
def call_title(el, **kwargs):
    return title(el, **kwargs)


def title(el, **kwargs):
    return get_title(el, kwargs)


def get_title(el, kwargs, field="title", first_lang_field="a", second_lang_field="b"):
    res = {}
    if isinstance(el, (tuple, list)):
        for _ in el:
            res.update(add_title_dict(_, kwargs, res, first_lang_field, second_lang_field))
    if isinstance(el, dict):
        res = add_title_dict(el, kwargs, res, first_lang_field=first_lang_field,
                       second_lang_field=second_lang_field)
    return {field: [res]}


def add_title_dict(el, kwargs, res, first_lang_field="a", second_lang_field="b"):
    first_lang = el.get(first_lang_field)
    if first_lang:
        res.update(get_title_dict(kwargs, first_lang))
    second_lang = el.get(second_lang_field)
    if second_lang:
        res["en"] = second_lang
    return res


def get_title_dict(kwargs, value):
    record = kwargs["record"]
    lang_object = record.get("04107", {})
    if isinstance(lang_object, dict):
        lang = lang_object.get("a")
    else:
        lang = None
    if not lang:
        lang = "ukn"
    py_lang = pycountry.languages.get(alpha_3=lang) or pycountry.languages.get(
        bibliographic=lang)
    if not py_lang:
        return {"ukn": ["Unknown language"]}
    return {py_lang.alpha_2: value}
