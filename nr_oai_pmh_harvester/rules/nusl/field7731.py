from oarepo_oai_pmh_harvester.transformer import OAITransformer


def related_item(el, **kwargs):
    res = {}
    item_isbn = el.get("z")
    if item_isbn:
        res["itemISBN"] = item_isbn
    item_title = el.get("t")
    if item_title:
        res["itemTitle"] = item_title
    item_issn = el.get("x")
    if item_issn:
        res["itemISSN"] = item_issn
    item_volume_issue = el.get("g")
    if item_volume_issue:
        item_volume_issue_parsed = parse_item_issue(item_volume_issue)
        if item_volume_issue_parsed:
            res.update(item_volume_issue_parsed)
        else:
            return {"relatedItem": "Warning: bad record"}
    if res:
        return {"relatedItem": res}
    else:
        return OAITransformer.PROCESSED


def parse_item_issue(text: str):
    dict_ = {
        "Roč. 22, č. 2 (2011)": {"itemVolume": "22", "itemIssue": "2", "itemYear": "2011"},
        "2008": {"itemYear": "2008"},
        "Roč. 19 (2013)": {"itemVolume": "19", "itemYear": "2013"},
        "Roč. 2016": {"itemYear": "2016"},
        "roč. 2, č. 2, s. 76-86": {
            "itemVolume": "2", "itemIssue": "2", "itemStartPage": "76", "itemEndPage": "86"
        }
    }
    return dict_.get("text")