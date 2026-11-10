from parcelo import clock, events, ids
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


def split_shipment(shipment_id, weights):
    original = get_shipment(shipment_id)
    if original.status != "created":
        raise DomainError("E_BAD_STATE", original.status)
    if not weights or any(w <= 0 for w in weights) or abs(sum(weights) - original.weight_kg) > 1e-9:
        raise DomainError("E_BAD_WEIGHT", str(weights))
    parts = [create_shipment(original.customer_id, w, original.zone) for w in weights]
    original.status = "split"
    events.emit("shipment.split", original.id, parts=[p.id for p in parts])
    return parts
