from oarepo_oai_pmh_harvester.transformer import OAITransformer
from oarepo_taxonomies.utils import get_taxonomy_json

from nr_oai_pmh_harvester.query import get_query_by_slug

from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "marcxml", "/650_7", phase="pre")
def call_subject(el, **kwargs):
    return subject(el, **kwargs)


def subject(el, **kwargs):
    res = {}
    subjects = []
    keywords = []
    if isinstance(el, (list, tuple)):
        for _ in el:
            subjects, keywords = get_subject_keyword(_, keywords, subjects)
    if isinstance(el, dict):
        subjects, keywords = get_subject_keyword(el, keywords, subjects)
    if subjects:
        res["subject"] = subjects
    if keywords:
        res["keywords"] = keywords
    if res:
        return res
    else:
        return OAITransformer.PROCESSED


def get_subject_keyword(_, keywords, subjects):
    subject = get_subject(_)
    if subject:
        subjects += subject
    else:
        keywords += get_keyword(_)
    return subjects, keywords


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
    if not term:
        return
    return get_taxonomy_json(code="subjects", slug=term.slug).paginated_data


def get_czmesh(el):
    slug = el.get("7").lower()
    query = get_query_by_slug("subjects", slug)
    term = query.one_or_none()
    if not term:
        return
    return get_taxonomy_json(code="subjects", slug=term.slug).paginated_data


def get_mednas(el):
    slug = el.get("7")
    query = get_query_by_slug("subjects", slug)
    term = query.one_or_none()
    return get_taxonomy_json(code="subjects", slug=term.slug).paginated_data


def get_keyword(el):
    return {"cs": el.get("a")}
