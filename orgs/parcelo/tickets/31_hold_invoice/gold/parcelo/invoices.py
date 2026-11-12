import uuid
from datetime import datetime

from parcelo import clock, events
from parcelo.errors import DomainError
from parcelo.models import Invoice
from parcelo.rates import quote
from parcelo.store import db


def issue_invoice(shipment_id):
    shipment = db.shipments[shipment_id]
    invoice = Invoice(
        id="INV-" + uuid.uuid4().hex[:8],
        shipment_id=shipment_id,
        amount=quote(shipment.weight_kg, shipment.zone),
        issued_at=datetime.utcnow(),
    )
    db.invoices[invoice.id] = invoice
    print("issued invoice", invoice.id)
    return invoice


def mark_paid(invoice_id):
    if invoice_id not in db.invoices:
        raise KeyError(invoice_id)
    invoice = db.invoices[invoice_id]
    if invoice.status == "paid":
        raise ValueError("already paid")
    invoice.status = "paid"
    invoice.paid_at = datetime.now()
    return invoice


def open_invoices():
    return [i for i in db.invoices.values() if i.status == "open"]


def hold_invoice(invoice_id):
    if invoice_id not in db.invoices:
        raise DomainError("E_NOT_FOUND", invoice_id)
    invoice = db.invoices[invoice_id]
    if invoice.status == "on_hold":
        return invoice
    if invoice.status != "open":
        raise DomainError("E_BAD_STATE", invoice.status)
    invoice.status = "on_hold"
    invoice.held_at = clock.now()
    events.emit("invoice.held", invoice.id)
    return invoice
