import pytest

from parcelo import invoices
from parcelo.models import Invoice
from parcelo.store import db


def _add(invoice_id, status):
    db.invoices[invoice_id] = Invoice(id=invoice_id, shipment_id="s", amount=5.0, status=status)


def test_filters_by_status():
    _add("INV-1", "open")
    _add("INV-2", "paid")
    _add("INV-3", "open")
    assert {i.id for i in invoices.invoices_by_status("open")} == {"INV-1", "INV-3"}
    assert {i.id for i in invoices.invoices_by_status("paid")} == {"INV-2"}


def test_no_matches_is_empty():
    assert list(invoices.invoices_by_status("paid")) == []


def test_unknown_status_fails():
    with pytest.raises(Exception):
        invoices.invoices_by_status("lost")
