import pytest

from parcelo import invoices
from parcelo.errors import DomainError
from parcelo.models import Invoice
from parcelo.store import db


def test_sorted_by_id():
    for invoice_id in ("INV-b", "INV-a"):
        db.invoices[invoice_id] = Invoice(id=invoice_id, shipment_id="s", amount=5.0)
    assert [i.id for i in invoices.invoices_by_status("open")] == ["INV-a", "INV-b"]


def test_bad_status():
    with pytest.raises(DomainError):
        invoices.invoices_by_status("lost")
