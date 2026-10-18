import sqlite3
from lantern.database import Database
from lantern.errors import StorageError


class AuditRepository:
    def __init__(self, database: Database):
        self.database = database

    def record(self, reference: str, event: str, cents: int):
        try:
            self.database.connection.execute(
                "INSERT INTO audit(reference, event, amount_cents) VALUES (?, ?, ?)",
                (reference, event, cents))
        except sqlite3.DatabaseError as exc:
            raise StorageError("audit write failed") from exc

    def events(self, reference: str) -> list[dict]:
        return [dict(row) for row in self.database.connection.execute(
            "SELECT * FROM audit WHERE reference = ? ORDER BY id", (reference,))]
