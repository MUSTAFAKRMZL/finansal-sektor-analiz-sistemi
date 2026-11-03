"""
main.py
Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi
Hafta 4 (v0.4.0): Çok Dönemli Zaman Serisi (Trend), Altman Z-Score İflas Riski Modeli,
Akıllı Finansal Yorum Asistanı ve Tek Tıkla Yazdırılabilir Finansal Karne.
"""
import os
import sys
from src.data_loader import FinancialDataLoader
from src.ratios import FinancialRatioCalculator
from src.sector_analysis import SectorAnalyzer
from src.anomaly_detector import FinancialAnomalyDetector
from src.ml_anomaly import HybridAnomalyEngine
from src.trend_analysis import TrendAnalyzer
from src.executive_commentary import FinancialCommentaryEngine
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
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 96)
    print("  AKILLI FİNANSAL PERFORMANS VE SEKTÖREL ANOMALİ ANALİZ SİSTEMİ (v0.4.0)  ")
    print("  Yazılım Geliştirme I - Hafta 4: Zaman Serisi (Trend), Altman Z-Score & Akıllı Yorum Asistanı  ")
    print("=" * 96)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "data", "companies_financials.csv")
    db_path = os.path.join(base_dir, "financial_analysis.db")
    dashboard_path = os.path.join(base_dir, "dashboard.html")

    print(f"\n[1] Veritabanı başlatılıyor: {db_path}")
    db = DatabaseManager(db_path)

    print(f"[2] CSV dosyasından 3 yıllık finansal tablolar okunuyor: {csv_path}")
    all_companies = FinancialDataLoader.load_from_csv(csv_path)
    print(f" -> Toplam {len(all_companies)} şirket-dönem kaydı başarıyla okundu ve doğrulandı.")

    print("[3] Şirket verileri ve rasyoları SQLite veritabanına kaydediliyor...")
    for comp in all_companies:
        db.save_company(comp)
        ratios = FinancialRatioCalculator.calculate_all(comp)
        db.save_ratios(comp.code, comp.period, ratios)

    # 4. En güncel dönem için Sektörel Kıyaslama ve Makine Öğrenmesi
    latest_companies = [c for c in all_companies if c.period == "2023/12"]
    analyzer = SectorAnalyzer(latest_companies)
    detector = FinancialAnomalyDetector(z_threshold=1.5)

    company_comparisons = {}
    base_risk_reports = {}
    for comp in latest_companies:
        comp_report = analyzer.compare_company_with_sector(comp.code)
        risk_report = detector.evaluate_risk(comp_report)
        company_comparisons[comp.code] = comp_report
        base_risk_reports[comp.code] = risk_report

    print("[4] Min-Max Veri Normalizasyonu ve Isolation Forest (ML) modeli eğitiliyor...")
    ml_engine = HybridAnomalyEngine()
    hybrid_reports = ml_engine.analyze_all_companies(
        companies=latest_companies,
        company_ratios=analyzer.company_ratios,
        base_risk_reports=base_risk_reports
    )

    for comp in latest_companies:
        h_rep = hybrid_reports[comp.code]
        db_record = dict(h_rep)
        db_record["risk_score"] = h_rep["hybrid_risk_score"]
        db_record["risk_level"] = h_rep["hybrid_risk_level"]
        db.save_anomaly_result(comp.code, comp.period, db_record)

    # 5. Hafta 4: Çok Dönemli Tarihsel Zaman Serisi & Altman Z-Score Analizi
    print("[5] 3 Yıllık Zaman Serisi (Trend), CAGR ve Altman Z-Score iflas modelleri hesaplanıyor...")
    trend_engine = TrendAnalyzer(all_companies)
    trend_reports = trend_engine.analyze_all()

    # 6. Hafta 4: Akıllı Finansal Yorum ve Yönetici Özeti Üretimi
    print("[6] Akıllı Finansal Yorum Asistanı (Doğal Dil Raporlayıcı) çalıştırılıyor...")
    commentaries = FinancialCommentaryEngine.generate_all(
        companies=latest_companies,
        company_comparisons=company_comparisons,
        hybrid_reports=hybrid_reports,
        trend_reports=trend_reports,
        company_ratios=analyzer.company_ratios
    )

    # 7. İnteraktif Görsel Analiz Ekranı (HTML5 + SVG + Trend + Yorum Asistanı + Yazdır/PDF)
    out_html = DashboardGenerator.export_dashboard(
        companies=latest_companies,
        sector_benchmarks=analyzer.sector_benchmarks,
        company_comparisons=company_comparisons,
        hybrid_reports=hybrid_reports,
        trend_reports=trend_reports,
        commentaries=commentaries,
        output_path=dashboard_path
    )
    print(f"[7] İnteraktif Görsel Analiz Ekranı üretildi: {out_html}")

    # 8. Konsol Özet Tablosu
    print("\n" + "=" * 96)
    print("  ŞİRKET FİNANSAL PERFORMANS, TREND VE HİBRİT ANOMALİ GENEL ÖZETİ  ")
    print("=" * 96)

    headers = [
        "Kod", "Şirket Adı", "Sektör", "Cari Or.", "Kaldıraç",
        "Altman Z", "Trend Sağlık", "IForest", "Hibrit Risk", "Risk Seviyesi"
    ]
    rows = []
    for comp in latest_companies:
        summary = db.get_company_summary(comp.code)
        h_rep = hybrid_reports[comp.code]
        t_rep = trend_reports[comp.code]
        c_ratio = f"{summary.get('current_ratio', 0):.2f}" if summary.get('current_ratio') else "-"
        lev = f"{summary.get('financial_leverage', 0):.2f}" if summary.get('financial_leverage') else "-"

        rows.append([
            comp.code,
            comp.name[:20],
            comp.sector[:15],
            c_ratio,
            lev,
            f"{t_rep['latest_altman']:.2f}",
            f"{t_rep['trend_score']:.0f}/100",
            f"{h_rep['isolation_forest_score']:.1f}",
            f"{h_rep['hybrid_risk_score']:.1f}",
            h_rep["hybrid_risk_level"][:18]
        ])

    print(format_table(headers, rows))

    print("\n" + "=" * 96)
    print(f" Görsel Analiz Dashboard Hazır: {out_html}")
    print(" Tarayıcıda doğrudan açabilir veya 'python main.py --serve' ile sunucuyu başlatabilirsiniz.")
    print("=" * 96)

    if "--serve" in sys.argv:
        DashboardGenerator.serve_dashboard(port=8080)

if __name__ == "__main__":
    main()
