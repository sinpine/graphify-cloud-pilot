from lantern.config import Policy
from lantern.database import Database
from lantern.errors import InputError
from lantern.money import parse_money
from lantern.refunds import RefundService


def submit_refund(reference: str, amount, database: Database, policy: Policy) -> dict:
    """Synthetic investigation fixture: adapter currently converts money twice."""
    try:
        converted = parse_money(amount)
        refunded = RefundService(database, policy).refund(reference, converted)
        return {"status": 200, "refunded_cents": refunded}
    except InputError as exc:
        return {"status": 400, "error": str(exc)}
