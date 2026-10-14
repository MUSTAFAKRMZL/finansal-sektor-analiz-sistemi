"""
main.py
Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi
Hafta 1 Çekirdek Prototip Çalıştırıcısı.
"""
import os
import json
from src.models import BalanceSheet, IncomeStatement, Company
from src.ratios import FinancialRatioCalculator
from src.sector_analysis import SectorAnalyzer
from src.anomaly_detector import FinancialAnomalyDetector

def load_companies(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    companies = []
    for item in data:
        bs_data = item["balance_sheet"]
        inc_data = item["income_statement"]
        bs = BalanceSheet(**bs_data)
        inc = IncomeStatement(**inc_data)
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

def format_table(headers, rows):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))
    
    header_str = " | ".join(f"{h:<{widths[i]}}" for i, h in enumerate(headers))
    sep_str = "-+-".join("-" * widths[i] for i in range(len(headers)))
    row_strs = [" | ".join(f"{str(val):<{widths[i]}}" for i, val in enumerate(row)) for row in rows]
    return f"{header_str}\n{sep_str}\n" + "\n".join(row_strs)

def main():
    print("=" * 75)
    print("  AKILLI FİNANSAL PERFORMANS VE SEKTÖREL ANOMALİ ANALİZ SİSTEMİ  ")
    print("  Yazılım Geliştirme I - Hafta 1 Çekirdek Prototip  ")
    print("=" * 75)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "sample_companies.json")

    print(f"\n[1] Veri seti yükleniyor: {data_path}")
    companies = load_companies(data_path)
    print(f" -> {len(companies)} şirket başarıyla yüklendi.")

    # 1. Sektör Analizini Başlat
    analyzer = SectorAnalyzer(companies)

    # 2. Her bir şirket için karşılaştırma ve risk analizi yap
    detector = FinancialAnomalyDetector(z_threshold=1.5)

    for comp in companies:
        print("\n" + "#" * 75)
        print(f" ŞİRKET: {comp.name} [{comp.code}]")
        print(f" SEKTÖR: {comp.sector} | DÖNEM: {comp.period}")
        print("#" * 75)

        # Karşılaştırma Raporu
        comp_report = analyzer.compare_company_with_sector(comp.code)
        risk_report = detector.evaluate_risk(comp_report)

        headers = ["Kategori", "Finansal Gösterge", "Şirket Değeri", "Sektör Ort.", "Fark (%)", "Z-Skor"]
        rows = []
        for c in comp_report["comparisons"]:
            metric_label = c["metric"].replace("_", " ").title()
            val = f"{c['company_value']:.4f}" if c["company_value"] is not None else "N/A"
            mean = f"{c['sector_mean']:.4f}" if c["sector_mean"] is not None else "N/A"
            diff = f"{c['diff_percentage']:+.1f}%" if c["diff_percentage"] is not None else "N/A"
            z = f"{c['z_score']:+.2f}" if c["z_score"] is not None else "-"
            rows.append([c["category"].upper(), metric_label, val, mean, diff, z])

        print(format_table(headers, rows))

        print("\n--- ANOMALİ VE RİSK DEĞERLENDİRMESİ ---")
        print(f"Bileşik Risk Puanı: {risk_report['risk_score']} / 100")
        print(f"Risk Durumu:        {risk_report['risk_level']}")
        
        if risk_report["anomalies"]:
            print(f"Tespit Edilen İstatistiksel Anomaliler ({risk_report['anomaly_count']} Adet):")
            for a in risk_report["anomalies"]:
                print(f"  * {a['metric']}: {a['message']} (Değer: {a['value']}, Z: {a['z_score']})")

        if risk_report["critical_flags"]:
            print("Kritik Finansal Uyarılar:")
            for flag in risk_report["critical_flags"]:
                print(f"  ! {flag}")

    print("\n" + "=" * 75)
    print(" Analiz Başarıyla Tamamlandı.")
    print("=" * 75)

if __name__ == "__main__":
    main()
