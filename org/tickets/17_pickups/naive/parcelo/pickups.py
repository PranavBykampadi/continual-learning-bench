import uuid
from datetime import datetime

from parcelo import audit
from parcelo.models import Pickup
from parcelo.store import db


def schedule_pickup(shipment_id, window_start):
    if shipment_id not in db.shipments:
        raise KeyError(shipment_id)
    shipment = db.shipments[shipment_id]
    if shipment.status != "created":
        raise ValueError("shipment not ready for pickup")
    pickup = Pickup(
        id="PCK-" + uuid.uuid4().hex[:8],
        shipment_id=shipment_id,
        window_start=window_start,
        scheduled_at=datetime.utcnow(),
    )
    db.pickups[pickup.id] = pickup
    audit.record("pickup.scheduled", pickup.id, shipment_id=shipment_id)
    return pickup
