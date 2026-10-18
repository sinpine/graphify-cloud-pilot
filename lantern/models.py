from dataclasses import dataclass


@dataclass(frozen=True)
class Line:
    sku: str
    quantity: int
    unit_cents: int


@dataclass(frozen=True)
class Order:
    reference: str
    customer: str
    lines: tuple[Line, ...]
    voucher: str


@dataclass(frozen=True)
class Quote:
    subtotal_cents: int
    discount_cents: int
    shipping_cents: int
    total_cents: int


@dataclass(frozen=True)
class Receipt:
    reference: str
    customer: str
    total_cents: int

    def as_dict(self) -> dict:
        return {"reference": self.reference, "customer": self.customer,
                "total_cents": self.total_cents}
