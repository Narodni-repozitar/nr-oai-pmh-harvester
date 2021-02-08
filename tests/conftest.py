import pathlib
import shutil
import tempfile

import pytest
from flask import Flask
from flask_principal import Principal
from invenio_access import InvenioAccess
from invenio_accounts import InvenioAccounts
from invenio_base.signals import app_loaded
from invenio_db import InvenioDB
from invenio_db import db as db_
from invenio_indexer import InvenioIndexer
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords
from invenio_records_rest import InvenioRecordsREST
from invenio_records_rest.utils import PIDConverter
from invenio_search import InvenioSearch, current_search_client
from lxml import etree
from nr_common.ext import NRCommon
from nr_events import NREvents
from nr_nresults import NRNresults
from nr_theses import NRTheses
from oarepo_oai_pmh_harvester.ext import OArepoOAIClient
from oarepo_records_draft.ext import RecordsDraft
from oarepo_taxonomies.ext import OarepoTaxonomies
from oarepo_validate.ext import OARepoValidate
from sqlalchemy_utils import database_exists, create_database


@pytest.yield_fixture()
def app():
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)

    app.config.update(
        JSONSCHEMAS_HOST="nusl.cz",
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SERVER_NAME='127.0.0.1:5000',
        INVENIO_INSTANCE_PATH=instance_path,
        DEBUG=True,
        # SQLALCHEMY_ECHO=True,
        SUPPORTED_LANGUAGES=["cs", "en"],
        SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://oarepo:oarepo@localhost/oarepo',
        OAREPO_OAI_PROVIDERS={
            "nusl": {
                "description": "NUŠL",
                "synchronizers": [
                    {
                        "name": "marcxml",
                        "oai_endpoint": "http://invenio.nusl.cz/oai2d/",
                        "set": "global",
                        "metadata_prefix": "marcxml",
                        "unhandled_paths": ['/leader', '/005', '/008', '020__/q', '/0248_',
                                            '/246__', '/340__', '/500__', '/502__/a', '/502__/b',
                                            '/502__/d', '/502__/g', '/506__', '/6530_', '/6557_',
                                            '/655_7', "/656_7/2", '/8560_',
                                            '/85642/z', '/8564_', '/909CO/p', '999c1', '/999C2',
                                            'FFT_0'],
                        "default_endpoint": "common",
                    }
                ]
            },
        },
        # RECORDS_REST_ENDPOINTS=RECORDS_REST_ENDPOINTS,
        PIDSTORE_RECID_FIELD='pid'
    )

    app.secret_key = 'changeme'

    InvenioDB(app)
    InvenioAccounts(app)
    InvenioAccess(app)
    Principal(app)
    InvenioJSONSchemas(app)
    InvenioSearch(app)
    InvenioIndexer(app)
    InvenioRecords(app)
    InvenioRecordsREST(app)
    InvenioPIDStore(app)
    app.url_map.converters['pid'] = PIDConverter
    OarepoTaxonomies(app)
    OArepoOAIClient(app)
    OARepoValidate(app)
    RecordsDraft(app)
    NRCommon(app)
    NRTheses(app)
    NRNresults(app)
    NREvents(app)

    app_loaded.send(app, app=app)

    with app.app_context():
        yield app

    shutil.rmtree(instance_path)


@pytest.yield_fixture()
def db(app):
    """Database fixture."""
    if not database_exists(str(db_.engine.url)):
        create_database(str(db_.engine.url))
    db_.create_all()
    yield db_


@pytest.fixture()
def xml():
    this_directory = pathlib.Path(__file__).parent.absolute()
    response_path = this_directory / "data" / "response.xml"
    with open(str(response_path), "r") as f:
        tree = etree.parse(f)
        root = tree.getroot()
    return root


@pytest.fixture()
def load_entry_points():
    import pkg_resources
    distribution = pkg_resources.Distribution(__file__)
    entry_point = pkg_resources.EntryPoint.parse('parsers = nr_oai_pmh_harvester.parser',
                                                 dist=distribution)
    entry_point2 = pkg_resources.EntryPoint.parse(
        'field001 = nr_oai_pmh_harvester.rules.nusl.field001', dist=distribution)
    distribution._ep_map = {
        'oarepo_oai_pmh_harvester.parsers': {'parsers': entry_point},
        'oarepo_oai_pmh_harvester.rules': {'field001': entry_point2}
    }
    pkg_resources.working_set.add(distribution)


@pytest.fixture()
def index(app):
    """"Returns fresh ES index"""
    with app.app_context():
        index = "test_index"
        if not current_search_client.indices.exists(index):
            current_search_client.indices.create(
                index=index,
                ignore=400,
                body={}
            )
        yield index
        if current_search_client.indices.exists("test_index"):
            current_search_client.indices.delete(index="test_index")


