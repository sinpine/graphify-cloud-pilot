import unittest
from lantern.config import Policy
from lantern.errors import InputError
from lantern.validation import normalize_customer, validate_order, validate_reference


def sample(reference="ORD-001", price="12.00", quantity=2):
    return {"reference": reference, "customer": "  SAMPLE   BUYER ", "voucher": "WELCOME",
            "lines": [{"sku": "BOX", "quantity": quantity, "unit_price": price}]}


class ValidationTests(unittest.TestCase):
    def test_customer_canonical(self):
        self.assertEqual(normalize_customer("  SAMPLE\u3000 Buyer "), "sample buyer")

    def test_quantity_bounds(self):
        for value in [0, 41, True, 1.5]:
            with self.subTest(value=value), self.assertRaises(InputError):
                validate_order(sample(quantity=value), Policy())

    def test_reference_validation(self):
        with self.assertRaises(InputError):
            validate_reference("bad ref")

    def test_order_normalizes(self):
        order = validate_order(sample(), Policy())
        self.assertEqual(order.customer, "sample buyer")
        self.assertEqual(order.lines[0].unit_cents, 1200)
