from oarepo_oai_pmh_harvester.decorators import rule


@rule("uk", "xoai", "/dc/date/issued/value", phase="pre")
def call_date_issued(el, **kwargs):
    return date_issued(el, **kwargs) # pragma: no cover


def date_issued(el, **kwargs):
    assert isinstance(el, list), "Element should be list"
    return {"dateIssued": el[-1]}