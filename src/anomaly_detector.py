"""
src/anomaly_detector.py
Finansal Anomali ve Risk Puanlama Motoru (FinancialAnomalyDetector).
Şirketin oranlarındaki aşırı sapmaları (Z-Score) ve kritik eşik ihlallerini tespit eder.
"""
from typing import Dict, Any, List

class FinancialAnomalyDetector:
    """Finansal anomalileri ve sektörden aşırı sapmaları tespit edip risk puanı üretir."""

    def __init__(self, z_threshold: float = 2.0):
        # |Z| > 2.0 olması istatistiksel olarak %95 güven aralığının dışındaki sapmaları gösterir
        self.z_threshold = z_threshold

    def evaluate_risk(self, comparison_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Şirketin karşılaştırma sonuçlarını inceleyerek:
        1. Anomali tespit edilen göstergeleri listeler
        2. 0-100 arasında bir bileşik Risk / Anomali Puanı üretir
        3. Risk seviyesini sınıflandırır (Düşük, Orta, Yüksek Risk)
        """
        comparisons = comparison_data.get("comparisons", [])
        anomalies = []
        critical_flags = []
        total_penalty = 0.0

        for item in comparisons:
            cat = item["category"]
            metric = item["metric"]
            val = item["company_value"]
            z = item["z_score"]

            if val is None:
                continue

            # 1. Z-Score Bazlı İstatistiksel Sapma Kontrolü
            if z is not None and abs(z) >= self.z_threshold:
                direction = "Aşırı Yüksek" if z > 0 else "Aşırı Düşük"
                anomalies.append({
                    "metric": f"{cat}.{metric}",
                    "value": val,
                    "z_score": z,
                    "message": f"Sektör ortalamasından {abs(z)} standart sapma kadar {direction}."
                })
                # Her Z-Score anomalisi için ceza puanı (maks 15 puan)
                total_penalty += min(abs(z) * 5.0, 15.0)

            # 2. Kural Bazlı Kritik Finansal Risk Eşikleri
            if metric == "current_ratio" and val < 1.0:
                critical_flags.append(f"Kritik Likidite Riski: Cari oran ({val}) 1.0'ın altında. Kısa vadeli borç ödeme güçlüğü.")
                total_penalty += 20.0
            elif metric == "financial_leverage" and val > 0.80:
                critical_flags.append(f"Yüksek Borçluluk Riski: Kaldıraç oranı ({val}) %80 üzerinde. Varlıkların ezici çoğunluğu borçla finanse ediliyor.")
                total_penalty += 20.0
            elif metric == "net_profit_margin" and val < -0.05:
                critical_flags.append(f"Net Zarar Riski: Net kâr marjı negatif ({val}). Şirket dönem zararı üretiyor.")
                total_penalty += 15.0
            elif metric == "acid_test_ratio" and val < 0.60:
                critical_flags.append(f"Stok Bağımlılığı / Likit Riski: Asit-Test oranı ({val}) 0.60'ın altında.")
                total_penalty += 10.0

        # Risk Puanını 0 - 100 arasına sınırla
        risk_score = round(min(max(total_penalty, 0.0), 100.0), 1)

        # Risk Düzeyi Etiketi
        if risk_score < 25.0:
            risk_level = "Düşük Risk (Normal / Dengeli)"
        elif risk_score < 55.0:
            risk_level = "Orta Risk (Takip Edilmeli)"
        else:
            risk_level = "Yüksek Risk / Kritik Anomali"

        return {
            "company_code": comparison_data["company_code"],
            "risk_score": risk_score,
            "risk_level": risk_level,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "critical_flags": critical_flags
        }
