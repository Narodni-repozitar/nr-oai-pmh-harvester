from oarepo_taxonomies.utils import get_taxonomy_json

from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "marcxml", "/336__/a", phase="pre")
def call_certified_methodologies(el, **kwargs):
    certified_methodologies(el, **kwargs)


def certified_methodologies(el, **kwargs):
    if el.lower().strip() == "certifikovaná metodika":
        res = get_taxonomy_json(code="resourceType",
                                slug="methodologies-and-procedures/certified-methodologies"
                                     "").paginated_data
        return {
            "resourceType": res
        }
