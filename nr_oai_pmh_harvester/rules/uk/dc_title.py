from nr_oai_pmh_harvester.rules.utils import filter_language, remove_country_from_lang_codes
from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "xoai", "/dc/title", phase="pre")
def call_title(el, **kwargs):
    return title(el, **kwargs)  # pragma: no cover


def title(el, **kwargs):
    assert len(el) <= 1
    el = filter_language(el)
    return {"title": [remove_country_from_lang_codes(el)]}
