"""
src/executive_commentary.py
Akıllı Finansal Yorum ve Karar Destek Asistanı (FinancialCommentaryEngine).
Şirketin rasyolarını, sektör karşılaştırma sonuçlarını, makine öğrenmesi (Isolation Forest)
risk skorunu ve 3 yıllık Altman Z-Score trendini sentezleyerek üst düzey yöneticiye
hitap eden otomatik sözel finansal karne yorumu üretir.
"""
from typing import Dict, Any, List, Optional

class FinancialCommentaryEngine:
    """Finansal karne ve sözel yönetici özeti üreten akıllı analiz motoru."""

    @classmethod
    def generate_company_commentary(
        cls,
        company_code: str,
        company_name: str,
        sector: str,
        ratios: Dict[str, Dict[str, Optional[float]]],
        comparison: Dict[str, Any],
        hybrid_report: Dict[str, Any],
        trend_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Bir şirket için kapsamlı ve kurumsal düzeyde finansal değerlendirme metni üretir."""
        
        liq = ratios.get("liquidity", {})
        lev = ratios.get("leverage", {})
        prof = ratios.get("profitability", {})
        act = ratios.get("activity", {})

        current_ratio = liq.get("current_ratio") or 0.0
        acid_test = liq.get("acid_test_ratio") or 0.0
        cash_ratio = liq.get("cash_ratio") or 0.0
        leverage = lev.get("financial_leverage") or 0.0
        net_margin = prof.get("net_profit_margin") or 0.0
        roe = prof.get("roe") or 0.0

        hybrid_score = hybrid_report.get("hybrid_risk_score", 0.0)
        risk_level = hybrid_report.get("hybrid_risk_level", "Normal")
        critical_flags = hybrid_report.get("critical_flags", [])

        # 1. GÜÇLÜ YÖNLER (STRENGTHS)
        strengths = []
        if current_ratio >= 1.5:
            strengths.append(f"Güçlü Kısa Vadeli Likidite: Cari oran ({current_ratio:.2f}) güvenli referans olan 1.50 seviyesinin üzerindedir; kısa vadeli borç ödeme kapasitesi son derece rahattır.")
        elif current_ratio >= 1.1:
            strengths.append(f"Yeterli Çalışma Sermayesi: Cari oran ({current_ratio:.2f}) kısa vadeli borçları karşılamaya yetecek düzeydedir.")

        if cash_ratio >= 0.20:
            strengths.append(f"Sağlam Nakit Tamponu: Nakit oranı (%{cash_ratio*100:.1f}) ani likidite şoklarına ve beklenmedik nakit çıkışlarına karşı güçlü bir koruma sağlamaktadır.")

        if leverage <= 0.50:
            strengths.append(f"Düşük Finansal Borçluluk: Varlıkların yalnızca %{leverage*100:.1f}'i borçla finanse edilmekte olup, şirketin özkaynak tabanı oldukça kuvvetlidir.")
        elif leverage <= 0.70:
            strengths.append(f"Dengeli Sermaye Yapısı: Kaldıraç oranı (%{leverage*100:.1f}) sektör kabul edilebilir sınırları içerisinde yönetilmektedir.")

        if net_margin >= 0.15:
            strengths.append(f"Yüksek Kârlılık Marjı: Net kâr marjı (%{net_margin*100:.1f}) şirketin operasyonel maliyetlerini ve fiyatlama gücünü etkin yönettiğini kanıtlamaktadır.")
        elif net_margin > 0.05:
            strengths.append(f"Pozitif Net Kârlılık: Şirket ciro üzerinden %{net_margin*100:.1f} oranında istikrarlı net dönem kârı üretmektedir.")

        if roe >= 0.20:
            strengths.append(f"Yüksek Özkaynak Verimliliği (ROE): Hissedar sermayesi üzerinden %{roe*100:.1f} getiri sağlanarak yüksek katma değer yaratılmaktadır.")

        # 2. ZAYIF YÖNLER VE RİSK SİNYALLERİ (WEAKNESSES & RISKS)
        weaknesses = []
        if critical_flags:
            for flag in critical_flags:
                weaknesses.append(f"Kritik Uyarı: {flag}")

        if current_ratio < 1.0:
            if "Perakende" in sector:
                weaknesses.append(f"Sektörel Negatif Çalışma Sermayesi: Cari oran ({current_ratio:.2f}) perakende sektörünün hızlı nakit dönüş modelinden kaynaklansa da tedarikçi borç vadelerinin sıkı takibini zorunlu kılmaktadır.")
            else:
                weaknesses.append(f"Likidite Sıkışıklığı Riski: Cari oran ({current_ratio:.2f}) 1.0'ın altında kalarak dönen varlıkların kısa vadeli yükümlülükleri karşılayamadığını göstermektedir.")

        if leverage > 0.75:
            weaknesses.append(f"Aşırı Borçluluk Baskısı: Kaldıraç oranının %{leverage*100:.1f} seviyesinde olması şirketi faiz oranlarındaki dalgalanmalara ve refinansman riskine karşı kırılgan kılmaktadır.")

        if net_margin < 0:
            weaknesses.append(f"Operasyonel Zarar Durumu: Net kâr marjı (%{net_margin*100:.1f}) zarara işaret etmekte ve özkaynakları eritmektedir.")
        elif net_margin < 0.03:
            weaknesses.append(f"İnce Kâr Marjı: Net kâr marjı (%{net_margin*100:.1f}) girdi maliyetlerindeki en ufak artışta operasyonel zarara düşme riski taşımaktadır.")

        if not weaknesses:
            weaknesses.append("Mevcut finansal tablolarda acil müdahale gerektiren majör bir zayıflık veya risk sinyali tespit edilmemiştir.")

        # 3. SEKTÖREL AKRAN KIYASLAMASI (PEER BENCHMARKING)
        sector_eval = []
        comp_list = comparison.get("comparisons", [])
        for item in comp_list:
            cat = item.get("category")
            metric = item.get("metric")
            c_val = item.get("company_value")
            s_mean = item.get("sector_mean")
            if c_val is None or s_mean is None:
                continue

            if cat == "liquidity" and metric == "current_ratio":
                if c_val > s_mean + 0.3:
                    sector_eval.append(f"Likidite tarafında cari oran ({c_val:.2f}) sektör ortalamasının ({s_mean:.2f}) belirgin şekilde üzerinde daha güvenli bir pozisyondadır.")
                elif c_val < s_mean - 0.3:
                    sector_eval.append(f"Cari oran ({c_val:.2f}) sektör ortalamasının ({s_mean:.2f}) gerisinde kalmaktadır.")

            if cat == "leverage" and metric == "financial_leverage":
                if c_val < s_mean - 0.08:
                    sector_eval.append(f"Kaldıraç oranı (%{c_val*100:.1f}) sektör akranlarına kıyasla (%{s_mean*100:.1f}) daha ihtiyatlı ve muhafazakar bir borçlanma stratejisi izlendiğini göstermektedir.")
                elif c_val > s_mean + 0.08:
                    sector_eval.append(f"Kaldıraç oranı (%{c_val*100:.1f}) sektör normunun (%{s_mean*100:.1f}) üzerinde seyrederek ek finansal risk yaratmaktadır.")

            if cat == "profitability" and metric == "net_profit_margin":
                if c_val > s_mean + 0.03:
                    sector_eval.append(f"Net kâr marjı (%{c_val*100:.1f}) sektör ortalamasını (%{s_mean*100:.1f}) geride bırakarak operasyonel rekabet üstünlüğü sağlamaktadır.")
                elif c_val < s_mean - 0.03:
                    sector_eval.append(f"Kâr marjı (%{c_val*100:.1f}) sektör akranlarının (%{s_mean*100:.1f}) altında baskı altındadır.")

        peer_summary = " ".join(sector_eval) if sector_eval else "Şirket finansal oranları sektör ortalamaları ile genel bir uyum sergilemektedir."

        # 4. TREND VE ALTMAN Z-SCORE ANALİZİ
        trend_summary = ""
        altman_summary = ""
        if trend_data:
            cagr_sales = trend_data.get("cagr_sales")
            t_score = trend_data.get("trend_score", 50.0)
            t_dir = trend_data.get("trend_direction", "Stabil")
            latest_z = trend_data.get("latest_altman", 0.0)
            z_zone = trend_data.get("latest_altman_zone", "")
            z_traj = trend_data.get("altman_trajectory", "Yatay")

            cagr_txt = f"3 yıllık bileşik ciro büyümesi (CAGR) %{cagr_sales:.1f} olarak" if cagr_sales is not None else "Ciro gelişimi"
            trend_summary = f"{cagr_txt} gerçekleşmiş olup, şirketin genel finansal gidişatı '{t_dir}' (Sağlık Skoru: {t_score}/100) olarak puanlanmıştır."
            altman_summary = f"Altman Z-Score İflas Modeli değeri {latest_z:.2f} ile '{z_zone}' sınıfındadır. 3 yıllık gidişatta risk göstergesi {z_traj.lower()} bir seyir izlemektedir."

        # 5. STRATEJİK EYLEM VE İYİLEŞTİRME ÖNERİLERİ (CFO TAVSİYELERİ)
        recommendations = []
        if leverage > 0.70:
            recommendations.append("Borç Kompozisyonu Optimizasyonu: Kısa vadeli borçlanma yerine uzun vadeli tahvil/kredi veya sermaye artırımı ile finansman yapısı rahatlatılmalıdır.")
        if current_ratio < 1.2 and "Perakende" not in sector:
            recommendations.append("Çalışma Sermayesi Güçlendirilmesi: Alacak tahsilat süreleri (DSO) kısaltılmalı ve atıl stoklar nakde dönüştürülerek cari oran 1.5 bandına yaklaştırılmalıdır.")
        if net_margin < 0.05 and net_margin >= 0:
            recommendations.append("Faaliyet Verimliliği ve Maliyet Disiplini: Satılan malın maliyeti (SMM) ve operasyonel harcamalar gözden geçirilerek brüt kâr marjı artırılmalıdır.")
        elif net_margin < 0:
            recommendations.append("Acil Finansal Yeniden Yapılandırma: Şirketin zarar eden birimleri küçültülmeli, sermaye enjeksiyonu planlanmalı ve nakit çıkışları dondurulmalıdır.")
        if current_ratio >= 2.5 and cash_ratio >= 0.5:
            recommendations.append("Nakit Getiri Verimliliği: Aşırı yüksek atıl nakit rezervi yüksek enflasyonist ortamda erime riski taşır; büyüme yatırımlarına veya temettü/finansal getiri araçlarına yönlendirilmelidir.")
        
        if not recommendations:
            recommendations.append("Mevcut dengeli sermaye ve kârlılık disiplini korunmalı; pazar payını artıracak stratejik yatırımlar sürdürülmelidir.")

        # 6. GENEL YÖNETİCİ ÖZETİ (EXECUTIVE BRIEF)
        if hybrid_score < 25:
            exec_brief = f"{company_name}, güçlü sermaye tabanı, sağlıklı likidite tamponu ve sektör üzeri kârlılığıyla son derece dayanıklı bir finansal profile sahiptir. Makine öğrenmesi ve istatistiksel modeller sıfıra yakın risk tespit etmiştir."
        elif hybrid_score < 50:
            exec_brief = f"{company_name}, sektör normlarına uygun dengeli bir performans sergilemekte olup orta düzey risk grubundadır. Operasyonel nakit akışları ve borç servis kapasitesi düzenli izlenmelidir."
        else:
            exec_brief = f"{company_name}, yüksek borçluluk, likidite açığı veya kârlılık erimesi nedeniyle yüksek finansal risk taşımaktadır. Hibrit anomali modelleri kritik sapmalar tespit etmiş olup acil finansal önlemler tavsiye edilmektedir."

        return {
            "company_code": company_code,
            "company_name": company_name,
            "sector": sector,
            "executive_brief": exec_brief,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "peer_benchmarking": peer_summary,
            "trend_summary": trend_summary,
            "altman_summary": altman_summary,
            "recommendations": recommendations,
            "risk_verdict": f"{risk_level} (Hibrit Risk: {hybrid_score:.1f}/100)"
        }

    @classmethod
    def generate_all(
        cls,
        companies: List[Any],
        company_comparisons: Dict[str, Any],
        hybrid_reports: Dict[str, Any],
        trend_reports: Optional[Dict[str, Any]] = None,
        company_ratios: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """Tüm şirketler için karne yorumlarını toplu olarak üretir."""
        from src.ratios import FinancialRatioCalculator
        commentaries = {}
        for comp in companies:
            code = comp.code
            comp_rep = company_comparisons.get(code, {})
            if company_ratios and code in company_ratios:
                ratios = company_ratios[code]
            elif hasattr(comp, "balance_sheet") and hasattr(comp, "income_statement"):
                ratios = FinancialRatioCalculator.calculate_all(comp)
            else:
                ratios = comp_rep.get("company_ratios", {})

            h_rep = hybrid_reports.get(code, {})
            t_data = trend_reports.get(code) if trend_reports else None

            commentaries[code] = cls.generate_company_commentary(
                company_code=code,
                company_name=comp.name,
                sector=comp.sector,
                ratios=ratios,
                comparison=comp_rep,
                hybrid_report=h_rep,
                trend_data=t_data
            )
        return commentaries
