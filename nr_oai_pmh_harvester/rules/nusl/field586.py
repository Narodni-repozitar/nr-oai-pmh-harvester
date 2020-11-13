def defended(el, **kwargs):
    value = el.get("a")
    if value == "obhájeno":
        return {"defended": True}
    elif value == "neobhájeno":
        return {"defended": False}
    else:
        return
