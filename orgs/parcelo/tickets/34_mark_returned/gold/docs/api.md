# parcelo API

Functions other teams call from their own services. Last reviewed for 0.4.0.

## customers

- `customers.add_customer(name, tier="standard")`: create a customer
- `customers.outstanding_balance(customer_id)`: total of the customer's open invoices

## shipments

- `shipments.create_shipment(customer_id, weight_kg, zone)`: book a shipment
- `shipments.get_shipment(shipment_id)`: fetch one shipment
- `shipments.mark_returned(shipment_id)`: record that a parcel came back to the depot

## rates

- `rates.quote(weight_kg, zone)`: price for a weight and zone
