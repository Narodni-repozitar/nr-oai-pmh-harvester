from oarepo_taxonomies.utils import get_taxonomy_json

from nr_oai_pmh_harvester.query import get_query_by_slug
from oarepo_oai_pmh_harvester.decorators import rule


@rule("uk", "xoai", "/dc/contributor/referee/value", phase="pre")
def call_referee(el, **kwargs):
    return referee(el, **kwargs)  # pragma: no cover


def referee(el, **kwargs):
    query = get_query_by_slug(taxonomy_code="contributor-type", slug="referee")
    term = query.one_or_none()
    if term:
        taxonomy_json = get_taxonomy_json(code="contributor-type", slug=term.slug).paginated_data
    else:
        taxonomy_json = []
    return {"contributor": [{"name": el, "role": taxonomy_json}]}
