from oarepo_oai_pmh_harvester.decorators import rule


@rule("uk", "xoai", "/dc/identifier/uri/value", phase="pre")
def call_original_record_id(el, **kwargs):
    return original_record_id(el, **kwargs)  # pragma: no cover


def original_record_id(el, **kwargs):
    if isinstance(el, (tuple, list)):
        id_ = el[-1]
    elif isinstance(el, str):
        id_ = el
    else:
        raise Exception("Bad format")
    return {
        "recordIdentifiers": {
            "originalRecord": id_
        }
    }
