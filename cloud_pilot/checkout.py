"""Checkout orchestration for the synthetic evaluation fixture."""
from dataclasses import dataclass

from cloud_pilot.pricing import calculate_total


@dataclass(frozen=True)
class Receipt:
    total_cents: int

    def as_dict(self) -> dict[str, int]:
        return {"total_cents": self.total_cents}


def checkout(items: list[tuple[int, int]], discount_cents: int = 0) -> Receipt:
    total = calculate_total(items, discount_cents)
    return Receipt(total)
