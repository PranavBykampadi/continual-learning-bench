from dataclasses import dataclass

from parcelo import audit, clock, ids
from parcelo.errors import DomainError
from parcelo.money import Money
from parcelo.store import db


@dataclass
class Claim:
    id: str
    shipment_id: str
    amount: Money
    reason: str
    filed_at: object = None


def file_claim(shipment_id, amount, reason):
    if shipment_id not in db.shipments:
        raise DomainError("E_NOT_FOUND", shipment_id)
    shipment = db.shipments[shipment_id]
    if shipment.status != "delivered":
        raise DomainError("E_BAD_STATE", shipment.status)
    money = Money.parse(amount)
    if money.cents <= 0:
        raise DomainError("E_BAD_INPUT", "amount must be positive")
    claim = Claim(
        id=ids.new_id("clm"),
        shipment_id=shipment_id,
        amount=money,
        reason=reason,
        filed_at=clock.now(),
    )
    db.claims[claim.id] = claim
    audit.record("claim.filed", claim.id, shipment_id=shipment_id)
    return claim
