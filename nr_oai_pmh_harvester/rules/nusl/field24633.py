from oarepo_oai_pmh_harvester.decorators import rule

from nr_oai_pmh_harvester.rules.nusl.field24500 import get_title_dict, add_title_dict


@rule("nusl", "marcxml", "/24633", phase="pre")
def call_title_alternate(el, **kwargs):
    return title_alternate(el, **kwargs)


def title_alternate(el, **kwargs):
    res = {}
    if isinstance(el, (tuple, list)):
        for _ in el:
            res = add_title_dict(_, kwargs, res)
    if isinstance(el, dict):
        res = add_title_dict(el, kwargs, res)
    return {"titleAlternate": [res]}
