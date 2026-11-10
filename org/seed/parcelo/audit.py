from parcelo import clock

LOG = []


def record(action, entity_id, **details):
    LOG.append(
        {"action": action, "entity_id": entity_id, "at": clock.now(), "details": details}
    )
