"""
src/sector_analysis.py
Sektör Ortalamaları ve Kıyaslama Modülü (SectorAnalyzer).
Şirket oranlarını sektör genelindeki diğer şirketlerle karşılaştırır.
"""
import math
from typing import List, Dict, Any, Optional
from collections import defaultdict
from src.models import Company
from src.ratios import FinancialRatioCalculator

class SectorAnalyzer:
    """Sektör bazlı istatistikleri (ortalama, medyan, standart sapma) hesaplar ve şirketleri kıyaslar."""

    def __init__(self, companies: List[Company]):
        self.companies = companies
        self.company_ratios: Dict[str, Dict[str, Dict[str, Optional[float]]]] = {}
        self.sector_companies: Dict[str, List[Company]] = defaultdict(list)
        self.sector_benchmarks: Dict[str, Dict[str, Dict[str, float]]] = {}
        
        self._process_all()

    def _process_all(self):
        # 1. Her şirketin oranlarını hesapla ve sektöre göre grupla
        for comp in self.companies:
            ratios = FinancialRatioCalculator.calculate_all(comp)
            self.company_ratios[comp.code] = ratios
            self.sector_companies[comp.sector].append(comp)

        # 2. Sektör ortalamaları, medyan ve standart sapmaları hesapla
        for sector, comps in self.sector_companies.items():
            self.sector_benchmarks[sector] = self._calculate_sector_metrics(sector)

    def _calculate_sector_metrics(self, sector: str) -> Dict[str, Dict[str, float]]:
        comps = self.sector_companies[sector]
        metrics: Dict[str, List[float]] = defaultdict(list)

        for comp in comps:
            ratios = self.company_ratios[comp.code]
            for cat, cat_dict in ratios.items():
                for metric, val in cat_dict.items():
                    if val is not None and not math.isnan(val):
                        metrics[f"{cat}.{metric}"].append(val)

        benchmarks: Dict[str, Dict[str, float]] = {}
        for metric_name, vals in metrics.items():
            if not vals:
                continue
            n = len(vals)
            avg = sum(vals) / n
            sorted_vals = sorted(vals)
            median = sorted_vals[n // 2] if n % 2 != 0 else (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2.0
            variance = sum((x - avg) ** 2 for x in vals) / n if n > 1 else 0.0
            std_dev = math.sqrt(variance)

            benchmarks[metric_name] = {
                "mean": round(avg, 4),
                "median": round(median, 4),
                "std_dev": round(std_dev, 4),
                "min": round(min(vals), 4),
                "max": round(max(vals), 4),
                "count": n
            }
        return benchmarks

    def compare_company_with_sector(self, company_code: str) -> Dict[str, Any]:
        """Belirli bir şirketin oranlarını kendi sektörünün ortalamalarıyla karşılaştırır."""
        comp = next((c for c in self.companies if c.code == company_code), None)
        if not comp:
            raise ValueError(f"Şirket kodu bulunamadı: {company_code}")

        sector = comp.sector
        benchmarks = self.sector_benchmarks.get(sector, {})
        ratios = self.company_ratios[company_code]

        comparison_results = []
        for cat, cat_dict in ratios.items():
            for metric, val in cat_dict.items():
                full_name = f"{cat}.{metric}"
                benchmark = benchmarks.get(full_name, {})
                sector_mean = benchmark.get("mean")
                sector_std = benchmark.get("std_dev", 0.0)

                z_score = None
                diff_pct = None
                if val is not None and sector_mean is not None:
                    if sector_std and sector_std > 0:
                        z_score = round((val - sector_mean) / sector_std, 2)
                    if sector_mean != 0:
                        diff_pct = round(((val - sector_mean) / abs(sector_mean)) * 100, 2)

                comparison_results.append({
                    "category": cat,
                    "metric": metric,
                    "company_value": val,
                    "sector_mean": sector_mean,
                    "sector_median": benchmark.get("median"),
                    "sector_std_dev": sector_std,
                    "diff_percentage": diff_pct,
                    "z_score": z_score
                })

        return {
            "company_code": comp.code,
            "company_name": comp.name,
            "sector": sector,
            "comparisons": comparison_results
        }
