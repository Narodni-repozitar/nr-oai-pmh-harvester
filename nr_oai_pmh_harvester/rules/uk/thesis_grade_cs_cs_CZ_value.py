from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "xoai", "/thesis/grade/cs/cs_CZ/value", phase="pre")
def call_defended(el, **kwargs):
    return defended(el, **kwargs)  # pragma: no cover


def defended(el, **kwargs):
    print(el)
