from nr_oai_pmh_harvester.query import find_in_json_list


def test_query(app, db):
    sqlalchemy_query = find_in_json_list("institutions", "formerNames", "Vysoká škola zemědělská v Brně")
    term = sqlalchemy_query.all()
    assert term[0].slug == '62156489'


