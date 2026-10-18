from lantern.database import Database


def net_revenue(database: Database) -> int:
    """Paid merchandise including delivery, less refunds, in integer cents."""
    row = database.connection.execute(
        "SELECT COALESCE(SUM(total_cents-refunded_cents),0) FROM orders WHERE status='paid'").fetchone()
    return int(row[0])


def order_count(database: Database) -> int:
    return database.connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
