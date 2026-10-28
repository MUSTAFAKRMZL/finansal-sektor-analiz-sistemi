"""
main.py
Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi
Hafta 3 (v0.3.0): Veri Normalizasyonu, Isolation Forest Makine Öğrenmesi Anomali Motoru
ve İnteraktif Web Görsel Analiz Ekranı (dashboard.html).
"""
import os
import sys
from src.data_loader import FinancialDataLoader
from src.ratios import FinancialRatioCalculator
from src.sector_analysis import SectorAnalyzer
from src.anomaly_detector import FinancialAnomalyDetector
from src.ml_anomaly import HybridAnomalyEngine
from src.database import DatabaseManager
from src.web_dashboard import DashboardGenerator

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
    print("=" * 88)
    print("  AKILLI FİNANSAL PERFORMANS VE SEKTÖREL ANOMALİ ANALİZ SİSTEMİ (v0.3.0)  ")
    print("  Yazılım Geliştirme I - Hafta 3: Hibrit ML (Isolation Forest) & Web Dashboard  ")
    print("=" * 88)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "data", "companies_financials.csv")
    db_path = os.path.join(base_dir, "financial_analysis.db")
    dashboard_path = os.path.join(base_dir, "dashboard.html")

    print(f"\n[1] Veritabanı başlatılıyor: {db_path}")
    db = DatabaseManager(db_path)

    print(f"[2] CSV dosyasından şirket finansalları okunuyor: {csv_path}")
    companies = FinancialDataLoader.load_from_csv(csv_path)
    print(f" -> {len(companies)} şirket başarıyla okundu ve doğrulandı.")

    print("[3] Şirket verileri SQLite veritabanına kaydediliyor...")
    for comp in companies:
        db.save_company(comp)

    # 4. Sektör ve İstatistiksel Analiz
    analyzer = SectorAnalyzer(companies)
    detector = FinancialAnomalyDetector(z_threshold=1.5)

    company_comparisons = {}
    base_risk_reports = {}
    for comp in companies:
        ratios = analyzer.company_ratios[comp.code]
        db.save_ratios(comp.code, comp.period, ratios)

        comp_report = analyzer.compare_company_with_sector(comp.code)
        risk_report = detector.evaluate_risk(comp_report)
        company_comparisons[comp.code] = comp_report
        base_risk_reports[comp.code] = risk_report

    # 5. Hafta 3: Veri Normalizasyonu ve Makine Öğrenmesi (Isolation Forest + k-NN) Hibrit Motoru
    print("[4] Min-Max Veri Normalizasyonu ve Isolation Forest (ML) modeli eğitiliyor...")
    ml_engine = HybridAnomalyEngine()
    hybrid_reports = ml_engine.analyze_all_companies(
        companies=companies,
        company_ratios=analyzer.company_ratios,
        base_risk_reports=base_risk_reports
    )

    for comp in companies:
        h_rep = hybrid_reports[comp.code]
        # Veritabanına hibrit risk skorunu kaydet
        db_record = dict(h_rep)
        db_record["risk_score"] = h_rep["hybrid_risk_score"]
        db_record["risk_level"] = h_rep["hybrid_risk_level"]
        db.save_anomaly_result(comp.code, comp.period, db_record)

    # 6. İnteraktif Görsel Analiz Ekranı (HTML5 + SVG Radar & Bar Charts) Üretimi
    out_html = DashboardGenerator.export_dashboard(
        companies=companies,
        sector_benchmarks=analyzer.sector_benchmarks,
        company_comparisons=company_comparisons,
        hybrid_reports=hybrid_reports,
        output_path=dashboard_path
    )
    print(f"[5] İnteraktif Görsel Analiz Ekranı üretildi: {out_html}")

    # 7. Konsol Özet Tablosu
    print("\n" + "=" * 88)
    print("  ŞİRKET FİNANSAL PERFORMANS VE HİBRİT MAKİNE ÖĞRENMESİ RİSK SIRALAMASI  ")
    print("=" * 88)

    headers = [
        "Kod", "Şirket Adı", "Sektör", "Cari Or.", "Kaldıraç",
        "İstat. Skor", "IForest (ML)", "k-NN Skor", "Hibrit Risk", "Risk Seviyesi"
    ]
    rows = []
    for comp in companies:
        summary = db.get_company_summary(comp.code)
        h_rep = hybrid_reports[comp.code]
        c_ratio = f"{summary.get('current_ratio', 0):.2f}" if summary.get('current_ratio') else "-"
        lev = f"{summary.get('financial_leverage', 0):.2f}" if summary.get('financial_leverage') else "-"

        rows.append([
            comp.code,
            comp.name[:22],
            comp.sector[:16],
            c_ratio,
            lev,
            f"{h_rep['statistical_rule_score']:.1f}",
            f"{h_rep['isolation_forest_score']:.1f}",
            f"{h_rep['knn_outlier_score']:.1f}",
            f"{h_rep['hybrid_risk_score']:.1f} / 100",
            h_rep["hybrid_risk_level"][:20]
        ])

    print(format_table(headers, rows))

    print("\n" + "=" * 88)
    print(f" Görsel Analiz Dashboard Hazır: {out_html}")
    print(" Tarayıcıda doğrudan açabilir veya 'python main.py --serve' ile sunucuyu başlatabilirsiniz.")
    print("=" * 88)

    if "--serve" in sys.argv:
        DashboardGenerator.serve_dashboard(port=8080)

if __name__ == "__main__":
    main()
