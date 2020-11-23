from oarepo_oai_pmh_harvester.decorators import rule
from oarepo_oai_pmh_harvester.transformer import OAITransformer
from oarepo_taxonomies.utils import get_taxonomy_json
from slugify import slugify

from nr_oai_pmh_harvester.query import find_in_json_list, find_in_title


@rule("nusl", "marcxml", "/656_7/a", phase="pre")
def call_studyfield(el, **kwargs):
    studyfield(el, **kwargs)


def studyfield(el, **kwargs):
    if "/" not in el:
        return get_study_field(el.strip())
    else:
        programme, field = el.split("/", maxsplit=1)
        field = field.strip()
        return get_study_field(field, programme=programme)


def get_study_field(field: str, programme: str = None):
    sqlalchemy_query = find_in_title(field, "studyfields")
    terms = sqlalchemy_query.all()
    if not terms:
        sqlalchemy_query = find_in_title(field, "studyfields", first_lang="de", second_lang="fr")
        terms = sqlalchemy_query.all()
    if not terms:
        terms = find_in_json_list("studyfields", "aliases", field).all()
    if not terms:
        return OAITransformer.PROCESSED
    if terms:
        return choose_term(terms, programme)


def choose_term(terms, programme: str = None):
    res = []
    l = len(terms)
    if l == 1:
        term = terms[0]
        res += get_taxonomy_json("studyfields", slug=term.slug).paginated_data
    if l > 1:
        if programme:
            parent_slug = f"p-{slugify(programme)}"
            for term in terms:
                if term.parent_slug == parent_slug:
                    res += get_taxonomy_json("studyfields", slug=term.slug).paginated_data
                    break
            if len(res) == 0:
                res += get_taxonomy_json("studyfields", slug=terms[0].slug).paginated_data
        else:
            res += get_taxonomy_json("studyfields", slug=terms[0].slug).paginated_data
    return {"studyField": res}
