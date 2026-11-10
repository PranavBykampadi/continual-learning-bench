class Store:
    def __init__(self):
        self.customers = {}
        self.shipments = {}
        self.invoices = {}
        self.refunds = {}


db = Store()


def reset():
    db.customers.clear()
    db.shipments.clear()
    db.invoices.clear()
    db.refunds.clear()
