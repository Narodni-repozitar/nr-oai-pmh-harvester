from oarepo_oai_pmh_harvester.transformer import OAITransformer


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
