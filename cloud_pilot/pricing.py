"""Pure pricing functions for a synthetic checkout example."""


def normalise_quantity(quantity: int) -> int:
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1:
        raise ValueError("quantity must be a positive integer")
    return quantity


def calculate_subtotal(items: list[tuple[int, int]]) -> int:
    return sum(normalise_quantity(quantity) * unit_cents
               for quantity, unit_cents in items)


def apply_discount(subtotal_cents: int, discount_cents: int) -> int:
    if discount_cents < 0:
        raise ValueError("discount cannot be negative")
    return max(0, subtotal_cents - discount_cents)


def calculate_total(items: list[tuple[int, int]], discount_cents: int = 0) -> int:
    subtotal = calculate_subtotal(items)
    return apply_discount(subtotal, discount_cents)
