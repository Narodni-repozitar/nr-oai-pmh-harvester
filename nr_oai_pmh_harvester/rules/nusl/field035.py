def original_record_oai(el, **kwargs):
    return {
        "recordIdentifiers": {
            "originalRecordOAI": el["a"]
        }
    }
