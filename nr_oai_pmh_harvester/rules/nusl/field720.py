from functools import lru_cache

from flask_taxonomies.proxies import current_flask_taxonomies
from oarepo_taxonomies.utils import get_taxonomy_json


def people(el, **kwargs):
    creator = []
    contributor = []
    for person in el:
        if person.get('a'):
            creator.append({
                "name": person.get('a'),
            })
        if person.get('i'):
            contributor.append({
                "name": person.get('i'),
                "role": get_taxonomy_json(code="contributor-type",
                                          slug=get_role(person.get('e')).slug).paginated_data,
            })
    return {
        "creator": creator,
        "contributor": contributor
    }


@lru_cache(maxsize=27)
def get_role(role):
    sqlalchemy_query = current_flask_taxonomies.list_taxonomy('contributor-type')
    sqlalchemy_query = current_flask_taxonomies.apply_term_query(sqlalchemy_query,
                                                                 f'title.en:"{role}"',
                                                                 "contributor-type")
    return sqlalchemy_query.one_or_none()
