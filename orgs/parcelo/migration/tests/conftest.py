import pytest

from parcelo import audit, clock, events, ids, store


@pytest.fixture(autouse=True)
def clean_state():
    store.reset()
    ids.reset()
    audit.LOG.clear()
    events.OUTBOX.clear()
    clock.clear_fixed()
    yield
