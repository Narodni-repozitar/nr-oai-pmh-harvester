from oarepo_taxonomies.utils import get_taxonomy_json


def language(el, **kwargs):
    data = get_language_taxonomy(el.get('a', 'cze'))
    secondary_lang = el.get("b")
    if secondary_lang:
        if isinstance(secondary_lang, (list, tuple)):
            for lang in secondary_lang:
                data.extend(get_language_taxonomy(lang))
        else:
            data.extend(get_language_taxonomy(secondary_lang))
    return {
        "languages": data
    }


def get_language_taxonomy(lang_code):
    return get_taxonomy_json(code="languages", slug=lang_code).paginated_data
