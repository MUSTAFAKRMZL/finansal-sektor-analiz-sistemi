"""
src/trend_analysis.py
Çok Dönemli Tarihsel Zaman Serisi ve Trend Analizi Modülü (TrendAnalyzer).
Şirketlerin 3 yıllık (2023-2025) mali tablolarını inceleyerek;
- Dönemsel büyüme oranları (YoY) ve CAGR (Bileşik Yıllık Büyüme Oranı),
- Finansal rasyo değişim dinamikleri (Cari oran, borçluluk, kârlılık yönü),
- Altman Z-Score iflas riski modeli ve gidişat trendini hesaplar.
"""
import math
from typing import List, Dict, Any, Optional
from collections import defaultdict
from src.models import Company
from src.ratios import FinancialRatioCalculator, safe_divide

class TrendAnalyzer:
    """Şirketlerin çok dönemli finansal performans ve trend analizini gerçekleştiren sınıf."""

    def __init__(self, companies: List[Company]):
        self.companies = companies
        self.company_history: Dict[str, List[Company]] = defaultdict(list)
        self._group_and_sort()

    def _group_and_sort(self):
        """Şirketleri kodlarına göre gruplar ve dönem sırasına (kronolojik) dizer."""
        for comp in self.companies:
            self.company_history[comp.code].append(comp)
        
        for code in self.company_history:
            self.company_history[code].sort(key=lambda c: c.period)

    @staticmethod
    def calculate_cagr(start_val: float, end_val: float, years: int) -> Optional[float]:
        """Bileşik Yıllık Büyüme Oranını (CAGR) hesaplar."""
        if start_val <= 0 or end_val <= 0 or years <= 0:
            return None
        return round(((end_val / start_val) ** (1.0 / years) - 1.0) * 100.0, 2)

    @staticmethod
    def calculate_altman_z_score(company: Company) -> Dict[str, Any]:
        """
        Klasik Altman Z-Score İflas Riski Modelini hesaplar:
        Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 0.999*X5
        X1 = Net Çalışma Sermayesi / Toplam Varlıklar
        X2 = Dağıtılmamış Kârlar / Toplam Varlıklar
        X3 = Faaliyet Kârı (EBIT) / Toplam Varlıklar
        X4 = Özkaynaklar / Toplam Borçlar
        X5 = Net Satışlar / Toplam Varlıklar
        """
        bs = company.balance_sheet
        inc = company.income_statement

        total_assets = bs.total_assets
        if total_assets <= 0:
            return {"z_score": 0.0, "zone": "Distress Zone (İflas Riski)", "code": "DISTRESS"}

        # X1: Net Working Capital / Total Assets
        nwc = bs.total_current_assets - bs.total_short_term_liabilities
        x1 = nwc / total_assets

        # X2: Retained Earnings / Total Assets
        x2 = bs.retained_earnings / total_assets

        # X3: EBIT (Faaliyet Kârı) / Total Assets
        x3 = inc.operating_profit / total_assets

        # X4: Equity / Total Liabilities
        x4 = safe_divide(bs.total_equity, bs.total_liabilities, default=0.0)

        # X5: Net Sales / Total Assets
        x5 = inc.net_sales / total_assets

        z = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 0.999 * x5
        z = round(z, 3)

        if z >= 2.99:
            zone = "Güvenli Bölge (Safe Zone)"
            status = "SAFE"
        elif z >= 1.81:
            zone = "Gri Bölge (Gray Zone - Dikkat)"
            status = "GRAY"
        else:
            zone = "Finansal Sıkıntı / İflas Riski (Distress Zone)"
            status = "DISTRESS"

        return {
            "z_score": z,
            "zone": zone,
            "status": status,
            "components": {
                "x1_nwc_ta": round(x1, 4),
                "x2_re_ta": round(x2, 4),
                "x3_ebit_ta": round(x3, 4),
                "x4_eq_liab": round(x4, 4),
                "x5_sales_ta": round(x5, 4)
            }
        }

    def analyze_company_trend(self, company_code: str) -> Dict[str, Any]:
        """Tek bir şirketin tüm dönemler boyunca tarihsel gelişimini analiz eder."""
        history = self.company_history.get(company_code, [])
        if not history:
            raise ValueError(f"Şirket bulunamadı: {company_code}")

        periods_data = []
        for comp in history:
            ratios = FinancialRatioCalculator.calculate_all(comp)
            z_data = self.calculate_altman_z_score(comp)
            
            p_dict = {
                "period": comp.period,
                "net_sales": comp.income_statement.net_sales,
                "net_profit": comp.income_statement.net_profit,
                "operating_profit": comp.income_statement.operating_profit,
                "total_assets": comp.balance_sheet.total_assets,
                "total_equity": comp.balance_sheet.total_equity,
                "total_liabilities": comp.balance_sheet.total_liabilities,
                "current_ratio": ratios["liquidity"]["current_ratio"],
                "financial_leverage": ratios["leverage"]["financial_leverage"],
                "net_profit_margin": ratios["profitability"]["net_profit_margin"],
                "roe": ratios["profitability"]["roe"],
                "altman_z": z_data["z_score"],
                "altman_zone": z_data["zone"],
                "altman_status": z_data["status"]
            }
            periods_data.append(p_dict)

        # YoY (Yıllık Değişim) Hesaplamaları
        yoy_changes = []
        for i in range(1, len(periods_data)):
            prev = periods_data[i - 1]
            curr = periods_data[i]

            def pct_change(c_val, p_val):
                if p_val and p_val != 0:
                    return round(((c_val - p_val) / abs(p_val)) * 100.0, 2)
                return None

            change = {
                "period_from": prev["period"],
                "period_to": curr["period"],
                "sales_growth": pct_change(curr["net_sales"], prev["net_sales"]),
                "profit_growth": pct_change(curr["net_profit"], prev["net_profit"]),
                "assets_growth": pct_change(curr["total_assets"], prev["total_assets"]),
                "equity_growth": pct_change(curr["total_equity"], prev["total_equity"]),
                "current_ratio_diff": round((curr["current_ratio"] or 0) - (prev["current_ratio"] or 0), 3),
                "leverage_diff": round((curr["financial_leverage"] or 0) - (prev["financial_leverage"] or 0), 3),
                "altman_z_diff": round(curr["altman_z"] - prev["altman_z"], 3)
            }
            yoy_changes.append(change)

        # 3 Yıllık Kümülatif Metrikler ve CAGR
        first = periods_data[0]
        last = periods_data[-1]
        years_span = max(1, len(periods_data) - 1)

        cagr_sales = self.calculate_cagr(first["net_sales"], last["net_sales"], years_span)
        cagr_assets = self.calculate_cagr(first["total_assets"], last["total_assets"], years_span)

        # Trend Yönü ve Sağlık Puanı Tespiti
        # Puanlama faktörleri: Satış büyümesi, kâr istikrarı, Altman Z değişimi, kaldıraç kontrolü
        trend_score = 50.0  # Nötr başlangıç

        # 1. Satış Büyümesi Etkisi
        if cagr_sales is not None:
            if cagr_sales > 20:
                trend_score += 15
            elif cagr_sales > 10:
                trend_score += 8
            elif cagr_sales < 0:
                trend_score -= 15

        # 2. Kârlılık Eğilimi
        if last["net_profit"] > first["net_profit"] and last["net_profit"] > 0:
            trend_score += 15
        elif last["net_profit"] < 0:
            trend_score -= 25

        # 3. Altman Z-Score Gidişatı
        z_diff = last["altman_z"] - first["altman_z"]
        if last["altman_status"] == "SAFE":
            trend_score += 15
        elif last["altman_status"] == "DISTRESS":
            trend_score -= 20

        if z_diff > 0.3:
            trend_score += 10
        elif z_diff < -0.3:
            trend_score -= 15

        # 4. Borçluluk Dinamiği
        lev_diff = (last["financial_leverage"] or 0) - (first["financial_leverage"] or 0)
        if lev_diff > 0.15:
            trend_score -= 10
        elif lev_diff < -0.05:
            trend_score += 5

        trend_score = max(0.0, min(100.0, round(trend_score, 1)))

        if trend_score >= 70:
            direction = "Güçlü İyileşme / Büyüme Trendi"
            badge = "POSITIVE"
        elif trend_score >= 45:
            direction = "Dengeli / İstikrarlı Seyir"
            badge = "STABLE"
        else:
            direction = "Bozulma / Yüksek Finansal Risk Eğilimi"
            badge = "NEGATIVE"

        return {
            "company_code": company_code,
            "company_name": history[-1].name,
            "sector": history[-1].sector,
            "period_count": len(history),
            "periods": periods_data,
            "yoy_changes": yoy_changes,
            "cagr_sales": cagr_sales,
            "cagr_assets": cagr_assets,
            "trend_score": trend_score,
            "trend_direction": direction,
            "trend_badge": badge,
            "latest_altman": last["altman_z"],
            "latest_altman_zone": last["altman_zone"],
            "altman_trajectory": "Yükseliyor" if z_diff > 0.1 else ("Düşüyor" if z_diff < -0.1 else "Yatay")
        }

    def analyze_all(self) -> Dict[str, Dict[str, Any]]:
        """Sistemdeki tüm şirketlerin trend analizini toplu olarak çalıştırır."""
        results = {}
        for code in self.company_history:
            results[code] = self.analyze_company_trend(code)
        return results
