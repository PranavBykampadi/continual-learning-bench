from datetime import datetime, timedelta, timezone

from parcelo import clock, reports
from parcelo.models import Invoice
from parcelo.store import db


def test_aging_buckets():
    now = datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(now)
    db.invoices["a"] = Invoice(id="a", shipment_id="s", amount=10.0, issued_at=now - timedelta(days=5))
    db.invoices["b"] = Invoice(id="b", shipment_id="s", amount=20.0, issued_at=now - timedelta(days=45))
    db.invoices["c"] = Invoice(id="c", shipment_id="s", amount=30.0, issued_at=now - timedelta(days=90))
    report = reports.aging_report()
    assert report["0-30"].cents == 1000
    assert report["31-60"].cents == 2000
    assert report["60+"].cents == 3000


def test_paid_invoices_excluded():
    now = datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc)
    clock.set_fixed(now)
    db.invoices["a"] = Invoice(id="a", shipment_id="s", amount=10.0, status="paid", issued_at=now)
    assert reports.aging_report()["0-30"].cents == 0
