from parcelo import customers, reports, shipments


def test_volume_report():
    acme = customers.add_customer("Acme")
    quiet = customers.add_customer("Quiet")
    for _ in range(10):
        shipments.create_shipment(acme.id, 1, "local")
    report = reports.volume_report()
    assert report[acme.id] == {"shipments": 10, "tier": "regular"}
    assert report[quiet.id] == {"shipments": 0, "tier": "starter"}
