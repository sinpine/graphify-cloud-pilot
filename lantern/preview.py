from lantern.config import Policy
from lantern.pricing import quote_order_preview
from lantern.validation import validate_order


def preview_checkout(payload: dict, policy: Policy) -> dict:
    """Calculate delivery estimate without database writes."""
    return quote_order_preview(validate_order(payload, policy), policy)
