import pathlib
from datetime import datetime
from pprint import pprint

import pytest

from nr_oai_pmh_harvester.rules.utils import filter_language


@pytest.mark.skip(reason="Potřebuje databazi s taxonomii. Nahradit nějakým mockem")
def test_subject_1(app, db):
    from nr_oai_pmh_harvester.rules.uk.dc_subject import subject
    el = [{'cs_CZ': [{'value': ['Bouzouki: řecký národní nástroj']}]}]
    res = subject(el)
    assert res == {'subject': [], 'keywords': [{'cs': 'Bouzouki: řecký národní nástroj'}]}


@pytest.mark.skip(reason="Potřebuje databazi s taxonomii. Nahradit nějakým mockem")
def test_subject_2(app, db):
    from nr_oai_pmh_harvester.rules.uk.dc_subject import subject
    el = [{
        'en_US': [{
            'value': ['Microseismic monitoring', 'hydraulic fracturing',
                      'moment tensor', 'source mechanisms', 'geomechanical model']
        }], 'cs_CZ': [{
            'value': ['Mikroseismické monitorování',
                      'hydraulické štěpení', 'momentový tenzor',
                      'zdrojové mechanismy', 'geomechanický model']
        }]
    }]
    res = subject(el)
    assert res == {
        'subject': [], 'keywords': [
            {'en': 'Microseismic monitoring', 'cs': 'Mikroseismické monitorování'},
            {'en': 'hydraulic fracturing', 'cs': 'hydraulické štěpení'},
            {'en': 'moment tensor', 'cs': 'momentový tenzor'},
            {'en': 'source mechanisms', 'cs': 'zdrojové mechanismy'},
            {'en': 'geomechanical model', 'cs': 'geomechanický model'}]
    }


@pytest.mark.skip(reason="Potřebuje databazi s taxonomii. Nahradit nějakým mockem")
def test_subject_3(app, db):
    from nr_oai_pmh_harvester.rules.uk.dc_subject import subject
    el = [
        {
            "en_US": [
                {
                    "value": [
                        "Quaternary benzo[c]fenanthridine alkaloids",
                        "sanguinarine",
                        "apoptosis"
                    ]
                }
            ],
            "cs_CZ": [
                {
                    "value": [
                        "Kvartérní benzo[c]fenantridinové alkaloidy",
                        "sanguinarin",
                        "apoptosa"
                    ]
                }
            ]
        }
    ]
    res = subject(el)
    assert res == {
        'keywords': [{
            'cs': 'Kvartérní benzo[c]fenantridinové alkaloidy',
            'en': 'Quaternary benzo[c]fenanthridine alkaloids'
        },
            {'cs': 'sanguinarin', 'en': 'sanguinarine'},
            {'cs': 'apoptosa', 'en': 'apoptosis'}],
        'subject': []
    }


@pytest.mark.skip(reason="Potřebuje databazi s taxonomii. Nahradit nějakým mockem")
def test_subject_4(app, db):
    from nr_oai_pmh_harvester.rules.uk.dc_subject import subject
    for i in range(100):
        el = [{
            'cs_CZ': [{
                'value': ['Přejatá slova', 'Pravidla českého pravopisu',
                          'dubleta (psaní z', 's', '-ing', '-ink', 'délka vokálů)',
                          'denní tisk']
            }], 'en_US': [{
                'value': ['Loanwords',
                          'Pravidla českého pravopisu (The Rules of the '
                          'Czech Ortography)',
                          'double form (z', 's', '-ing', '-ink', 'short',
                          'long vowels)', 'daily press']
            }]
        }]
        t0 = datetime.now()
        res = subject(el)
        dt = datetime.now() - t0
        print(f"Time {dt}")
        assert res == {
            'subject': [], 'keywords': [{'cs': 'Přejatá slova', 'en': 'Loanwords'}, {
                'cs': 'Pravidla českého pravopisu',
                'en': 'Pravidla českého pravopisu (The Rules of the Czech Ortography)'
            }, {'cs': 'dubleta (psaní z', 'en': 'double form (z'}, {'cs': 's', 'en': 's'},
                                        {'cs': '-ing', 'en': '-ing'},
                                        {'cs': '-ink', 'en': '-ink'},
                                        {'cs': 'délka vokálů)', 'en': 'short'},
                                        {'cs': 'denní tisk', 'en': 'long vowels)'}]
        }


def test_filter_language():
    el = [{'cs_CZ': [{'value': ['Bouzouki: řecký národní nástroj']}]}]
    t0 = datetime.now()
    res = filter_language(el)
    dt = datetime.now() - t0
    print(f"Time {dt}")
    assert res == {'cs_CZ': 'Bouzouki: řecký národní nástroj'}


def test_filter_language_2():
    el = [{
        'en_US': [{
            'value': ['Microseismic monitoring', 'hydraulic fracturing',
                      'moment tensor', 'source mechanisms', 'geomechanical model']
        }], 'cs_CZ': [{
            'value': ['Mikroseismické monitorování',
                      'hydraulické štěpení', 'momentový tenzor',
                      'zdrojové mechanismy', 'geomechanický model']
        }]
    }]
    res = filter_language(el)
    assert res == {
        'cs_CZ': ['Mikroseismické monitorování',
                  'hydraulické štěpení',
                  'momentový tenzor',
                  'zdrojové mechanismy',
                  'geomechanický model'],
        'en_US': ['Microseismic monitoring',
                  'hydraulic fracturing',
                  'moment tensor',
                  'source mechanisms',
                  'geomechanical model']
    }


