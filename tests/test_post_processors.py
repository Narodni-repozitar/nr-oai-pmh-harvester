def test_remove_duplicates(app, db):
    from nr_oai_pmh_harvester.post_processors import remove_duplicates
    res = remove_duplicates(input())
    assert res == [{
                       'ico': '00216208', 'url': 'http://www.cuni.cz', 'type': ['veřejná VŠ'],
                       'title': {'cs': 'Univerzita Karlova', 'en': 'Charles University'},
                       'status': 'active', 'aliases': ['UK'], 'related': {'rid': '11000'},
                       'provider': 'true', 'is_ancestor': True, 'links': {
            'self': 'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208'
        }
                   }, {
                       'title': {'cs': 'Přírodovědecká fakulta', 'en': 'Faculty of Science'},
                       'is_ancestor': True, 'links': {
            'self': 'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208'
                    '/prirodovedecka-fakulta-3',
            'parent': 'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208'
        }
                   }, {
                       'title': {'cs': 'Katedra experimentální biologie rostlin'},
                       'is_ancestor': False, 'links': {
            'self': 'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208'
                    '/prirodovedecka-fakulta-3/katedra-experimentalni-biologie-rostlin-1',
            'parent': 'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208'
                      '/prirodovedecka-fakulta-3'
        }
                   }]


def input():
    return [{
        'ico': '00216208', 'url': 'http://www.cuni.cz', 'type': ['veřejná VŠ'],
        'title': {'cs': 'Univerzita Karlova', 'en': 'Charles University'},
        'status': 'active', 'aliases': ['UK'], 'related': {'rid': '11000'},
        'provider': 'true', 'is_ancestor': True,
        'links': {'self': 'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208'}
    }, {
        'title': {'cs': 'Přírodovědecká fakulta', 'en': 'Faculty of Science'},
        'is_ancestor': True, 'links': {
            'self': 'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208'
                    '/prirodovedecka-fakulta-3',
            'parent': 'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208'
        }
    }, {
        'title': {'cs': 'Katedra experimentální biologie rostlin'}, 'is_ancestor': False,
        'links': {
            'self': 'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208'
                    '/prirodovedecka-fakulta-3/katedra-experimentalni-biologie-rostlin-1',
            'parent': 'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208'
                      '/prirodovedecka-fakulta-3'
        }
    }, {
        'title': {'cs': 'Přírodovědecká fakulta', 'en': 'Faculty of Science'},
        'is_ancestor': False, 'links': {
            'self': 'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208'
                    '/prirodovedecka-fakulta-3',
            'parent': 'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208'
        }
    }]
