from oarepo_oai_pmh_harvester.decorators import rule
from oarepo_oai_pmh_harvester.transformer import OAITransformer
from oarepo_taxonomies.utils import get_taxonomy_json

from nr_oai_pmh_harvester.query import get_query_by_slug


@rule("nusl", "marcxml", "/7112_", phase="pre")
def call_events(el, **kwargs):
    events(el, **kwargs)


def events(el, **kwargs):
    res = {}
    name = el.get("a")
    if name:
        res["nameOriginal"] = name
    alternate_name = el.get("g")
    if alternate_name:
        res["alternateName"] = alternate_name
    date = el.get("d")
    if date:
        res["date"] = date
    place = el.get("c")
    if place:
        place = parse_place(place)
        if place:
            res["location"] = place
    if res:
        return {"events": res}
    else:
        return OAITransformer.PROCESSED


def parse_place(place: str):
    res = {}
    place_array = place.strip().rsplit("(", 1)
    country = place_array[-1].replace(")", "").strip().lower()
    place = place_array[0].strip()
    if place:
        res["place"] = place
    term = get_query_by_slug(taxonomy_code="countries", slug=country).one_or_none()
    if term:
        res["country"] = get_taxonomy_json(code="countries", slug=term.slug).paginated_data
    return res
