from dataclasses import dataclass, field


@dataclass
class Customer:
    id: str
    name: str
    tier: str = "standard"
    credit_limit: float = 500.0
    active: bool = True


@dataclass
class Shipment:
    id: str
    customer_id: str
    weight_kg: float
    zone: str
    status: str = "created"
    created_at: object = None
    delivered_at: object = None
    notes: list = field(default_factory=list)


@dataclass
class Invoice:
    id: str
    shipment_id: str
    amount: float
    status: str = "open"
    issued_at: object = None
    paid_at: object = None


@dataclass
class Refund:
    id: str
    invoice_id: str
    amount: object
    created_at: object = None
