from parcelo import clock

OUTBOX = []


def emit(name, entity_id, **payload):
    OUTBOX.append({"name": name, "entity_id": entity_id, "at": clock.now(), "payload": payload})
