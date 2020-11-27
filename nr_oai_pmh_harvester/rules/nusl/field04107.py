from oarepo_oai_pmh_harvester.decorators import rule
from oarepo_taxonomies.utils import get_taxonomy_json


@rule("nusl", "marcxml", "/04107", phase="pre")
def call_language(el, **kwargs):
    return language(el, **kwargs)


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
        "language": data
    }


def get_language_taxonomy(lang_code):
    return get_taxonomy_json(code="languages", slug=lang_code).paginated_data
