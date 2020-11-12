import pytest
from flask_taxonomies.proxies import current_flask_taxonomies
from flask_taxonomies.term_identification import TermIdentification

from nr_oai_pmh_harvester.rules.nusl.field502__c import degree_grantor, choose_term


def test_choose_term(app, db):
    taxonomy = current_flask_taxonomies.get_taxonomy(code="institutions")
    term_identification = TermIdentification(taxonomy=taxonomy,
                                             slug="216305/institut-celozivotniho-vzdelavani-1")
    term1 = list(current_flask_taxonomies.filter_term(term_identification))[0]

    term_identification2 = TermIdentification(taxonomy=taxonomy,
                                              slug='62156489/institut-celozivotniho-vzdelavani')
    term2 = list(current_flask_taxonomies.filter_term(term_identification2))[0]
    terms = [term1, term2]
    grantor_array = ['Mendelova univerzita', 'Institut celoživotního vzdělávání']
    reversed_grantor_array = reversed(grantor_array)
    term = choose_term(terms, reversed_grantor_array, reversed_level=0)
    assert term.slug == '62156489/institut-celozivotniho-vzdelavani'


def test_degree_grantor(app, db):
    res = degree_grantor("Vysoká škola zemědělská v Brně")
    assert res == {
        'degreeGrantor': [{
            'aliases': ['MENDELU', 'Mendelova univerzita'],
            'formerNames': ['Vysoká škola zemědělská v Brně',
                            'Mendelova zemědělská a lesnická '
                            'univerzita v Brně'],
            'ico': '62156489',
            'is_ancestor': True,
            'links': {
                'self':
                    'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489'
            },
            'provider': 'true',
            'related': {'rid': '43000'},
            'status': 'active',
            'title': {
                'cs': 'Mendelova univerzita v Brně',
                'en': 'Mendel University in Brno'
            },
            'type': ['veřejná VŠ'],
            'url': 'www.mendelu.cz'
        },
            {
                'aliases': ['Fakulta Institut celoživotního vzdělávání'],
                'is_ancestor': False,
                'links': {
                    'parent':
                        'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489',
                    'self':
                        'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489/institut'
                        '-celozivotniho-vzdelavani'
                },
                'title': {'cs': 'Institut celoživotního vzdělávání'}
            }]
    }


def test_degree_grantor_2(app, db):
    res = degree_grantor("Mendelova univerzita, Institut celoživotního vzdělávání")
    assert res == {
        'degreeGrantor': [{
            'aliases': ['MENDELU', 'Mendelova univerzita'],
            'formerNames': ['Vysoká škola zemědělská v Brně',
                            'Mendelova zemědělská a lesnická '
                            'univerzita v Brně'],
            'ico': '62156489',
            'is_ancestor': True,
            'links': {
                'self':
                    'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489'
            },
            'provider': 'true',
            'related': {'rid': '43000'},
            'status': 'active',
            'title': {
                'cs': 'Mendelova univerzita v Brně',
                'en': 'Mendel University in Brno'
            },
            'type': ['veřejná VŠ'],
            'url': 'www.mendelu.cz'
        },
            {
                'aliases': ['Fakulta Institut celoživotního vzdělávání'],
                'is_ancestor': False,
                'links': {
                    'parent':
                        'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489',
                    'self':
                        'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489/institut'
                        '-celozivotniho-vzdelavani'
                },
                'title': {'cs': 'Institut celoživotního vzdělávání'}
            }]
    }


def test_degree_grantor_3(app, db):
    res = degree_grantor("MENDELU")
    assert res == {
        'degreeGrantor': [{
            'aliases': ['MENDELU', 'Mendelova univerzita'],
            'formerNames': ['Vysoká škola zemědělská v Brně',
                            'Mendelova zemědělská a lesnická '
                            'univerzita v Brně'],
            'ico': '62156489',
            'is_ancestor': True,
            'links': {
                'self':
                    'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489'
            },
            'provider': 'true',
            'related': {'rid': '43000'},
            'status': 'active',
            'title': {
                'cs': 'Mendelova univerzita v Brně',
                'en': 'Mendel University in Brno'
            },
            'type': ['veřejná VŠ'],
            'url': 'www.mendelu.cz'
        },
            {
                'aliases': ['Fakulta Institut celoživotního vzdělávání'],
                'is_ancestor': False,
                'links': {
                    'parent':
                        'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489',
                    'self':
                        'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489/institut'
                        '-celozivotniho-vzdelavani'
                },
                'title': {'cs': 'Institut celoživotního vzdělávání'}
            }]
    }


