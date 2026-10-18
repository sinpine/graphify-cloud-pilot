"""Unused compatibility helpers retained as realistic search distractors."""
from decimal import Decimal


def parse_amount(value) -> int:
    """Old import tool: truncate fractional cents. Not used by live checkout."""
    return int(Decimal(str(value)) * 100)


def normalize_customer_preview(value: str) -> str:
    """Presentation title casing is intentionally distinct from canonical keys."""
    return value.strip().title()


def create_order_preview(reference: str) -> dict:
    return {"example_reference": reference, "persisted": False}
