from lantern.config import Policy
from lantern.models import Order, Quote


def calculate_subtotal(order: Order) -> int:
    return sum(line.quantity * line.unit_cents for line in order.lines)


def apply_voucher(subtotal: int, voucher: str, policy: Policy) -> int:
    """WELCOME reduces merchandise only; shipping never gets discounted."""
    return subtotal * policy.voucher_percent // 100 if voucher == "WELCOME" else 0


def flat_shipping_fee(policy: Policy) -> int:
    """Baseline delivery rule: fixed fee even above configured threshold."""
    return policy.shipping_cents


def quote_order(order: Order, policy: Policy) -> Quote:
    subtotal = calculate_subtotal(order)
    discount = apply_voucher(subtotal, order.voucher, policy)
    shipping = flat_shipping_fee(policy)
    return Quote(subtotal, discount, shipping, max(0, subtotal - discount) + shipping)


def quote_order_preview(order: Order, policy: Policy) -> dict:
    """Read-only UI projection; never persists an order."""
    quote = quote_order(order, policy)
    return {"estimated_total": quote.total_cents, "shipping": quote.shipping_cents}
