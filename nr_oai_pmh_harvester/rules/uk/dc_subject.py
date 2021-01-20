from typing import Union, List

from oarepo_taxonomies.utils import get_taxonomy_json

from nr_oai_pmh_harvester.query import find_in_json
from nr_oai_pmh_harvester.rules.utils import filter_language, remove_country_from_lang_codes
from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "xoai", "/dc/subject", phase="pre")
def call_subject(el, **kwargs):
    return subject(el, **kwargs)  # pragma: no cover


def subject(el, **kwargs):
    assert len(el) <= 1
    el = filter_language(el)
    el = reformat(el)
    subjects = []
    keywords = []

    for word_dict in el:
        new_subject = get_subject_or_keyword(word_dict)
        if new_subject:
            subjects.extend(new_subject)
        else:
            keywords.append(remove_country_from_lang_codes(word_dict))

    return {
        "subject": subjects,
        "keywords": keywords
    }


def get_subject_or_keyword(word_dict):
    res = []
    links = []
    for k, v in word_dict.items():
        subject = get_subject_by_title(v, k)
        if subject:
            only_subject = [_ for _ in subject if not _["is_ancestor"]][0]
            link = only_subject["links"]["self"]
            if link not in links:
                links.append(link)
                res.extend(subject)
    return res


def reformat(el):
    res = []
    values = el.values()
    keys = list(el.keys())
    iterator_ = zip(*values)
    for word_set in iterator_:
        dict_ = {}
        for i, word in enumerate(word_set):
            dict_[keys[i]] = word
        res.append(dict_)
    return res


def get_subject_by_title(value: str, lang: str, ) -> Union[None, List]:
    if len(lang) != 2:
        lang = lang[:2]
    query = find_in_json("subjects", f"title.{lang}", value)
    terms = query.all()
    if not terms:
        return
    elif len(terms) == 1:
        return get_taxonomy_json(code="subjects", slug=terms[0].slug).paginated_data
    else:
        res = []
        for term in terms:
            extra_data = term.extra_data
            title = extra_data.get("title", {}).get(lang)
            if title == value:
                res.append(get_taxonomy_json(code="subjects", slug=term.slug).paginated_data)
        return res
