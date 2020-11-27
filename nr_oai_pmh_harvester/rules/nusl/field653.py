from oarepo_oai_pmh_harvester.decorators import rule
from oarepo_oai_pmh_harvester.transformer import OAITransformer


@rule("nusl", "marcxml", "/653__", phase="pre")
def call_keyword(el, **kwargs):
    return keyword(el, **kwargs)


def keyword(el, **kwargs):
    record = kwargs["record"]
    en_keywords = record.get("6530_")
    res = []
    if en_keywords:
        for cze, eng in zip(el, en_keywords):
            res.append({"cs": cze["a"], "eng": eng["a"]})
    else:
        for _ in el:
            res.append({"cs": _["a"]})
    if res:
        return {"keywords": res}
    else:
        return OAITransformer.PROCESSED
