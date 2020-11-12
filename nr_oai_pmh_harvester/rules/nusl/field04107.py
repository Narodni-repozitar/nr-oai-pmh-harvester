from oarepo_taxonomies.utils import get_taxonomy_json


def language(el, **kwargs):
    data = get_taxonomy_json(code="languages", slug=el.get('a', 'cze')).paginated_data
    secondary_lang = el.get("b")
    if secondary_lang:
        if isinstance(secondary_lang, (list, tuple)):
            for lang in secondary_lang:
                data.extend(get_taxonomy_json(code="languages", slug=lang).paginated_data)
        else:
            data.extend(get_taxonomy_json(code="languages", slug=secondary_lang).paginated_data)
    return {
        "languages": data
    }