from pprint import pprint


def test_24500_1(app, db):
    from nr_oai_pmh_harvester.rules.nusl.field24500 import get_title
    el = [
        {
            "a": "czech",
            "b": "english"
        },
        {
            "a": "czech 2",
            "b": "english 2"
        },
    ]
    res = get_title(el, {
        "record": {
            "04107":
                {"a": "cze"}
        }
    })
    assert res == {
        'title': [
            {'cs': 'czech', 'en': 'english'},
            {'cs': 'czech 2', 'en': 'english 2'}
        ]
    }
