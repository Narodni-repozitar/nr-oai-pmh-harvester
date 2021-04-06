import pytest


@pytest.mark.skip(reason="Potřebuje databazi s taxonomii. Nahradit nějakým mockem")
def test_date_issued_1(app, db):
    from nr_oai_pmh_harvester.rules.uk.dc_date_issued import date_issued
    res = date_issued([["2005"]])
    assert res == {
        'accessRights': [{
                             'is_ancestor': False,
                             'level': 1,
                             'links': {
                                 'self':
                                     'http://127.0.0.1:5000/api/2.0/taxonomies/accessRights/c-16ec'
                             },
                             'relatedURI': {'coar': 'http://purl.org/coar/access_right/c_16ec'},
                             'title': {
                                 'cs': 'omezený přístup',
                                 'en': 'restricted access'
                             }
                         }],
        'accessibility': {
            'cs': 'Dostupné v digitálním repozitáři UK (pouze z IP '
                  'adres univerzity).',
            'en': 'Available in the Charles University Digital '
                  'Repository (accessible only from computers with '
                  'university IP address).'
        },
        'dateIssued': '2005'
    }


def test_date_issued_2(app, db):
    from nr_oai_pmh_harvester.rules.uk.dc_date_issued import date_issued
    res = date_issued([["2006"]])
    assert res == {'dateIssued': '2006'}
