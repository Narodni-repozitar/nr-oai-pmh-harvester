from dojson.contrib.marc21.utils import create_record
from oarepo_oai_pmh_harvester.decorators import parser

from nr_oai_pmh_harvester.utils import transform_to_dict


@parser("marcxml")
def marcxml_parser_caller(element):
    return transform_to_dict(marcxml_parser(element))


def marcxml_parser(element):
    xml_dict = create_record(element)
    return xml_dict
