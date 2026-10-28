"""
src/data_loader.py
Şirket finansal tablolarını CSV ve JSON dosyalarından içeri aktaran veri yükleyici modülü.
Veri doğrulama, eksik alan kontrolü ve tip dönüşümlerini yönetir.
"""
import os
import csv
import json
from typing import List, Dict, Any, Optional
from src.models import BalanceSheet, IncomeStatement, Company

class FinancialDataLoader:
    """Finansal verileri dosya sisteminden okur, doğrular ve Company nesnelerine dönüştürür."""

    REQUIRED_BS_FIELDS = [
        "cash_and_equivalents", "accounts_receivable", "inventories", "other_current_assets",
        "tangible_assets", "intangible_assets", "other_non_current_assets",
        "short_term_financial_debt", "short_term_trade_payables", "other_short_term_debt",
        "long_term_financial_debt", "other_long_term_debt",
        "paid_in_capital", "retained_earnings", "net_period_profit_bs"
    ]

    REQUIRED_INC_FIELDS = [
        "net_sales", "cost_of_sales", "operating_expenses",
        "financial_expenses", "tax_expenses", "net_profit"
    ]

    @classmethod
    def load_from_json(cls, file_path: str) -> List[Company]:
        """JSON dosyasından şirket finansal verilerini yükler."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Veri dosyası bulunamadı: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        companies = []
        for item in data:
            cls._validate_item(item)
            bs = BalanceSheet(**item["balance_sheet"])
            inc = IncomeStatement(**item["income_statement"])
            comp = Company(
                code=item["code"],
                name=item["name"],
                sector=item["sector"],
                period=item["period"],
                balance_sheet=bs,
                income_statement=inc
            )
            companies.append(comp)
        return companies

    @classmethod
    def load_from_csv(cls, file_path: str) -> List[Company]:
        """CSV dosyasından şirket finansal verilerini okur ve doğrular."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV dosyası bulunamadı: {file_path}")

        companies = []
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                bs_data = {}
                for field in cls.REQUIRED_BS_FIELDS:
                    val = row.get(field, "0").strip()
                    bs_data[field] = float(val) if val else 0.0

                inc_data = {}
                for field in cls.REQUIRED_INC_FIELDS:
                    val = row.get(field, "0").strip()
                    inc_data[field] = float(val) if val else 0.0

                bs = BalanceSheet(**bs_data)
                inc = IncomeStatement(**inc_data)

                comp = Company(
                    code=row["code"].strip(),
                    name=row["name"].strip(),
                    sector=row["sector"].strip(),
                    period=row["period"].strip(),
                    balance_sheet=bs,
                    income_statement=inc
                )
                companies.append(comp)
        return companies

    @classmethod
    def _validate_item(cls, item: Dict[str, Any]):
        """Şirket veri yapısının eksik anahtar içermediğini kontrol eder."""
        for key in ["code", "name", "sector", "period", "balance_sheet", "income_statement"]:
            if key not in item:
                raise ValueError(f"Eksik şirket anahtarı: '{key}' (Şirket: {item.get('code', 'Bilinmeyen')})")

        bs = item["balance_sheet"]
        for f in cls.REQUIRED_BS_FIELDS:
            if f not in bs:
                raise ValueError(f"Bilanço verisinde eksik alan: '{f}' (Şirket: {item['code']})")

        inc = item["income_statement"]
        for f in cls.REQUIRED_INC_FIELDS:
            if f not in inc:
                raise ValueError(f"Gelir tablosu verisinde eksik alan: '{f}' (Şirket: {item['code']})")
