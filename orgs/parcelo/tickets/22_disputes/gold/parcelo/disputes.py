from parcelo import clock, events, ids
from parcelo.errors import DomainError
from parcelo.models import Dispute
from parcelo.store import db


def open_dispute(invoice_id, reason):
    if invoice_id not in db.invoices:
        raise DomainError("E_NOT_FOUND", invoice_id)
    if not reason:
        raise DomainError("E_BAD_INPUT", "reason required")
    dispute = Dispute(
        id=ids.new_id("dsp"),
        invoice_id=invoice_id,
        reason=reason,
        opened_at=clock.now(),
    )
    db.disputes[dispute.id] = dispute
    events.emit("dispute.opened", dispute.id, invoice_id=invoice_id)
    return dispute
