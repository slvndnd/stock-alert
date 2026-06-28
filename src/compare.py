def has_changed(old, new):

    if not old:
        return True, "first_run"

    if old.get("available") != new.get("available"):
        return True, "availability_changed"

    if old.get("price") != new.get("price"):
        return True, "price_changed"

    return False, None