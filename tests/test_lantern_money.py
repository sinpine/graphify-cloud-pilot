import unittest
from lantern.errors import InputError
from lantern.money import parse_money, parse_money_preview
from lantern.legacy import parse_amount


class MoneyTests(unittest.TestCase):
    def test_half_up(self):
        self.assertEqual(parse_money("1.005"), 101)
        self.assertEqual(parse_money("1.004"), 100)

    def test_invalid_money(self):
        for value in [True, "NaN", "Infinity", -1, "oops"]:
            with self.subTest(value=value), self.assertRaises(InputError):
                parse_money(value)

    def test_preview_format(self):
        self.assertEqual(parse_money_preview("1.005"), "1.01")

    def test_legacy_truncates(self):
        self.assertEqual(parse_amount("1.005"), 100)