def test_degree_grantor_4(app, db):
    res = degree_grantor("Mendelova univerzita (Brno), Fakulta provozně ekonomická")
    assert res == {
        'degreeGrantor': [{
            'aliases': ['MENDELU',
                        'Mendelova univerzita',
                        'Mendelova zemědělská a lesnická univerzita',
                        'Mendelova univerzita (Brno)'],
            'formerNames': ['Vysoká škola zemědělská v Brně',
                            'Mendelova zemědělská a lesnická '
                            'univerzita v Brně'],
            'ico': '62156489',
            'is_ancestor': True,
            'links': {
                'self':
                    'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489'
            },
            'provider': 'true',
            'related': {'rid': '43000'},
            'status': 'active',
            'title': {
                'cs': 'Mendelova univerzita v Brně',
                'en': 'Mendel University in Brno'
            },
            'type': ['veřejná VŠ'],
            'url': 'www.mendelu.cz'
        },
            {
                'aliases': ['Fakulta provozně ekonomická'],
                'is_ancestor': False,
                'links': {
                    'parent':
                        'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489',
                    'self':
                        'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489/provozne'
                        '-ekonomicka-fakulta'
                },
                'title': {'cs': 'Provozně ekonomická fakulta'}
            }]
    }


def test_degree_grantor_5(app, db):
    res = degree_grantor(", Agronomická a zootechnická fakulta")
    assert res == {
        'degreeGrantor': [{
            'aliases': ['MENDELU',
                        'Mendelova univerzita',
                        'Mendelova zemědělská a lesnická univerzita',
                        'Mendelova univerzita (Brno)'],
            'formerNames': ['Vysoká škola zemědělská v Brně',
                            'Mendelova zemědělská a lesnická '
                            'univerzita v Brně'],
            'ico': '62156489',
            'is_ancestor': True,
            'links': {
                'self':
                    'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489'
            },
            'provider': 'true',
            'related': {'rid': '43000'},
            'status': 'active',
            'title': {
                'cs': 'Mendelova univerzita v Brně',
                'en': 'Mendel University in Brno'
            },
            'type': ['veřejná VŠ'],
            'url': 'www.mendelu.cz'
        },
            {
                'aliases': ['Agronomická a zootechnická fakulta'],
                'is_ancestor': False,
                'links': {
                    'parent':
                        'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489',
                    'self':
                        'http://127.0.0.1:5000/api/2.0/taxonomies/institutions/62156489'
                        '/agronomicka-fakulta'
                },
                'title': {'cs': 'Agronomická fakulta'}
            }]
    }


def test_degree_grantor_6(app, db, input_data):
    for _ in input_data:
        university_name = _["key"]
        if university_name in ["Akademie věd České republiky", ", Lednice na Moravě", ", Ústav agrikulturní chemie", ", Ústav agrochemický"]:
            continue
        print(university_name)
        res = degree_grantor(university_name)
        assert res is not None, f"{university_name}"


