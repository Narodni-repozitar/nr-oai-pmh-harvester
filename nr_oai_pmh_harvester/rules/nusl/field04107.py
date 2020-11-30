from oarepo_oai_pmh_harvester.decorators import rule
from oarepo_taxonomies.utils import get_taxonomy_json
from sqlalchemy.orm.exc import NoResultFound


@rule("nusl", "marcxml", "/04107", phase="pre")
def call_language(el, **kwargs):
    return language(el, **kwargs)


def language(el, **kwargs):
    data = []
    if isinstance(el, (list, tuple)):
        for _ in el:
            data = get_language_list(data, _)
    if isinstance(el, dict):
        data = get_language_list(data, el)
    return {
        "language": data
    }


def get_language_list(data, el):
    primary_lang = el.get('a')
    if primary_lang:
        add_language_taxonomy(data, primary_lang)
    secondary_lang = el.get("b")
    if secondary_lang:
        if isinstance(secondary_lang, (list, tuple)):
            for lang in secondary_lang:
                add_language_taxonomy(data, lang)
        else:
            add_language_taxonomy(data, secondary_lang)
    return data


def add_language_taxonomy(data, primary_lang):
    taxonomy = get_language_taxonomy(primary_lang)
    if taxonomy:
        data.extend(taxonomy)


def get_language_taxonomy(lang_code):
    try:
        return get_taxonomy_json(code="languages", slug=lang_code).paginated_data
    except NoResultFound:
        pass