from nr_oai_pmh_harvester.query import find_in_json_list, get_query_by_slug


def test_query(app, db):
    sqlalchemy_query = find_in_json_list("institutions", "formerNames",
                                         "Vysoká škola zemědělská v Brně")
    term = sqlalchemy_query.all()
    assert term[0].slug == '62156489'


def test_query_2(app, db):
    sqlalchemy_query = find_in_json_list("institutions", "aliases",
                                         "Katedra experimentální biologie rostlin")
    term = sqlalchemy_query.one_or_none()
    assert term[0].slug == '62156489'


def test_get_query_by_slug(app, db):
    query = get_query_by_slug("subjects", "PSH120")
    terms = query.all()
    print(query, terms)
