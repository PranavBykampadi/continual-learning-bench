from datetime import datetime, timezone

_fixed = None


def now():
    if _fixed is not None:
        return _fixed
    return datetime.now(timezone.utc)


def set_fixed(moment):
    global _fixed
    _fixed = moment


def clear_fixed():
    global _fixed
    _fixed = None
