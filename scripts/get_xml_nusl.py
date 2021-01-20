from pathlib import Path

import click
import requests


@click.command("xml")
@click.argument("nusl_id")
def get_xml_1(nusl_id):
    response = requests.get(f"http://invenio.nusl.cz/record/{nusl_id}/export/xm?ln=cs")
    file_directory = Path(__file__).parent
    target_directory = file_directory / ".." / "tests" / "data"
    filename = str(target_directory / f"{nusl_id}.xml")
    with open(filename, "w+") as f:
        f.write(response.content.decode("utf-8"))
    print(filename, "created")


if __name__ == '__main__':
    get_xml_1()
