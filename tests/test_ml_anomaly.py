"""
tests/test_ml_anomaly.py
Hafta 3: Veri normalizasyonu, Isolation Forest makine öğrenmesi modeli,
k-NN aykırı değer dedektörü ve Web Dashboard dışa aktarımını doğrulayan birim testler.
"""
import os
import unittest
from src.ml_anomaly import DataNormalizer, IsolationForestDetector, KNNOutlierDetector
from src.data_loader import FinancialDataLoader
from src.sector_analysis import SectorAnalyzer
from src.anomaly_detector import FinancialAnomalyDetector
from src.ml_anomaly import HybridAnomalyEngine
from src.web_dashboard import DashboardGenerator


class TestMLAnomalyAndDashboard(unittest.TestCase):

    def test_min_max_normalization_and_zero_variance(self):
        # 1. sütun normal değişen, 2. sütun sabit (max == min -> 0.5 olmalı)
        matrix = [
            [10.0, 5.0],
            [20.0, 5.0],
            [30.0, 5.0]
        ]
        norm, bounds = DataNormalizer.min_max_normalize(matrix)
        self.assertEqual(norm[0][0], 0.0)
        self.assertEqual(norm[1][0], 0.5)
        self.assertEqual(norm[2][0], 1.0)
        # Sabit sütunda ZeroDivisionError olmamalı, 0.5 atanmalı
        self.assertEqual(norm[0][1], 0.5)
        self.assertEqual(norm[1][1], 0.5)

    def test_isolation_forest_detects_outlier(self):
        # 5 adet birbirine yakın normal şirket vektörü, 1 adet aşırı uç vektör
        data = [
            [0.50, 0.48, 0.52],
            [0.51, 0.49, 0.50],
            [0.49, 0.50, 0.51],
            [0.52, 0.47, 0.49],
            [0.50, 0.51, 0.50],
            [0.99, 0.01, 0.98]  # Aykırı şirket (indeks 5)
        ]
        iforest = IsolationForestDetector(n_estimators=100, random_state=42)
        iforest.fit(data)
        scores = iforest.score_samples(data)

        outlier_score = scores[5]
        normal_avg = sum(scores[:5]) / 5.0
        self.assertGreater(outlier_score, normal_avg)

    def test_knn_outlier_detector(self):
        data = [
            [0.1, 0.1],
            [0.12, 0.11],
            [0.11, 0.09],
            [0.95, 0.95]  # Uzak nokta (indeks 3)
        ]
        knn = KNNOutlierDetector(k=2)
        scores = knn.score_samples(data)
        self.assertEqual(scores[3], max(scores))
        self.assertGreater(scores[3], 80.0)

    def test_hybrid_engine_and_dashboard_generation(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, "data", "companies_financials.csv")
        test_html = os.path.join(base_dir, "test_dashboard_out.html")

        try:
            companies = FinancialDataLoader.load_from_csv(csv_path)
            analyzer = SectorAnalyzer(companies)
            detector = FinancialAnomalyDetector(z_threshold=1.5)

            comparisons = {c.code: analyzer.compare_company_with_sector(c.code) for c in companies}
            base_risks = {c.code: detector.evaluate_risk(comparisons[c.code]) for c in companies}

            engine = HybridAnomalyEngine()
            hybrid_reports = engine.analyze_all_companies(companies, analyzer.company_ratios, base_risks)

            # RISKY_TECH en yüksek hibrit risk skoruna sahip olmalı
            self.assertGreaterEqual(hybrid_reports["RISKY_TECH"]["hybrid_risk_score"], 80.0)
            self.assertLess(hybrid_reports["ASELS_SIM"]["hybrid_risk_score"], 40.0)

            out_file = DashboardGenerator.export_dashboard(
                companies, analyzer.sector_benchmarks, comparisons, hybrid_reports, output_path=test_html
            )
            self.assertTrue(os.path.exists(out_file))
            with open(out_file, "r", encoding="utf-8") as f:
                html_text = f.read()
            self.assertIn("radarSvg", html_text)
            self.assertIn("RISKY_TECH", html_text)
        finally:
            if os.path.exists(test_html):
                os.remove(test_html)


if __name__ == "__main__":
    unittest.main()
