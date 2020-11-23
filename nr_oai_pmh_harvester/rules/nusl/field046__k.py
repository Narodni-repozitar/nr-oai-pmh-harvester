from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "marcxml", "/046__/k", phase="pre")
def call_date_issued(el, **kwargs):
    date_issued(el, **kwargs)


def date_issued(el, **kwargs):
    return {"dateIssued": el}
