from nr_oai_pmh_harvester.query import find_in_json_list, get_query_by_slug, find_in_json, \
    find_in_title_jsonb


def test_query(app, db):
    sqlalchemy_query = find_in_json_list("institutions", "formerNames",
                                         "Vysoká škola zemědělská v Brně")
    term = sqlalchemy_query.all()
    assert term[0].slug == '62156489'


def test_query_2(app, db):
    sqlalchemy_query = find_in_json_list("institutions", "aliases",
                                         "Mendelova univerzita")
    term = sqlalchemy_query.one_or_none()
    assert term.slug == '62156489'


def test_get_query_by_slug(app, db):
    query = get_query_by_slug("subjects", "PSH120")
    terms = query.all()
    print(query, terms)


def test_find_in_title_jsonb(app, db):
    query = find_in_title_jsonb("epilepsie", "subjects", lang="cs")
    terms = query.all()
    assert len(terms) > 0
    assert str(query) == """SELECT taxonomy_term.id AS taxonomy_term_id, taxonomy_term.slug AS taxonomy_term_slug, taxonomy_term.extra_data AS taxonomy_term_extra_data, taxonomy_term.level AS taxonomy_term_level, taxonomy_term.parent_id AS taxonomy_term_parent_id, taxonomy_term.taxonomy_id AS taxonomy_term_taxonomy_id, taxonomy_term.taxonomy_code AS taxonomy_term_taxonomy_code, taxonomy_term.busy_count AS taxonomy_term_busy_count, taxonomy_term.obsoleted_by_id AS taxonomy_term_obsoleted_by_id, taxonomy_term.status AS taxonomy_term_status 
FROM taxonomy_term JOIN taxonomy_taxonomy ON taxonomy_taxonomy.id = taxonomy_term.taxonomy_id 
WHERE taxonomy_taxonomy.code = %(code_1)s AND taxonomy_term.status = %(status_1)s AND (taxonomy_term.extra_data @> %(extra_data_1)s) ORDER BY taxonomy_term.slug"""
