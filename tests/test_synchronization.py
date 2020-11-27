from oarepo_oai_pmh_harvester.proxies import current_oai_client


def test_synchronization(app, db):
    current_oai_client.run()
