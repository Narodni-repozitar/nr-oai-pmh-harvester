from oarepo_oai_pmh_harvester.decorators import rule
from oarepo_oai_pmh_harvester.transformer import OAITransformer


@rule("nusl", "marcxml", "/4900_", phase="pre")
def call_series(el, **kwargs):
    series(el, **kwargs)


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