@pytest.fixture()
def input_data():
    return [
        {
            "key": "Univerzita Karlova",
            "doc_count": 69469
        },
        {
            "key": "Vysoká škola ekonomická v Praze",
            "doc_count": 40554
        },
        {
            "key": "JIHOČESKÁ UNIVERZITA V ČESKÝCH BUDĚJOVICÍCH",
            "doc_count": 29446
        },
        {
            "key": "Mendelova univerzita, Provozně ekonomická fakulta",
            "doc_count": 5162
        },
        {
            "key": "Mendelova univerzita, Agronomická fakulta",
            "doc_count": 4242
        },
        {
            "key": "Mendelova univerzita, Lesnická a dřevařská fakulta",
            "doc_count": 2477
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Agronomická fakulta",
            "doc_count": 1847
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Provozně ekonomická fakulta",
            "doc_count": 1744
        },
        {
            "key": "Mendelova univerzita, Fakulta regionálního rozvoje a mezinárodních studií",
            "doc_count": 1191
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Lesnická a dřevařská fakulta",
            "doc_count": 1129
        },
        {
            "key": "Mendelova univerzita, Zahradnická fakulta",
            "doc_count": 950
        },
        {
            "key": "Akademie múzických umění v Praze.Hudební a taneční fakulta",
            "doc_count": 724
        },
        {
            "key": "Akademie múzických umění v Praze. Hudební a taneční fakulta AMU",
            "doc_count": 686
        },
        {
            "key": "Akademie múzických umění v Praze. Divadelní fakulta AMU",
            "doc_count": 589
        },
        {
            "key": "Akademie múzických umění v Praze. Filmová a televizní fakulta AMU",
            "doc_count": 584
        },
        {
            "key": "Akademie múzických umění v Praze.Divadelní fakulta",
            "doc_count": 476
        },
        {
            "key": "Akademie múzických umění v Praze.Filmová a televizní fakulta",
            "doc_count": 453
        },
        {
            "key": "Mendelova univerzita, Institut celoživotního vzdělávání",
            "doc_count": 445
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Agronomická fakulta",
            "doc_count": 260
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita",
            "doc_count": 244
        },
        {
            "key": "Vysoká škola zemědělská v Brně",
            "doc_count": 238
        },
        {
            "key": "Mendelova univerzita",
            "doc_count": 221
        },
        {
            "key": "Akademie múzických umění v Praze. Hudební fakulta AMU",
            "doc_count": 142
        },
        {
            "key": "Mendelova univerzita (Brno), Fakulta lesnická a dřevařská",
            "doc_count": 138
        },
        {
            "key": "Mendelova univerzita (Brno), Fakulta provozně ekonomická",
            "doc_count": 109
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Zahradnická fakulta",
            "doc_count": 69
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Provozně ekonomická fakulta",
            "doc_count": 38
        },
        {
            "key": ", Agronomická a zootechnická fakulta",
            "doc_count": 25
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Lesnická fakulta",
            "doc_count": 17
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Institut celoživotního vzdělávání",
            "doc_count": 15
        },
        {
            "key": "Vysoká škola zemědělská a lesnická v Brně, Lesnická fakulta",
            "doc_count": 12
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav morfologie, fyziologie a "
                   "genetiky zvířat",
            "doc_count": 11
        },
        {
            "key": "Univerzita Karlova, Právnická fakulta",
            "doc_count": 11
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav zemědělské, potravinářské a "
                   "environmentální techniky",
            "doc_count": 10
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav chovu a šlechtění zvířat",
            "doc_count": 9
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav agrochemie, půdoznalství, "
                   "mikrobiologie a výživy rostlin",
            "doc_count": 8
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav aplikované a krajinné "
                   "ekologie",
            "doc_count": 8
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav chovu hospodářských zvířat",
            "doc_count": 8
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav technologie potravin",
            "doc_count": 8
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav šlechtění a množení "
                   "zahradnických rostlin",
            "doc_count": 8
        },
        {
            "key": "Vysoká škola zemědělská a lesnická v Brně",
            "doc_count": 8
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav chemie a biochemie",
            "doc_count": 7
        },
        {
            "key": "Mendelova univerzita (Brno), Fakulta Institut celoživotního vzdělávání",
            "doc_count": 6
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav lesnické botaniky, "
                   "dendrologie a geobiocenologie",
            "doc_count": 6
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav nábytku, designu a bydlení",
            "doc_count": 6
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav ochrany lesů a myslivosti",
            "doc_count": 6
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav účetnictví a daní",
            "doc_count": 6
        },
        {
            "key": "Vysoká škola zemědělská a lesnická v Brně, Zootechnická fakulta",
            "doc_count": 6
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra zemědělské techniky",
            "doc_count": 6
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra základní agrotechniky",
            "doc_count": 6
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav lesnické botaniky, "
                   "dendrologie a typologie",
            "doc_count": 5
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav pěstování a šlechtění "
                   "rostlin",
            "doc_count": 5
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav techniky a automobilové "
                   "dopravy",
            "doc_count": 5
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav tvorby a ochrany krajiny",
            "doc_count": 5
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav výživy zvířat a pícninářství",
            "doc_count": 5
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav základů techniky a "
                   "automobilové dopravy",
            "doc_count": 5
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra hospodářské úpravy lesa",
            "doc_count": 5
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra půdoznalství a meteorologie",
            "doc_count": 5
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra rostlinné výroby",
            "doc_count": 5
        },
        {
            "key": ", Agronomická fakulta",
            "doc_count": 4
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav biologie rostlin",
            "doc_count": 4
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav managementu",
            "doc_count": 4
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav nauky o dřevě",
            "doc_count": 4
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav zakládání a pěstění lesů",
            "doc_count": 4
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra obecné zootechniky",
            "doc_count": 4
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav biotechniky zeleně",
            "doc_count": 3
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav ekonomie",
            "doc_count": 3
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav hospodářské úpravy lesů",
            "doc_count": 3
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav podnikové ekonomiky",
            "doc_count": 3
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav pěstování, šlechtění "
                   "rostlin a rostlinolékařství",
            "doc_count": 3
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav výživy a krmení "
                   "hospodářských zvířat",
            "doc_count": 3
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav zahradní a krajinářské "
                   "architektury",
            "doc_count": 3
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav základního zpracování dřeva",
            "doc_count": 3
        },
        {
            "key": "Univerzita Karlova, Pedagogická fakulta (Praha, Česko)",
            "doc_count": 3
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra sadovnictví, krajinářství a "
                   "květinářství",
            "doc_count": 3
        },
        {
            "key": "Akademie věd České republiky",
            "doc_count": 2
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav agrosystémů a "
                   "bioklimatologie",
            "doc_count": 2
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav botaniky a fyziologie "
                   "rostlin",
            "doc_count": 2
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav ekologie lesa",
            "doc_count": 2
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav lesnické a dřevařské "
                   "techniky",
            "doc_count": 2
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav marketingu a obchodu",
            "doc_count": 2
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav ochrany rostlin",
            "doc_count": 2
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav půdoznalství a mikrobiologie",
            "doc_count": 2
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav statistiky a operačního "
                   "výzkumu",
            "doc_count": 2
        },
        {
            "key": "Mendelova zemědělská a lesnická univerzita, Ústav zoologie, rybářství, "
                   "hydrobiologie a včelařství",
            "doc_count": 2
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra botaniky a mikrobiologie",
            "doc_count": 2
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra chovu koní, ovcí a kožešinových zvířat",
            "doc_count": 2
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra chovu skotu",
            "doc_count": 2
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra ekonomiky a řízení zemědělství",
            "doc_count": 2
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra inženýrských staveb lesnických a "
                   "hrazení bystřin",
            "doc_count": 2
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra lesnické botaniky a fytocenologie",
            "doc_count": 2
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra organizace podniků a pracovních "
                   "procesů v zemědělství",
            "doc_count": 2
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra politické ekonomie",
            "doc_count": 2
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra půdoznalství, meteorologie a "
                   "klimatologie",
            "doc_count": 2
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra zemědělské ekonomiky a organizace "
                   "socialistických zemědělských podniků",
            "doc_count": 2
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Katedra šlechtění rostlin a zahradnictví",
            "doc_count": 2
        },
        {
            "key": "Vysoká škola zemědělská v Brně, Zootechnická fakulta",
            "doc_count": 2
        },
        {
            "key": ", Lednice na Moravě",
            "doc_count": 1
        },
        {
            "key": ", Ústav agrikulturní chemie",
            "doc_count": 1
        },
        {
            "key": ", Ústav agrochemický",
            "doc_count": 1
        }
    ]
