"""
tests/test_ratios.py
Finansal oran hesaplamalarını ve sınır durumları test eden birim testler.
"""
import unittest
from src.models import BalanceSheet, IncomeStatement, Company
from src.ratios import FinancialRatioCalculator, safe_divide

class TestFinancialRatios(unittest.TestCase):

    def setUp(self):
        self.bs = BalanceSheet(
            cash_and_equivalents=1000.0,
            accounts_receivable=2000.0,
            inventories=1500.0,
            other_current_assets=500.0,
            tangible_assets=4000.0,
            intangible_assets=1000.0,
            other_non_current_assets=0.0,
            short_term_financial_debt=1000.0,
            short_term_trade_payables=1500.0,
            other_short_term_debt=500.0,
            long_term_financial_debt=2000.0,
            other_long_term_debt=0.0,
            paid_in_capital=3000.0,
            retained_earnings=1000.0,
            net_period_profit_bs=1000.0
        )
        self.inc = IncomeStatement(
            net_sales=10000.0,
            cost_of_sales=6000.0,
            operating_expenses=2000.0,
            financial_expenses=500.0,
            tax_expenses=500.0,
            net_profit=1000.0
        )
        self.company = Company(
            code="TEST",
            name="Test Şirketi A.Ş.",
            sector="Test",
            period="2023/12",
            balance_sheet=self.bs,
            income_statement=self.inc
        )

    def test_current_ratio(self):
        # Dönen Varlıklar: 1000+2000+1500+500 = 5000
        # KVYK: 1000+1500+500 = 3000
        # Cari Oran = 5000 / 3000 = 1.6667
        liq = FinancialRatioCalculator.calculate_liquidity_ratios(self.bs)
        self.assertAlmostEqual(liq["current_ratio"], 1.6667, places=4)

    def test_acid_test_ratio(self):
        # (Dönen Varlıklar - Stoklar) / KVYK = (5000 - 1500) / 3000 = 3500 / 3000 = 1.1667
        liq = FinancialRatioCalculator.calculate_liquidity_ratios(self.bs)
        self.assertAlmostEqual(liq["acid_test_ratio"], 1.1667, places=4)

    def test_safe_divide_by_zero(self):
        # Sıfıra bölünme hatası fırlatmamalı, None döndürmeli
        result = safe_divide(100.0, 0.0)
        self.assertIsNone(result)

    def test_profitability_margins(self):
        prof = FinancialRatioCalculator.calculate_profitability_ratios(self.bs, self.inc)
        # Net Kâr Marjı: 1000 / 10000 = 0.10 (%10)
        self.assertEqual(prof["net_profit_margin"], 0.10)
        # Brüt Kâr: 10000 - 6000 = 4000 -> Marj: 4000 / 10000 = 0.40 (%40)
        self.assertEqual(prof["gross_profit_margin"], 0.40)

if __name__ == "__main__":
    unittest.main()
