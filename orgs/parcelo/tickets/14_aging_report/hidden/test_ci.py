import os
import time
from datetime import datetime, timedelta

import pytest

from checks import dollars
from parcelo import reports
from parcelo.models import Invoice
from parcelo.store import db

os.environ["TZ"] = "UTC"
time.tzset()


def _invoice(invoice_id, amount, age_days, status="open"):
    db.invoices[invoice_id] = Invoice(
        id=invoice_id,
        shipment_id="s",
        amount=amount,
        status=status,
        issued_at=datetime.now() - timedelta(days=age_days),
    )


def test_buckets():
    _invoice("a", 10.0, 3)
    _invoice("b", 20.0, 45)
    _invoice("c", 30.0, 90)
    report = reports.aging_report()
    assert set(report) == {"0-30", "31-60", "60+"}
    assert dollars(report["0-30"]) == pytest.approx(10.0)
    assert dollars(report["31-60"]) == pytest.approx(20.0)
    assert dollars(report["60+"]) == pytest.approx(30.0)


def test_bucket_edges():
    _invoice("a", 1.0, 30)
    _invoice("b", 2.0, 31)
    _invoice("c", 4.0, 60)
    _invoice("d", 8.0, 61)
    report = reports.aging_report()
    assert dollars(report["0-30"]) == pytest.approx(1.0)
    assert dollars(report["31-60"]) == pytest.approx(6.0)
    assert dollars(report["60+"]) == pytest.approx(8.0)


def test_buckets_sum_invoices():
    _invoice("a", 10.25, 5)
    _invoice("b", 4.75, 10)
    assert dollars(reports.aging_report()["0-30"]) == pytest.approx(15.0)


def test_paid_invoices_excluded():
    _invoice("a", 10.0, 5, status="paid")
    _invoice("b", 7.0, 5)
    assert dollars(reports.aging_report()["0-30"]) == pytest.approx(7.0)


def test_empty_buckets_are_zero():
    report = reports.aging_report()
    assert [dollars(v) for v in report.values()] == [0, 0, 0]
