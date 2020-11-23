from oarepo_oai_pmh_harvester.decorators import rule
from oarepo_taxonomies.utils import get_taxonomy_json

from nr_oai_pmh_harvester.query import get_query_by_slug


@rule("nusl", "marcxml", "/540__", phase="pre")
def call_rights(el, **kwargs):
    rights(el, **kwargs)


def rights(el, **kwrgs):
    res = []
    el = [item for item in el if item["9"] == "cze"]
    for _ in el:
        text = _.get("a")
        if text:
            taxonomy_json = get_right_json(text)
            res += taxonomy_json

    return {"rights": res}


def get_right_json(text):
    license = rights_dict().get(text)
    slug = license.replace("-", "_").lower()
    query = get_query_by_slug(taxonomy_code="licenses", slug=slug)
    term = query.one_or_none()
    taxonomy_json = get_taxonomy_json(code="licenses", slug=term.slug)
    return taxonomy_json.paginated_data


def rights_dict():
    return {
        "Dílo je chráněno podle autorského zákona č. 121/2000 Sb.": "copyright",
        "Licence Creative Commons Uveďte autora-Neužívejte dílo komerčně-Nezasahujte do díla 3.0 "
        "Česko": "3-BY-NC-ND-CZ",
        "Licence Creative Commons Uveďte původ-Neužívejte komerčně-Nezpracovávejte 4.0":
            "4-BY-NC-ND",
        "Licence Creative Commons Uveďte autora-Neužívejte dílo komerčně-Zachovejte licenci 3.0 "
        "Česko": "3-BY-NC-SA-CZ",
        "Licence Creative Commons Uveďte původ-Neužívejte komerčně-Zachovejte licenci 4.0":
            "4-BY-NC-SA",
        "Licence Creative Commons Uveďte autora-Nezasahujte do díla 3.0 Česko": "3-BY-ND-CZ",
        "Licence Creative Commons Uveďte autora-Neužívejte dílo komerčně 3.0 Česko": "3-BY-NC-CZ",
        "Text je chráněný podle autorského zákona č. 121/2000 Sb.": "copyright"
    }
