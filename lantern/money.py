from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from lantern.errors import InputError


def parse_money(value) -> int:
    """Convert major-unit money into nonnegative integer cents, half up."""
    if isinstance(value, bool):
        raise InputError("money must not be boolean")
    try:
        amount = Decimal(str(value))
        if not amount.is_finite() or amount < 0:
            raise InputError("money must be finite and nonnegative")
        return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise InputError("invalid money") from exc


def format_money(cents: int) -> str:
    return f"{cents // 100}.{cents % 100:02d}"


def parse_money_preview(value) -> str:
    """UI-only rendering, deliberately not the persistence converter."""
    return format_money(parse_money(value))
