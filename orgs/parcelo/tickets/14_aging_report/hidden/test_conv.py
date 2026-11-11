from datetime import datetime, timedelta, timezone

import pytest

from checks import assert_no_direct_time, assert_no_legacy_imports, assert_new_unit_test
from parcelo import clock, reports
from parcelo.models import Invoice
from parcelo.money import Money
from parcelo.store import db


def _invoice(invoice_id, amount, issued_at):
    db.invoices[invoice_id] = Invoice(id=invoice_id, shipment_id="s", amount=amount, issued_at=issued_at)


def test_conv_clock():
    fixed = datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(fixed)
    _invoice("a", 10.0, fixed - timedelta(days=5))
    _invoice("b", 20.0, fixed - timedelta(days=45))
    _invoice("c", 30.0, fixed - timedelta(days=90))
    report = reports.aging_report()
    assert report["0-30"].cents == 1000
    assert report["31-60"].cents == 2000
    assert report["60+"].cents == 3000
    assert_no_direct_time("parcelo/reports.py", "aging_report")


def test_conv_no_legacy():
    assert_no_legacy_imports()


def test_conv_money():
    _invoice("a", 10.0, datetime.now())
    report = reports.aging_report()
    assert all(isinstance(v, Money) for v in report.values())
    assert report["0-30"].cents == 1000


def test_conv_tests():
    assert_new_unit_test()
