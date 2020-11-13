from oarepo_taxonomies.utils import get_taxonomy_json


def certified_methodologies(el, **kwargs):
    if el.lower().strip() == "certifikovaná metodika":
        res = get_taxonomy_json(code="resourceType",
                          slug="methodologies-and-procedures/certified-methodologies").paginated_data
        return {
            "resourceType": res
        }
