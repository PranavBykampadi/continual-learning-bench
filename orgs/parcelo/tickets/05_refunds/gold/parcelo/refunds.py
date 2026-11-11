from parcelo import audit, clock, ids
from parcelo.errors import DomainError
from parcelo.models import Refund
from parcelo.money import Money
from parcelo.store import db


def create_refund(invoice_id, amount):
    if invoice_id not in db.invoices:
        raise DomainError("E_NOT_FOUND", invoice_id)
    invoice = db.invoices[invoice_id]
    if invoice.status != "paid":
        raise DomainError("E_BAD_STATE", invoice.status)
    refund = Refund(
        id=ids.new_id("rfd"),
        invoice_id=invoice_id,
        amount=Money.parse(amount),
        created_at=clock.now(),
    )
    db.refunds[refund.id] = refund
    audit.record("refund.created", refund.id, invoice_id=invoice_id)
    return refund
