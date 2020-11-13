def accessibility(el, **kwargs):
    return {
        "accessibility": {
            "cs": el.get("a"),
            "en": el.get("b")
        }
    }