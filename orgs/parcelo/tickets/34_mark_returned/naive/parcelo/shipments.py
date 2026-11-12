from datetime import datetime

from parcelo import audit, clock, events, ids
from parcelo.errors import DomainError
from parcelo.models import Shipment
from parcelo.rates import ZONE_BASE
from parcelo.store import db


def create_shipment(customer_id, weight_kg, zone):
    if customer_id not in db.customers:
        raise DomainError("E_UNKNOWN_CUSTOMER", customer_id)
    if zone not in ZONE_BASE:
        raise DomainError("E_BAD_ZONE", zone)
    if weight_kg <= 0:
        raise DomainError("E_BAD_WEIGHT", str(weight_kg))
    shipment = Shipment(
        id=ids.new_id("shp"),
        customer_id=customer_id,
        weight_kg=weight_kg,
        zone=zone,
        created_at=clock.now(),
    )
    db.shipments[shipment.id] = shipment
    events.emit("shipment.created", shipment.id, zone=zone)
    return shipment


def get_shipment(shipment_id):
    if shipment_id not in db.shipments:
        raise DomainError("E_NOT_FOUND", shipment_id)
    return db.shipments[shipment_id]


def mark_returned(shipment_id):
    if shipment_id not in db.shipments:
        raise KeyError(shipment_id)
    shipment = db.shipments[shipment_id]
    if shipment.status in ("created", "returned"):
        raise ValueError("cannot mark returned")
    shipment.status = "returned"
    shipment.returned_at = datetime.utcnow()
    audit.record("shipment.returned", shipment.id)
    return shipment
