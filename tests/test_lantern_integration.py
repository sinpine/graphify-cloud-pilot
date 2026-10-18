import json
import unittest
from unittest.mock import patch
from lantern.api import create_order
from lantern.batch import import_orders
from lantern.cli import run_checkout
from lantern.config import Policy
from lantern.database import Database
from lantern.errors import InputError, StorageError
from lantern.repository import OrderRepository
from lantern.reporting import net_revenue, order_count
from lantern.service import CheckoutService
from lantern.preview import preview_checkout
from test_lantern_validation import sample


CSV = "reference,customer,sku,quantity,unit_price,voucher\nCSV-001, SAMPLE BUYER ,BOX,2,12.00,WELCOME\n"


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.policy = Policy()

    def tearDown(self):
        self.db.close()

    def test_api_persists(self):
        result = create_order(sample(), self.db, self.policy)
        self.assertEqual(result["status"], 201)
        self.assertEqual(OrderRepository(self.db).get("ORD-001")["total_cents"], 2460)

    def test_api_duplicate_409(self):
        create_order(sample(), self.db, self.policy)
        self.assertEqual(create_order(sample(), self.db, self.policy)["status"], 409)
        self.assertEqual(order_count(self.db), 1)

    def test_api_bad_quantity_400(self):
        self.assertEqual(create_order(sample(quantity=True), self.db, self.policy)["status"], 400)
        self.assertEqual(order_count(self.db), 0)

    def test_atomic_audit_failure_503(self):
        with patch("lantern.audit.AuditRepository.record", side_effect=StorageError("synthetic")):
            result = create_order(sample(), self.db, self.policy)
        self.assertEqual(result["status"], 503)
        self.assertEqual(order_count(self.db), 0)

    def test_csv_import(self):
        result = import_orders(CSV, self.db, self.policy)
        self.assertEqual(result["accepted"], ["CSV-001"])
        self.assertEqual(OrderRepository(self.db).for_customer(" SAMPLE BUYER ")[0]["customer"],
                         "sample buyer")

    def test_csv_duplicate_rejected(self):
        import_orders(CSV, self.db, self.policy)
        self.assertEqual(len(import_orders(CSV, self.db, self.policy)["rejected"]), 1)

    def test_csv_bad_quantity(self):
        with self.assertRaises(InputError):
            import_orders(CSV.replace(",2,", ",oops,"), self.db, self.policy)

    def test_cli_round_trip(self):
        result = json.loads(run_checkout(json.dumps(sample()), self.db, self.policy))
        self.assertEqual(result["total_cents"], 2460)

    def test_preview_no_write(self):
        self.assertEqual(preview_checkout(sample(), self.policy)["shipping"], 300)
        self.assertEqual(order_count(self.db), 0)

    def test_customer_lookup_normalized(self):
        CheckoutService(self.db, self.policy).place(sample())
        self.assertEqual(len(OrderRepository(self.db).for_customer("SAMPLE\u3000BUYER")), 1)

    def test_revenue_paid_only(self):
        CheckoutService(self.db, self.policy).place(sample())
        self.assertEqual(net_revenue(self.db), 2460)
