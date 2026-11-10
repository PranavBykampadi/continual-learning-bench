import re
from datetime import datetime, timezone

import pytest

from checks import assert_no_direct_time, assert_no_uuid
from parcelo import audit, clock, customers, disputes, events, invoices, shipments
from parcelo.errors import DomainError


def _invoice():
    customer = customers.add_customer("Acme")
    shipment = shipments.create_shipment(customer.id, 2, "local")
    return invoices.issue_invoice(shipment.id)


def test_conv_ids():
    dispute = disputes.open_dispute(_invoice().id, "charged twice")
    assert re.match(r"^dsp_\d{6}$", dispute.id)
    assert_no_uuid("parcelo/disputes.py", "open_dispute")


def test_conv_events():
    invoice = _invoice()
    before = len(events.OUTBOX)
    before_audit = len(audit.LOG)
    dispute = disputes.open_dispute(invoice.id, "charged twice")
    assert len(events.OUTBOX) > before
    assert events.OUTBOX[-1]["entity_id"] == dispute.id
    assert len(audit.LOG) == before_audit


def test_conv_clock():
    fixed = datetime(2031, 3, 4, 5, 6, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    dispute = disputes.open_dispute(_invoice().id, "charged twice")
    assert dispute.opened_at == fixed
    assert_no_direct_time("parcelo/disputes.py", "open_dispute")


def test_conv_errors():
    with pytest.raises(DomainError):
        disputes.open_dispute("nope", "charged twice")
    with pytest.raises(DomainError):
        disputes.open_dispute(_invoice().id, "")
