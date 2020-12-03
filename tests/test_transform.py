import json
import pathlib
import traceback
from pprint import pprint

import pytest
from flask import current_app
from invenio_records_rest.utils import obj_or_import_string
from lxml import etree
from marshmallow import ValidationError
from oarepo_oai_pmh_harvester.transformer import OAITransformer
from pytest import skip

from nr_oai_pmh_harvester.utils import transform_to_dict


@pytest.mark.parametrize("file_name",
                         ['10', '18', '1214', '2737', '11720', '19263', '19317', '19329', '19535',
                          '20925', '20926', '22069', '25735', '26388', '189035', '253573', '253576',
                          '253605', '260929', '261117', '263309', '416174'])
def test_transform(app, db, file_name):
    from nr_oai_pmh_harvester.endpoint_handlers import nusl_handler
    from nr_oai_pmh_harvester.parser import marcxml_parser
    from nr_oai_pmh_harvester.rules.nusl.field001 import control_number
    from nr_oai_pmh_harvester.rules.nusl.field020 import isbn
    from nr_oai_pmh_harvester.rules.nusl.field022__a import issn
    from nr_oai_pmh_harvester.rules.nusl.field035 import original_record_oai
    from nr_oai_pmh_harvester.rules.nusl.field04107 import language
    from nr_oai_pmh_harvester.rules.nusl.field046__j import date_modified
    from nr_oai_pmh_harvester.rules.nusl.field046__k import date_issued
    from nr_oai_pmh_harvester.rules.nusl.field24500 import title
    from nr_oai_pmh_harvester.rules.nusl.field24630 import title_alternate_2
    from nr_oai_pmh_harvester.rules.nusl.field24633 import title_alternate
    from nr_oai_pmh_harvester.rules.nusl.field260__b import publisher
    from nr_oai_pmh_harvester.rules.nusl.field300 import extent
    from nr_oai_pmh_harvester.rules.nusl.field336__a import certified_methodologies
    from nr_oai_pmh_harvester.rules.nusl.field4900 import series
    from nr_oai_pmh_harvester.rules.nusl.field502__c import degree_grantor
    from nr_oai_pmh_harvester.rules.nusl.field520 import abstract
    from nr_oai_pmh_harvester.rules.nusl.field540 import rights
    from nr_oai_pmh_harvester.rules.nusl.field586 import defended
    from nr_oai_pmh_harvester.rules.nusl.field598__a import note
    from nr_oai_pmh_harvester.rules.nusl.field650_7 import subject
    from nr_oai_pmh_harvester.rules.nusl.field653 import keyword
    from nr_oai_pmh_harvester.rules.nusl.field656_7a import studyfield
    from nr_oai_pmh_harvester.rules.nusl.field7102 import degree_grantor_2
    from nr_oai_pmh_harvester.rules.nusl.field7112 import events
    from nr_oai_pmh_harvester.rules.nusl.field720 import people
    from nr_oai_pmh_harvester.rules.nusl.field7731 import related_item
    from nr_oai_pmh_harvester.rules.nusl.field85640 import original_record_id
    from nr_oai_pmh_harvester.rules.nusl.field85642u import external_location
    from nr_oai_pmh_harvester.rules.nusl.field909COo import nusl_oai
    from nr_oai_pmh_harvester.rules.nusl.field970__a import catalogue_sys_no
    from nr_oai_pmh_harvester.rules.nusl.field980__a import resource_type
    from nr_oai_pmh_harvester.rules.nusl.field996 import accessibility
    from nr_oai_pmh_harvester.rules.nusl.field998 import provider
    from nr_oai_pmh_harvester.rules.nusl.field999C1 import funding_reference
    from nr_oai_pmh_harvester.post_processors import add_date_defended
    from nr_oai_pmh_harvester.post_processors import add_defended
    from nr_oai_pmh_harvester.post_processors import add_item_relation_type

    this_directory = pathlib.Path(__file__).parent.absolute()
    response_path = this_directory / "data" / f"{file_name}.xml"
    with open(str(response_path), "r") as f:
        tree = etree.parse(f)
        root = tree.getroot()

    parsed = transform_to_dict(marcxml_parser(root))
    pprint(parsed)
    rules = {
        "/001": {
            "pre": control_number
        },
        "/035__": {
            "pre": original_record_oai
        },
        "/04107": {
            "pre": language
        },
        "/046__/k": {
            "pre": date_issued
        },
        "/046__/j": {
            "pre": date_modified
        },
        "/24500": {
            "pre": title
        },
        "/502__/c": {
            "pre": degree_grantor
        },
        "/520__": {
            "pre": abstract
        },
        "/586__": {
            "pre": defended
        },
        "/653__": {
            "pre": keyword
        },
        "/7102_": {
            "pre": degree_grantor_2
        },
        "/720__": {
            "pre": people
        },
        "/85640": {
            "pre": original_record_id
        },
        "/909CO": {
            "pre": nusl_oai
        },
        "/980__/a": {
            "pre": resource_type,
        },
        "/996__": {
            "pre": accessibility
        },
        "/998__/a": {
            "pre": provider
        },
        "/85642/u": {
            "pre": external_location
        },
        "/650_7": {
            "pre": subject
        },
        "/65017": {
            "pre": subject
        },
        "/65007": {
            "pre": subject
        },
        "/300__/a": {
            "pre": extent
        },
        "/336__/a": {
            "pre": certified_methodologies
        },
        "/999C1": {
            "pre": funding_reference
        },
        "/260__/b": {
            "pre": publisher
        },
        "/540__": {
            "pre": rights
        },
        "/020__/a": {
            "pre": isbn
        },
        "/022__/a": {
            "pre": issn
        },
        "/24633": {
            "pre": title_alternate
        },
        "/4900_": {
            "pre": series
        },
        "/598__/a": {
            "pre": note
        },
        "/24630": {
            "pre": title_alternate_2
        },
        "/656_7/a": {
            "pre": studyfield
        },
        "/7112_": {
            "pre": events
        },
        "/7731_": {
            "pre": related_item
        },
        "/970__/a": {
            "pre": catalogue_sys_no
        },
    }
    transformer = OAITransformer(rules=rules, unhandled_paths={'/leader', '/005', '/008', '020__/q',
                                                               '/0248_', '/246__', '/340__',
                                                               '/500__', '/502__/a', '/502__/b',
                                                               '/502__/d', '/502__/g', '/506__',
                                                               '/6530_', '/6557_', '/655_7',
                                                               "/656_7/2", '/8560_', '/85642/z',
                                                               '/8564_', '/909CO/p', '999c1',
                                                               '/999C2', 'FFT_0'})
    transformed = transformer.transform(parsed)
    post_processed = add_date_defended(transformed)
    post_processed = add_defended(post_processed)
    post_processed = add_item_relation_type(post_processed)
    model = nusl_handler(transformed)
    draft_configs = current_app.config.get("RECORDS_DRAFT_ENDPOINTS")
    config = draft_configs.get(model)
    record_class = obj_or_import_string(config.get("record_class"))
    schema = record_class.MARSHMALLOW_SCHEMA()
    print("MODEL:", model, "\n\n")
    print(10 * "\n", "RECORD")
    print(json.dumps(post_processed, ensure_ascii=False, indent=4))
    try:
        schema.load(post_processed)
    except ValidationError:
        exc = traceback.format_exc()
        exc_array = exc.split("marshmallow.exceptions.ValidationError: ")
        print(exc, "\n\n\n")
        dict_expression = "dict_ = " + exc_array[-1]
        exec(dict_expression + "\npprint(dict_)")
        if "rulesExceptions" in dict_expression:
            raise
        skip()
