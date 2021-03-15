def test_language(app, db):
    from nr_oai_pmh_harvester.rules.nusl.field04107 import language
    res = language({'a': 'cze'})
    assert res == {
        'language': [{
                         'alias': 'ces',
                         'alpha2': 'cs',
                         'is_ancestor': False,
                         'links': {
                             'self': 'http://127.0.0.1:5000/api/2.0/taxonomies/languages/cze'
                         },
                         'title': {'cs': 'čeština', 'en': 'Czech'}
                     }]
    }
