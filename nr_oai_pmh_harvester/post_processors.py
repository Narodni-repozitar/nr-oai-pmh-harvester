from oarepo_oai_pmh_harvester.decorators import post_processor
from oarepo_taxonomies.utils import get_taxonomy_json


@post_processor("nusl", "marcxml")
def call_add_date_defended(data):
    return add_date_defended(data) # pragma: no cover


@post_processor("nusl", "marcxml")
def call_add_defended(data):
    return add_defended(data) # pragma: no cover


@post_processor("nusl", "marcxml")
def call_add_item_relation_type(data):
    return add_item_relation_type(data) # pragma: no cover


def add_date_defended(data):
    resource_type = data.get("resourceType")
    resource_type = [_ for _ in resource_type if _["links"]["self"].split("/")[-1] == "theses-etds"]
    if len(resource_type) > 0:
        data["dateDefended"] = data["dateIssued"]
    return data


def add_defended(data):
    resource_type = data.get("resourceType")
    resource_type = [_ for _ in resource_type if _["links"]["self"].split("/")[-1] == "theses-etds"]
    if len(resource_type) > 0:
        if not data.get("defended"):
            data["defended"] = True
    return data


def add_item_relation_type(data):
    if "relatedItem" not in data:
        return data
    resource_type = data.get("resourceType")
    resource_type = [_ for _ in resource_type if not _["is_ancestor"]]
    mapping = {
        "conference-papers": "isPartOf",
        "articles": "isPartOf",
        "conference-proceedings": "hasVersion",
        "books": "hasVersion",
        "conference-posters": "isPartOf",
        "research-reports": "isPartOf",

    }
    for _ in resource_type:
        link = _["links"]["self"]
        if link.endswith("/"):
            link = link.rstrip("/")
        slug = link.split("/")[-1]
        relation_type_slug = mapping.get(slug)
        if not relation_type_slug:
            return data
        else:
            taxonomy_json = get_taxonomy_json(code="itemRelationType",
                                              slug=relation_type_slug.lower()).paginated_data
            if taxonomy_json:
                for _ in data["relatedItem"]:
                    _["itemRelationType"] = taxonomy_json
            return data
