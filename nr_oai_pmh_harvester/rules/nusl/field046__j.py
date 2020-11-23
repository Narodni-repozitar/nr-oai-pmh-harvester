from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "marcxml", "/046__/j", phase="pre")
def call_date_modified(el, **kwargs):
    date_modified(el, **kwargs)


def date_modified(el, **kwargs):
    return {"dateModified": el}
