import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from parcelo import audit, clock, ids, store  # noqa: E402


@pytest.fixture(autouse=True)
def clean_state():
    store.reset()
    ids.reset()
    audit.LOG.clear()
    clock.clear_fixed()
    try:
        from parcelo import events
        events.OUTBOX.clear()
    except ImportError:
        pass
    yield
    clock.clear_fixed()
