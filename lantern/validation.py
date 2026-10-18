import re
from lantern.config import Policy
from lantern.errors import InputError
from lantern.models import Line, Order
from lantern.money import parse_money


def normalize_customer(value: str) -> str:
    """Canonical customer key used by placement, CSV import and lookup."""
    if not isinstance(value, str):
        raise InputError("customer must be a string")
    result = " ".join(value.split()).casefold()
    if not result or len(result) > 80:
        raise InputError("invalid customer")
    return result


def validate_reference(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Z][A-Z0-9-]{2,24}", value):
        raise InputError("invalid reference")
    return value


def validate_line(raw: dict, policy: Policy) -> Line:
    quantity = raw.get("quantity")
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise InputError("quantity must be integer")
    if not 1 <= quantity <= policy.max_quantity:
        raise InputError("quantity out of range")
    sku = raw.get("sku", "")
    if not isinstance(sku, str) or not sku.strip():
        raise InputError("missing sku")
    return Line(sku.strip(), quantity, parse_money(raw.get("unit_price")))


def validate_order(raw: dict, policy: Policy) -> Order:
    if not isinstance(raw, dict) or not isinstance(raw.get("lines"), list):
        raise InputError("order lines required")
    if not raw["lines"]:
        raise InputError("empty order")
    return Order(validate_reference(raw.get("reference")),
                 normalize_customer(raw.get("customer")),
                 tuple(validate_line(item, policy) for item in raw["lines"]),
                 str(raw.get("voucher", "")))
