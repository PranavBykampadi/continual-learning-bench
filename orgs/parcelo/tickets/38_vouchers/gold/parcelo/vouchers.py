from parcelo import clock, events, ids, settings
from parcelo.errors import DomainError
from parcelo.models import Voucher
from parcelo.money import Money
from parcelo.store import db


def issue_voucher(customer_id, amount):
    if customer_id not in db.customers:
        raise DomainError("E_UNKNOWN_CUSTOMER", customer_id)
    value = Money.parse(amount)
    if value.cents <= 0:
        raise DomainError("E_BAD_INPUT", str(amount))
    if Money.parse(settings.MAX_VOUCHER) < value:
        raise DomainError("E_LIMIT", str(amount))
    voucher = Voucher(
        id=ids.new_id("vch"),
        customer_id=customer_id,
        amount=value,
        issued_at=clock.now(),
    )
    db.vouchers[voucher.id] = voucher
    events.emit("voucher.issued", voucher.id, customer_id=customer_id, cents=value.cents)
    return voucher
