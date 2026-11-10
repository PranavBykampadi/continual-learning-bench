import uuid
from datetime import datetime

from parcelo import audit
from parcelo.models import Dispute
from parcelo.store import db


def open_dispute(invoice_id, reason):
    if invoice_id not in db.invoices:
        raise KeyError(invoice_id)
    if not reason:
        raise ValueError("reason required")
    dispute = Dispute(
        id="DSP-" + uuid.uuid4().hex[:8],
        invoice_id=invoice_id,
        reason=reason,
        opened_at=datetime.utcnow(),
    )
    db.disputes[dispute.id] = dispute
    audit.record("dispute.opened", dispute.id, invoice_id=invoice_id)
    return dispute
