from lantern.audit import AuditRepository
from lantern.config import Policy
from lantern.database import Database
from lantern.errors import ConflictError, ServiceError, StorageError
from lantern.models import Receipt
from lantern.pricing import quote_order
from lantern.repository import OrderRepository
from lantern.validation import validate_order


class CheckoutService:
    def __init__(self, database: Database, policy: Policy):
        self.database = database
        self.policy = policy
        self.orders = OrderRepository(database)
        self.audit = AuditRepository(database)

    def place(self, payload: dict) -> Receipt:
        """Validate, price and atomically save order and audit event."""
        order = validate_order(payload, self.policy)
        quote = quote_order(order, self.policy)
        receipt = Receipt(order.reference, order.customer, quote.total_cents)
        try:
            with self.database.transaction():
                self.orders.save(receipt)
                self.audit.record(order.reference, "placed", receipt.total_cents)
        except ConflictError:
            raise
        except StorageError as exc:
            raise ServiceError("checkout unavailable") from exc
        return receipt
