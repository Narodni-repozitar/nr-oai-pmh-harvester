from oarepo_oai_pmh_harvester.transformer import OAITransformer


def series(el, **kwargs):
    res = {}
    if title := el.get("a"):
        res["seriesTitle"] = title
    if volume := el.get("v"):
        res["seriesVolume"] = volume
    if res:
        return {"series": res}
    else:
        return OAITransformer.PROCESSED
