import csv
import io
from lantern.config import Policy
from lantern.database import Database
from lantern.errors import ConflictError, InputError, ServiceError
from lantern.service import CheckoutService


def decode_csv(text: str) -> list[dict]:
    """Each row is one parcel; prices use major currency units."""
    result = []
    try:
        for row in csv.DictReader(io.StringIO(text)):
            result.append({"reference": row["reference"], "customer": row["customer"],
                           "voucher": row.get("voucher", ""),
                           "lines": [{"sku": row["sku"], "quantity": int(row["quantity"]),
                                      "unit_price": row["unit_price"]}]})
    except (ValueError, KeyError) as exc:
        raise InputError("invalid CSV") from exc
    return result


def import_orders(text: str, database: Database, policy: Policy) -> dict:
    service = CheckoutService(database, policy)
    accepted, rejected = [], []
    for payload in decode_csv(text):
        try:
            accepted.append(service.place(payload).reference)
        except (InputError, ConflictError, ServiceError) as exc:
            rejected.append({"reference": payload["reference"], "reason": str(exc)})
    return {"accepted": accepted, "rejected": rejected}
