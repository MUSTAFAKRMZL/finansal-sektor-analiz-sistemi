"""
src/database.py
SQLite tabanlı ilişkisel veritabanı yönetim modülü (DatabaseManager).
Şirket kayıtları, bilanço, gelir tablosu, hesaplanan rasyolar ve anomali sonuçlarını kalıcı olarak saklar.
"""
import sqlite3
import json
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from src.models import Company, BalanceSheet, IncomeStatement

class DatabaseManager:
    """Finansal analiz veritabanı işlemlerini yöneten sınıf."""

    def __init__(self, db_path: str = "financial_analysis.db"):
        self.db_path = db_path
        self._init_tables()

    @contextmanager
    def get_connection(self):
        """Bağlantıyı otomatik açıp işlem sonunda kapatan güvenli context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_tables(self):
        """Veritabanı tablolarını ve ilişkilerini oluşturur."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Şirketler Tablosu
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                sector TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 2. Finansal Tablolar (Bilanço ve Gelir Tablosu Kalemleri)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_statements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                period TEXT NOT NULL,
                total_current_assets REAL,
                total_non_current_assets REAL,
                total_assets REAL,
                total_short_term_liabilities REAL,
                total_long_term_liabilities REAL,
                total_liabilities REAL,
                total_equity REAL,
                net_sales REAL,
                cost_of_sales REAL,
                gross_profit REAL,
                operating_profit REAL,
                net_profit REAL,
                raw_json TEXT,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                UNIQUE(company_id, period)
            )
            """)

            # 3. Finansal Oranlar Tablosu
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS calculated_ratios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                period TEXT NOT NULL,
                current_ratio REAL,
                acid_test_ratio REAL,
                cash_ratio REAL,
                financial_leverage REAL,
                debt_to_equity REAL,
                equity_ratio REAL,
                net_profit_margin REAL,
                gross_profit_margin REAL,
                operating_profit_margin REAL,
                roa REAL,
                roe REAL,
                asset_turnover REAL,
                inventory_turnover REAL,
                calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                UNIQUE(company_id, period)
            )
            """)

            # 4. Anomali ve Risk Değerlendirme Sonuçları
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS anomaly_evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                period TEXT NOT NULL,
                risk_score REAL NOT NULL,
                risk_level TEXT NOT NULL,
                anomaly_count INTEGER NOT NULL,
                anomalies_json TEXT,
                critical_flags_json TEXT,
                evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id)
            )
            """)

            conn.commit()

    def save_company(self, company: Company) -> int:
        """Şirket ve finansal tablo verilerini veritabanına kaydeder veya günceller."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Şirketi ekle veya id al
            cursor.execute("""
            INSERT INTO companies (code, name, sector)
            VALUES (?, ?, ?)
            ON CONFLICT(code) DO UPDATE SET
                name = excluded.name,
                sector = excluded.sector
            """, (company.code, company.name, company.sector))

            cursor.execute("SELECT id FROM companies WHERE code = ?", (company.code,))
            company_id = cursor.fetchone()["id"]

            bs = company.balance_sheet
            inc = company.income_statement
            raw_data = {
                "bs": bs.__dict__,
                "inc": inc.__dict__
            }

            cursor.execute("""
            INSERT INTO financial_statements (
                company_id, period, total_current_assets, total_non_current_assets,
                total_assets, total_short_term_liabilities, total_long_term_liabilities,
                total_liabilities, total_equity, net_sales, cost_of_sales,
                gross_profit, operating_profit, net_profit, raw_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(company_id, period) DO UPDATE SET
                total_current_assets = excluded.total_current_assets,
                total_assets = excluded.total_assets,
                total_liabilities = excluded.total_liabilities,
                total_equity = excluded.total_equity,
                net_sales = excluded.net_sales,
                net_profit = excluded.net_profit,
                raw_json = excluded.raw_json
            """, (
                company_id, company.period, bs.total_current_assets, bs.total_non_current_assets,
                bs.total_assets, bs.total_short_term_liabilities, bs.total_long_term_liabilities,
                bs.total_liabilities, bs.total_equity, inc.net_sales, inc.cost_of_sales,
                inc.gross_profit, inc.operating_profit, inc.net_profit, json.dumps(raw_data)
            ))

            conn.commit()
            return company_id

    def save_ratios(self, company_code: str, period: str, ratios: Dict[str, Dict[str, Optional[float]]]):
        """Hesaplanan oranları veritabanına kaydeder."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM companies WHERE code = ?", (company_code,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Şirket bulunamadı: {company_code}")
            company_id = row["id"]

            liq = ratios.get("liquidity", {})
            lev = ratios.get("leverage", {})
            prof = ratios.get("profitability", {})
            act = ratios.get("activity", {})

            cursor.execute("""
            INSERT INTO calculated_ratios (
                company_id, period, current_ratio, acid_test_ratio, cash_ratio,
                financial_leverage, debt_to_equity, equity_ratio,
                net_profit_margin, gross_profit_margin, operating_profit_margin,
                roa, roe, asset_turnover, inventory_turnover
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(company_id, period) DO UPDATE SET
                current_ratio = excluded.current_ratio,
                financial_leverage = excluded.financial_leverage,
                net_profit_margin = excluded.net_profit_margin,
                roa = excluded.roa,
                roe = excluded.roe
            """, (
                company_id, period,
                liq.get("current_ratio"), liq.get("acid_test_ratio"), liq.get("cash_ratio"),
                lev.get("financial_leverage"), lev.get("debt_to_equity"), lev.get("equity_ratio"),
                prof.get("net_profit_margin"), prof.get("gross_profit_margin"), prof.get("operating_profit_margin"),
                prof.get("roa"), prof.get("roe"),
                act.get("asset_turnover"), act.get("inventory_turnover")
            ))
            conn.commit()

    def save_anomaly_result(self, company_code: str, period: str, risk_result: Dict[str, Any]):
        """Anomali ve risk değerlendirmesini kaydeder."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM companies WHERE code = ?", (company_code,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Şirket bulunamadı: {company_code}")
            company_id = row["id"]

            cursor.execute("""
            INSERT INTO anomaly_evaluations (
                company_id, period, risk_score, risk_level, anomaly_count,
                anomalies_json, critical_flags_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                company_id, period,
                risk_result.get("risk_score", 0.0),
                risk_result.get("risk_level", "Bilinmiyor"),
                risk_result.get("anomaly_count", 0),
                json.dumps(risk_result.get("anomalies", []), ensure_ascii=False),
                json.dumps(risk_result.get("critical_flags", []), ensure_ascii=False)
            ))
            conn.commit()

    def get_all_companies(self) -> List[Dict[str, Any]]:
        """Kayıtlı tüm şirketleri döndürür."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM companies ORDER BY sector, name")
            return [dict(r) for r in cursor.fetchall()]

    def get_company_summary(self, company_code: str) -> Optional[Dict[str, Any]]:
        """Belirli bir şirketin son finansal durumu, oranları ve anomali geçmişini çeker."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT c.code, c.name, c.sector, fs.period,
                   r.current_ratio, r.financial_leverage, r.net_profit_margin, r.roa, r.roe,
                   a.risk_score, a.risk_level, a.anomaly_count
            FROM companies c
            LEFT JOIN financial_statements fs ON c.id = fs.company_id
            LEFT JOIN calculated_ratios r ON c.id = r.company_id AND fs.period = r.period
            LEFT JOIN anomaly_evaluations a ON c.id = a.company_id AND fs.period = a.period
            WHERE c.code = ?
            ORDER BY a.id DESC LIMIT 1
            """, (company_code,))
            row = cursor.fetchone()
            return dict(row) if row else None
