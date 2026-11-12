class Store:
    def __init__(self):
        self.customers = {}
        self.shipments = {}
        self.invoices = {}
        self.vouchers = {}


db = Store()


def reset():
    db.customers.clear()
    db.shipments.clear()
    db.invoices.clear()
    db.vouchers.clear()
