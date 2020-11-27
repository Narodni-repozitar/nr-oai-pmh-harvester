from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "marcxml", "/260__/b", phase="pre")
def call_date_publisher(el, **kwargs):
    return publisher(el, **kwargs)


def publisher(el, **kwargs):
    return {"publisher": el}
