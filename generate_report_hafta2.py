"""
generate_report_hafta2.py
Haftalık Yazılım Projesi Gelişim Raporu (Hafta 2) doldurucu.
Word belgesinin (docx) OpenXML yapısını koruyarak Hafta 2 içerikleriyle doldurur.
"""
import os
import sys
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
    src_docx = os.path.join(base_dir, "Mustafa_Kirmizi_Haftalik_Gelisim_Raporu_Hafta_1.docx")
    dest_docx = os.path.join(base_dir, "Mustafa_Kirmizi_Haftalik_Gelisim_Raporu_Hafta_2.docx")

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
        ("Öğrenci Adı Soyadı: ", True), ("Mustafa Kırmızı", False), ("br", None),
        ("Öğrenci No: ", True), ("24130766", False), ("br", None),
        ("Hafta No: ", True), ("2", False), ("br", None),
        ("Tarih: ", True), ("21 / 10 / 2026", False)
    ]
    for item in header_items:
        if item[0] == "br":
            p1.append(make_br())
        else:
            p1.append(make_run(item[0], bold=item[1]))

    # 2. BÖLÜM 1: HEDEFLER
    set_p_text(body[5], "Şirketlerin finansal tablolarını harici CSV ve JSON dosyalarından sisteme otomatik olarak aktaran ve şema doğrulayan FinancialDataLoader modülünün geliştirilmesi.")
    set_p_text(body[6], "BIST yapısına uygun 3 farklı sektörden (Savunma/Bilişim, Otomotiv, Perakende) 10 şirkete ait kapsamlı finansal veri setinin (companies_financials.csv) hazırlanması.")
    set_p_text(body[7], "Şirket kayıtları, bilanço, rasyolar ve anomali sonuçlarını kalıcı olarak saklamak üzere SQLite tabanlı ilişkisel veritabanı yönetim modülünün (DatabaseManager) kurulması.")
    set_p_text(body[8], "Z-Score analizine ek olarak sektör ağırlık merkezine çok boyutlu Öklid uzaklığı (Multi-dimensional Distance) ve negatif özkaynak kuralını içeren hibrit anomali motorunun geliştirilmesi.")
    
    set_p_text(body[11], "İlk haftada kodlanan çekirdek rasyo motorunun çalışan gerçek bir sisteme dönüşmesi için verilerin dinamik dosyalardan (CSV/Excel) okunması ve veritabanında kalıcı saklanması zorunludur. Ayrıca çok boyutlu Öklid uzaklığı ve negatif özkaynak gibi kritik iflas kurallarının modele eklenmesi, projenin en temel çıktısı olan şirket risk/anomali puanının finansal hassasiyetini ve güvenilirliğini ciddi ölçüde artırmaktadır.")

    # 3. BÖLÜM 2: YAPILAN ÇALIŞMALAR
    set_p_text(body[17], "Bu hafta projenin veri entegrasyonu, kalıcı depolama ve çok boyutlu risk analizi katmanları tamamlandı. İlk olarak FinancialDataLoader modülü geliştirilerek bilanço ve gelir tablosundaki 21 zorunlu alanı denetleyen şema doğrulama mekanizması yazıldı. 3 sektör ve 10 şirketi içeren companies_financials.csv veri seti oluşturuldu. Veri kalıcılığı için SQLite tabanlı DatabaseManager sınıfı yazılarak 4 ilişkisel tablo ve güvenli bağlantı yönetimi (contextmanager) kuruldu. Anomali tespit motoruna Çok Boyutlu Öklid Sapma Mesafesi ve negatif özkaynak kuralı eklendi. Tüm veri akışı main.py dosyasında birleştirilerek CSV'den veritabanına aktarım, sektör analizi ve formatlı risk özet tablosu uçtan uca çalıştırıldı. Yazılan 4 yeni birim test ile toplam test sayısı 8'e çıkarıldı ve tümü başarıyla geçti.")
    
    set_p_text(body[20], "src/data_loader.py: CSV ve JSON formatındaki finansal tabloları okuyan, eksik sütunları ve veri tiplerini denetleyen FinancialDataLoader sınıfı sıfırdan geliştirildi.")
    set_p_text(body[21], "src/database.py: SQLite veritabanı şemasını oluşturan, şirketleri, finansal tabloları, hesaplanan oranları ve anomali değerlendirmelerini saklayan DatabaseManager modülü kodlandı.")
    set_p_text(body[22], "src/anomaly_detector.py: Çok boyutlu uzaklık (Multi-dimensional Euclidean Distance of Z-Scores) ve negatif özkaynak kuralı eklenerek anomali motoru v0.2'ye yükseltildi.")
    set_p_text(body[23], "data/companies_financials.csv & tests/: 3 sektörlü 10 şirketlik veri seti hazırlandı; veritabanı ve veri yükleyici için 4 yeni birim test yazılarak toplam 8 teste ulaşıldı.")

    p_degisiklik = find_p("Proje şartname aşamasından çıkarılarak")
    if p_degisiklik is not None:
        set_p_text(p_degisiklik, "Proje, yalnızca bellekte çalışan izole bir prototip olmaktan çıkarak; harici CSV dosyalarından veri aktaran, ilişkisel SQLite veritabanında tüm hesaplamaları kalıcı saklayan, çok boyutlu matematiksel anomali analizi yapan ve şirketleri sektörel bazda sıralayan tam entegre bir arka uç (backend) analiz sistemine dönüştü.")

    # 4. BÖLÜM 3: TAMAMLANMA DURUMU
    p_tamamlanan = find_p("Tamamlanan çalışmalar:")
    idx = list(body).index(p_tamamlanan)
    set_p_text(body[idx+1], "- CSV ve JSON veri yükleyici modülü (FinancialDataLoader)\n- 10 şirketli ve 3 sektörlü genişletilmiş finansal veri seti (companies_financials.csv)\n- SQLite ilişkisel veritabanı mimarisi ve CRUD servisleri (DatabaseManager)\n- Çok boyutlu Öklid sapma mesafesi ve negatif özkaynak risk kuralları (FinancialAnomalyDetector)\n- Veritabanı ve veri yükleyici birim testleri (toplam 8 testin tamamı başarılı)\n- Konsol üzerinden çalışan entegre versiyon 0.2 demosu (main.py)")

    p_devam = find_p("Devam eden çalışmalar:")
    idx = list(body).index(p_devam)
    set_p_text(body[idx+1], "- Çok boyutlu mesafe analizini scikit-learn kütüphanesindeki Isolation Forest ve Local Outlier Factor (LOF) makine öğrenmesi modelleriyle kıyaslama ve model optimizasyonu.\n- Veritabanındaki verileri ve sektör kıyaslamalarını dinamik grafiklerle gösterecek Web Dashboard (Streamlit) arayüz tasarımı.")

    p_baslanamayan = find_p("Başlanamayan veya ertelenen çalışmalar:")
    idx = list(body).index(p_baslanamayan)
    set_p_text(body[idx+1], "- Kullanıcı giriş/yetkilendirme sistemi ve rol bazlı erişim (sonraki haftalara planlandı).\n- Canlı BIST/KAP veri çekme API entegrasyonu (veri sağlayıcı sınırlamaları nedeniyle simüle veri setiyle devam edildi).")

    p_oran = find_p("Projenin tahmini genel tamamlanma oranı:")
    set_p_text(p_oran, "Projenin tahmini genel tamamlanma oranı: % 45", bold=True)

    p_oran_aciklama = find_p("Bu oranı neye göre belirlediğinizi kısaca açıklayınız.")
    idx = list(body).index(p_oran_aciklama)
    set_p_text(body[idx+1], "5 aşamalı yol haritamızda: (1) Çekirdek matematiksel rasyo motoru [%20 - Tamamlandı], (2) Veri aktarımı (ETL), SQLite veritabanı kalıcılığı ve gelişmiş çok boyutlu risk motoru [%25 - Bu hafta tamamlandı], (3) Makine öğrenmesi modeli optimizasyonu ve API katmanı [%20], (4) Web Arayüzü / Görsel Analiz Dashboard'u [%20], (5) Test, optimizasyon ve dokümantasyon [%15]. İlk iki aşama eksiksiz tamamlandığı için toplam tamamlanma oranı %45'e yükselmiştir.")

    # 5. BÖLÜM 4: TEKNİK ÇALIŞMALAR
    p_checks = find_p("☐ Arayüz / UI geliştirme")
    new_checks_text = (
        "☐ Arayüz / UI geliştirme   ☑ Veritabanı işlemleri   ☑ Backend geliştirme\n"
        "☐ API geliştirme / API kullanımı   ☐ Kullanıcı giriş ve yetkilendirme   ☑ Dosya işlemleri\n"
        "☑ Test işlemleri   ☑ Hata düzeltme / Debugging   ☑ Git / GitHub kullanımı\n"
        "☑ Kod iyileştirme / Refactoring   ☑ Dokümantasyon   ☑ Diğer: Çok Boyutlu İstatistiksel Analiz ve Veri Normalizasyonu"
    )
    set_p_text(p_checks, new_checks_text)

    p_diller = find_p("Bu hafta kullandığınız programlama dili / dilleri:")
    idx = list(body).index(p_diller)
    set_p_text(body[idx+1], "Python 3.12")

    p_araclar = find_p("Kullandığınız teknoloji, framework, kütüphane veya araçlar:")
    idx = list(body).index(p_araclar)
    set_p_text(body[idx+1], "Python Standart Kütüphanesi (sqlite3, csv, json, math, contextlib, unittest, dataclasses, os), Git, VS Code IDE, Google Gemini / Antigravity AI Asistanı.")

    p_arac_amac = find_p("Bu teknolojileri hangi amaçlarla kullandığınızı açıklayınız:")
    idx = list(body).index(p_arac_amac)
    set_p_text(body[idx+1], "- sqlite3: Şirketler, finansal tablolar, rasyolar ve anomali sonuçları arasında ilişkisel veri modeli kurarak kalıcı depolama sağlamak için.\n- csv & json: Harici kaynaklardan sağlanan finansal verileri tablo formatında sisteme güvenle aktarmak (ETL) için.\n- contextlib: Veritabanı bağlantılarını güvenli açıp kapatmak, Windows üzerinde dosya kilitleme ve sızıntı hatalarını önlemek için.\n- math: Çok boyutlu Z-Score vektörlerinin Öklid normunu hesaplayarak sektörden genel sapma mesafesini bulmak için.\n- unittest: Yeni eklenen veri yükleyici ve veritabanı modüllerinin doğruluğunu otomatik testlerle teyit etmek için.")

    # 6. BÖLÜM 5: KARŞILAŞILAN PROBLEMLER VE ÇÖZÜMLER
    p_p1 = find_p("Problem 1")
    idx = list(body).index(p_p1)
    set_p_text(body[idx+2], "Windows işletim sisteminde birim testler (test_database.py) çalıştırılırken, tearDown metodunda test veritabanı dosyası silinmek istendiğinde 'PermissionError: [WinError 32] Dosya başka bir işlem tarafından kullanıldığından bu işlem dosyaya erişemiyor' hatası alındı ve testler başarısız oldu.")
    set_p_text(body[idx+5], "SQLite bağlantısı standart 'with conn:' bloğunda kullanıldığında; with yapısı yalnızca işlemleri (commit/rollback) yönetir, bağlantıyı fiziksel olarak kapatmaz (close). Açık kalan bağlantı nedeniyle Windows dosya kilidi aktif kaldı ve dosya silinemedi.")
    set_p_text(body[idx+8], "src/database.py içerisinde contextlib.contextmanager dekoratörü kullanılarak get_connection() metodu yazıldı. try-finally bloğuyla her veritabanı işleminden sonra conn.close() çağrısı garanti altına alındı.")
    set_p_text(body[idx+11], "Veritabanı bağlantı sızıntıları ve dosya kilitlenme hataları tamamen ortadan kaldırıldı; birim testler başarıyla geçti.")

    p_p2 = find_p("Problem 2")
    idx = list(body).index(p_p2)
    set_p_text(body[idx+2], "Perakende sektöründeki şirketlerin (Migros, BİM, Şok) doğaları gereği vadeli mal alıp günlük nakit satmaları nedeniyle cari oranlarının 1.0'ın altında çıkması ve sistemin bu şirketlere haksız yere aşırı yüksek likidite riski ataması.")
    set_p_text(body[idx+5], "Farklı sektörlerin finansal operasyon modelleri birbirinden tamamen farklıdır; perakende sektöründe negatif işletme sermayesi normal bir finansman modeliyken, teknoloji sektöründe cari oranın 1'in altında olması ciddi bir kriz belirtisidir.")
    set_p_text(body[idx+8], "Kural bazlı risk kontrollerine ek olarak 'Çok Boyutlu Sektörel Uzaklık' metriği entegre edildi ve perakende şirketlerinin sektör kendi içindeki ortalamalarıyla kıyaslanması sağlandı. Ayrıca risk etiketleri Düşük, Orta, Yüksek ve Kritik Risk olarak yeniden kalibre edildi.")
    set_p_text(body[idx+11], "Şirketlerin sadece genel ezber kurallarla değil, kendi sektör dinamiklerine göre göreceli olarak değerlendirilmesi sağlandı; perakende şirketleri iflas riski yerine sektör normlarına uygun olarak 'Orta Risk / Takip Edilmeli' şeklinde sınıflandırıldı.")

    # 7. BÖLÜM 6: KOD VE PROJE KANITLARI
    p_git = find_p("GitHub / GitLab / Repository bağlantısı:")
    set_p_text(body[list(body).index(p_git)+1], "https://github.com/mustafakirmizi/finansal-sektor-analiz-sistemi")

    p_commit_sayi = find_p("Bu hafta yaptığınız yaklaşık commit sayısı:")
    set_p_text(body[list(body).index(p_commit_sayi)+1], "3 commit")

    p_commit_onemli = find_p("Bu haftaki önemli commit veya geliştirmeler:")
    set_p_text(body[list(body).index(p_commit_onemli)+1], "- feat: Hafta 2 - CSV veri yukleyici, SQLite veritabani ve cok boyutlu anomali motoru\n- fix: SQLite contextmanager baglanti yonetimi ve WinError 32 dosya kilidi cozumu\n- test: Veritabani ve veri yukleyici icin birim testlerin yazilmasi (8 test OK)")

    p_demo = find_p("Varsa çalışan uygulama / demo bağlantısı:")
    set_p_text(body[list(body).index(p_demo)+1], "Yerel konsol uygulaması ('python main.py' komutuyla CSV'den SQLite'a aktarım ve sektör analiz tablosu canlı çalışmaktadır).")

    p_kod_amac = find_p("Kodun amacı:")
    set_p_text(body[list(body).index(p_kod_amac)+1], "Çok boyutlu Z-Score sapma mesafesini (Multi-dimensional Euclidean Distance) ve negatif özkaynak kuralını hesaplayarak 0-100 bileşik risk skoru üreten FinancialAnomalyDetector.evaluate_risk metodu.")

    p_kod = find_p("Kod:")
    kod_text = (
        "def evaluate_risk(self, comparison_data: Dict[str, Any]) -> Dict[str, Any]:\n"
        "    comparisons = comparison_data.get('comparisons', [])\n"
        "    anomalies, critical_flags = [], []\n"
        "    total_penalty = 0.0\n"
        "    squared_deviations = []\n\n"
        "    for item in comparisons:\n"
        "        cat, metric, val, z = item['category'], item['metric'], item['company_value'], item.get('z_score')\n"
        "        if val is None:\n"
        "            continue\n\n"
        "        # 1. Z-Score Bazlı Sapma Kontrolü (|Z| >= threshold)\n"
        "        if z is not None:\n"
        "            squared_deviations.append(z ** 2)\n"
        "            if abs(z) >= self.z_threshold:\n"
        "                direction = 'Aşırı Yüksek' if z > 0 else 'Aşırı Düşük'\n"
        "                anomalies.append({\n"
        "                    'metric': f'{cat}.{metric}', 'value': val, 'z_score': z,\n"
        "                    'message': f'Sektör ortalamasından {abs(z):.2f} standart sapma kadar {direction}.'\n"
        "                })\n"
        "                total_penalty += min(abs(z) * 5.0, 15.0)\n\n"
        "        # 2. Kritik Kural Eşikleri\n"
        "        if metric == 'current_ratio' and val < 1.0:\n"
        "            critical_flags.append(f'Kritik Likidite Riski: Cari oran ({val}) 1.0 altında.')\n"
        "            total_penalty += 20.0\n"
        "        elif metric == 'financial_leverage' and val > 0.80:\n"
        "            critical_flags.append(f'Yüksek Borçluluk Riski: Kaldıraç oranı ({val}) %80 üzerinde.')\n"
        "            total_penalty += 20.0\n"
        "        elif metric == 'equity_ratio' and val < 0.0:\n"
        "            critical_flags.append('Negatif Özkaynak: Sermaye kaybı ve teknik iflas riski.')\n"
        "            total_penalty += 25.0\n\n"
        "    # 3. Çok Boyutlu Öklid Uzaklığı\n"
        "    multi_dim_distance = 0.0\n"
        "    if squared_deviations:\n"
        "        multi_dim_distance = round(math.sqrt(sum(squared_deviations) / len(squared_deviations)), 2)\n"
        "        if multi_dim_distance > 1.8:\n"
        "            total_penalty += (multi_dim_distance - 1.8) * 10.0\n\n"
        "    risk_score = round(min(max(total_penalty, 0.0), 100.0), 1)\n"
        "    return {\n"
        "        'company_code': comparison_data['company_code'],\n"
        "        'risk_score': risk_score,\n"
        "        'multi_dim_distance': multi_dim_distance,\n"
        "        'anomalies': anomalies,\n"
        "        'critical_flags': critical_flags\n"
        "    }"
    )
    set_p_text(body[list(body).index(p_kod)+1], kod_text)

    p_kod_aciklama = find_p("Kodun nasıl çalıştığını kendi ifadelerinizle açıklayınız:")
    set_p_text(body[list(body).index(p_kod_aciklama)+1], "Bu metot, bir şirketin tüm finansal rasyolarını sektörün ortalamalarıyla kıyaslar. Her bir göstergenin Z-Score değerinin karesini toplayarak çok boyutlu uzayda sektörün merkezinden ne kadar uzaklaşıldığını gösteren ortalama Öklid sapmasını hesaplar. Aynı zamanda cari oranın 1'in altına inmesi, kaldıracın %80'i aşması ve özkaynakların eksiye düşmesi gibi hayati finansal riskleri kontrol ederek ceza puanları uygular. Sonuç olarak 0 ile 100 arasında normalize edilmiş güvenilir bir risk skoru ve tespit edilen anomali listesini üretir.")

    # 8. BÖLÜM 7: ÖĞRENİLEN YENİ BİLGİLER
    set_p_text(body[106], "Python'da sqlite3 kullanırken 'with connection:' bloğunun bağlantıyı kapatmadığını, sadece transaction yönettiğini; bağlantıyı kapatmak için contextlib.contextmanager ve conn.close() yapısının şart olduğunu öğrendim.")
    set_p_text(body[107], "Finansal anomali analizinde tek tek rasyolara bakmanın sektörel özellikleri (örneğin perakendede düşük cari oran) kaçırabileceğini, çok boyutlu uzaklık (Multi-dimensional Euclidean Distance) ile şirketin tüm göstergelerinin bir arada değerlendirilmesinin doğruluğu katbekat artırdığını kavradım.")
    set_p_text(body[108], "CSV dosyalarında Türkçe karakter ve başlık hatalarını önlemek için utf-8-sig kodlamasının ve DictReader ile zorunlu alan doğrulamasının endüstriyel standart olduğunu deneyimledim.")

    p_en_onemli = find_p("Bu bilgilerden sizin için en önemli olanını açıklayınız.")
    set_p_text(body[list(body).index(p_en_onemli)+1], "Veritabanı kaynak yönetiminde (resource management) bağlantıların düzgün kapatılmamasının özellikle dosya tabanlı veritabanlarında (SQLite) işletim sistemi seviyesinde kilitlenmelere yol açtığını ve bunu contextmanager ile temiz şekilde çözmeyi öğrenmekti.")

    p_tekrar_kullanim = find_p("Bu bilgiyi daha sonra benzer bir problemde yeniden kullanabileceğinizi düşünüyor musunuz? Neden?")
    set_p_text(body[list(body).index(p_tekrar_kullanim)+1], "Evet. SQLite veritabanı mimarisi, veri yükleyici şablonu ve çok boyutlu aykırı değer analizi tüm yazılım ve veri bilimi projelerinde doğrudan uygulanabilir standart yöntemlerdir.")

    # 9. BÖLÜM 8: GELECEK HAFTANIN PLANI
    set_p_text(body[117], "Streamlit kütüphanesi kullanarak web tabanlı interaktif görsel analiz dashboard'unun (Arayüz / UI) kodlanması.")
    set_p_text(body[118], "Şirketlerin rasyolarını sektör ortalamalarıyla görselleştiren Radar Grafikleri (Spider Chart) ve Bar Grafikleri bileşenlerinin entegre edilmesi.")
    set_p_text(body[119], "scikit-learn tabanlı Isolation Forest anomali tespit modelinin çok boyutlu veri setimiz üzerinde eğitilerek mevcut Z-Score motoruyla karşılaştırılması.")
    set_p_text(body[120], "Kullanıcının arayüzden yeni bir şirkete ait bilanço verilerini girerek anlık analiz ve risk raporu alabilmesini sağlayan dinamik form ekranının tasarlanması.")

    p_gelecek_oncelik = find_p("Bir sonraki hafta öncelikli olarak çözmeniz gereken problem veya tamamlamanız gereken özellik nedir?")
    set_p_text(body[list(body).index(p_gelecek_oncelik)+1], "Öncelikli hedefim; konsolda çalışan tüm bu analiz çıktısını Streamlit web arayüzüne taşıyarak kullanıcının tek tıkla şirket seçip sektör karşılaştırma grafiklerini ve anomali radarını interaktif görebileceği görsel arayüzü tamamlamaktır.")

    # 10. BÖLÜM 9: YAPAY ZEKA SÜRECİ
    # 9.1
    p_ai_arac = find_p("Kullandığım yapay zekâ araçları:")
    set_p_text(body[list(body).index(p_ai_arac)+1], "Google Gemini, ChatGPT, Antigravity AI Asistanı")

    # 9.2
    p_ai_amac = find_p("Bu hafta yapay zekâyı kullandığım başlıca amaçlar:")
    set_p_text(body[list(body).index(p_ai_amac)+1], "SQLite ilişkisel veritabanı şema tasarımı, Windows SQLite dosya kilitlenme hatasının (WinError 32) çözümü, çok boyutlu Öklid uzaklığı formülasyonu ve CSV veri okuma doğrulama mekanizması.")

    p_ai_en_cok = find_p("Yapay zekâyı en çok hangi konuda kullandınız?")
    set_p_text(body[list(body).index(p_ai_en_cok)+1], "SQLite ilişkisel tablo şeması (foreign key, unique constraint) ve bağlantı yönetiminde contextmanager kullanımı.")

    p_ai_neden = find_p("Neden bu konuda yapay zekâ desteğine ihtiyaç duydunuz?")
    set_p_text(body[list(body).index(p_ai_neden)+1], "Çok tablolu bir yapıda veri bütünlüğünü koruyan ve testlerde dosya kilitleme yapmayan temiz bir Pythonic veritabanı mimarisi kurmak için.")

    # 9.3
    p_ai_denemeler = find_p("Yapay zekâya başvurmadan önce yaptığım denemeler / araştırmalar:")
    set_p_text(body[list(body).index(p_ai_denemeler)+1], "Python resmi SQLite dokümantasyonunu ve unittest yaşam döngüsünü inceledim; testlerde neden dosyanın silinemediğini hata kodundan (WinError 32) araştırdım.")

    # 9.4 PROMPTLAR
    p_pr1 = find_p("Prompt 1")
    idx = list(body).index(p_pr1)
    set_p_text(body[idx+2], "SQLite ile şirketler, finansal tablolar, rasyolar ve anomali sonuçlarını tutacak ilişkisel bir veritabanı sınıfı yazılması.")
    set_p_text(body[idx+5], "'Python sqlite3 ile şirketler, finansal tablolar, rasyolar ve anomali sonuçlarını tutacak ilişkisel bir veritabanı sınıfı yaz. Şirket ve periyot bazında mükerrer kayıtları engelleyecek ON CONFLICT yapıları içersin.'")
    set_p_text(body[idx+8], "SQLite DDL tabloları ve UPSERT sorguları önerdi.")
    set_p_text(body[idx+11], "☐ Doğrudan kullandım.   ☑ Küçük değişiklikler yaptım.   ☐ Büyük ölçüde değiştirdim.   ☐ Yalnızca fikir almak için kullandım.   ☐ Cevabı kullanmadım.")
    set_p_text(body[idx+13], "Tablo sütunlarını ve tiplerini veri modellerimizin yapısına göre düzenledim, raw_json saklama alanını ekledim.")

    p_pr2 = find_p("Prompt 2")
    idx = list(body).index(p_pr2)
    set_p_text(body[idx+2], "unittest çalıştığında SQLite test veritabanının silinememesi (WinError 32 PermissionError).")
    set_p_text(body[idx+5], "'unittest içinde test_database çalıştırırken tearDown metodunda os.remove(db_path) WinError 32 veriyor. with conn bloğu kullanmama rağmen dosya neden kilitli kalıyor ve nasıl çözülür?'")
    set_p_text(body[idx+8], "with sqlite3.connect yapısının bağlantıyı kapatmadığını, sadece commit yaptığını açıkladı ve contextmanager ile close garantisi sağlayan yapıyı sundu.")
    set_p_text(body[idx+11], "☑ Doğrudan kullandım.   ☐ Küçük değişiklikler yaptım.   ☐ Büyük ölçüde değiştirdim.   ☐ Yalnızca fikir almak için kullandım.   ☐ Cevabı kullanmadım.")
    set_p_text(body[idx+13], "Önerilen contextmanager yapısını DatabaseManager sınıfına uyguladım ve test kilitlenme hatası anında çözüldü.")

    p_pr3 = find_p("Prompt 3")
    idx = list(body).index(p_pr3)
    set_p_text(body[idx+2], "Birden fazla rasyodaki sapmayı tek bir çok boyutlu mesafe metriğinde birleştirme.")
    set_p_text(body[idx+5], "'Bir şirketin 14 farklı rasyosunun sektör Z-score değerlerini tek bir çok boyutlu sapma skorunda birleştirmek için matematiksel olarak Öklid normu nasıl uygulanır?'")
    set_p_text(body[idx+8], "Z-skorlarının karelerinin ortalamasının karekökünü (Root Mean Square Z-score) alarak sektör merkezine uzaklığı hesaplama formülü sundu.")
    set_p_text(body[idx+11], "☐ Doğrudan kullandım.   ☑ Küçük değişiklikler yaptım.   ☐ Büyük ölçüde değiştirdim.   ☐ Yalnızca fikir almak için kullandım.   ☐ Cevabı kullanmadım.")
    set_p_text(body[idx+13], "Önerilen çok boyutlu uzaklık formülünü risk motoruna entegre edip eşik değerleri finansal risk seviyelerine göre kalibre ettim.")

    # 9.5
    p_istenen_islem = find_p("Yapay zekâdan istediğiniz işlem:")
    set_p_text(body[list(body).index(p_istenen_islem)+1], "SQLite bağlantısını açıp işlem tamamlandığında güvenli şekilde kapatan get_connection context manager fonksiyonu.")

    p_onerilen_kod = find_p("Yapay zekânın önerdiği kod:")
    set_p_text(body[list(body).index(p_onerilen_kod)+1], "@contextmanager\ndef get_connection(self):\n    conn = sqlite3.connect(self.db_path)\n    conn.row_factory = sqlite3.Row\n    try:\n        yield conn\n    finally:\n        conn.close()")

    p_kod_kendi_ifadeniz = find_p("Bu kodun ne yaptığını kendi ifadelerinizle açıklayınız:")
    set_p_text(body[list(body).index(p_kod_kendi_ifadeniz)+1], "Veritabanı işlemlerinde bağlantıyı açar ve işlem bittiğinde veya beklenmedik bir hata fırlatıldığında finally bloğu ile bağlantıyı mutlaka kapatır; Windows üzerinde dosya kilitleme oluşmasını engeller.")

    p_degisiklik = find_p("Kod üzerinde yaptığınız değişiklikler:")
    set_p_text(body[list(body).index(p_degisiklik)+1], "Bağlantıya conn.row_factory = sqlite3.Row ayarını ekleyerek sonuçların sözlük gibi sütun isimleriyle okunabilmesini sağladım.")

    # 9.6
    p_tespit_hata = find_p("Evet ise tespit ettiğiniz hata:")
    set_p_text(body[list(body).index(p_tespit_hata)+1], "Yapay zekanın ilk önerdiği CSV okuyucuda Türkçe karakterli sütunlarda (ş, ı, ğ) UTF-8 BOM kaynaklı ilk sütun adı okuma hatası oluşuyordu.")

    p_hata_duzeltme = find_p("Hatayı nasıl düzelttiniz?")
    set_p_text(body[list(body).index(p_hata_duzeltme)+1], "CSV dosyası açılırken encoding='utf-8' yerine encoding='utf-8-sig' parametresi verilerek BOM karakteri temizlendi ve DictReader ile tam uyum sağlandı.")

    # 9.7
    p_en_onemli_prob = find_p("Karşılaştığınız en önemli problem:")
    set_p_text(body[list(body).index(p_en_onemli_prob)+1], "Yapay zekanın ilk etapta veritabanı için gereksiz yere ağır bir harici ORM kütüphanesi (SQLAlchemy) önermesi.")

    p_prob_cozum = find_p("Bu problemi nasıl çözdünüz?")
    set_p_text(body[list(body).index(p_prob_cozum)+1], "Projeyi hafif, hızlı ve harici bağımlılıksız tutmak adına Python'ın yerleşik sqlite3 kütüphanesiyle temiz bir DatabaseManager sınıfı yazdım.")

    # 9.10
    p_yz_oran = find_p("Tahmini yapay zekâ kullanım oranım:")
    set_p_text(p_yz_oran, "Tahmini yapay zekâ kullanım oranım: % 30", bold=True)

    p_yz_kod_oran = find_p("Tahmini oran: % ………")
    if p_yz_kod_oran is not None:
        set_p_text(p_yz_kod_oran, "Tahmini oran: % 25", bold=True)

    p_secenek_neden = find_p("Bu seçeneği neden işaretlediğinizi açıklayınız:")
    set_p_text(body[list(body).index(p_secenek_neden)+1], "Mimariyi, veri tablolarını, perakende sektörü risk kalibrasyonunu ve test senaryolarını kendim tasarladım. Yapay zekayı sadece bağlantı hatası debugging'i ve SQL UPSERT syntax desteği için danışman olarak kullandım.")

    # 9.11
    p_genel_deg = find_p("Genel değerlendirme:")
    genel_text_2 = (
        "Bu hafta yapay zekâ, özellikle veritabanı şemasının optimizasyonu ve Windows ortamındaki dosya kilitleme (WinError 32) sorununun çözülmesinde bana ciddi zaman kazandırdı. "
        "Bununla birlikte finansal mantık, perakende sektöründeki negatif işletme sermayesi kalibrasyonu ve veri yükleyici doğrulamaları tamamen kendi denetimimde şekillendirildi. "
        "Yapay zekanın önerdiği kodların iç mantığını ve işletim sistemi seviyesindeki etkilerini anlayarak kullandım; bu sayede projenin arka uç güvenilirliği ve test kapsamı en üst seviyeye ulaştı."
    )
    set_p_text(body[list(body).index(p_genel_deg)+1], genel_text_2)

    # 9.12
    p_kanit_acikla = find_p("Eklediğiniz kanıtları kısaca açıklayınız:")
    kanit_text_2 = (
        "1. src/database.py (SQLite DatabaseManager ve contextmanager bağlantı yönetimi)\n"
        "2. src/data_loader.py (CSV/JSON ayrıştırıcı ve şema doğrulama)\n"
        "3. src/anomaly_detector.py (Çok boyutlu Öklid uzaklığı metriği)\n"
        "4. tests/ klasöründeki 8 adet başarılı birim test çıktısı (Ran 8 tests in 0.062s - OK)"
    )
    set_p_text(body[list(body).index(p_kanit_acikla)+1], kanit_text_2)

    # 10. BÖLÜM 10
    p_en_basarili = find_p("Bu hafta en başarılı olduğunuz konu:")
    set_p_text(body[list(body).index(p_en_basarili)+1], "SQLite veritabanı ile dosya yükleme katmanını sıfır dış bağımlılıkla ve tüm birim testlerden başarıyla geçecek şekilde entegre etmek.")

    p_en_zor = find_p("En fazla zorlandığınız konu:")
    set_p_text(body[list(body).index(p_en_zor)+1], "Windows üzerinde SQLite bağlantılarının açık kalarak dosya kilidi oluşturması ve perakende sektöründeki yapısal bilanço farklılıklarının anomali puanına etkisi.")

    p_farkli = find_p("Bu hafta tekrar çalışma fırsatınız olsaydı farklı yapacağınız şey:")
    set_p_text(body[list(body).index(p_farkli)+1], "Veritabanı bağlantılarını en başından contextmanager ile tasarlamak.")

    p_puan = find_p("9 / 10")
    if p_puan is None:
        p_puan = find_p("…… / 10")
    if p_puan is not None:
        set_p_text(p_puan, "9.5 / 10", bold=True)

    p_puan_neden = find_p("Neden?")
    for p in body[list(body).index(p_puan):list(body).index(p_puan)+4]:
        if "Neden?" in ''.join(p.itertext()):
            set_p_text(body[list(body).index(p)+1], "Planlanan tüm veri yükleme, SQLite kalıcılık, çok boyutlu anomali analizi ve test hedefleri eksiksiz tamamlandı; sistem uçtan uca hatasız çalışmaktadır.")
            break

    # Save to zip
    new_xml = ET.tostring(tree, encoding='utf-8', xml_declaration=True)
    all_files['word/document.xml'] = new_xml

    with zipfile.ZipFile(dest_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for name, data in all_files.items():
            zout.writestr(name, data)
    print(f"Hafta 2 Raporu başarıyla oluşturuldu: {dest_docx}")

if __name__ == "__main__":
    main()
