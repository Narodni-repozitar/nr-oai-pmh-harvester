from oarepo_oai_pmh_harvester.decorators import rule
from oarepo_oai_pmh_harvester.transformer import OAITransformer


@rule("nusl", "marcxml", "/996__", phase="pre")
def call_accessibility(el, **kwargs):
    return accessibility(el, **kwargs)


def accessibility(el, **kwargs):
    res = {}
    cs = el.get("a")
    en = el.get("b")
    if cs:
        res["cs"] = cs
    if en:
        res["en"] = en
    if res:
        return {"accessibility": res}
    return OAITransformer.PROCESSED
