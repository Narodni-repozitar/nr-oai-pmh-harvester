from oarepo_taxonomies.utils import get_taxonomy_json

from nr_oai_pmh_harvester.query import get_query_by_slug


def subject(el, **kwargs):
    res = []
    keywords = []
    if isinstance(el, (list, tuple)):
        for _ in el:
            res, keywords = get_subject_keyword(_, keywords, res)
    if isinstance(el, dict):
        res, keywords = get_subject_keyword(el, keywords, res)
    return {
        "subject": res,
        "keywords": keywords
    }


def get_subject_keyword(_, keywords, res):
    subject = get_subject(_)
    if subject:
        res += subject
    else:
        keywords += get_keyword(_)
    return res, keywords


def get_subject(el):
    type_ = el.get("2").lower()
    type_dict = {
        "psh": get_psh,
        "czmesh": get_czmesh,
        "mednas": get_mednas
    }
    handler = type_dict.get(type_)
    if not handler:
        return
    return handler(el)


def get_psh(el):
    url = el.get("0")
    slug = url.split("/")[-1].lower()
    query = get_query_by_slug("subjects", slug)
    term = query.one_or_none()
    return get_taxonomy_json(code="subjects", slug=term.slug).paginated_data


def get_czmesh(el):
    slug = el.get("7").lower()
    query = get_query_by_slug("subjects", slug)
    term = query.one_or_none()
    return get_taxonomy_json(code="subjects", slug=term.slug).paginated_data


def get_mednas(el):
    slug = el.get("7")
    query = get_query_by_slug("subjects", slug)
    term = query.one_or_none()
    return get_taxonomy_json(code="subjects", slug=term.slug).paginated_data


def get_keyword(el):
    return {"cs": el.get("a")}
