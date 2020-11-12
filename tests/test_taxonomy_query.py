from flask_taxonomies.models import TaxonomyTerm
from flask_taxonomies.proxies import current_flask_taxonomies


def test_query(app, db):
    sqlalchemy_query = current_flask_taxonomies.list_taxonomy('countries')
    sqlalchemy_query = current_flask_taxonomies.apply_term_query(sqlalchemy_query,
                                                                 'title.cs:"Angola" OR '
                                                                 'title.en:"Anglola"',
                                                                 "countries")
    print("\n\nQUERY:", sqlalchemy_query, "\n\n")
    term = sqlalchemy_query.one_or_none()
    assert isinstance(term, TaxonomyTerm)
    assert term.slug == 'ao'
