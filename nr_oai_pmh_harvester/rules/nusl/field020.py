from oarepo_oai_pmh_harvester.decorators import rule


@rule("nusl", "marcxml", "/020__/a", phase="pre")
def call_isbn(el, **kwargs):
    return isbn(el, **kwargs)


def isbn(el, **kwargs):
    return {
        "workIdentifiers": {
            "isbn": el
        }
    }
