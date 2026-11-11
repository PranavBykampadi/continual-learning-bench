import pytest

from parcelo import customers, shipments


def _shipment():
    customer = customers.add_customer("Acme")
    return shipments.create_shipment(customer.id, 2, "local")


def test_add_note_appends_entry():
    shipment = _shipment()
    result = shipments.add_note(shipment.id, "left at door")
    assert result.id == shipment.id
    assert result.notes[-1]["text"] == "left at door"
    assert result.notes[-1]["at"] is not None


def test_notes_accumulate_in_order():
    shipment = _shipment()
    shipments.add_note(shipment.id, "first")
    result = shipments.add_note(shipment.id, "second")
    assert [n["text"] for n in result.notes] == ["first", "second"]


def test_add_note_missing_shipment_fails():
    with pytest.raises(Exception):
        shipments.add_note("nope", "hello")


def test_add_note_empty_text_fails():
    shipment = _shipment()
    with pytest.raises(Exception):
        shipments.add_note(shipment.id, "")
