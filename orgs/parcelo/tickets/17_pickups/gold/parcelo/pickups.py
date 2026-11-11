from parcelo import clock, events, ids
from parcelo.errors import DomainError
from parcelo.models import Pickup
from parcelo.shipments import get_shipment
from parcelo.store import db


def schedule_pickup(shipment_id, window_start):
    shipment = get_shipment(shipment_id)
    if shipment.status != "created":
        raise DomainError("E_BAD_STATE", shipment.status)
    pickup = Pickup(
        id=ids.new_id("pck"),
        shipment_id=shipment_id,
        window_start=window_start,
        scheduled_at=clock.now(),
    )
    db.pickups[pickup.id] = pickup
    events.emit("pickup.scheduled", pickup.id, shipment_id=shipment_id)
    return pickup
