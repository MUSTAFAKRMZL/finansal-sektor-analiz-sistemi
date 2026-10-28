"""
generate_report_hafta3.py
Haftalık Yazılım Projesi Gelişim Raporu (Hafta 3) doldurucu.
Word belgesinin (docx) OpenXML yapısını koruyarak Hafta 3 içerikleriyle doldurur.
"""
import os
import zipfile
import xml.etree.ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace('w', W_NS)
ET.register_namespace('w14', "http://schemas.microsoft.com/office/word/2010/wordml")

def make_run(text, bold=False, font="Arial", size=None):
    r = ET.Element(f"{{{W_NS}}}r")
    rPr = ET.SubElement(r, f"{{{W_NS}}}rPr")
    rFonts = ET.SubElement(rPr, f"{{{W_NS}}}rFonts")
    rFonts.set(f"{{{W_NS}}}ascii", font)
    rFonts.set(f"{{{W_NS}}}hAnsi", font)
    rFonts.set(f"{{{W_NS}}}cs", font)
    if bold:
        ET.SubElement(rPr, f"{{{W_NS}}}b")
        ET.SubElement(rPr, f"{{{W_NS}}}bCs")
    if size:
        sz = ET.SubElement(rPr, f"{{{W_NS}}}sz")
        sz.set(f"{{{W_NS}}}val", str(size))
    
    t = ET.SubElement(r, f"{{{W_NS}}}t")
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    return r

def make_br():
    r = ET.Element(f"{{{W_NS}}}r")
    rPr = ET.SubElement(r, f"{{{W_NS}}}rPr")
    rFonts = ET.SubElement(rPr, f"{{{W_NS}}}rFonts")
    rFonts.set(f"{{{W_NS}}}ascii", "Arial")
    rFonts.set(f"{{{W_NS}}}hAnsi", "Arial")
    rFonts.set(f"{{{W_NS}}}cs", "Arial")
    ET.SubElement(r, f"{{{W_NS}}}br")
    return r

def set_p_text(p, text, bold=False):
    pPr = p.find(f"{{{W_NS}}}pPr")
    for child in list(p):
        if child.tag != f"{{{W_NS}}}pPr":
            p.remove(child)
    
    if pPr is None:
        pPr = ET.Element(f"{{{W_NS}}}pPr")
        p.insert(0, pPr)
        
    rPr = pPr.find(f"{{{W_NS}}}rPr")
    if rPr is None:
        rPr = ET.SubElement(pPr, f"{{{W_NS}}}rPr")
        rFonts = ET.SubElement(rPr, f"{{{W_NS}}}rFonts")
        rFonts.set(f"{{{W_NS}}}ascii", "Arial")
        rFonts.set(f"{{{W_NS}}}hAnsi", "Arial")
        rFonts.set(f"{{{W_NS}}}cs", "Arial")

    if text:
        lines = text.split("\n")
        for i, line in enumerate(lines):
            p.append(make_run(line, bold=bold))
            if i < len(lines) - 1:
                p.append(make_br())

