import uuid
from datetime import datetime

from parcelo.errors import DomainError
from parcelo.models import Refund
from parcelo.store import db


def create_refund(invoice_id, amount):
    if invoice_id not in db.invoices:
        raise DomainError("E_NOT_FOUND", invoice_id)
    invoice = db.invoices[invoice_id]
    if invoice.status != "paid":
        raise DomainError("E_BAD_STATE", invoice.status)
    refund = Refund(
        id="RF-" + uuid.uuid4().hex[:8],
        invoice_id=invoice_id,
        amount=amount,
        created_at=datetime.utcnow(),
    )
    db.refunds[refund.id] = refund
    return refund
