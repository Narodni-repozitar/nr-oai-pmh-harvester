from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "marcxml", "/909CO", phase="pre")
def call_nusl_oai(el, **kwargs):
    nusl_oai(el, **kwargs)


def nusl_oai(el, **kwargs):
    url = el.get("o")
    if url:
        return {
            "recordIdentifiers": {
                "nuslOAI": url
            }
        }
    return {
        "recordIdentifiers": {
            "nuslOAI": ["Nutná kontrola"]
        }
    }
