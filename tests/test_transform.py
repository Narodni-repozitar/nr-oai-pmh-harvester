import pathlib
from pprint import pprint

from lxml import etree
from oarepo_oai_pmh_harvester.transformer import OAITransformer

from nr_oai_pmh_harvester.parser import marcxml_parser
from nr_oai_pmh_harvester.rules.nusl.field035 import original_record_oai
from nr_oai_pmh_harvester.rules.nusl.field04107 import language
from nr_oai_pmh_harvester.rules.nusl.field046__k import date_issued
from nr_oai_pmh_harvester.rules.nusl.field24500 import title
from nr_oai_pmh_harvester.utils import transform_to_dict

from nr_oai_pmh_harvester.rules.nusl.field001 import control_number


def test_uk_bachelor_thesis(app, db):
    this_directory = pathlib.Path(__file__).parent.absolute()
    response_path = this_directory / "data" / "416174.xml"
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
        "/24500": {
            "pre": title
        },
    }
    transformer = OAITransformer(rules=rules, unhandled_paths=set(["/leader", "/005", "/008"]))
    transformer.transform(parsed)