def test_filter_language_3():
    el = {
        'cs_CZ': [{
            'value': ['komparative Phonetik', None, 'l ʃ d t', None, 'Tschechisch',
                      'Deutsch', 'sprachliche Akkommodation', 'Palatalisation',
                      'Velarisation', 'Dentalisation', 'akustische Analyse']
        }], 'en_US': [{
            'value': ['comparative phonetics', None, 'l ʃ d t', None,
                      'Czech', 'German', 'speech accommodation',
                      'palatalization', 'velarization', 'dentalization',
                      'acoustic analysis']
        }]
    }
    res = filter_language(el)
    assert res == {
        'cs_CZ': ['komparative Phonetik',
                  'l ʃ d t',
                  'Tschechisch',
                  'Deutsch',
                  'sprachliche Akkommodation',
                  'Palatalisation',
                  'Velarisation',
                  'Dentalisation',
                  'akustische Analyse'],
        'en_US': ['comparative phonetics',
                  'l ʃ d t',
                  'Czech',
                  'German',
                  'speech accommodation',
                  'palatalization',
                  'velarization',
                  'dentalization',
                  'acoustic analysis']
    }


def test_reformat_1(app, db):
    from nr_oai_pmh_harvester.rules.uk.dc_subject import reformat
    el = {'cs_CZ': 'Bouzouki: řecký národní nástroj'}
    res = reformat(el)
    assert res == [{'cs_CZ': 'Bouzouki: řecký národní nástroj'}]


def test_reformat_2(app, db):
    from nr_oai_pmh_harvester.rules.uk.dc_subject import reformat
    el = {
        'cs_CZ': ['Mikroseismické monitorování',
                  'hydraulické štěpení',
                  'momentový tenzor',
                  'zdrojové mechanismy',
                  'geomechanický model'],
        'en_US': ['Microseismic monitoring',
                  'hydraulic fracturing',
                  'moment tensor',
                  'source mechanisms',
                  'geomechanical model']
    }
    res = reformat(el)
    assert res == [{'cs_CZ': 'Mikroseismické monitorování', 'en_US': 'Microseismic monitoring'},
                   {'cs_CZ': 'hydraulické štěpení', 'en_US': 'hydraulic fracturing'},
                   {'cs_CZ': 'momentový tenzor', 'en_US': 'moment tensor'},
                   {'cs_CZ': 'zdrojové mechanismy', 'en_US': 'source mechanisms'},
                   {'cs_CZ': 'geomechanický model', 'en_US': 'geomechanical model'}]


@pytest.mark.skip(reason="Potřebuje databazi s taxonomii. Nahradit nějakým mockem")
def test_speed_subject(app, db):
    from nr_oai_pmh_harvester.rules.uk.dc_subject import get_subject_by_title
    root_dir = pathlib.Path(__file__).parent.absolute()
    with open(str(root_dir / ".." / ".." / "data" / "cs_CZ_utf8.dic"), "r") as f:
        for i, line in enumerate(f):
            t0 = datetime.now()
            res = get_subject_by_title(line.strip(), "cs")
            dt = datetime.now() - t0
            # pprint(res)
            print(f"Time: {dt}")
            if i == 100:
                break


@pytest.mark.skip(reason="Potřebuje databazi s taxonomii. Nahradit nějakým mockem")
def test_speed_subject_2(app, db):
    el = [
        {
            'en_US': [
                {
                    'value': ['Microseismic monitoring', 'hydraulic fracturing',
                              'moment tensor', 'source mechanisms', 'geomechanical model']
                }
            ],
            'cs_CZ': [
                {
                    'value': ['Mikroseismické monitorování',
                              'hydraulické štěpení', 'momentový tenzor',
                              'zdrojové mechanismy', 'geomechanický model']
                }
            ]
        }
    ]
    from nr_oai_pmh_harvester.rules.uk.dc_subject import subject
    root_dir = pathlib.Path(__file__).parent.absolute()
    with open(str(root_dir / ".." / ".." / "data" / "cs_CZ_utf8.dic"), "r") as f:
        for i, line in enumerate(f):
            el[0]["cs_CZ"][0]["value"].append(line.strip().split("/")[0])
            el[0]["en_US"][0]["value"].append(line.strip().split("/")[0])
            if i == 1000:
                break
    res = subject(el)
    pprint(res)


@pytest.mark.skip(reason="Potřebuje databazi s taxonomii. Nahradit nějakým mockem")
def test_speed_subject_3(app, db):
    el = [{
        'cs_CZ': [{
            'value': ['Osobní asistence', 'financování osobní asistence',
                      'epilepsie', 'epileptický záchvat', 'léčba epilepsie',
                      'Lennox-Gastautův syndrom',
                      'typy záchvatů při tomto syndromu']
        }], 'en_US': [{
            'value': ['Personal assistance',
                      'financing personal assistance', 'epilepsy',
                      'epileptic seizure', 'treatment of epilepsy',
                      'Lennox-Gastaut syndrome',
                      'types of seizures in this syndrome']
        }]
    }]
    from nr_oai_pmh_harvester.rules.uk.dc_subject import subject
    for i in range(100):
        t0 = datetime.now()
        subject(el)
        dt = datetime.now() - t0
        print(f"Cycle time: {dt}")