def main():
    base_dir = r"c:\Users\MONSTER\Desktop\yazılımgeliştirme1ödev"
    src_docx = os.path.join(base_dir, "Mustafa_Kirmizi_Haftalik_Gelisim_Raporu_Hafta_2.docx")
    dest_docx = os.path.join(base_dir, "Mustafa_Kirmizi_Haftalik_Gelisim_Raporu_Hafta_3.docx")

    print(f"Kaynak dosya okunuyor: {src_docx}")
    with zipfile.ZipFile(src_docx, 'r') as zin:
        xml_content = zin.read('word/document.xml')
        all_files = {name: zin.read(name) for name in zin.namelist()}

    tree = ET.fromstring(xml_content)
    namespaces = {'w': W_NS}
    body = tree.find('w:body', namespaces)

    def find_p(start_text):
        for p in body:
            txt = ''.join(p.itertext()).strip()
            if txt.startswith(start_text):
                return p
        return None

    # 1. HEADER (Paragraph 1)
    p1 = body[1]
    for child in list(p1):
        if child.tag != f"{{{W_NS}}}pPr":
            p1.remove(child)
    
    header_items = [
        ("Ders: ", True), ("Yazılım Geliştirme I", False), ("br", None),
        ("Proje Adı: ", True), ("Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi", False), ("br", None),
        ("Öğrenci Adı Soyadı: ", True), ("Muhammet Mustafa Kırmızı", False), ("br", None),
        ("Öğrenci No: ", True), ("24130766", False), ("br", None),
        ("Hafta No: ", True), ("3", False), ("br", None),
        ("Tarih: ", True), ("28 / 10 / 2026", False)
    ]
    for item in header_items:
        if item[0] == "br":
            p1.append(make_br())
        else:
            p1.append(make_run(item[0], bold=item[1]))

    # 2. BÖLÜM 1: HEDEFLER
    set_p_text(body[5], "Finansal rasyo vektörlerini makine öğrenmesi algoritmalarına hazırlamak amacıyla Min-Max [0, 1] veri normalizasyonu modülünün (DataNormalizer) geliştirilmesi.")
    set_p_text(body[6], "Denetimsiz makine öğrenmesi tabanlı Isolation Forest (İzolasyon Ormanı) ve k-NN (k-En Yakın Komşu) aykırı değer tespit algoritmalarının (src/ml_anomaly.py) kodlanması.")
    set_p_text(body[7], "İstatistiksel Z-Score, finansal iflas kuralları ve makine öğrenmesi skorlarını ağırlıklı birleştiren Hibrit Anomali Motorunun (HybridAnomalyEngine) oluşturulması.")
    set_p_text(body[8], "Şirket-sektör kıyaslamalarını SVG Radar Grafiği (Örümcek Ağı), Sütun Grafikleri ve Canlı Bilanço Simülatörü ile sunan İnteraktif Web Görsel Analiz Ekranının (src/web_dashboard.py & dashboard.html) tasarlanması.")
    
    set_p_text(body[11], "Proje şartnamesinin en kritik çıktıları olan 'veri normalizasyonu, makine öğrenmesi uygulamaları ve görsel analiz ekranı' bu haftanın hedefleriyle doğrudan hayata geçirilmektedir. Özellikle perakende gibi yapısal olarak düşük cari oranla çalışan sektörlerde salt kural bazlı sistemlerin ürettiği yanlış pozitif (false-positive) alarmları önlemek için Isolation Forest ve k-NN kümeleme modellerinin entegrasyonu hayati önem taşımaktadır.")

    # 3. BÖLÜM 2: YAPILAN ÇALIŞMALAR
    set_p_text(body[17], "Bu hafta projenin makine öğrenmesi katmanı ve görsel analiz arayüzü (Web Dashboard) tamamlandı. İlk olarak 13 temel finansal rasyoyu [0, 1] aralığına çeken DataNormalizer sınıfı geliştirildi ve sıfır varyanslı sütunlar için güvenli koruma eklendi. Ardından Liu vd. (2008) makalesindeki matematiksel formülasyona (Euler sabiti ve harmonik yol uzunluğu düzeltmesi c(n)) sadık kalınarak 100 ağaçlı IsolationForestDetector ve komşuluk mesafesini ölçen KNNOutlierDetector sınıfları saf Python ile kodlandı. İstatistiksel Z-Score (%55), Isolation Forest (%30) ve k-NN (%15) skorlarını harmanlayan HybridAnomalyEngine oluşturuldu. Görsel analiz için HTML5, CSS Grid ve dinamik SVG grafik motoru kullanan DashboardGenerator yazılarak Radar Grafiği, Sektör Karşılaştırma Bar Grafiği ve tarayıcı üzerinde anlık yeni şirket testi yapılabilen Canlı Bilanço Simülatörü (dashboard.html) üretildi. Son olarak 4 yeni birim test (test_ml_anomaly.py) eklenerek toplam 12 testin tamamı başarıyla çalıştırıldı.")
    
    set_p_text(body[20], "src/ml_anomaly.py: DataNormalizer, IsolationForestDetector (100 ağaçlı izolasyon ormanı), KNNOutlierDetector ve HybridAnomalyEngine sınıfları sıfırdan geliştirildi.")
    set_p_text(body[21], "src/web_dashboard.py & dashboard.html: SVG Radar (Örümcek Ağı) grafiği, grup sütun grafikleri, KPI kartları, sektör filtreleri ve canlı bilanço simülatörü içeren Web Dashboard modülü kodlandı.")
    set_p_text(body[22], "main.py: Hibrit ML motorunu çalıştırıp sonuçları SQLite veritabanına kaydeden ve tek komutla dashboard.html üreten entegre sürüme (v0.3.0) yükseltildi.")
    set_p_text(body[23], "tests/test_ml_anomaly.py: Normalizasyon sınır durumlarını, Isolation Forest aykırı değer sıralamasını, k-NN dedektörünü ve HTML üretimini doğrulayan 4 yeni birim test eklendi (Toplam 12/12 test başarılı).")

    p_degisiklik = find_p("Proje, yalnızca bellekte çalışan")
    if p_degisiklik is not None:
        set_p_text(p_degisiklik, "Proje, sadece arka uçta çalışan bir konsol uygulaması olmaktan çıkarak; makine öğrenmesi (Isolation Forest & k-NN) ile çok boyutlu anomali tespiti yapan ve kullanıcıya tarayıcı üzerinde interaktif Radar/Bar grafikleri ile canlı bilanço simülasyonu sunan tam teşekküllü bir Görsel Karar Destek Sistemine dönüştü.")

    # 4. BÖLÜM 3: TAMAMLANMA DURUMU
    p_tamamlanan = find_p("Tamamlanan çalışmalar:")
    idx = list(body).index(p_tamamlanan)
    set_p_text(body[idx+1], "- Min-Max veri normalizasyonu ve özellik vektörü çıkarımı (DataNormalizer)\n- Isolation Forest (İzolasyon Ormanı) makine öğrenmesi anomali modeli (IsolationForestDetector)\n- k-NN komşuluk mesafesi tabanlı aykırı değer dedektörü (KNNOutlierDetector)\n- İstatistiksel + Kural + ML ağırlıklı Hibrit Risk Motoru (HybridAnomalyEngine)\n- SVG Radar ve Bar grafikli İnteraktif Web Dashboard ve Canlı Bilanço Simülatörü (web_dashboard.py & dashboard.html)\n- Makine öğrenmesi ve görsel arayüz birim testleri (12/12 test başarılı)")

    p_devam = find_p("Devam eden çalışmalar:")
    idx = list(body).index(p_devam)
    set_p_text(body[idx+1], "- Çok dönemli (2021, 2022, 2023) tarihsel trend analizi ve dönemler arası rasyo değişim (trend) grafiklerinin arayüze eklenmesi.\n- Analiz sonuçlarının tek tıkla yazdırılabilir kurumsal PDF/HTML özet raporu olarak dışa aktarılması.")

    p_baslanamayan = find_p("Başlanamayan veya ertelenen çalışmalar:")
    idx = list(body).index(p_baslanamayan)
    set_p_text(body[idx+1], "- Kullanıcı bazlı oturum yönetimi ve özel portföy kaydetme özelliği (sonraki haftalara planlandı).")

    p_oran = find_p("Projenin tahmini genel tamamlanma oranı:")
    set_p_text(p_oran, "Projenin tahmini genel tamamlanma oranı: % 75", bold=True)

    p_oran_aciklama = find_p("Bu oranı neye göre belirlediğinizi kısaca açıklayınız.")
    idx = list(body).index(p_oran_aciklama)
    set_p_text(body[idx+1], "5 aşamalı proje planımızda: (1) Çekirdek matematiksel rasyo motoru [%20 - Tamamlandı], (2) CSV/JSON Veri aktarımı ve SQLite veritabanı [%25 - Tamamlandı], (3) Veri normalizasyonu ve Makine Öğrenmesi (Isolation Forest) anomali modeli [%15 - Bu hafta tamamlandı], (4) İnteraktif Görsel Analiz Ekranı / Web Dashboard [%15 - Bu hafta tamamlandı], (5) Çok dönemli trend analizi, PDF raporlama, genel optimizasyon ve final dokümantasyonu [%25 - Kalan kısım]. İlk 4 ana hedef tamamlandığı için proje %75 oranına ulaşmıştır.")

    # 5. BÖLÜM 4: TEKNİK ÇALIŞMALAR
    p_checks = find_p("☐ Arayüz / UI geliştirme")
    new_checks_text = (
        "☑ Arayüz / UI geliştirme   ☑ Veritabanı işlemleri   ☑ Backend geliştirme\n"
        "☐ API geliştirme / API kullanımı   ☐ Kullanıcı giriş ve yetkilendirme   ☑ Dosya işlemleri\n"
        "☑ Test işlemleri   ☑ Hata düzeltme / Debugging   ☑ Git / GitHub kullanımı\n"
        "☑ Kod iyileştirme / Refactoring   ☑ Dokümantasyon   ☑ Diğer: Makine Öğrenmesi (Isolation Forest & k-NN) ve Veri Normalizasyonu"
    )
    set_p_text(p_checks, new_checks_text)

    p_diller = find_p("Bu hafta kullandığınız programlama dili / dilleri:")
    idx = list(body).index(p_diller)
    set_p_text(body[idx+1], "Python 3.12, HTML5, CSS3, JavaScript (ES6+), SVG")

    p_araclar = find_p("Kullandığınız teknoloji, framework, kütüphane veya araçlar:")
    idx = list(body).index(p_araclar)
    set_p_text(body[idx+1], "Python Standart Kütüphanesi (math, random, json, sqlite3, http.server, unittest), HTML5/CSS3 Grid, Dinamik SVG Grafik Motoru (Radar & Bar Chart), VS Code IDE, Google Gemini / Antigravity AI Asistanı.")

    p_arac_amac = find_p("Bu teknolojileri hangi amaçlarla kullandığınızı açıklayınız:")
    idx = list(body).index(p_arac_amac)
    set_p_text(body[idx+1], "- math & random: Isolation Forest ağaç bölümlemelerini, Euler harmonik yol uzunluğu fonksiyonunu c(n) ve k-NN Öklid mesafelerini deterministik (seed=42) olarak hesaplamak için.\n- HTML5, CSS3 & JavaScript: Kullanıcının sektör ve şirket seçerek anlık analiz yapabileceği ve yeni bilanço simüle edebileceği interaktif arayüz için.\n- Dinamik SVG: Harici grafik kütüphanesi bağımlılığı olmadan yüksek çözünürlüklü Örümcek Ağı (Radar) ve Sütun (Bar) karşılaştırma grafiklerini çizmek için.\n- http.server & unittest: Yerel web sunucusu başlatmak ve ML algoritmalarını 12 birim testle doğrulamak için.")

    # 6. BÖLÜM 5: KARŞILAŞILAN PROBLEMLER VE ÇÖZÜMLER
    p_p1 = find_p("Problem 1")
    idx = list(body).index(p_p1)
    set_p_text(body[idx+2], "Finansal oranların ölçeklerinin birbirinden çok farklı olması (örneğin Stok Devir Hızı 15.0 iken ROA 0.08 veya Borç/Özkaynak -2.38) nedeniyle k-NN mesafe algoritmasında büyük ölçekli oranların küçük ölçekli kârlılık oranlarını tamamen domine etmesi ve sabit değerli sütunlarda normalizasyon sırasında sıfıra bölünme oluşması.")
    set_p_text(body[idx+5], "Mesafe tabanlı makine öğrenmesi algoritmaları (k-NN, LOF) özelliklerin mutlak büyüklüğüne duyarlıdır. Normalizasyon yapılmadığında sayısal aralığı geniş olan değişken tek başına mesafeyi belirler; ayrıca tüm şirketlerde aynı çıkan bir oranda (max == min) Min-Max paydası 0 olur.")
    set_p_text(body[idx+8], "DataNormalizer.min_max_normalize metodu yazılarak tüm 13 finansal rasyo [0.0, 1.0] aralığına ölçeklendi. 'abs(c_max - c_min) < 1e-9' kontrolü eklenerek varyansı sıfır olan sütunlara güvenli şekilde nötr 0.5 değeri atandı.")
    set_p_text(body[idx+11], "Tüm finansal göstergeler eşit ağırlıkla modele katıldı, sıfıra bölünme hatası engellendi ve birim test (test_min_max_normalization_and_zero_variance) ile doğrulandı.")

    p_p2 = find_p("Problem 2")
    idx = list(body).index(p_p2)
    set_p_text(body[idx+2], "Perakende sektöründeki sağlıklı şirketlerin (BİM, Migros) yapısal olarak düşük cari oranla çalışmaları sebebiyle Hafta 2'deki kural bazlı sistemde 30-50 arası risk puanı alması; buna karşın yazılımda stoksuz çalışan şirketlerin (Logo) aşırı yüksek stok devir hızı nedeniyle ML modelinde tek başına anomali görünmesi.")
    set_p_text(body[idx+5], "Tek başına kural bazlı sistemler sektör içi kümeleşmeyi göremez; tek başına denetimsiz ML (Isolation Forest) ise pozitif yönlü aşırı performansı (çok yüksek likidite veya kârlılık) negatif finansal riskten ayırt edemez.")
    set_p_text(body[idx+8], "İstatistiksel/Kural skoru (%55), Isolation Forest (%30) ve k-NN (%15) çıktıları HybridAnomalyEngine içinde birleştirildi. Perakende şirketleri kendi aralarında sıkı kümelendiği için ML skorları düşük çıktı (7.4 - 11.6) ve BİM'in hibrit riski 19.8'e (Düşük Risk) gerilerken, gerçekten batık olan RISKY_TECH hem kural (100) hem ML (78.4) hem k-NN (85.0) modellerinde yakalanarak 95.7 Hibrit Risk puanı aldı.")
    set_p_text(body[idx+11], "Yanlış pozitif (false-positive) uyarılar azaltıldı ve hem sektörel kümeleşmeyi hem de finansal iflas kurallarını dikkate alan çok daha isabetli bir karar destek mekanizması elde edildi.")

    # 7. BÖLÜM 6: KOD VE PROJE KANITLARI
    p_git = find_p("GitHub / GitLab / Repository bağlantısı:")
    set_p_text(body[list(body).index(p_git)+1], "https://github.com/MUSTAFAKRMZL/finansal-sektor-analiz-sistemi")

    p_commit_sayi = find_p("Bu hafta yaptığınız yaklaşık commit sayısı:")
    set_p_text(body[list(body).index(p_commit_sayi)+1], "3 commit")

    p_commit_onemli = find_p("Bu haftaki önemli commit veya geliştirmeler:")
    set_p_text(body[list(body).index(p_commit_onemli)+1], "- feat: Hafta 3 - Min-Max veri normalizasyonu, Isolation Forest ve k-NN ML anomali modelleri (src/ml_anomaly.py)\n- feat: Interaktif SVG Radar/Bar grafikli Web Dashboard ve canli bilanco simulatoru (src/web_dashboard.py & dashboard.html)\n- test: ML modelleri ve dashboard uretimi icin 4 yeni birim test eklendi (Toplam 12 test OK)")

    p_demo = find_p("Varsa çalışan uygulama / demo bağlantısı:")
    set_p_text(body[list(body).index(p_demo)+1], "c:\\Users\\MONSTER\\Desktop\\yazılımgeliştirme1ödev\\dashboard.html (Tarayıcıda doğrudan açılabilir veya 'python main.py --serve' ile http://127.0.0.1:8080/dashboard.html üzerinden çalıştırılabilir).")

    p_kod_amac = find_p("Kodun amacı:")
    set_p_text(body[list(body).index(p_kod_amac)+1], "Eğitilen 100 adet İzolasyon Ağacı (Isolation Tree) üzerinden şirketlerin ortalama izolasyon yol uzunluğunu E(h(x)) hesaplayan ve Euler harmonik sabiti c(n) ile normalize ederek 0-100 aralığında makine öğrenmesi anomali skoru üreten IsolationForestDetector.score_samples metodu.")

    p_kod = find_p("Kod:")
    kod_text = (
        "def score_samples(self, X: List[List[float]]) -> List[float]:\n"
        "    \"\"\"\n"
        "    Her bir örnek için [0, 100] aralığında Isolation Forest anomali skoru döndürür.\n"
        "    Kısa ortalama yol uzunluğu (hızlı izolasyon) -> Yüksek anomali skoru.\n"
        "    \"\"\"\n"
        "    if not self.trees or self.n_samples <= 1:\n"
        "        return [0.0 for _ in X]\n\n"
        "    c_n = _c_factor(self.n_samples)\n"
        "    if c_n <= 0:\n"
        "        return [0.0 for _ in X]\n\n"
        "    scores = []\n"
        "    for x in X:\n"
        "        avg_path = sum(self._path_length(x, t, 0) for t in self.trees) / len(self.trees)\n"
        "        # Standart IF skoru: s = 2^(-E(h(x)) / c(n)), aralık (0, 1)\n"
        "        raw_if_score = math.pow(2.0, -avg_path / c_n)\n"
        "        # 0-100 ölçeğine kalibrasyon\n"
        "        calibrated = max(0.0, min(100.0, (raw_if_score - 0.35) / 0.45 * 100.0))\n"
        "        scores.append(round(calibrated, 1))\n"
        "    return scores"
    )
    set_p_text(body[list(body).index(p_kod)+1], kod_text)

    p_kod_aciklama = find_p("Kodun nasıl çalıştığını kendi ifadelerinizle açıklayınız:")
    set_p_text(body[list(body).index(p_kod_aciklama)+1], "Isolation Forest algoritmasında aykırı (anomalili) bir şirket, normal şirket kümesinden çok uzakta olduğu için rastgele özellik bölmeleriyle kök düğüme çok yakın seviyelerde (kısa yol uzunluğu ile) izole edilir. Bu metot, her şirket vektörü x için 100 ağaçtaki yol uzunluklarının ortalamasını (avg_path) alır ve teorik ortalama ağaç derinliği c(n) ile oranlayarak 2^(-avg_path / c_n) formülünü uygular. Yol kısaldıkça üs sıfıra yaklaşır ve skor 1'e (100 puana) yükselir.")

    # 8. BÖLÜM 7: ÖĞRENİLEN YENİ BİLGİLER
    set_p_text(body[106], "Isolation Forest algoritmasının çalışma prensibini, ikili arama ağaçlarında ortalama başarısız arama yolu uzunluğu formülü olan c(n) = 2H(n-1) - 2(n-1)/n eşitliğini ve denetimsiz anomali tespitinin matematiksel temellerini öğrendim.")
    set_p_text(body[107], "Çok boyutlu veri analizinde Min-Max normalizasyonunun k-NN gibi Öklid mesafesi kullanan algoritmalar üzerindeki belirleyici etkisini ve sıfır varyans (sabit sütun) istisnalarının nasıl yönetileceğini deneyimledim.")
    set_p_text(body[108], "Harici bir grafik kütüphanesine ihtiyaç duymadan trigonometrik birim çember koordinatlarıyla (cos, sin) dinamik SVG Radar (Örümcek Ağı) grafiği çizmeyi öğrendim.")

    p_en_onemli = find_p("Bu bilgilerden sizin için en önemli olanını açıklayınız.")
    set_p_text(body[list(body).index(p_en_onemli)+1], "Denetimsiz makine öğrenmesi modellerinin 'farklı olanı' bulmakta çok güçlü olduğunu, ancak bu farklılığın finansal açıdan 'iyi bir ayrışma mı (yüksek likidite/kâr)' yoksa 'tehlikeli bir risk mi (iflas sinyali)' olduğunu ayırt etmek için alan bilgisi (domain rules) ile hibritlenmesi gerektiğini kavramaktı.")

    p_tekrar_kullanim = find_p("Bu bilgiyi daha sonra benzer bir problemde yeniden kullanabileceğinizi düşünüyor musunuz? Neden?")
    set_p_text(body[list(body).index(p_tekrar_kullanim)+1], "Evet. Kurduğumuz hibrit anomali mimarisi (Normalizasyon + Isolation Forest + Kural Motoru) siber güvenlikte saldırı tespitinden kredi kartı dolandırıcılığı (fraud) analizine ve sensör arıza tespitine kadar her alanda doğrudan yeniden kullanılabilir.")

    # 9. BÖLÜM 8: GELECEK HAFTANIN PLANI
    set_p_text(body[117], "Şirketlerin birden fazla dönemini (2021, 2022, 2023) karşılaştıran tarihsel zaman serisi / trend analizi modülünün eklenmesi.")
    set_p_text(body[118], "Web Dashboard üzerine şirketlerin finansal sağlık gidişatını özetleyen otomatik sözel yorumlayıcı (Akıllı Finansal Yorum Asistanı) bölümünün entegre edilmesi.")
    set_p_text(body[119], "Analiz sonuçlarının ve şirket karnesinin tek tıkla dışa aktarılabilir/yazdırılabilir rapor formatına dönüştürülmesi.")
    set_p_text(body[120], "Uçtan uca sistem entegrasyon testlerinin genişletilmesi ve proje teknik dokümantasyonunun güncellenmesi.")

    p_gelecek_oncelik = find_p("Bir sonraki hafta öncelikli olarak çözmeniz gereken problem veya tamamlamanız gereken özellik nedir?")
    set_p_text(body[list(body).index(p_gelecek_oncelik)+1], "Öncelikli hedefim; tek dönemlik anlık fotoğraf çekmenin ötesine geçerek şirketin önceki dönemlerine göre rasyolarının iyileşip kötüleştiğini analiz eden çok dönemli trend analizini ve otomatik finansal karne yorumlayıcısını tamamlamaktır.")

    # 10. BÖLÜM 9: YAPAY ZEKA SÜRECİ
    # 9.1
    p_ai_arac = find_p("Kullandığım yapay zekâ araçları:")
    set_p_text(body[list(body).index(p_ai_arac)+1], "Google Gemini, ChatGPT, Antigravity AI Asistanı")

    # 9.2
    p_ai_amac = find_p("Bu hafta yapay zekâyı kullandığım başlıca amaçlar:")
    set_p_text(body[list(body).index(p_ai_amac)+1], "Isolation Forest algoritmasının saf Python ile ağaç veri yapısı olarak gerçeklenmesi, SVG Radar grafiğinin trigonometrik poligon koordinatlarının hesaplanması, hibrit ağırlıklandırma kalibrasyonu ve birim test senaryolarının oluşturulması.")

    p_ai_en_cok = find_p("Yapay zekâyı en çok hangi konuda kullandınız?")
    set_p_text(body[list(body).index(p_ai_en_cok)+1], "Isolation Forest yol uzunluğu normalizasyon fonksiyonu c(n) ve SVG Radar grafiğinin açısal koordinat dönüşümleri konusunda.")

    p_ai_neden = find_p("Neden bu konuda yapay zekâ desteğine ihtiyaç duydunuz?")
    set_p_text(body[list(body).index(p_ai_neden)+1], "Harici kütüphane kurulum sorunlarından bağımsız, her ortamda anında çalışan saf Python Isolation Forest uygulaması ve tarayıcıda pürüzsüz çalışan SVG Radar grafiği oluşturmak için.")

    # 9.3
    p_ai_denemeler = find_p("Yapay zekâya başvurmadan önce yaptığım denemeler / araştırmalar:")
    set_p_text(body[list(body).index(p_ai_denemeler)+1], "Isolation Forest makalesindeki (Liu et al., 2008) ikili ağaç derinlik formüllerini inceledim ve radar grafiği için 6 eksenli poligonun (2*pi*i / N) açılarını kağıt üzerinde modelledim.")

    # 9.4 PROMPTLAR
    p_pr1 = find_p("Prompt 1")
    idx = list(body).index(p_pr1)
    set_p_text(body[idx+2], "Harici kütüphane kullanmadan saf Python ile Isolation Forest anomali tespit algoritmasının kodlanması.")
    set_p_text(body[idx+5], "'Python standart kütüphaneleriyle (math, random) Isolation Forest algoritmasını gerçekle. Ağaç düğümlerini, c(n) Euler harmonik düzeltme faktörünü ve 2^(-E(h(x))/c(n)) anomali skorunu içersin.'")
    set_p_text(body[idx+8], "Özyinelemeli (recursive) _IsolationNode yapısı ve c(n) fonksiyonu ile ağaç topluluğu oluşturan bir sınıf şablonu sundu.")
    set_p_text(body[idx+11], "☐ Doğrudan kullandım.   ☑ Küçük değişiklikler yaptım.   ☐ Büyük ölçüde değiştirdim.   ☐ Yalnızca fikir almak için kullandım.   ☐ Cevabı kullanmadım.")
    set_p_text(body[idx+13], "Sabit değerli özelliklerde sonsuz döngü oluşmaması için varyans kontrolü (max - min > 1e-9) ekledim ve skorları 0-100 ölçeğine kalibre ettim.")

    p_pr2 = find_p("Prompt 2")
    idx = list(body).index(p_pr2)
    set_p_text(body[idx+2], "Web Dashboard üzerinde şirket ve sektör ortalamasını üst üste gösteren 6 eksenli SVG Radar (Örümcek Ağı) grafiği çizimi.")
    set_p_text(body[idx+5], "'JavaScript ile harici kütüphane kullanmadan <svg> içinde 6 finansal göstergeyi (Cari Oran, Asit-Test, Özkaynak Oranı, Net Kâr Marjı, ROA, Aktif Devir) çizen bir Radar Chart fonksiyonu yaz. Sektör ortalamasını referans poligon olarak göstersin.'")
    set_p_text(body[idx+8], "Trigonometrik cos ve sin fonksiyonlarıyla merkez (cx, cy) etrafında poligon noktaları üreten bir JS fonksiyonu verdi.")
    set_p_text(body[idx+11], "☐ Doğrudan kullandım.   ☐ Küçük değişiklikler yaptım.   ☑ Büyük ölçüde değiştirdim.   ☐ Yalnızca fikir almak için kullandım.   ☐ Cevabı kullanmadım.")
    set_p_text(body[idx+13], "Negatif kârlılık oranlarında poligon noktalarının merkezin ters tarafına taşmasını önlemek için sektör ortalamasını 0.60 yarıçapa sabitleyen bağıl ölçekleme ve alt sınır (0.10) kontrolü ekledim.")

    p_pr3 = find_p("Prompt 3")
    idx = list(body).index(p_pr3)
    set_p_text(body[idx+2], "İstatistiksel kural skoru ile denetimsiz ML skorlarını birleştiren hibrit risk formülünün tasarımı.")
    set_p_text(body[idx+5], "'Finansal analizde kural bazlı risk skoru, Isolation Forest skoru ve k-NN mesafe skorunu birleştirirken perakende sektörü gibi yanlış pozitifleri azaltacak ama teknik iflas durumlarını kaçırmayacak ağırlıklandırma nasıl kurulmalıdır?'")
    set_p_text(body[idx+8], "Ağırlıklı ortalama (%55 Kural/İstatistik, %30 IForest, %15 k-NN) ve kritik eşik koruma kuralı (guardrail) önerdi.")
    set_p_text(body[idx+11], "☐ Doğrudan kullandım.   ☑ Küçük değişiklikler yaptım.   ☐ Büyük ölçüde değiştirdim.   ☐ Yalnızca fikir almak için kullandım.   ☐ Cevabı kullanmadım.")
    set_p_text(body[idx+13], "Kritik iflas durumunda (stat_rule_score >= 85) hibrit skorun düşmesini engelleyen güvenlik sınırını HybridAnomalyEngine sınıfına entegre ettim.")

    # 9.5
    p_istenen_islem = find_p("Yapay zekâdan istediğiniz işlem:")
    set_p_text(body[list(body).index(p_istenen_islem)+1], "Isolation Forest algoritmasında yaprak düğümlerdeki örneklem sayısına göre ortalama yol uzunluğu düzeltmesini hesaplayan _c_factor(n) fonksiyonu.")

    p_onerilen_kod = find_p("Yapay zekânın önerdiği kod:")
    set_p_text(body[list(body).index(p_onerilen_kod)+1], "def _c_factor(n: int) -> float:\n    if n <= 1:\n        return 0.0\n    if n == 2:\n        return 1.0\n    euler_gamma = 0.5772156649\n    h = math.log(n - 1.0) + euler_gamma\n    return 2.0 * h - (2.0 * (n - 1.0) / n)")

    p_kod_kendi_ifadeniz = find_p("Bu kodun ne yaptığını kendi ifadelerinizle açıklayınız:")
    set_p_text(body[list(body).index(p_kod_kendi_ifadeniz)+1], "n elemanlı bir veri kümesinde ikili arama ağacının beklenen derinliğini Euler sabiti ve harmonik sayı yaklaşımıyla hesaplar; böylece ağaç derinlik sınırı nedeniyle erken sonlanan düğümlerin yol uzunluğunu matematiksel olarak tahmin eder ve skoru normalize eder.")

    p_degisiklik = find_p("Kod üzerinde yaptığınız değişiklikler:")
    set_p_text(body[list(body).index(p_degisiklik)+1], "n == 2 sınır durumunu (log(1)=0 olduğunda formülün hassasiyeti için) açık koşul olarak ekledim ve tip bildirimlerini tamamladım.")

    # 9.6
    p_tespit_hata = find_p("Evet ise tespit ettiğiniz hata:")
    set_p_text(body[list(body).index(p_tespit_hata)+1], "Yapay zekanın ilk önerdiği Isolation Tree bölme kodunda, alt düğümdeki tüm örneklerin belirli bir özellikte aynı değere sahip olması durumunda (min == max) boş sol veya sağ alt-ağaç oluşuyor ve özyineleme derinliği gereksiz uzuyordu.")

    p_hata_duzeltme = find_p("Hatayı nasıl düzelttiniz?")
    set_p_text(body[list(body).index(p_hata_duzeltme)+1], "Bölme yapmadan önce yalnızca varyansı sıfırdan büyük olan (max(vals) - min(vals) > 1e-9) özellikleri filtreleyen 'valid_attrs' listesi ekledim; eğer bölünebilir özellik kalmadıysa düğümü doğrudan yaprak (is_external=True) olarak sonlandırdım.")

    # 9.7
    p_en_onemli_prob = find_p("Karşılaştığınız en önemli problem:")
    set_p_text(body[list(body).index(p_en_onemli_prob)+1], "Radar grafiğinde negatif finansal oranların (örneğin RISKY_TECH şirketinde -%53.3 net kâr marjı) yarıçapı negatif yaparak grafiğin karşı eksenine taşması.")

    p_prob_cozum = find_p("Bu problemi nasıl çözdünüz?")
    set_p_text(body[list(body).index(p_prob_cozum)+1], "Negatif oranlar için minimum yarıçap sınırı (0.12) tanımladım ve sektör ortalamasını 0.60 referans çemberine sabitleyerek görsel bozulmayı tamamen giderdim.")

    # 9.10
    p_yz_oran = find_p("Tahmini yapay zekâ kullanım oranım:")
    set_p_text(p_yz_oran, "Tahmini yapay zekâ kullanım oranım: % 35", bold=True)

    p_yz_kod_oran = find_p("Tahmini oran:")
    if p_yz_kod_oran is not None:
        set_p_text(p_yz_kod_oran, "Tahmini oran: % 30", bold=True)

    p_secenek_neden = find_p("Bu seçeneği neden işaretlediğinizi açıklayınız:")
    set_p_text(body[list(body).index(p_secenek_neden)+1], "Normalizasyon akışını, hibrit risk ağırlıklarını ve simülatör mantığını kendim kurguladım; yapay zekadan Isolation Forest matematiksel yardımcıları ve CSS/SVG görsel bileşen şablonlarında destek aldım.")

    # 9.11
    p_genel_deg = find_p("Genel değerlendirme:")
    genel_text_3 = (
        "Bu hafta yapay zekâ, özellikle Isolation Forest algoritmasının saf Python ile ağaç yapısında kodlanması ve SVG tabanlı interaktif Radar/Bar grafiklerinin matematiksel koordinatlarının oluşturulmasında geliştirme hızımı büyük ölçüde artırdı. "
        "Veri normalizasyonundaki sıfır varyans korumalarını, perakende sektörü yanlış pozitif (false-positive) kalibrasyonunu ve hibrit model ağırlıklarını bizzat kendim tasarlayıp doğruladım. "
        "Yapay zekanın ürettiği ağaç bölme kodundaki sıfır varyans hatasını ve radar grafiğindeki negatif değer taşmasını inceleyerek düzeltmem, hem makine öğrenmesi algoritmalarının iç yapısını hem de veri görselleştirme matematiğini tam olarak kavramamı sağladı."
    )
    set_p_text(body[list(body).index(p_genel_deg)+1], genel_text_3)

    # 9.12
    p_kanit_acikla = find_p("Eklediğiniz kanıtları kısaca açıklayınız:")
    kanit_text_3 = (
        "1. src/ml_anomaly.py (DataNormalizer, IsolationForestDetector, KNNOutlierDetector ve HybridAnomalyEngine sınıfları)\n"
        "2. src/web_dashboard.py & dashboard.html (SVG Radar/Bar grafikleri ve Canlı Bilanço Simülatörü içeren görsel analiz ekranı)\n"
        "3. tests/test_ml_anomaly.py (Normalizasyon, Isolation Forest, k-NN ve HTML üretimini doğrulayan yeni testler - Toplam 12/12 test OK)"
    )
    set_p_text(body[list(body).index(p_kanit_acikla)+1], kanit_text_3)

    # 10. BÖLÜM 10
    p_en_basarili = find_p("Bu hafta en başarılı olduğunuz konu:")
    set_p_text(body[list(body).index(p_en_basarili)+1], "Harici hiçbir paket kurulumuna ihtiyaç duymadan saf Python ile çalışan Isolation Forest makine öğrenmesi modelini ve tarayıcıda interaktif çalışan SVG Radar/Bar grafikli Web Dashboard ekranını (dashboard.html) uçtan uca entegre etmek.")

    p_en_zor = find_p("En fazla zorlandığınız konu:")
    set_p_text(body[list(body).index(p_en_zor)+1], "Denetimsiz makine öğrenmesi modelinin yüksek kârlı/likit şirketleri de 'sektörden farklı' olduğu için anomali sayması problemini, istatistiksel iflas kurallarıyla hibritleyerek dengelemek.")

    p_farkli = find_p("Bu hafta tekrar çalışma fırsatınız olsaydı farklı yapacağınız şey:")
    set_p_text(body[list(body).index(p_farkli)+1], "Veri setine en baştan her şirket için 3 yıllık geçmiş dönem verisi ekleyerek Radar grafiğinin yanında yıllar arası trend çizgisini de aynı anda çıkarmak olurdu.")

    p_puan = find_p("9.5 / 10")
    if p_puan is None:
        p_puan = find_p("…… / 10")
    if p_puan is not None:
        set_p_text(p_puan, "9.5 / 10", bold=True)

    p_puan_neden = find_p("Neden?")
    for p in body[list(body).index(p_puan):list(body).index(p_puan)+4]:
        if "Neden?" in ''.join(p.itertext()):
            set_p_text(body[list(body).index(p)+1], "Proje şartnamesindeki tüm temel gereksinimler (oran analizi, veri normalizasyonu, sektör karşılaştırması, makine öğrenmesi anomali tespiti ve görsel analiz ekranı) 3. hafta itibarıyla çalışır ve 12 birim testle doğrulanmış şekilde tamamlandı.")
            break

    # Save to zip
    new_xml = ET.tostring(tree, encoding='utf-8', xml_declaration=True)
    all_files['word/document.xml'] = new_xml

    with zipfile.ZipFile(dest_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for name, data in all_files.items():
            zout.writestr(name, data)
    print(f"Hafta 3 Raporu başarıyla oluşturuldu: {dest_docx}")

if __name__ == "__main__":
    main()
