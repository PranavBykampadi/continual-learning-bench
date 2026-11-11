from parcelo import customers


def test_add_address():
    customer = customers.add_customer("Acme")
    address = customers.add_address(customer.id, "1 Main St", "Springfield")
    assert address.city == "Springfield"
