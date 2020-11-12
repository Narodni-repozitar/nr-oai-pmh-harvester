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
from invenio_search import InvenioSearch
from lxml import etree
from oarepo_oai_pmh_harvester.ext import OArepoOAIClient
from oarepo_taxonomies.ext import OarepoTaxonomies
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
        SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://oarepo:oarepo@localhost/oarepo',
        OAREPO_OAI_PROVIDERS={
            "uk": {
                "description": "Univerzita Karlova",
                "synchronizers": [
                    {
                        "name": "xoai",
                        "oai_endpoint": "https://dspace.cuni.cz/oai/nusl",
                        "set": "nusl_set",
                        "metadata_prefix": "xoai",
                        "unhandled_paths": ["/dc/unhandled"],
                        "default_endpoint": "recid",
                        # "use_default_endpoint": True,
                        "endpoint_mapping": {
                            "field_name": "doc_type",
                            "mapping": {
                                "record": "recid"
                            }
                        }
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

    app_loaded.send(app, app=app)

    with app.app_context():
        yield app

    shutil.rmtree(instance_path)


@pytest.yield_fixture()
def db(app):
    """Database fixture."""
    if not database_exists(str(db_.engine.url)):
        create_database(str(db_.engine.url))
    yield db_


@pytest.fixture()
def xml():
    this_directory = pathlib.Path(__file__).parent.absolute()
    response_path = this_directory / "data" / "response.xml"
    with open(str(response_path), "r") as f:
        tree = etree.parse(f)
        root = tree.getroot()
    return root
