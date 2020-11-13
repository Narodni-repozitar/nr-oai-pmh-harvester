from oarepo_oai_pmh_harvester.transformer import OAITransformer


def nusl_oai(el, **kwargs):
    url = el.get("o")
    if url:
        return {
                "recordIdentifiers": {
                    "nuslOAI": url
                }
            }
    return OAITransformer.PROCESSED