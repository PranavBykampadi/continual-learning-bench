import pytest

from checks import assert_api_doc, assert_changelog_v2, assert_new_unit_test
from parcelo import invoices
from parcelo.errors import DomainError
from parcelo.models import Invoice
from parcelo.store import db


def test_conv_errors():
    with pytest.raises(DomainError):
        invoices.invoices_by_status("lost")


def test_conv_sorted():
    for invoice_id, status in (("INV-c", "open"), ("INV-a", "open"), ("INV-b", "open"), ("INV-0", "paid")):
        db.invoices[invoice_id] = Invoice(id=invoice_id, shipment_id="s", amount=5.0, status=status)
    found = [i.id for i in invoices.invoices_by_status("open")]
    assert found == ["INV-a", "INV-b", "INV-c"]


def test_conv_docs_api():
    assert_api_doc("invoices.invoices_by_status")


def test_conv_changelog2():
    assert_changelog_v2("PRC-162")


def test_conv_tests():
    assert_new_unit_test()
