"""
tests/test_data_loader.py
CSV ve JSON veri yükleyicilerini test eden birim testler.
"""
import os
import unittest
from src.data_loader import FinancialDataLoader

class TestFinancialDataLoader(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.json_path = os.path.join(self.base_dir, "data", "sample_companies.json")
        self.csv_path = os.path.join(self.base_dir, "data", "companies_financials.csv")

    def test_load_from_json(self):
        companies = FinancialDataLoader.load_from_json(self.json_path)
        self.assertGreater(len(companies), 0)
        self.assertEqual(companies[0].code, "ASELS_SIM")
        self.assertGreater(companies[0].balance_sheet.total_assets, 0)

    def test_load_from_csv(self):
        companies = FinancialDataLoader.load_from_csv(self.csv_path)
        self.assertGreaterEqual(len(companies), 10)
        codes = [c.code for c in companies]
        self.assertIn("BIMAS_SIM", codes)
        self.assertIn("FROTO_SIM", codes)

if __name__ == "__main__":
    unittest.main()
