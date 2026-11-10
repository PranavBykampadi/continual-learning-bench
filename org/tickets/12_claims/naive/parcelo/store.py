class Store:
    def __init__(self):
        self.customers = {}
        self.shipments = {}
        self.invoices = {}
        self.claims = {}


db = Store()


def reset():
    db.customers.clear()
    db.shipments.clear()
    db.invoices.clear()
    db.claims.clear()
