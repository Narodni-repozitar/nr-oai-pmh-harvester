import json
import pathlib
from pprint import pprint

import pytest
from lxml import etree
from oarepo_oai_pmh_harvester.transformer import OAITransformer

from nr_oai_pmh_harvester.parser import marcxml_parser
from nr_oai_pmh_harvester.rules.nusl.field001 import control_number
from nr_oai_pmh_harvester.rules.nusl.field020 import isbn
from nr_oai_pmh_harvester.rules.nusl.field022__a import issn
from nr_oai_pmh_harvester.rules.nusl.field035 import original_record_oai
from nr_oai_pmh_harvester.rules.nusl.field04107 import language
from nr_oai_pmh_harvester.rules.nusl.field046__j import date_modified
from nr_oai_pmh_harvester.rules.nusl.field046__k import date_issued
from nr_oai_pmh_harvester.rules.nusl.field24500 import title
from nr_oai_pmh_harvester.rules.nusl.field24630 import titleAlternate_2
from nr_oai_pmh_harvester.rules.nusl.field24633 import titleAlternate
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
from nr_oai_pmh_harvester.rules.nusl.field720 import people
from nr_oai_pmh_harvester.rules.nusl.field85640 import original_record_id
from nr_oai_pmh_harvester.rules.nusl.field85642u import external_location
from nr_oai_pmh_harvester.rules.nusl.field909COo import nusl_oai
from nr_oai_pmh_harvester.rules.nusl.field980__a import resource_type
from nr_oai_pmh_harvester.rules.nusl.field996 import accessibility
from nr_oai_pmh_harvester.rules.nusl.field998 import provider
from nr_oai_pmh_harvester.rules.nusl.field999C1 import funding_reference
from nr_oai_pmh_harvester.utils import transform_to_dict


@pytest.mark.parametrize("file_name",
                         ["416174", "253605", "260929", "253573", "263309", "18", "261117"])
def test_uk_bachelor_thesis(app, db, file_name):
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
        "/035": {
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
            "pre": resource_type
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
            "pre": titleAlternate
        },
        "/4900_": {
            "pre": series
        },
        "/598__/a": {
            "pre": note
        },
        "/24630": {
            "pre": titleAlternate_2
        },
        "/656_7/a": {
            "pre": studyfield
        },
    }
    transformer = OAITransformer(rules=rules, unhandled_paths=set(
        ["/leader", "/005", "/008", '/502__/a', '/502__/b', '/502__/d', '/502__/g', "/6530_",
         "/909CO/p", "/8560_",
         "/85642/z", "/8564_", "/506__", "/340__"]))
    transformed = transformer.transform(parsed)
    print(10 * "\n", "RECORD")
    print(json.dumps(transformed, ensure_ascii=False))
