"""
src/api_server.py
Hafta 5 (v0.5.0): Canlı Web Sunucusu ve REST API Katmanı.
SQLite veritabanından beslenen sıfır dış bağımlılıklı ThreadingHTTPServer tabanlı REST API.
Dashboard ön yüzünün sunucuyla canlı haberleşmesini, şirket detaylarının sorgulanmasını
ve tarayıcıdan gelen simülasyon verilerinin Python analiz motorlarında gerçek zamanlı
hesaplanmasını sağlar.
"""
import os
import json
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from typing import Dict, Any, Optional, List

from src.models import BalanceSheet, IncomeStatement, Company
from src.database import DatabaseManager
from src.ratios import FinancialRatioCalculator
from src.sector_analysis import SectorAnalyzer
from src.anomaly_detector import FinancialAnomalyDetector
from src.ml_anomaly import HybridAnomalyEngine
from src.trend_analysis import TrendAnalyzer
from src.executive_commentary import FinancialCommentaryEngine


class FinancialAnalysisService:
    """Veritabanından tüm analiz pipeline'ını çalıştıran ve API uçlarına veri sağlayan servis katmanı."""

    VERSION = "0.5.0"

    def __init__(self, db_path: str = "financial_analysis.db"):
        self.db_path = db_path
        self.db = DatabaseManager(db_path)
        self.all_companies: List[Company] = []
        self.latest_period: str = ""
        self.latest_companies: List[Company] = []
        self.analyzer: Optional[SectorAnalyzer] = None
        self.detector = FinancialAnomalyDetector(z_threshold=1.5)
        self.comparisons: Dict[str, Any] = {}
        self.base_risks: Dict[str, Any] = {}
        self.hybrid_reports: Dict[str, Any] = {}
        self.trend_reports: Dict[str, Any] = {}
        self.commentaries: Dict[str, Any] = {}
        self.refresh()

    def refresh(self):
        """Veritabanındaki güncel verilerden tüm analizleri yeniden hesaplar."""
        self.all_companies = self.db.load_companies_from_db()
        if not self.all_companies:
            self.latest_period = ""
            self.latest_companies = []
            self.analyzer = None
            self.comparisons = {}
            self.base_risks = {}
            self.hybrid_reports = {}
            self.trend_reports = {}
            self.commentaries = {}
            return

        self.latest_period = max(c.period for c in self.all_companies)
        self.latest_companies = [c for c in self.all_companies if c.period == self.latest_period]

        self.analyzer = SectorAnalyzer(self.latest_companies)
        self.comparisons = {}
        self.base_risks = {}
        for comp in self.latest_companies:
            comp_rep = self.analyzer.compare_company_with_sector(comp.code)
            self.comparisons[comp.code] = comp_rep
            self.base_risks[comp.code] = self.detector.evaluate_risk(comp_rep)

        ml_engine = HybridAnomalyEngine()
        self.hybrid_reports = ml_engine.analyze_all_companies(
            companies=self.latest_companies,
            company_ratios=self.analyzer.company_ratios,
            base_risk_reports=self.base_risks
        )

        self.trend_reports = TrendAnalyzer(self.all_companies).analyze_all()
        self.commentaries = FinancialCommentaryEngine.generate_all(
            companies=self.latest_companies,
            company_comparisons=self.comparisons,
            hybrid_reports=self.hybrid_reports,
            trend_reports=self.trend_reports,
            company_ratios=self.analyzer.company_ratios
        )

    def get_health_payload(self) -> Dict[str, Any]:
        sectors = list(self.analyzer.sector_benchmarks.keys()) if self.analyzer else []
        return {
            "status": "ok",
            "version": self.VERSION,
            "service": "Finansal Sektör Analiz Sistemi REST API",
            "latest_period": self.latest_period,
            "total_companies": len(self.latest_companies),
            "total_period_records": len(self.all_companies),
            "sectors": sorted(sectors)
        }

    def get_dashboard_payload(self) -> Dict[str, Any]:
        return {
            "companies": [
                {
                    "code": c.code,
                    "name": c.name,
                    "sector": c.sector,
                    "period": c.period,
                    "total_assets": c.balance_sheet.total_assets,
                    "total_liabilities": c.balance_sheet.total_liabilities,
                    "total_equity": c.balance_sheet.total_equity,
                    "net_sales": c.income_statement.net_sales,
                    "net_profit": c.income_statement.net_profit
                }
                for c in self.latest_companies
            ],
            "sector_benchmarks": self.analyzer.sector_benchmarks if self.analyzer else {},
            "comparisons": self.comparisons,
            "hybrid_reports": self.hybrid_reports,
            "trend_reports": self.trend_reports,
            "commentaries": self.commentaries
        }

    def get_companies_summary(self) -> List[Dict[str, Any]]:
        items = []
        for comp in self.latest_companies:
            code = comp.code
            h_rep = self.hybrid_reports.get(code, {})
            t_rep = self.trend_reports.get(code, {})
            ratios = self.analyzer.company_ratios.get(code, {}) if self.analyzer else {}
            items.append({
                "code": code,
                "name": comp.name,
                "sector": comp.sector,
                "period": comp.period,
                "current_ratio": ratios.get("liquidity", {}).get("current_ratio"),
                "financial_leverage": ratios.get("leverage", {}).get("financial_leverage"),
                "net_profit_margin": ratios.get("profitability", {}).get("net_profit_margin"),
                "roe": ratios.get("profitability", {}).get("roe"),
                "hybrid_risk_score": h_rep.get("hybrid_risk_score", 0.0),
                "hybrid_risk_level": h_rep.get("hybrid_risk_level", "Bilinmiyor"),
                "altman_z": t_rep.get("latest_altman"),
                "trend_score": t_rep.get("trend_score")
            })
        return items

    def get_company_detail(self, company_code: str) -> Optional[Dict[str, Any]]:
        comp = next((c for c in self.latest_companies if c.code == company_code), None)
        if not comp:
            return None
        return {
            "company": {
                "code": comp.code,
                "name": comp.name,
                "sector": comp.sector,
                "period": comp.period,
                "balance_sheet": comp.balance_sheet.__dict__,
                "income_statement": comp.income_statement.__dict__
            },
            "ratios": self.analyzer.company_ratios.get(company_code, {}) if self.analyzer else {},
            "comparison": self.comparisons.get(company_code, {}),
            "hybrid_report": self.hybrid_reports.get(company_code, {}),
            "trend_report": self.trend_reports.get(company_code, {}),
            "commentary": self.commentaries.get(company_code, {})
        }

    def get_sectors_payload(self) -> Dict[str, Any]:
        return self.analyzer.sector_benchmarks if self.analyzer else {}

    def analyze_simulation_payload(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Kullanıcının gönderdiği ham simülasyon bilançosunu gerçek Python motorlarıyla analiz eder."""
        required = [
            "sector", "current_assets", "inventories", "cash",
            "total_assets", "short_term_debt", "total_debt",
            "equity", "net_sales", "net_profit"
        ]
        for field in required:
            if field not in data:
                raise ValueError(f"Eksik simülasyon alanı: {field}")

        name = str(data.get("name") or "Simülasyon A.Ş.")
        sector = str(data["sector"])
        cur_assets = float(data["current_assets"])
        inventories = float(data["inventories"])
        cash = float(data["cash"])
        total_assets = float(data["total_assets"])
        short_debt = float(data["short_term_debt"])
        total_debt = float(data["total_debt"])
        equity = float(data["equity"])
        net_sales = float(data["net_sales"])
        net_profit = float(data["net_profit"])

        if total_assets <= 0:
            raise ValueError("Toplam varlıklar (Aktif) sıfırdan büyük olmalıdır.")

        # BalanceSheet & IncomeStatement kalemlerini mantıksal olarak türet
        other_cur = max(0.0, cur_assets - cash - inventories)
        non_cur = max(0.0, total_assets - cur_assets)
        long_debt = max(0.0, total_debt - short_debt)

        bs = BalanceSheet(
            cash_and_equivalents=cash,
            accounts_receivable=other_cur * 0.6,
            inventories=inventories,
            other_current_assets=other_cur * 0.4,
            tangible_assets=non_cur * 0.8,
            intangible_assets=non_cur * 0.2,
            other_non_current_assets=0.0,
            short_term_financial_debt=short_debt * 0.5,
            short_term_trade_payables=short_debt * 0.5,
            other_short_term_debt=0.0,
            long_term_financial_debt=long_debt,
            other_long_term_debt=0.0,
            paid_in_capital=equity * 0.6,
            retained_earnings=equity * 0.4,
            net_period_profit_bs=0.0
        )
        # EBIT/Faaliyet kârı tahmini (vergi + faiz öncesi)
        est_cost = max(0.0, net_sales - net_profit) * 0.75
        est_opex = max(0.0, net_sales - net_profit) * 0.15
        inc = IncomeStatement(
            net_sales=net_sales,
            cost_of_sales=est_cost,
            operating_expenses=est_opex,
            financial_expenses=0.0,
            tax_expenses=0.0,
            net_profit=net_profit
        )
        temp_comp = Company(
            code="SIM_TMP",
            name=name,
            sector=sector,
            period=self.latest_period or "2025/12",
            balance_sheet=bs,
            income_statement=inc
        )

        ratios = FinancialRatioCalculator.calculate_all(temp_comp)
        altman = TrendAnalyzer.calculate_altman_z_score(temp_comp)

        benchmarks = (self.analyzer.sector_benchmarks.get(sector, {}) if self.analyzer else {})
        comp_results = []
        for cat, cat_dict in ratios.items():
            for metric, val in cat_dict.items():
                full_name = f"{cat}.{metric}"
                b = benchmarks.get(full_name, {})
                s_mean = b.get("mean")
                s_std = b.get("std_dev", 0.0)
                z_score = None
                diff_pct = None
                if val is not None and s_mean is not None:
                    if s_std and s_std > 0:
                        z_score = round((val - s_mean) / s_std, 2)
                    if s_mean != 0:
                        diff_pct = round(((val - s_mean) / abs(s_mean)) * 100, 2)
                comp_results.append({
                    "category": cat,
                    "metric": metric,
                    "company_value": val,
                    "sector_mean": s_mean,
                    "sector_median": b.get("median"),
                    "diff_percentage": diff_pct,
                    "z_score": z_score
                })

        comparison = {
            "company_code": temp_comp.code,
            "company_name": temp_comp.name,
            "sector": sector,
            "comparisons": comp_results
        }
        risk_rep = self.detector.evaluate_risk(comparison)
        hybrid_sim = {
            "hybrid_risk_score": risk_rep["risk_score"],
            "hybrid_risk_level": risk_rep["risk_level"],
            "critical_flags": risk_rep["critical_flags"],
            "anomalies": risk_rep["anomalies"]
        }
        commentary = FinancialCommentaryEngine.generate_company_commentary(
            company_code=temp_comp.code,
            company_name=name,
            sector=sector,
            ratios=ratios,
            comparison=comparison,
            hybrid_report=hybrid_sim,
            trend_data={
                "cagr_sales": None,
                "trend_score": 50.0,
                "trend_direction": "Simülasyon Anlık Görünüm",
                "latest_altman": altman["z_score"],
                "latest_altman_zone": altman["zone"],
                "altman_trajectory": "Yatay"
            }
        )

        return {
            "name": name,
            "sector": sector,
            "ratios": ratios,
            "altman": altman,
            "risk_report": risk_rep,
            "commentary": commentary,
            "sector_benchmarks": {
                "current_ratio_mean": benchmarks.get("liquidity.current_ratio", {}).get("mean"),
                "financial_leverage_mean": benchmarks.get("leverage.financial_leverage", {}).get("mean"),
                "net_profit_margin_mean": benchmarks.get("profitability.net_profit_margin", {}).get("mean")
            }
        }


class FinancialAPIHandler(SimpleHTTPRequestHandler):
    """REST API uçlarını ve güvenli statik dashboard dosyalarını sunan HTTP istek işleyicisi."""

    service: FinancialAnalysisService = None
    static_dir: str = "."

    def translate_path(self, path: str) -> str:
        # Statik dosya sunumunu yalnızca static_dir ile sınırla
        clean_path = urllib.parse.urlparse(path).path.lstrip("/")
        if not clean_path or clean_path == "":
            clean_path = "dashboard.html"
        safe_path = os.path.normpath(os.path.join(self.static_dir, clean_path))
        if not safe_path.startswith(os.path.abspath(self.static_dir)):
            return os.path.join(self.static_dir, "dashboard.html")
        return safe_path

    def _send_json(self, status_code: int, payload: Any):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args):
        # Test ve konsol çıktısını temiz tut
        pass

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            return self._send_json(200, self.service.get_health_payload())

        if path == "/api/dashboard-data":
            return self._send_json(200, self.service.get_dashboard_payload())

        if path == "/api/companies":
            return self._send_json(200, {"companies": self.service.get_companies_summary()})

        if path.startswith("/api/companies/"):
            code = urllib.parse.unquote(path[len("/api/companies/"):]).strip("/")
            if not code:
                return self._send_json(400, {"error": "Şirket kodu belirtilmelidir."})
            detail = self.service.get_company_detail(code)
            if not detail:
                return self._send_json(404, {"error": f"Şirket bulunamadı: {code}"})
            return self._send_json(200, detail)

        if path == "/api/sectors":
            return self._send_json(200, {"sectors": self.service.get_sectors_payload()})

        if path.startswith("/api/"):
            return self._send_json(404, {"error": f"Bilinmeyen API uç noktası: {path}"})

        # Yalnızca izin verilen statik web dosyalarını sun (.html, .css, .js, .svg)
        if path in ("/", "/dashboard.html"):
            return super().do_GET()

        ext = os.path.splitext(path)[1].lower()
        if ext in (".html", ".css", ".js", ".svg", ".png", ".ico"):
            return super().do_GET()

        return self._send_json(403, {"error": "Bu kaynağa doğrudan erişim izni yok."})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/analyze":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length <= 0:
                    return self._send_json(400, {"error": "Boş istek gövdesi."})
                raw_body = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(raw_body)
                result = self.service.analyze_simulation_payload(data)
                return self._send_json(200, result)
            except ValueError as ve:
                return self._send_json(400, {"error": str(ve)})
            except json.JSONDecodeError:
                return self._send_json(400, {"error": "Geçersiz JSON formatı."})
            except Exception as exc:
                return self._send_json(500, {"error": f"Sunucu hatası: {exc}"})

        return self._send_json(404, {"error": f"Bilinmeyen POST uç noktası: {path}"})


def create_api_server(
    host: str = "127.0.0.1",
    port: int = 8080,
    db_path: str = "financial_analysis.db",
    static_dir: str = "."
) -> ThreadingHTTPServer:
    """Yapılandırılmış ThreadingHTTPServer örneği oluşturur."""
    service = FinancialAnalysisService(db_path=db_path)

    class ConfiguredHandler(FinancialAPIHandler):
        pass

    ConfiguredHandler.service = service
    ConfiguredHandler.static_dir = os.path.abspath(static_dir)

    return ThreadingHTTPServer((host, port), ConfiguredHandler)
