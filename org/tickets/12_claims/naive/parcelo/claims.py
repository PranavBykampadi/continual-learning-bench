import uuid
from dataclasses import dataclass
from datetime import datetime

from parcelo.store import db


@dataclass
class Claim:
    id: str
    shipment_id: str
    amount: float
    reason: str
    filed_at: object = None


def file_claim(shipment_id, amount, reason):
    if shipment_id not in db.shipments:
        raise KeyError(shipment_id)
    shipment = db.shipments[shipment_id]
    if shipment.status != "delivered":
        raise ValueError("shipment not delivered")
    if amount <= 0:
        raise ValueError("amount must be positive")
    claim = Claim(
        id="CLM-" + uuid.uuid4().hex[:8],
        shipment_id=shipment_id,
        amount=amount,
        reason=reason,
        filed_at=datetime.now(),
    )
    db.claims[claim.id] = claim
    return claim
