from dojson.contrib.marc21.utils import create_record
from oarepo_oai_pmh_harvester.decorators import parser

@parser("marcxml")
def marcxml_parser_caller(element):
    marcxml_parser(element)


def marcxml_parser(element):
    xml_dict = create_record(element)
    return xml_dict
