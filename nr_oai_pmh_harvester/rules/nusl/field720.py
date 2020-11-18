from functools import lru_cache

from flask_taxonomies.proxies import current_flask_taxonomies
from oarepo_taxonomies.utils import get_taxonomy_json


def people(el, **kwargs):
    creator = []
    contributor = []
    res = {}
    if isinstance(el, (list, tuple)):
        for person in el:
            get_person(person, contributor, creator)
    if isinstance(el, dict):
        get_person(el, contributor, creator)
    if creator:
        res["creator"] = creator
    if contributor:
        res["contributor"] = contributor
    return res


def get_person(person, contributor_list, creator_list):
    if person.get('a'):
        creator_list.append({
            "name": person.get('a'),
        })
    if person.get('i'):
        contributor_list.append({
            "name": person.get('i'),
            "role": get_taxonomy_json(code="contributor-type",
                                      slug=get_role(person.get('e')).slug).paginated_data,
        })


@lru_cache(maxsize=27)
def get_role(role):
    sqlalchemy_query = current_flask_taxonomies.list_taxonomy('contributor-type')
    sqlalchemy_query = current_flask_taxonomies.apply_term_query(sqlalchemy_query,
                                                                 f'title.en:"{role}"',
                                                                 "contributor-type")
    return sqlalchemy_query.one_or_none()
