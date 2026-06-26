import unittest
import numpy as np


# ---------------------------------------
# Ratio Formula Functions
# ---------------------------------------

def net_profit_margin(net_profit, sales):
    if sales == 0:
        return np.nan
    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales):
    if sales == 0:
        return np.nan
    return round((operating_profit / sales) * 100, 2)


def roe(net_profit, equity, reserves):
    capital = equity + reserves

    if capital <= 0:
        return np.nan

    return round((net_profit / capital) * 100, 2)


def roce(ebit, equity, reserves, borrowings):
    capital_employed = equity + reserves + borrowings

    if capital_employed <= 0:
        return np.nan

    return round((ebit / capital_employed) * 100, 2)


def roa(net_profit, total_assets):
    if total_assets == 0:
        return np.nan

    return round((net_profit / total_assets) * 100, 2)


def validate_opm(calculated, source):

    difference = abs(calculated - source)

    if difference > 1:
        return "FAIL"

    return "PASS"


# ---------------------------------------
# Unit Tests
# ---------------------------------------

class TestFinancialRatios(unittest.TestCase):

    # Test 1
    def test_net_profit_margin(self):

        self.assertEqual(
            net_profit_margin(250, 1000),
            25.00
        )

    # Test 2
    def test_zero_sales_returns_nan(self):

        self.assertTrue(
            np.isnan(
                net_profit_margin(100, 0)
            )
        )

    # Test 3
    def test_operating_profit_margin(self):

        self.assertEqual(
            operating_profit_margin(350, 1000),
            35.00
        )

    # Test 4
    def test_opm_cross_check_pass(self):

        self.assertEqual(
            validate_opm(20.15, 20.80),
            "PASS"
        )

    # Test 5
    def test_opm_cross_check_fail(self):

        self.assertEqual(
            validate_opm(20.15, 23.80),
            "FAIL"
        )

    # Test 6
    def test_roe(self):

        self.assertEqual(
            roe(
                net_profit=200,
                equity=100,
                reserves=900
            ),
            20.00
        )

    # Test 7
    def test_negative_equity_returns_nan(self):

        self.assertTrue(
            np.isnan(
                roe(
                    100,
                    -200,
                    100
                )
            )
        )

    # Test 8
    def test_roce(self):

        self.assertEqual(
            roce(
                ebit=300,
                equity=500,
                reserves=500,
                borrowings=500
            ),
            20.00
        )

    # Test 9
    def test_roa(self):

        self.assertEqual(
            roa(
                100,
                1000
            ),
            10.00
        )

    # Test 10
    def test_zero_assets_returns_nan(self):

        self.assertTrue(
            np.isnan(
                roa(
                    100,
                    0
                )
            )
        )


if __name__ == "__main__":
    unittest.main()