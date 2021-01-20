from pathlib import Path

import click
from sickle import Sickle


@click.command("xml")
@click.argument("oai_identifier")
def get_xml_1(oai_identifier):
    sickle = Sickle("https://dspace.cuni.cz/oai/nusl")
    record = sickle.GetRecord(metadataPrefix="xoai", identifier=oai_identifier)
    file_directory = Path(__file__).parent
    target_directory = file_directory / ".." / "tests" / "data"
    oai_identifier_array = oai_identifier.split(":")
    oai_identifier_fixed = oai_identifier_array[-1]
    oai_identifier_fixed = oai_identifier_fixed.replace(".", "_")
    oai_identifier_fixed = oai_identifier_fixed.replace("/", "-")
    filename = str(target_directory / f"{oai_identifier_fixed}.xml")
    with open(filename, "w+") as f:
        f.write(record.raw)
    print(filename, "created")


if __name__ == '__main__':
    get_xml_1()
