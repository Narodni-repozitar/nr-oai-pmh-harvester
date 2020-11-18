from oarepo_oai_pmh_harvester.transformer import OAITransformer


def funding_reference(el, **kwargs):
    # TODO: vyřešit s Péťou
    return OAITransformer.PROCESSED
    res = {}
    project_id = el.get("a")
    funder = el.get("b")
    if project_id:
        res["projectID"] = project_id
    if funder:
        res["funder"] = get_funder(funder)
    return {
        "fundingReference": res
    }


def get_funder(funder):
    pass
