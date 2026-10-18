import json
from lantern.config import Policy
from lantern.database import Database
from lantern.errors import InputError
from lantern.service import CheckoutService


def run_checkout(text: str, database: Database, policy: Policy) -> str:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise InputError("invalid JSON") from exc
    return json.dumps(CheckoutService(database, policy).place(payload).as_dict(), sort_keys=True)
