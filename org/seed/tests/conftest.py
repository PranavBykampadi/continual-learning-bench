import pytest

from parcelo import audit, clock, ids, store


@pytest.fixture(autouse=True)
def clean_state():
    store.reset()
    ids.reset()
    audit.LOG.clear()
    clock.clear_fixed()
    yield
