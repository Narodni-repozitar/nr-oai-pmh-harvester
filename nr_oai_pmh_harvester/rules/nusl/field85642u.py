from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "marcxml", "/85642/u", phase="pre")
def call_external_location(el, **kwargs):
    external_location(el, **kwargs)


def external_location(el, **kwargs):
    return {"externalLocation": el.strip()}
