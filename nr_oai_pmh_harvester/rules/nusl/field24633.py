from oarepo_oai_pmh_harvester.decorators import rule

from nr_oai_pmh_harvester.rules.nusl.field24500 import get_title_dict


@rule("nusl", "marcxml", "/24633", phase="pre")
def call_title_alternate(el, **kwargs):
    title_alternate(el, **kwargs)


def title_alternate(el, **kwargs):
    res = [get_title_dict(kwargs, el.get("a"))]
    return {"titleAlternate": res}
