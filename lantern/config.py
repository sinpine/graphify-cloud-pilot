from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class Policy:
    shipping_cents: int = 300
    free_shipping_threshold: int = 5000
    max_quantity: int = 40
    voucher_percent: int = 10
    max_refund_cents: int = 20000


def load_policy(path: str | Path) -> Policy:
    """Load the parcel ledger's non-secret checkout policy."""
    with open(path, "rb") as stream:
        values = tomllib.load(stream)["checkout"]
    result = Policy(**values)
    if not 0 <= result.voucher_percent <= 100:
        raise ValueError("voucher_percent out of range")
    return result
