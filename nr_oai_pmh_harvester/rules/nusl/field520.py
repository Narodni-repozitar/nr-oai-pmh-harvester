from nr_oai_pmh_harvester.rules.nusl.field04107 import get_language_taxonomy

from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "marcxml", "/520__", phase="pre")
def call_abstract(el, **kwargs):
    abstract(el, **kwargs)


def abstract(el, **kwargs):
    res = {}
    if isinstance(el, (list, tuple)):
        for _ in el:
            res.update(get_abstract(_))
    if isinstance(el, dict):
        res.update(get_abstract(el))
    return {"abstract": res}


def get_abstract(abstract_dict):
    lang_json = get_language_taxonomy(abstract_dict.get("9"))[0]
    return {
        lang_json["alpha2"]: abstract_dict.get("a")
    }
