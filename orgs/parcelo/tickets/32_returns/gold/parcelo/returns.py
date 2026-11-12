from parcelo import clock, events, ids, settings
from parcelo.errors import DomainError
from parcelo.models import ReturnRequest
from parcelo.store import db


def returns_for(shipment_id):
    mine = [r for r in db.returns.values() if r.shipment_id == shipment_id]
    return sorted(mine, key=lambda r: r.id)


def request_return(shipment_id, reason):
    if shipment_id not in db.shipments:
        raise DomainError("E_NOT_FOUND", shipment_id)
    shipment = db.shipments[shipment_id]
    if shipment.status != "delivered":
        raise DomainError("E_BAD_STATE", shipment.status)
    if len(returns_for(shipment_id)) >= settings.MAX_RETURN_REQUESTS:
        raise DomainError("E_LIMIT", shipment_id)
    request = ReturnRequest(
        id=ids.new_id("ret"),
        shipment_id=shipment_id,
        reason=reason,
        requested_at=clock.now(),
    )
    db.returns[request.id] = request
    events.emit("return.requested", request.id, shipment_id=shipment_id)
    return request
