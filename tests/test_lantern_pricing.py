import unittest
from pathlib import Path
from lantern.config import Policy, load_policy
from lantern.pricing import quote_order, quote_order_preview
from lantern.validation import validate_order
from test_lantern_validation import sample


class PricingTests(unittest.TestCase):
    def test_voucher_merchandise_only(self):
        quote = quote_order(validate_order(sample(), Policy()), Policy())
        self.assertEqual((quote.subtotal_cents, quote.discount_cents, quote.shipping_cents),
                         (2400, 240, 300))
        self.assertEqual(quote.total_cents, 2460)

    def test_shipping_baseline(self):
        quote = quote_order(validate_order(sample(price="30.00"), Policy()), Policy())
        self.assertEqual(quote.shipping_cents, 300)

    def test_preview_uses_quote(self):
        self.assertEqual(quote_order_preview(validate_order(sample(), Policy()), Policy())
                         ["estimated_total"], 2460)

    def test_load_policy(self):
        path = Path(__file__).parents[1] / "lantern" / "policy.toml"
        self.assertEqual(load_policy(path), Policy())
