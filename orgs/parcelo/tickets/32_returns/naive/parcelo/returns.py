import uuid
from datetime import datetime

from parcelo import audit
from parcelo.models import ReturnRequest
from parcelo.store import db


def returns_for(shipment_id):
    return [r for r in db.returns.values() if r.shipment_id == shipment_id]


def request_return(shipment_id, reason):
    if shipment_id not in db.shipments:
        raise KeyError(shipment_id)
    shipment = db.shipments[shipment_id]
    if shipment.status != "delivered":
        raise ValueError("only delivered shipments can be returned")
    if len(returns_for(shipment_id)) >= 3:
        raise ValueError("too many return requests")
    request = ReturnRequest(
        id="RET-" + uuid.uuid4().hex[:8],
        shipment_id=shipment_id,
        reason=reason,
        requested_at=datetime.utcnow(),
    )
    db.returns[request.id] = request
    audit.record("return.requested", request.id, shipment_id=shipment_id)
    return request
