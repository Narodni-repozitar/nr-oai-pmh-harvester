from nr_oai_pmh_harvester.rules.nusl.field24500 import get_title, get_title_dict


def titleAlternate(el, **kwargs):
    res = [get_title_dict(kwargs, el.get("a"))]
    return {"titleAlternate": res}
