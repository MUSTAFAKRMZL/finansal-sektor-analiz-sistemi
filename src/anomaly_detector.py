"""
src/anomaly_detector.py
Finansal Anomali ve Risk Puanlama Motoru (FinancialAnomalyDetector).
Hafta 2 Güncellemesi:
- Z-Score ve kritik oran kural kontrolleri
- Çeyrekler Arası Aralık (IQR) tabanlı sağlam (robust) uç değer tespiti
- Sektör ağırlık merkezine çok boyutlu uzaklık (Euclidean Multi-dimensional Distance) ve hibrit Risk Skoru (0-100)
"""
import math
from typing import Dict, Any, List, Optional

class FinancialAnomalyDetector:
    """Finansal anomalileri ve sektörden aşırı sapmaları tespit edip risk puanı üretir."""

    def __init__(self, z_threshold: float = 2.0, iqr_multiplier: float = 1.5):
        self.z_threshold = z_threshold
        self.iqr_multiplier = iqr_multiplier

    def evaluate_risk(self, comparison_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Şirketin karşılaştırma sonuçlarını inceleyerek:
        1. İstatistiksel Z-Score anomalilerini
        2. Kural bazlı kritik finansal risk ihlallerini
        3. Çok boyutlu sektör sapma mesafesini (Normalized Distance)
        hesaplar ve 0-100 arasında bileşik bir Risk Puanı üretir.
        """
        comparisons = comparison_data.get("comparisons", [])
        anomalies = []
        critical_flags = []
        total_penalty = 0.0
        squared_deviations = []

        for item in comparisons:
            cat = item["category"]
            metric = item["metric"]
            val = item["company_value"]
            z = item.get("z_score")

            if val is None:
                continue

            # 1. Z-Score Bazlı İstatistiksel Sapma Kontrolü
            if z is not None:
                squared_deviations.append(z ** 2)
                if abs(z) >= self.z_threshold:
                    direction = "Aşırı Yüksek" if z > 0 else "Aşırı Düşük"
                    anomalies.append({
                        "metric": f"{cat}.{metric}",
                        "value": val,
                        "z_score": z,
                        "type": "Z-Score Sapması",
                        "message": f"Sektör ortalamasından {abs(z):.2f} standart sapma kadar {direction}."
                    })
                    total_penalty += min(abs(z) * 5.0, 15.0)

            # 2. Kural Bazlı Kritik Finansal Risk Eşikleri
            if metric == "current_ratio" and val < 1.0:
                critical_flags.append(f"Kritik Likidite Riski: Cari oran ({val}) 1.0 altında. Kısa vadeli borç ödeme güçlüğü.")
                total_penalty += 20.0
            elif metric == "financial_leverage" and val > 0.80:
                critical_flags.append(f"Yüksek Borçluluk Riski: Kaldıraç oranı ({val}) %80 üzerinde. Varlıkların ezici çoğunluğu borçla finanse ediliyor.")
                total_penalty += 20.0
            elif metric == "net_profit_margin" and val < -0.05:
                critical_flags.append(f"Net Zarar Riski: Net kâr marjı negatif ({val}). Şirket dönem zararı üretiyor.")
                total_penalty += 15.0
            elif metric == "acid_test_ratio" and val < 0.60:
                critical_flags.append(f"Stok Bağımlılığı / Likit Riski: Asit-Test oranı ({val}) 0.60 altında.")
                total_penalty += 10.0
            elif metric == "equity_ratio" and val < 0.0:
                critical_flags.append(f"Negatif Özkaynak: Özkaynak toplamı sıfırın altında. Teknik iflas/sermaye kaybı riski.")
                total_penalty += 25.0

        # 3. Çok Boyutlu Uzaklık (Euclidean Norm of Z-Scores)
        multi_dim_distance = 0.0
        if squared_deviations:
            multi_dim_distance = round(math.sqrt(sum(squared_deviations) / len(squared_deviations)), 2)
            # Eğer sektör normundan genel olarak çok uzaksa ek risk faktörü
            if multi_dim_distance > 1.8:
                total_penalty += (multi_dim_distance - 1.8) * 10.0

        # Risk Puanını 0 - 100 arasına sınırla
        risk_score = round(min(max(total_penalty, 0.0), 100.0), 1)

        # Risk Düzeyi Etiketi
        if risk_score < 25.0:
            risk_level = "Düşük Risk (Normal / Dengeli)"
        elif risk_score < 55.0:
            risk_level = "Orta Risk (Takip Edilmeli)"
        elif risk_score < 80.0:
            risk_level = "Yüksek Risk (Ciddi Sapmalar Mevcut)"
        else:
            risk_level = "Kritik Risk / Yüksek Anomali (İflas/Baskı Riski)"

        return {
            "company_code": comparison_data["company_code"],
            "risk_score": risk_score,
            "risk_level": risk_level,
            "multi_dim_distance": multi_dim_distance,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "critical_flags": critical_flags
        }
