from contextlib import contextmanager
import sqlite3


class Database:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.initialize()

    def initialize(self):
        self.connection.executescript("""
        CREATE TABLE IF NOT EXISTS orders (
            reference TEXT PRIMARY KEY, customer TEXT NOT NULL,
            total_cents INTEGER NOT NULL CHECK(total_cents >= 0),
            refunded_cents INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'paid');
        CREATE TABLE IF NOT EXISTS audit (
            id INTEGER PRIMARY KEY, reference TEXT NOT NULL,
            event TEXT NOT NULL, amount_cents INTEGER NOT NULL);
        """)

    @contextmanager
    def transaction(self):
        try:
            yield self.connection
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise

    def close(self):
        self.connection.close()
