from oarepo_oai_pmh_harvester.transformer import OAITransformer


def original_record_id(el, **kwargs):
    if isinstance(el, (list, tuple)):
        for _ in el:
            record_id = get_original_record_id(_)
            if record_id:
                return record_id
        return OAITransformer.PROCESSED
    if isinstance(el, dict):
        return get_original_record_id(el) or OAITransformer.PROCESSED

def get_original_record_id(el):
    if el.get("z") == 'Odkaz na původní záznam':
        return {
            "recordIdentifiers": {
                "originalRecord": el.get("u")
            }
        }
