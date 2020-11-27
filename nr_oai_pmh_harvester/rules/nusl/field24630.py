from oarepo_oai_pmh_harvester.decorators import rule
from oarepo_oai_pmh_harvester.transformer import OAITransformer

from nr_oai_pmh_harvester.rules.nusl.field24500 import get_title_dict


@rule("nusl", "marcxml", "/24630", phase="pre")
def call_title_alternate_2(el, **kwargs):
    return title_alternate_2(el, **kwargs)


def title_alternate_2(el, **kwargs):
    res = []
    if number := el.get("n"):
        res.append(get_title_dict(kwargs, number))
    if name := el.get("p"):
        res.append(get_title_dict(kwargs, name))
    if res:
        return {"titleAlternate": res}
    return OAITransformer.PROCESSED
