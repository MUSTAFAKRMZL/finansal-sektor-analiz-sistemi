"""
tests/test_commentary.py
FinancialCommentaryEngine modülünün birim testleri.
"""
import unittest
from src.executive_commentary import FinancialCommentaryEngine

class TestExecutiveCommentary(unittest.TestCase):

    def test_commentary_generation_healthy(self):
        ratios = {
            "liquidity": {"current_ratio": 2.2, "acid_test_ratio": 1.5, "cash_ratio": 0.4},
            "leverage": {"financial_leverage": 0.35, "debt_to_equity": 0.54, "equity_ratio": 0.65},
            "profitability": {"net_profit_margin": 0.18, "roe": 0.25, "roa": 0.12},
            "activity": {"asset_turnover": 0.8, "inventory_turnover": 6.0}
        }
        comparison = {
            "comparisons": [
                {"category": "liquidity", "metric": "current_ratio", "company_value": 2.2, "sector_mean": 1.5},
                {"category": "leverage", "metric": "financial_leverage", "company_value": 0.35, "sector_mean": 0.60},
                {"category": "profitability", "metric": "net_profit_margin", "company_value": 0.18, "sector_mean": 0.08}
            ]
        }
        hybrid = {
            "hybrid_risk_score": 12.0,
            "hybrid_risk_level": "Düşük Risk",
            "critical_flags": [],
            "anomalies": []
        }
        trend = {
            "cagr_sales": 25.0,
            "trend_score": 85.0,
            "trend_direction": "Güçlü İyileşme / Büyüme Trendi",
            "latest_altman": 3.45,
            "latest_altman_zone": "Güvenli Bölge (Safe Zone)",
            "altman_trajectory": "Yükseliyor"
        }

        comm = FinancialCommentaryEngine.generate_company_commentary(
            company_code="TEST_HEALTHY",
            company_name="Test Sağlıklı Şirket A.Ş.",
            sector="Bilişim",
            ratios=ratios,
            comparison=comparison,
            hybrid_report=hybrid,
            trend_data=trend
        )

        self.assertIn("dayanıklı bir finansal profile sahiptir", comm["executive_brief"])
        self.assertGreater(len(comm["strengths"]), 0)
        self.assertIn("sektör ortalamasının", comm["peer_benchmarking"])
        self.assertIn("Güvenli Bölge", comm["altman_summary"])
        self.assertGreater(len(comm["recommendations"]), 0)

    def test_commentary_generation_critical(self):
        ratios = {
            "liquidity": {"current_ratio": 0.45, "acid_test_ratio": 0.2, "cash_ratio": 0.05},
            "leverage": {"financial_leverage": 1.25, "debt_to_equity": -5.0, "equity_ratio": -0.25},
            "profitability": {"net_profit_margin": -0.20, "roe": 0.0, "roa": -0.15},
            "activity": {"asset_turnover": 0.6, "inventory_turnover": 2.0}
        }
        comparison = {"comparisons": []}
        hybrid = {
            "hybrid_risk_score": 92.0,
            "hybrid_risk_level": "Kritik Risk",
            "critical_flags": ["Negatif Özkaynak", "Cari Oran < 1.0", "Net Zarar"],
            "anomalies": []
        }

        comm = FinancialCommentaryEngine.generate_company_commentary(
            company_code="TEST_RISKY",
            company_name="Test Riskli Şirket A.Ş.",
            sector="Teknoloji",
            ratios=ratios,
            comparison=comparison,
            hybrid_report=hybrid,
            trend_data=None
        )

        self.assertIn("yüksek finansal risk taşımaktadır", comm["executive_brief"])
        self.assertTrue(any("Kritik Uyarı" in w for w in comm["weaknesses"]))
        self.assertTrue(any("Acil Finansal Yeniden Yapılandırma" in r or "Borç" in r for r in comm["recommendations"]))

if __name__ == "__main__":
    unittest.main()
