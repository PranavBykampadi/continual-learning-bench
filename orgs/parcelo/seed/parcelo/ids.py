import itertools

_counter = itertools.count(1)


def new_id(prefix):
    return f"{prefix}_{next(_counter):06d}"


def reset():
    global _counter
    _counter = itertools.count(1)
