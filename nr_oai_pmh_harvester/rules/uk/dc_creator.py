from oarepo_oai_pmh_harvester.decorators import rule


@rule("uk", "xoai", "/dc/creator/value", phase="pre")
def call_creator(el, **kwargs):
    return creator(el, **kwargs)  # pragma: no cover


def creator(el, **kwargs):
    return {"creator": [{"name": el}]}
