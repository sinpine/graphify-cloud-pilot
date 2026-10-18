import unittest
from lantern.config import Policy
from lantern.database import Database
from lantern.errors import InputError
from lantern.refund_api import submit_refund
from lantern.refunds import RefundService
from lantern.reporting import net_revenue
from lantern.service import CheckoutService
from test_lantern_validation import sample


class RefundTests(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.policy = Policy()
        CheckoutService(self.db, self.policy).place(sample())

    def tearDown(self):
        self.db.close()

    def test_service_refund(self):
        self.assertEqual(RefundService(self.db, self.policy).refund("ORD-001", "5.00"), 500)
        self.assertEqual(net_revenue(self.db), 1960)

    def test_api_double_conversion_reproducer(self):
        # Characterize the intentional bug without pretending it is fixed.
        self.assertEqual(submit_refund("ORD-001", "5.00", self.db, self.policy)["status"], 400)
        self.assertEqual(net_revenue(self.db), 2460)

    def test_refund_balance_guard(self):
        with self.assertRaises(InputError):
            RefundService(self.db, self.policy).refund("ORD-001", "100.00")

    def test_refund_zero_guard(self):
        with self.assertRaises(InputError):
            RefundService(self.db, self.policy).refund("ORD-001", "0")
