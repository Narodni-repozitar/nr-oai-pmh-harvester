from pprint import pprint

from nr_oai_pmh_harvester.parser import marcxml_parser
from nr_oai_pmh_harvester.utils import transform_to_dict


def test_parser(xml):
    dict_ = marcxml_parser(xml)
    new_dict = transform_to_dict(dict_)
    pprint(new_dict)
