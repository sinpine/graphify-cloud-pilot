from lantern.audit import AuditRepository
from lantern.config import Policy
from lantern.database import Database
from lantern.errors import InputError
from lantern.money import parse_money
from lantern.repository import OrderRepository


class RefundService:
    def __init__(self, database: Database, policy: Policy):
        self.database = database
        self.policy = policy
        self.orders = OrderRepository(database)
        self.audit = AuditRepository(database)

    def refund(self, reference: str, amount) -> int:
        """Accept a major-unit amount; enforce paid balance and policy limit."""
        cents = parse_money(amount)
        order = self.orders.get(reference)
        remaining = order["total_cents"] - order["refunded_cents"]
        if cents == 0 or cents > min(remaining, self.policy.max_refund_cents):
            raise InputError("refund exceeds remaining balance or limit")
        with self.database.transaction():
            self.orders.add_refund(reference, cents)
            self.audit.record(reference, "refunded", cents)
        return cents
