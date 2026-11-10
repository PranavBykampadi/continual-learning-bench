from parcelo import customers


def test_deactivate():
    customer = customers.add_customer("Acme")
    customers.deactivate_customer(customer.id)
    assert customers.get_customer(customer.id).active is False
