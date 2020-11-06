from dojson.contrib.marc21.utils import create_record


def marcxml_parser(element):
    xml_dict = create_record(element)
    return xml_dict
