"""
tests/test_trend_analysis.py
TrendAnalyzer ve Altman Z-Score modelinin birim testleri.
"""
import unittest
from src.models import Company, BalanceSheet, IncomeStatement
from src.trend_analysis import TrendAnalyzer

class TestTrendAnalysis(unittest.TestCase):

    def setUp(self):
        # 3 Yıllık Sağlıklı Test Şirketi
        self.healthy_comps = [
            Company(
                code="GROWTH_CO",
                name="Büyüyen Şirket A.Ş.",
                sector="Teknoloji",
                period="2021/12",
                balance_sheet=BalanceSheet(
                    cash_and_equivalents=2000, accounts_receivable=3000, inventories=1000,
                    other_current_assets=500, tangible_assets=5000, intangible_assets=1000,
                    other_non_current_assets=500, short_term_financial_debt=1000,
                    short_term_trade_payables=2000, other_short_term_debt=500,
                    long_term_financial_debt=1500, other_long_term_debt=500,
                    paid_in_capital=4000, retained_earnings=2000, net_period_profit_bs=1500
                ),
                income_statement=IncomeStatement(
                    net_sales=10000, cost_of_sales=6000, operating_expenses=1500,
                    financial_expenses=500, tax_expenses=500, net_profit=1500
                )
            ),
            Company(
                code="GROWTH_CO",
                name="Büyüyen Şirket A.Ş.",
                sector="Teknoloji",
                period="2022/12",
                balance_sheet=BalanceSheet(
                    cash_and_equivalents=3000, accounts_receivable=4000, inventories=1200,
                    other_current_assets=600, tangible_assets=6000, intangible_assets=1200,
                    other_non_current_assets=600, short_term_financial_debt=1200,
                    short_term_trade_payables=2400, other_short_term_debt=600,
                    long_term_financial_debt=1800, other_long_term_debt=600,
                    paid_in_capital=4500, retained_earnings=3200, net_period_profit_bs=2300
                ),
                income_statement=IncomeStatement(
                    net_sales=14000, cost_of_sales=8200, operating_expenses=2000,
                    financial_expenses=600, tax_expenses=900, net_profit=2300
                )
            ),
            Company(
                code="GROWTH_CO",
                name="Büyüyen Şirket A.Ş.",
                sector="Teknoloji",
                period="2023/12",
                balance_sheet=BalanceSheet(
                    cash_and_equivalents=4500, accounts_receivable=5500, inventories=1500,
                    other_current_assets=800, tangible_assets=7500, intangible_assets=1500,
                    other_non_current_assets=800, short_term_financial_debt=1500,
                    short_term_trade_payables=3000, other_short_term_debt=800,
                    long_term_financial_debt=2200, other_long_term_debt=800,
                    paid_in_capital=5000, retained_earnings=5000, net_period_profit_bs=3500
                ),
                income_statement=IncomeStatement(
                    net_sales=20000, cost_of_sales=11500, operating_expenses=2800,
                    financial_expenses=800, tax_expenses=1400, net_profit=3500
                )
            )
        ]

    def test_cagr_calculation(self):
        # 10,000 -> 20,000 in 2 years = (20000/10000)^(1/2) - 1 = sqrt(2) - 1 = 41.42%
        cagr = TrendAnalyzer.calculate_cagr(10000, 20000, 2)
        self.assertIsNotNone(cagr)
        self.assertAlmostEqual(cagr, 41.42, delta=0.1)

        # Negatif veya sıfır değer koruması
        self.assertIsNone(TrendAnalyzer.calculate_cagr(0, 100, 2))
        self.assertIsNone(TrendAnalyzer.calculate_cagr(-50, 100, 2))

    def test_altman_z_score_healthy_and_distressed(self):
        # Sağlıklı şirket
        healthy = self.healthy_comps[-1]
        z_data = TrendAnalyzer.calculate_altman_z_score(healthy)
        self.assertIn("z_score", z_data)
        self.assertIn("zone", z_data)
        self.assertGreater(z_data["z_score"], 1.81)

        # İflas riski olan batık şirket
        distressed = Company(
            code="DISTRESSED",
            name="Batık Şirket",
            sector="İnşaat",
            period="2023/12",
            balance_sheet=BalanceSheet(
                cash_and_equivalents=100, accounts_receivable=200, inventories=300,
                other_current_assets=50, tangible_assets=500, intangible_assets=50,
                other_non_current_assets=50, short_term_financial_debt=1500,
                short_term_trade_payables=1000, other_short_term_debt=500,
                long_term_financial_debt=1000, other_long_term_debt=200,
                paid_in_capital=500, retained_earnings=-3000, net_period_profit_bs=-1000
            ),
            income_statement=IncomeStatement(
                net_sales=800, cost_of_sales=900, operating_expenses=400,
                financial_expenses=300, tax_expenses=0, net_profit=-1000
            )
        )
        z_dist = TrendAnalyzer.calculate_altman_z_score(distressed)
        self.assertEqual(z_dist["status"], "DISTRESS")
        self.assertLess(z_dist["z_score"], 1.81)

    def test_trend_analyzer_trajectory(self):
        analyzer = TrendAnalyzer(self.healthy_comps)
        trend = analyzer.analyze_company_trend("GROWTH_CO")
        
        self.assertEqual(trend["period_count"], 3)
        self.assertEqual(len(trend["yoy_changes"]), 2)
        self.assertGreater(trend["trend_score"], 70)
        self.assertEqual(trend["trend_badge"], "POSITIVE")
        self.assertEqual(trend["altman_trajectory"], "Yükseliyor")

if __name__ == "__main__":
    unittest.main()
