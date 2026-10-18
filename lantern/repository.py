import sqlite3
from lantern.database import Database
from lantern.errors import ConflictError, InputError, StorageError
from lantern.models import Receipt
from lantern.validation import normalize_customer


class OrderRepository:
    def __init__(self, database: Database):
        self.database = database

    def save(self, receipt: Receipt):
        try:
            self.database.connection.execute(
                "INSERT INTO orders(reference, customer, total_cents) VALUES (?, ?, ?)",
                (receipt.reference, receipt.customer, receipt.total_cents))
        except sqlite3.IntegrityError as exc:
            raise ConflictError("reference already exists") from exc
        except sqlite3.DatabaseError as exc:
            raise StorageError("order write failed") from exc

    def get(self, reference: str) -> dict:
        row = self.database.connection.execute(
            "SELECT * FROM orders WHERE reference = ?", (reference,)).fetchone()
        if row is None:
            raise InputError("order not found")
        return dict(row)

    def for_customer(self, customer: str) -> list[dict]:
        key = normalize_customer(customer)
        rows = self.database.connection.execute(
            "SELECT * FROM orders WHERE customer = ? ORDER BY reference", (key,))
        return [dict(row) for row in rows]

    def add_refund(self, reference: str, cents: int):
        self.database.connection.execute(
            "UPDATE orders SET refunded_cents = refunded_cents + ? WHERE reference = ?",
            (cents, reference))
