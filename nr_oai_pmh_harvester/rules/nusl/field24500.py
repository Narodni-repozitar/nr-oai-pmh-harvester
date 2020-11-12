import pycountry


def title(el, **kwargs):
    record = kwargs["record"]
    lang = record["04107"]["a"]
    py_lang = pycountry.languages.get(alpha_3=lang) or pycountry.languages.get(bibliographic=lang)
    res = {
        "title": {
            py_lang.alpha_2: el["a"]
        }
    }
    if lang2 := el.get("b"):
        res["title"]["en"] = lang2
    return res
