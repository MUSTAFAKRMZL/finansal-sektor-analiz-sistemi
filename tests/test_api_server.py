"""
tests/test_api_server.py
Hafta 5: REST API Sunucusu, SQLite dinamik veri geri yükleme ve canlı simülasyon uç noktası testleri.
"""
import os
import json
import threading
import unittest
import urllib.request
import urllib.error

from src.data_loader import FinancialDataLoader
from src.database import DatabaseManager
from src.api_server import create_api_server


class TestAPIServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db = "test_api_server.db"
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

        db = DatabaseManager(cls.test_db)
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "companies_financials.csv")
        companies = FinancialDataLoader.load_from_csv(csv_path)
        for comp in companies:
            db.save_company(comp)

        cls.server = create_api_server(
            host="127.0.0.1",
            port=0,
            db_path=cls.test_db,
            static_dir=os.path.dirname(os.path.dirname(__file__))
        )
        cls.port = cls.server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

    def _get_json(self, path):
        with urllib.request.urlopen(f"{self.base_url}{path}") as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    def test_health_endpoint(self):
        status, data = self._get_json("/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["version"], "0.5.0")
        self.assertEqual(data["total_companies"], 10)
        self.assertEqual(data["total_period_records"], 30)
        self.assertEqual(data["latest_period"], "2025/12")

    def test_companies_and_detail_endpoints(self):
        status, data = self._get_json("/api/companies")
        self.assertEqual(status, 200)
        self.assertEqual(len(data["companies"]), 10)

        status_detail, detail = self._get_json("/api/companies/ASELS_SIM")
        self.assertEqual(status_detail, 200)
        self.assertEqual(detail["company"]["code"], "ASELS_SIM")
        self.assertIn("ratios", detail)
        self.assertIn("commentary", detail)
        self.assertIn("trend_report", detail)

        # Olmayan şirket 404 dönmeli
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(f"{self.base_url}/api/companies/OLMAYAN_SIRKET")
        self.assertEqual(ctx.exception.code, 404)

    def test_sectors_endpoint(self):
        status, data = self._get_json("/api/sectors")
        self.assertEqual(status, 200)
        self.assertIn("Savunma ve Bilişim", data["sectors"])

    def test_post_analyze_simulation(self):
        payload = {
            "name": "API Test Teknoloji A.Ş.",
            "sector": "Savunma ve Bilişim",
            "current_assets": 25000000,
            "inventories": 5000000,
            "cash": 8000000,
            "total_assets": 50000000,
            "short_term_debt": 10000000,
            "total_debt": 20000000,
            "equity": 30000000,
            "net_sales": 60000000,
            "net_profit": 9000000
        }
        req = urllib.request.Request(
            f"{self.base_url}/api/analyze",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            res_data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(res_data["name"], "API Test Teknoloji A.Ş.")
            self.assertAlmostEqual(res_data["ratios"]["liquidity"]["current_ratio"], 2.5, places=2)
            self.assertIn("altman", res_data)
            self.assertIn("commentary", res_data)

    def test_security_blocks_python_and_db_files(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(f"{self.base_url}/src/models.py")
        self.assertEqual(ctx.exception.code, 403)


if __name__ == "__main__":
    unittest.main()
