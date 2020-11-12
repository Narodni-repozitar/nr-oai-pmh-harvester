from flask_taxonomies.models import TaxonomyTerm
from flask_taxonomies.proxies import current_flask_taxonomies
from sqlalchemy import func


def find_in_json_list(taxonomy_code: str, field: str, value: str):
    sqlalchemy_query = current_flask_taxonomies.list_taxonomy(f'{taxonomy_code}')
    sqlalchemy_query = sqlalchemy_query.filter(
        func.jsonb_extract_path(TaxonomyTerm.extra_data, field).op('?')(
            value))
    return sqlalchemy_query