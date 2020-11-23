from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "marcxml", "/035", phase="pre")
def call_original_record_oai(el, **kwargs):
    original_record_oai(el, **kwargs)


def original_record_oai(el, **kwargs):
    return {
        "recordIdentifiers": {
            "originalRecordOAI": el["a"]
        }
    }
