from typing import Iterable

from flask_taxonomies.proxies import current_flask_taxonomies
from oarepo_taxonomies.utils import get_taxonomy_json
from sqlalchemy.orm.exc import MultipleResultsFound

from nr_oai_pmh_harvester.query import find_in_json_list

from oarepo_oai_pmh_harvester.decorators import rule
from oarepo_oai_pmh_harvester.transformer import OAITransformer


@rule("nusl", "marcxml", "/502__/c", phase="pre")
def call_degree_grantor(el, **kwargs):
    return degree_grantor(el, **kwargs)  # pragma: no cover


# TODO: https://www.postgresql.org/docs/9.6/functions-json.html, sepsat do Notion nebo článek

def degree_grantor(el, **kwargs):
    if "," in el:
        grantor_array = [x.strip() for x in el.split(",", maxsplit=2) if x.strip()]
    elif "." in el:
        grantor_array = [x.strip() for x in el.split(".", maxsplit=2) if x.strip()]
    else:
        grantor_array = [el]
    reversed_grantor_array = list(reversed(grantor_array))
    for reversed_level, unit in enumerate(reversed_grantor_array):
        term = get_institution_term(unit, reversed_grantor_array, reversed_level)
        if term:
            return {
                "degreeGrantor": get_taxonomy_json(code="institutions",
                                                   slug=term.slug).paginated_data
            }
        else:
            return OAITransformer.PROCESSED


def get_institution_term(unit, reversed_grantor_array: Iterable = None, reversed_level: int = None):
    if not reversed_grantor_array:
        reversed_grantor_array = [unit]
    if reversed_level is None:
        reversed_level = 0
    sqlalchemy_query = current_flask_taxonomies.list_taxonomy('institutions')
    sqlalchemy_query_title_cs = current_flask_taxonomies.apply_term_query(sqlalchemy_query,
                                                                          f'title.cs:"{unit}"',
                                                                          "institutions")
    try:
        term = sqlalchemy_query_title_cs.one_or_none()
    except MultipleResultsFound:
        terms = sqlalchemy_query_title_cs.all()
        term = choose_term(terms, reversed_grantor_array, reversed_level)
        if not term:
            return
    if not term:
        sqlalchemy_query_title_en = current_flask_taxonomies.apply_term_query(sqlalchemy_query,
                                                                              f'title.en:"'
                                                                              f'{unit}"',
                                                                              "institutions")
        term = sqlalchemy_query_title_en.one_or_none()
    if not term:
        sqlalchemy_query_alias = find_in_json_list("institutions", "aliases", unit)
        term = sqlalchemy_query_alias.one_or_none()
    if not term:
        sqlalchemy_query_formerName = find_in_json_list("institutions", "formerNames", unit)
        term = sqlalchemy_query_formerName.one_or_none()
    return term


def choose_term(terms, reversed_grantor_array, reversed_level):
    parent_term = get_institution_term(reversed_grantor_array[reversed_level + 1],
                                       reversed_grantor_array, reversed_level + 1)
    if not parent_term:
        return
    for term in terms:
        if term.parent.id == parent_term.id:
            return term
