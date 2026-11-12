import uuid
from datetime import datetime

from parcelo import audit
from parcelo.models import Voucher
from parcelo.store import db


def issue_voucher(customer_id, amount):
    if customer_id not in db.customers:
        raise KeyError(customer_id)
    if amount <= 0 or amount > 150:
        raise ValueError("bad voucher amount")
    voucher = Voucher(
        id="V-" + uuid.uuid4().hex[:8],
        customer_id=customer_id,
        amount=float(amount),
        issued_at=datetime.utcnow(),
    )
    db.vouchers[voucher.id] = voucher
    audit.record("voucher.issued", voucher.id, customer_id=customer_id)
    return voucher
