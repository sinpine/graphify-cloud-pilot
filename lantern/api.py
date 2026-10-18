from lantern.config import Policy
from lantern.database import Database
from lantern.errors import ConflictError, InputError, ServiceError
from lantern.service import CheckoutService


def error_response(exc: Exception) -> dict:
    if isinstance(exc, InputError):
        return {"status": 400, "error": str(exc)}
    if isinstance(exc, ConflictError):
        return {"status": 409, "error": "duplicate reference"}
    return {"status": 503, "error": "checkout unavailable"}


def create_order(payload: dict, database: Database, policy: Policy) -> dict:
    """HTTP-shaped adapter; no network server or user authentication."""
    try:
        receipt = CheckoutService(database, policy).place(payload)
        return {"status": 201, "receipt": receipt.as_dict()}
    except (InputError, ConflictError, ServiceError) as exc:
        return error_response(exc)
