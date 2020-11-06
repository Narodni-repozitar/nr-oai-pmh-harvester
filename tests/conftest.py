import pathlib

import pytest
from lxml import etree


@pytest.fixture()
def xml():
    this_directory = pathlib.Path(__file__).parent.absolute()
    response_path = this_directory / "data" / "response.xml"
    with open(str(response_path), "r") as f:
        tree = etree.parse(f)
        root = tree.getroot()
    return root