@pytest.fixture()
def valid_uk_record():
    return {
        "contributor": [
            {
                "name": "Eisner, Leo",
                "role": [
                    {
                        "title": {
                            "cs": "vedoucí",
                            "en": "advisor"
                        },
                        "marcCode": "ths",
                        "is_ancestor": False,
                        "links": {
                            "self": "http://127.0.0.1:5000/api/2.0/taxonomies/contributor-type"
                                    "/advisor"
                        }
                    }
                ]
            }
        ],
        "creator": [
            {
                "name": "Staněk, František"
            }
        ],
        "dateIssued": "2018",
        "recordIdentifiers": {
            "originalRecord": "http://hdl.handle.net/20.500.11956/103772",
            "originalRecordOAI": "oai:dspace.cuni.cz:20.500.11956/103772"
        },
        "abstract": {
            "cs": "Pochopení ekonomické úspěšnosti nekonvenční těžby z břidlic vyžaduje "
                  "vysvětlení vztahu mezi indukovanou seismicitou a hydraulickým štěpením. Tato "
                  "práce se zabývá pozorováním a analýzou syntetických a reálných dat z "
                  "hydraulického štěpení a seismického monitorování. Zejména se opírá o analýzu "
                  "zdrojových mechanismů indukovaných seismických jevů, které se v několika "
                  "posledních letech začaly určovat a interpretovat i v průmyslu. Výsledky "
                  "analýzy jsou interpretovány pomocí geomechanického modelu vztahu mezi "
                  "hydraulickým štěpením břidlic a indukovanou seismicitou. Studium zdrojových "
                  "mechanismů začíná detailní analýzou prostorového rozložení stability inverze "
                  "plného momentového tensoru, které bylo vymapováno dle synteticky napočtených "
                  "kondičních čísel v prostoru okolo různých typů monitorovacích sítí, zahrnující "
                  "husté sítě na povrchu, ale i řídké sítě s přijímači ve vrtech. Stabilita "
                  "výpočtu zdrojových mechanismů byla testována v závislosti na různých "
                  "podmínkách, především pak na velikosti a geometrii monitorovací sítě a různých "
                  "hladinách šumu v datech. V této práci je ukázáno, že husté povrchové "
                  "monitorovací sítě mohou dosahovat velmi dobré stability invertovaných "
                  "zdrojových mechanismů, které mohou být dále interpretovány. Zároveň tato "
                  "studie ukazuje rostoucí podíl nestřižné složky momentového tensoru s...",
            "en": "Understanding economic success of unconventional production from shales "
                  "requires an explanation of the relationship between induced seismicity and "
                  "hydraulic fracturing. This thesis deals with observing and analyzing synthetic "
                  "and real microseismic monitoring data acquired during hydraulic fracturing. "
                  "The thesis is based on observation and analyses of source mechanisms of "
                  "induced microseismic events that have recently become regularly inverted and "
                  "interpreted in the oil and gas industry. The results of analyses are "
                  "interpreted with the geomechanical model of the relationship between hydraulic "
                  "fracturing and induced seismicity. The study of source mechanisms starts with "
                  "detailed analyses of spatial distribution of full moment tensor inversion "
                  "stability. It was mapped based on synthetically computed condition numbers in "
                  "the vicinity of different monitoring arrays including dense arrays at the "
                  "surface and sparse arrays with sensors in the boreholes. Stability of "
                  "inversion was tested under several conditions, mainly dependency on size and "
                  "geometry of monitoring array and level of noise in the data. In this part of "
                  "the thesis it is shown that dense surface arrays may provide very stable "
                  "inversion of source mechanisms which may be interpreted. The study shows that "
                  "an increasing percentage of non-shear..."
        },
        "degreeGrantor": [
            {
                "ico": "00216208",
                "url": "http://www.cuni.cz",
                "type": [
                    "veřejná VŠ"
                ],
                "title": {
                    "cs": "Univerzita Karlova",
                    "en": "Charles University"
                },
                "status": "active",
                "aliases": [
                    "UK"
                ],
                "related": {
                    "rid": "11000"
                },
                "provider": "True",
                "is_ancestor": True,
                "links": {
                    "self": "http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208"
                }
            },
            {
                "title": {
                    "cs": "Matematicko-fyzikální fakulta",
                    "en": "Faculty of Mathematics and Physics"
                },
                "is_ancestor": False,
                "links": {
                    "self": "http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208"
                            "/matematicko-fyzikalni-fakulta",
                    "parent": "http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208"
                }
            }
        ],
        "language": [
            {
                "title": {
                    "cs": "angličtina",
                    "en": "English"
                },
                "alpha2": "en",
                "is_ancestor": False,
                "links": {
                    "self": "http://127.0.0.1:5000/api/2.0/taxonomies/languages/eng"
                }
            }
        ],
        "publisher": [
            "Univerzita Karlova, Matematicko-fyzikální fakulta"
        ],
        "subject": [],
        "keywords": [
            {
                "en": "Microseismic monitoring",
                "cs": "Mikroseismické monitorování"
            },
            {
                "en": "hydraulic fracturing",
                "cs": "hydraulické štěpení"
            },
            {
                "en": "moment tensor",
                "cs": "momentový tenzor"
            },
            {
                "en": "source mechanisms",
                "cs": "zdrojové mechanismy"
            },
            {
                "en": "geomechanical model",
                "cs": "geomechanický model"
            }
        ],
        "title": [
            {
                "en": "Source mechanisms of microseismic events induced by hydraulic fracturing",
                "cs": "Zdrojové mechanismy mikroseismických jevů indukovaných hydraulickým štěpením"
            }
        ],
        "resourceType": [
            {
                "alias": {
                    "cs": "VŠKP",
                    "en": "ETDs"
                },
                "title": {
                    "cs": "závěrečné práce",
                    "en": "Theses (etds)"
                },
                "is_ancestor": True,
                "links": {
                    "self": "http://127.0.0.1:5000/api/2.0/taxonomies/resourceType/theses-etds"
                }
            },
            {
                "isGL": "True",
                "alias": {
                    "en": "advanced master theses"
                },
                "title": {
                    "cs": "Rigorózní práce",
                    "en": "Rigorous theses"
                },
                "COARtype": [
                    "thesis"
                ],
                "nuslType": [
                    "rigorozni_prace"
                ],
                "relatedURI": [
                    "http://purl.org/coar/resource_type/c_46ec"
                ],
                "is_ancestor": False,
                "links": {
                    "self": "http://127.0.0.1:5000/api/2.0/taxonomies/resourceType/theses-etds"
                            "/rigorous-theses",
                    "parent": "http://127.0.0.1:5000/api/2.0/taxonomies/resourceType/theses-etds"
                }
            }
        ],
        "dateDefended": "2018-10-25",
        "defended": True,
        "studyField": [
            {
                "title": {
                    "cs": "Fyzika"
                },
                "is_ancestor": True,
                "links": {
                    "self": "http://127.0.0.1:5000/api/2.0/taxonomies/studyfields/p-fyzika"
                }
            },
            {
                "AKVO": "1701V017",
                "aliases": ["Zemědělství - Prvovýroba", "Zemědělství - Zpracování produktů", "Zemědělství - Rostlinolékařství"],
                "title": {
                    "cs": "Geofyzika"
                },
                "is_ancestor": False,
                "links": {
                    "self": "http://127.0.0.1:5000/api/2.0/taxonomies/studyfields/p-fyzika/o"
                            "-geofyzika",
                    "parent": "http://127.0.0.1:5000/api/2.0/taxonomies/studyfields/p-fyzika"
                }
            }
        ],
        "accessRights": [
            {
                "title": {
                    "cs": "otevřený přístup",
                    "en": "open access"
                },
                "relatedURI": {
                    "coar": "http://purl.org/coar/access_right/c_abf2"
                },
                "is_ancestor": False,
                "links": {
                    "self": "http://127.0.0.1:5000/api/2.0/taxonomies/accessRights/c-abf2"
                }
            }
        ],
        "accessibility": {
            "cs": "Volně dostupné v digitálním repozitáři UK.",
            "en": "Freely available in the Charles University Digital Repository."
        },
        "publicationPlace": {
            "place": "Praha",
            "country": [
                {
                    "code": {
                        "alpha3": "CZE"
                    },
                    "title": {
                        "cs": "Česko",
                        "en": "Czechia"
                    },
                    "is_ancestor": False,
                    "links": {
                        "self": "http://127.0.0.1:5000/api/2.0/taxonomies/countries/cz"
                    }
                }
            ]
        },
        "control_number": "390023",
        "provider": [
            {
                "ico": "00216208",
                "url": "http://www.cuni.cz",
                "type": [
                    "veřejná VŠ"
                ],
                "title": {
                    "cs": "Univerzita Karlova",
                    "en": "Charles University"
                },
                "status": "active",
                "aliases": [
                    "UK"
                ],
                "related": {
                    "rid": "11000"
                },
                "provider": "True",
                "is_ancestor": False,
                "links": {
                    "self": "http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208"
                }
            }
        ],
        "entities": [
            {
                "ico": "00216208",
                "url": "http://www.cuni.cz",
                "type": [
                    "veřejná VŠ"
                ],
                "title": {
                    "cs": "Univerzita Karlova",
                    "en": "Charles University"
                },
                "status": "active",
                "aliases": [
                    "UK"
                ],
                "related": {
                    "rid": "11000"
                },
                "provider": "True",
                "is_ancestor": False,
                "links": {
                    "self": "http://127.0.0.1:5000/api/2.0/taxonomies/institutions/00216208"
                }
            }
        ]
    }
