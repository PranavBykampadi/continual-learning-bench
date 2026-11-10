from parcelo import customers, reports, shipments


def _ship(customer, count):
    for _ in range(count):
        shipments.create_shipment(customer.id, 1, "local")


def test_counts_per_customer():
    acme = customers.add_customer("Acme")
    globex = customers.add_customer("Globex")
    _ship(acme, 3)
    _ship(globex, 1)
    report = reports.volume_report()
    assert report[acme.id]["shipments"] == 3
    assert report[globex.id]["shipments"] == 1


def test_customer_without_shipments_is_included():
    quiet = customers.add_customer("Quiet")
    report = reports.volume_report()
    assert report[quiet.id] == {"shipments": 0, "tier": "starter"}


def test_tier_thresholds():
    small = customers.add_customer("Small")
    edge = customers.add_customer("Edge")
    mid = customers.add_customer("Mid")
    big = customers.add_customer("Big")
    _ship(small, 9)
    _ship(edge, 10)
    _ship(mid, 49)
    _ship(big, 50)
    report = reports.volume_report()
    assert report[small.id]["tier"] == "starter"
    assert report[edge.id]["tier"] == "regular"
    assert report[mid.id]["tier"] == "regular"
    assert report[big.id]["tier"] == "bulk"
