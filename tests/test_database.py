"""
tests/test_database.py
SQLite veritabanı işlemlerini, kayıt ve okuma fonksiyonlarını doğrulayan birim testler.
"""
import os
import unittest
from src.models import BalanceSheet, IncomeStatement, Company
from src.database import DatabaseManager
from src.ratios import FinancialRatioCalculator

class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_financial.db"
        self.db = DatabaseManager(self.test_db)
        
        self.bs = BalanceSheet(
            cash_and_equivalents=1000.0, accounts_receivable=2000.0, inventories=1500.0,
            other_current_assets=500.0, tangible_assets=4000.0, intangible_assets=1000.0,
            other_non_current_assets=0.0, short_term_financial_debt=1000.0,
            short_term_trade_payables=1500.0, other_short_term_debt=500.0,
            long_term_financial_debt=2000.0, other_long_term_debt=0.0,
            paid_in_capital=3000.0, retained_earnings=1000.0, net_period_profit_bs=1000.0
        )
        self.inc = IncomeStatement(
            net_sales=10000.0, cost_of_sales=6000.0, operating_expenses=2000.0,
            financial_expenses=500.0, tax_expenses=500.0, net_profit=1000.0
        )
        self.company = Company(
            code="TEST_DB", name="Test DB Şirketi", sector="Yazılım",
            period="2023/12", balance_sheet=self.bs, income_statement=self.inc
        )

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_save_and_get_company(self):
        company_id = self.db.save_company(self.company)
        self.assertGreater(company_id, 0)

        companies = self.db.get_all_companies()
        codes = [c["code"] for c in companies]
        self.assertIn("TEST_DB", codes)

    def test_save_ratios_and_summary(self):
        self.db.save_company(self.company)
        ratios = FinancialRatioCalculator.calculate_all(self.company)
        self.db.save_ratios(self.company.code, self.company.period, ratios)

        summary = self.db.get_company_summary(self.company.code)
        self.assertIsNotNone(summary)
        self.assertEqual(summary["code"], "TEST_DB")
        self.assertAlmostEqual(summary["current_ratio"], 1.6667, places=4)

if __name__ == "__main__":
    unittest.main()
