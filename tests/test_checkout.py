import unittest

from cloud_pilot.checkout import Receipt, checkout
from cloud_pilot.pricing import calculate_total, normalise_quantity


class CheckoutTests(unittest.TestCase):
    def test_checkout_total(self):
        result = checkout([(2, 100), (1, 250)], discount_cents=50)
        self.assertIsInstance(result, Receipt)
        self.assertEqual(result.as_dict(), {"total_cents": 400})

    def test_discount(self):
        self.assertEqual(calculate_total([(1, 100)], 150), 0)

    def test_invalid_quantity(self):
        for quantity in [0, -1, True, 1.5]:
            with self.assertRaises(ValueError):
                normalise_quantity(quantity)

    def test_negative_discount(self):
        with self.assertRaises(ValueError):
            calculate_total([(1, 100)], -1)

    def test_empty_cart(self):
        self.assertEqual(checkout([]).total_cents, 0)


if __name__ == "__main__":
    unittest.main()
