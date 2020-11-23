from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "marcxml", "/300__/a", phase="pre")
def call_date_extent(el, **kwargs):
    extent(el, **kwargs)


def extent(el, **kwargs):
    return {"extent": el}
