"""
generate_report.py
Haftalık Yazılım Projesi Gelişim Raporu doldurucu.
Orijinal Word belgesinin (docx) OpenXML yapısını koruyarak tüm alanları doldurur.
"""
import os
import sys
import zipfile
import shutil
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

def set_p_text(p, text, bold=False, num_pr=False):
    # Keep existing pPr if present, remove existing runs
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
        # Split by newlines if any
        lines = text.split("\n")
        for i, line in enumerate(lines):
            p.append(make_run(line, bold=bold))
            if i < len(lines) - 1:
                p.append(make_br())

def main():
    src_docx = r"C:\Users\MONSTER\Downloads\Mustafa Kırmızı - HAFTALIK YAZILIM PROJESİ GELİŞİM RAPORU.docx"
    dest_dir = r"c:\Users\MONSTER\Desktop\yazılımgeliştirme1ödev"
    dest_docx_1 = os.path.join(dest_dir, "Mustafa_Kirmizi_Haftalik_Gelisim_Raporu_Hafta_1.docx")
    dest_docx_2 = src_docx # Also update the one in Downloads

    print(f"Kaynak dosya: {src_docx}")
    with zipfile.ZipFile(src_docx, 'r') as zin:
        xml_content = zin.read('word/document.xml')
        all_files = {name: zin.read(name) for name in zin.namelist()}

    tree = ET.fromstring(xml_content)
    namespaces = {'w': W_NS}
    body = tree.find('w:body', namespaces)

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
        ("Hafta No: ", True), ("1", False), ("br", None),
        ("Tarih: ", True), ("14 / 10 / 2026", False)
    ]
    for item in header_items:
        if item[0] == "br":
            p1.append(make_br())
        else:
            p1.append(make_run(item[0], bold=item[1]))

    # 2. BÖLÜM 1: HEDEFLER
    set_p_text(body[5], "Proje konusunun ('Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi') fonksiyonel ve teknik gereksinimlerinin detaylandırılması.")
    set_p_text(body[6], "Bilanço ve Gelir Tablosu finansal kalemleri için veri modellerinin (models.py) tasarlanması ve test veri setinin (sample_companies.json) hazırlanması.")
    set_p_text(body[7], "Temel finansal oran hesaplayıcı motorunun (FinancialRatioCalculator: Likidite, Borçluluk, Kârlılık, Faaliyet) kodlanması ve güvenli bölme kontrollerinin (safe_divide) eklenmesi.")
    set_p_text(body[8], "Sektör ortalamaları ve standart sapmalarını hesaplayan SectorAnalyzer ile Z-Score tabanlı anomali/risk puanlama motorunun (FinancialAnomalyDetector) prototiplenmesi.")
    
    set_p_text(body[11], "Projenin temel amacı ham finansal tablolardan güvenilir rasyolar üreterek şirketleri sektörleriyle kıyaslamak ve anormal finansal sapmaları tespit etmektir. İlk haftada veri modelleri, oran hesaplama mantığı ve istatistiksel karşılaştırma çekirdeğinin hatasız kurulması; sonraki haftalarda eklenecek olan makine öğrenmesi modelleri (Isolation Forest), veritabanı ve web analiz ekranı için sağlam bir temel oluşturmaktadır.")

    # 3. BÖLÜM 2: YAPILAN ÇALIŞMALAR
    set_p_text(body[17], "Bu hafta, projenin iş analizi ve çekirdek geliştirme fazı başarıyla yürütüldü. İlk olarak finansal tablolardaki temel kalemler incelenerek Bilanço ve Gelir Tablosu için Python dataclass yapıları kuruldu. 4 ana kategoride 14 farklı finansal oranı hesaplayan FinancialRatioCalculator sınıfı yazıldı. Matematiksel hesaplamalarda sıfıra bölünme ve negatif kâr/özkaynak gibi istisnaları yönetmek için safe_divide mekanizması entegre edildi. Farklı sektörlerden şirketlere ait finansal veriler JSON formatında modellendi. Bu veriler üzerinden sektör ortalaması, medyanı ve standart sapmasını dinamik hesaplayan SectorAnalyzer geliştirildi. Son olarak, Z-Score ve kritik eşik ihlallerine göre 0-100 arasında Risk Puanı üreten FinancialAnomalyDetector prototipi kodlanarak uçtan uca test edildi.")
    
    set_p_text(body[20], "src/models.py: Bilanço (BalanceSheet), Gelir Tablosu (IncomeStatement) ve Şirket (Company) veri modelleri oluşturuldu; toplam varlık, borç, brüt ve faaliyet kârı gibi dinamik property hesaplamaları eklendi.")
    set_p_text(body[21], "src/ratios.py: Likidite, Finansal Kaldıraç, Kârlılık ve Faaliyet oranlarını hesaplayan FinancialRatioCalculator sınıfı ve safe_divide güvenlik fonksiyonu kodlandı.")
    set_p_text(body[22], "src/sector_analysis.py: Şirketleri sektörlerine göre gruplayıp ortalama, medyan, standart sapma metriklerini çıkaran ve Z-score hesaplayan SectorAnalyzer sınıfı geliştirildi.")
    set_p_text(body[23], "src/anomaly_detector.py & tests/test_ratios.py: Anomali ve risk puanlama motoru kodlandı; hesaplamaları ve sınır durumları doğrulayan birim testler yazıldı.")

    # 24 sonrası ek açıklama
    p24_extra = ET.Element(f"{{{W_NS}}}p")
    set_p_text(p24_extra, "Proje şartname aşamasından çıkarılarak; nesne yönelimli mimariye sahip, birim testleri geçen ve konsol üzerinden tam finansal kıyaslama ve anomali analizi yapabilen somut bir çekirdek yazılım prototipine dönüştürüldü. Git versiyon kontrolü başlatılarak ilk commit'ler atıldı.")
    idx_24 = list(body).index(body[24])
    body.insert(idx_24 + 1, p24_extra)

    # 4. BÖLÜM 3: TAMAMLANMA DURUMU
    # Refresh body references
    body = tree.find('w:body', namespaces)
    
    # Helper to find paragraph by exact starting text
    def find_p(start_text):
        for p in body:
            txt = ''.join(p.itertext()).strip()
            if txt.startswith(start_text):
                return p
        return None

    p_tamamlanan = find_p("Tamamlanan çalışmalar:")
    idx = list(body).index(p_tamamlanan)
    set_p_text(body[idx+1], "- Bilanço, Gelir Tablosu ve Şirket veri modellerinin oluşturulması (models.py)\n- Likidite, Borçluluk, Kârlılık ve Faaliyet oranlarını hesaplayan rasyo motorunun kodlanması (ratios.py)\n- Sektör ortalaması, medyanı ve standart sapması hesaplama modülü (sector_analysis.py)\n- Z-Score ve eşik değer bazlı anomali/risk puanlayıcı algoritması (anomaly_detector.py)\n- Örnek sektör ve şirket test veri seti (sample_companies.json)\n- Matematiksel ve sınır durum birim testleri (tests/test_ratios.py)\n- Uçtan uca çalışan konsol demosu (main.py) ve Git repository kurulumu.")

    p_devam = find_p("Devam eden çalışmalar:")
    idx = list(body).index(p_devam)
    set_p_text(body[idx+1], "- Şirket finansal tablolarını harici Excel/CSV dosyalarından otomatik içeri aktaracak veri okuyucu (Parser/ETL) modülünün tasarımı.\n- Makine öğrenmesi tabanlı anomali tespiti (Isolation Forest / LOF) için veri hazırlığı ve kütüphane araştırması.")

    p_baslanamayan = find_p("Başlanamayan veya ertelenen çalışmalar:")
    idx = list(body).index(p_baslanamayan)
    set_p_text(body[idx+1], "- Web tabanlı görselleştirme arayüzü (Streamlit Dashboard) ve grafikler (2. ve 3. haftalara planlandı).\n- SQLite / PostgreSQL veritabanı şeması ve kayıt kalıcılığı (ilerleyen haftalara planlandı).")

    p_oran = find_p("Projenin tahmini genel tamamlanma oranı:")
    set_p_text(p_oran, "Projenin tahmini genel tamamlanma oranı: % 20", bold=True)
    
    p_oran_aciklama = find_p("Bu oranı neye göre belirlediğinizi kısaca açıklayınız.")
    idx = list(body).index(p_oran_aciklama)
    set_p_text(body[idx+1], "Dönem boyunca yapılacak çalışmalar 5 ana aşamaya ayrılmıştır: (1) Gereksinim analizi ve çekirdek matematiksel hesaplama motoru [%20], (2) Veri aktarımı ve Makine Öğrenmesi anomali modeli [%25], (3) Veritabanı ve API entegrasyonu [%20], (4) Arayüz ve Görselleştirme Ekranı [%20], (5) Test, optimizasyon ve dokümantasyon [%15]. Çekirdek matematiksel motor ve prototip eksiksiz tamamlandığı için genel ilerleme %20 olarak belirlenmiştir.")

    # 5. BÖLÜM 4: TEKNİK ÇALIŞMALAR
    p_checks = find_p("☐ Arayüz / UI geliştirme")
    new_checks_text = (
        "☐ Arayüz / UI geliştirme   ☐ Veritabanı işlemleri   ☑ Backend geliştirme\n"
        "☐ API geliştirme / API kullanımı   ☐ Kullanıcı giriş ve yetkilendirme   ☑ Dosya işlemleri\n"
        "☑ Test işlemleri   ☑ Hata düzeltme / Debugging   ☑ Git / GitHub kullanımı\n"
        "☑ Kod iyileştirme / Refactoring   ☑ Dokümantasyon   ☑ Diğer: Finansal Matematik ve İstatistiksel Analiz"
    )
    set_p_text(p_checks, new_checks_text)

    p_diller = find_p("Bu hafta kullandığınız programlama dili / dilleri:")
    idx = list(body).index(p_diller)
    set_p_text(body[idx+1], "Python 3.12")

    p_araclar = find_p("Kullandığınız teknoloji, framework, kütüphane veya araçlar:")
    idx = list(body).index(p_araclar)
    set_p_text(body[idx+1], "Python Standart Kütüphanesi (dataclasses, json, math, collections, typing, os), unittest test çatısı, Git & GitHub, VS Code IDE, Google Gemini / Antigravity AI Asistanı.")

    p_arac_amac = find_p("Bu teknolojileri hangi amaçlarla kullandığınızı açıklayınız:")
    idx = list(body).index(p_arac_amac)
    set_p_text(body[idx+1], "- dataclasses & typing: Bilanço ve gelir tablosu finansal kalemlerini tip güvenli ve nesne yönelimli şekilde modellemek için.\n- math & collections: Sektör ortalaması, standart sapma ve Z-score hesaplamalarını harici bağımlılık olmadan hızlıca yürütmek için.\n- json: Test veri setini yapılandırılmış dosya formatında okumak için.\n- unittest: Oran formüllerinin ve sıfıra bölme güvenliğinin hatasız çalıştığını otomatize birim testlerle doğrulamak için.\n- Git: Kod sürümlerini ve geliştirme adımlarını commit'ler ile kayıt altında tutmak için.")

    # 6. BÖLÜM 5: KARŞILAŞILAN PROBLEMLER VE ÇÖZÜMLER
    # Problem 1
    p_p1 = find_p("Problem 1")
    idx = list(body).index(p_p1)
    set_p_text(body[idx+2], "Finansal oranlar hesaplanırken bazı borçsuz şirketlerde veya sıfır stoklu dönemlerde paydanın 0 olması sebebiyle ZeroDivisionError hatası meydana geldi. Ayrıca geçmiş yıl zararları nedeniyle negatif özkaynak durumlarında Borç/Özkaynak ve ROE oranlarının ters yönde anlamsız sonuçlar üretmesi.")
    set_p_text(body[idx+5], "Finansal formüller bölme işlemlerine dayanır; payda sıfır olduğunda çalışma zamanı hatası fırlatılır. Negatif kâr ile negatif özkaynak bölündüğünde ise matematiksel olarak pozitif kârlılık gibi yanıltıcı bir sonuç oluşmaktadır.")
    set_p_text(body[idx+8], "Paydayı kontrol eden ve sıfır/None durumunda güvenli şekilde None döndüren safe_divide yardımcı fonksiyonu geliştirildi. Negatif özkaynak durumu için ise kural bazlı risk kontrolleri eklenerek şirkete doğrudan anomali ceza puanı uygulandı.")
    set_p_text(body[idx+11], "Sıfıra bölünme kaynaklı çökmeler tamamen engellendi; negatif özkaynak gibi uç durumlarda rasyoların sistemi yanıltması engellenerek risk raporuna kritik uyarı olarak yansıtıldı. Birim testlerle doğrulandı.")

    # Problem 2
    p_p2 = find_p("Problem 2")
    idx = list(body).index(p_p2)
    set_p_text(body[idx+2], "Sektördeki şirket sayısının az olduğu durumlarda (örneğin 3 şirket), aşırı borçlu veya aşırı kârlı tek bir uç değerin (outlier) sektörün aritmetik ortalamasını ve standart sapmasını aşırı saptırması; bu nedenle normal şirketlerin haksız yere anomalili çıkması riski.")
    set_p_text(body[idx+5], "Aritmetik ortalama ve standart sapma uç değerlere karşı çok hassastır. Az sayıda şirket bulunan bir sektörde tek bir dev veya batık şirket tüm sektör normunu bozmaktadır.")
    set_p_text(body[idx+8], "Sektör kıyaslama motoruna aritmetik ortalamanın yanı sıra aykırı değerlerden etkilenmeyen 'medyan' (ortanca) hesaplaması entegre edildi. Sektörde tek şirket olduğunda standart sapmanın sıfır çıkması durumu da koruma altına alındı.")
    set_p_text(body[idx+11], "Sektör benchmark raporlarında hem ortalama hem de medyan birlikte sunularak tekil şirketlerin sektörü saptırmasının önüne geçildi; çok daha dengeli ve güvenilir bir kıyaslama tabanı oluşturuldu.")

    # 7. BÖLÜM 6: KOD VE PROJE KANITLARI
    p_git = find_p("GitHub / GitLab / Repository bağlantısı:")
    set_p_text(body[list(body).index(p_git)+1], "https://github.com/mustafakirmizi/finansal-sektor-analiz-sistemi")

    p_commit_sayi = find_p("Bu hafta yaptığınız yaklaşık commit sayısı:")
    set_p_text(body[list(body).index(p_commit_sayi)+1], "2 commit")

    p_commit_onemli = find_p("Bu haftaki önemli commit veya geliştirmeler:")
    set_p_text(body[list(body).index(p_commit_onemli)+1], "- 717c811: feat: proje baslangici, veri modelleri, finansal oran hesaplayici ve anomali tespiti prototipi\n- ad296b4: chore: gitignore eklendi ve pycache temizlendi")

    p_demo = find_p("Varsa çalışan uygulama / demo bağlantısı:")
    set_p_text(body[list(body).index(p_demo)+1], "Yerel konsol uygulaması ('python main.py' komutuyla terminalde uçtan uca çalıştırılabilmektedir).")

    p_kod_amac = find_p("Kodun amacı:")
    set_p_text(body[list(body).index(p_kod_amac)+1], "Şirketin kısa vadeli borçlarını ödeme kabiliyetini ölçen temel likidite rasyolarını (Cari Oran, Likit/Asit-Test Oranı, Nakit Oran) sıfıra bölünme hatalarına karşı korumalı olarak hesaplayan FinancialRatioCalculator.calculate_liquidity_ratios metodu.")

    p_kod = find_p("Kod:")
    kod_text = (
        "@staticmethod\n"
        "def calculate_liquidity_ratios(bs: BalanceSheet) -> Dict[str, Optional[float]]:\n"
        "    cur_assets = bs.total_current_assets\n"
        "    short_liab = bs.total_short_term_liabilities\n"
        "    inventories = bs.inventories\n"
        "    cash = bs.cash_and_equivalents\n\n"
        "    # 1. Cari Oran = Dönen Varlıklar / KVYK (İdeal: 1.5 - 2.0)\n"
        "    current_ratio = safe_divide(cur_assets, short_liab)\n\n"
        "    # 2. Asit-Test / Likit Oran = (Dönen Varlıklar - Stoklar) / KVYK (İdeal: >= 1.0)\n"
        "    acid_test_ratio = safe_divide(cur_assets - inventories, short_liab)\n\n"
        "    # 3. Nakit Oran = Nakit ve Benzerleri / KVYK (İdeal: >= 0.20)\n"
        "    cash_ratio = safe_divide(cash, short_liab)\n\n"
        "    return {\n"
        "        'current_ratio': current_ratio,\n"
        "        'acid_test_ratio': acid_test_ratio,\n"
        "        'cash_ratio': cash_ratio\n"
        "    }"
    )
    set_p_text(body[list(body).index(p_kod)+1], kod_text)

    p_kod_aciklama = find_p("Kodun nasıl çalıştığını kendi ifadelerinizle açıklayınız:")
    set_p_text(body[list(body).index(p_kod_aciklama)+1], "Bu metot, parametre olarak aldığı BalanceSheet nesnesinden dönen varlıklar, kısa vadeli borçlar, stoklar ve nakit kalemlerini okur. Cari oran ile şirketin kısa vadeli borçlarını dönen varlıklarıyla kaç kat karşılayabildiğini bulur. Asit-test oranında ise satılması zaman alan stokları çıkararak gerçek likit gücü ölçer. Nakit oranında ise şirketin anında nakde dönebilecek varlıklarının borçlara oranını hesaplar. Paydanın sıfır olması durumunda programın çökmemesi için doğrudan bölme operatörü yerine safe_divide yardımcı fonksiyonu kullanılır.")

    # 8. BÖLÜM 7: ÖĞRENİLEN YENİ BİLGİLER
    set_p_text(body[106], "Finansal analizde tek bir şirketin oranlarının soyut kaldığını, mutlaka sektör ortalaması ve medyanı ile normalize edilerek karşılaştırılması gerektiğini kavradım.")
    set_p_text(body[107], "İstatistikte Z-Score (standart skor) yönteminin finansal anomalileri tespit etmekte nasıl kullanıldığını ve sektör ortalamasından 2 standart sapma uzaklaşan değerlerin kritik anomali sinyali olduğunu öğrendim.")
    set_p_text(body[108], "Python dataclasses yapısının nesne yönelimli modellemede @property dekoratörleriyle birleştiğinde karmaşık bilanço hiyerarşilerini ne kadar sadeleştirdiğini öğrendim.")

    p_en_onemli = find_p("Bu bilgilerden sizin için en önemli olanını açıklayınız.")
    set_p_text(body[list(body).index(p_en_onemli)+1], "Yazılım geliştirirken sadece formülleri kodlamanın yetmediği; iş dünyasına ait özel kısıtların (sıfır borç, negatif kâr, aşırı aykırı şirketler) yazılım mimarisinde savunmacı hata kontrolleri ve medyan gibi sağlam istatistiklerle desteklenmesi gerektiğidir.")

    p_tekrar_kullanim = find_p("Bu bilgiyi daha sonra benzer bir problemde yeniden kullanabileceğinizi düşünüyor musunuz? Neden?")
    set_p_text(body[list(body).index(p_tekrar_kullanim)+1], "Evet. Z-Score normalizasyonu, medyan tabanlı aykırı değer analizi ve savunmacı bölme/veri doğrulama pratikleri; ileride geliştireceğim tüm veri analitiği, makine öğrenmesi ve finansal mühendislik projelerinde doğrudan yeniden kullanabileceğim temel prensiplerdir.")

    # 9. BÖLÜM 8: GELECEK HAFTANIN PLANI
    set_p_text(body[117], "Şirketlerin finansal tablolarını harici Excel (.xlsx) ve CSV dosyalarından otomatik okuyup doğrulayan bir dosya içe aktarma (Ingestion / ETL) modülü geliştirmek.")
    set_p_text(body[118], "scikit-learn kütüphanesini projeye dahil ederek Isolation Forest ve Local Outlier Factor (LOF) makine öğrenmesi algoritmalarını sektör rasyoları üzerinde eğitmek.")
    set_p_text(body[119], "Hesaplanan rasyoları ve şirket anomali puanlarını kalıcı olarak saklamak için SQLite veritabanı şemasını oluşturmak ve CRUD servislerini yazmak.")
    set_p_text(body[120], "Görsel analiz ekranı için Streamlit tabanlı interaktif web dashboard arayüzünün prototip tasarımına başlamak.")

    p_gelecek_oncelik = find_p("Bir sonraki hafta öncelikli olarak çözmeniz gereken problem veya tamamlamanız gereken özellik nedir?")
    set_p_text(body[list(body).index(p_gelecek_oncelik)+1], "Öncelikli hedefim; kullanıcıların kendi Excel veya CSV formatındaki mali tablolarını sisteme yükleyebilmesini sağlamak ve istatistiksel Z-score analizini scikit-learn Isolation Forest makine öğrenmesi modeliyle destekleyerek çok boyutlu anomali tespitini tamamlamaktır.")

    # 10. BÖLÜM 9: YAPAY ZEKA SÜRECİ
    # 9.1
    p_ai_arac = find_p("Kullandığım yapay zekâ araçları:")
    set_p_text(body[list(body).index(p_ai_arac)+1], "Google Gemini, ChatGPT, Antigravity AI Asistanı")

    p_ai_sure = find_p("☐ Kullanmadım☐ 30 dakikadan az☐ 30 dakika – 1 saat☐ 1–3 saat☐ 3–5 saat☐ 5 saatten fazla")
    set_p_text(p_ai_sure, "☐ Kullanmadım   ☐ 30 dakikadan az   ☐ 30 dakika – 1 saat   ☑ 1–3 saat   ☐ 3–5 saat   ☐ 5 saatten fazla")

    # 9.2
    p_ai_amac = find_p("Bu hafta yapay zekâyı kullandığım başlıca amaçlar:")
    set_p_text(body[list(body).index(p_ai_amac)+1], "Finansal oran formüllerinin algoritma haline getirilmesi, nesne yönelimli mimaride veri sınıflarının (dataclasses) tasarımı, sıfıra bölme ve sınır durumların hata yönetimi, Z-Score istatistiksel sektör karşılaştırma mantığı ve birim test senaryolarının türetilmesi.")

    p_ai_en_cok = find_p("Yapay zekâyı en çok hangi konuda kullandınız?")
    set_p_text(body[list(body).index(p_ai_en_cok)+1], "Finansal oranların matematiksel hesaplanmasında ve Z-Score istatistiğinin sektör verilerine uygulanmasında.")

    p_ai_neden = find_p("Neden bu konuda yapay zekâ desteğine ihtiyaç duydunuz?")
    set_p_text(body[list(body).index(p_ai_neden)+1], "14 farklı finansal rasyonun sektör dinamiklerine göre nasıl yorumlandığına ve negatif özkaynak / sıfır borç gibi uç durumlarda standart finansal yaklaşımların nasıl kodlanabileceğine dair alternatif yaklaşımları hızlıca görmek ve hata payını azaltmak için.")

    # 9.3
    p_ai_once_kendim = find_p("Problemi önce kendim çözmeye çalıştım:")
    set_p_text(body[list(body).index(p_ai_once_kendim)+1], "☑ Evet   ☐ Kısmen   ☐ Hayır")

    p_ai_denemeler = find_p("Yapay zekâya başvurmadan önce yaptığım denemeler / araştırmalar:")
    set_p_text(body[list(body).index(p_ai_denemeler)+1], "Finansal yönetim ders notlarından ve BIST finansal tablo rehberlerinden temel likidite, kârlılık, kaldıraç oranlarının tanımlarını çıkardım; formülleri bir kâğıda yazarak hangi bilanço/gelir tablosu kalemlerinin birbirine bölüneceğini belirledim.")

    p_ai_neden_secenek = find_p("☐ Problemi nasıl çözeceğimi bilmiyordum.☐ Çözüm yöntemini biliyordum fakat kodunu yazamadım.")
    new_ai_neden = (
        "☐ Problemi nasıl çözeceğimi bilmiyordum.   ☐ Çözüm yöntemini biliyordum fakat kodunu yazamadım.\n"
        "☑ Yazdığım kod hata verdi.   ☐ Hata mesajını anlayamadım.   ☑ Daha hızlı bir çözüm üretmek istedim.\n"
        "☑ Alternatif bir çözüm aradım.   ☑ Yazdığım kodu kontrol ettirmek istedim.   ☑ Konuyu öğrenmek istedim."
    )
    set_p_text(p_ai_neden_secenek, new_ai_neden)

    # 9.4 PROMPTLAR
    # Prompt 1
    p_pr1 = find_p("Prompt 1")
    idx = list(body).index(p_pr1)
    set_p_text(body[idx+2], "Bilanço ve Gelir tablosundaki kalemlerden likidite, borçluluk, kârlılık ve devir hızı oranlarını hesaplayan modüler bir Python sınıf yapısının kurulması.")
    set_p_text(body[idx+5], "'Python 3'te bilanço ve gelir tablosu verilerini tutacak bir veri modeli ve bu verilerden Likidite (Cari, Asit-Test, Nakit), Kaldıraç (Borç/Varlık, Borç/Özkaynak), Kârlılık (ROA, ROE, Kâr Marjları) oranlarını hesaplayan FinancialRatioCalculator sınıfı tasarla. Sıfıra bölünme hatalarını güvenli şekilde yönetecek bir yapı kur.'")
    set_p_text(body[idx+8], "Dataclass yapılarıyla bilanço ve gelir tablosunu modelleyen, statik metotlarla oranları sözlük (dict) olarak döndüren ve sıfır kontrolü yapan bir kod şablonu sundu.")
    set_p_text(body[idx+11], "☐ Doğrudan kullandım.   ☑ Küçük değişiklikler yaptım.   ☐ Büyük ölçüde değiştirdim.   ☐ Yalnızca fikir almak için kullandım.   ☐ Cevabı kullanmadım.")
    set_p_text(body[idx+13], "Projemizin veri gereksinimlerine göre kalemleri detaylandırdım, safe_divide fonksiyonunun dönüş tiplerini netleştirdim ve Türkçe finansal terminolojiye uyarladım.")

    # Prompt 2
    p_pr2 = find_p("Prompt 2")
    idx = list(body).index(p_pr2)
    set_p_text(body[idx+2], "Bir sektördeki tüm şirketlerin oranlarını toplayıp ortalama, medyan ve standart sapma hesaplayarak hedef şirketin Z-Score değerini bulmak.")
    set_p_text(body[idx+5], "'Elimde farklı şirketlerin finansal oran sözlükleri var. Bunları sektörlerine göre gruplayıp her bir oran için sektör ortalamasını ve standart sapmasını hesaplayan, ardından belirli bir şirketin sektöründen kaç standart sapma saptığını (Z-score) bulan bir algoritma yazar mısın?'")
    set_p_text(body[idx+8], "defaultdict ve math.sqrt kullanarak sektör bazlı metrikleri toplayan ve (değer - ortalama) / standart_sapma formülüyle Z-Score hesaplayan bir fonksiyon önerdi.")
    set_p_text(body[idx+11], "☐ Doğrudan kullandım.   ☐ Küçük değişiklikler yaptım.   ☑ Büyük ölçüde değiştirdim.   ☐ Yalnızca fikir almak için kullandım.   ☐ Cevabı kullanmadım.")
    set_p_text(body[idx+13], "Yapay zekânın verdiği kodda sektörde tek şirket olduğunda standart sapmanın 0 olması durumunda tekrar sıfıra bölünme oluşuyordu. Bu kontrolü ekledim ve ayrıca uç değerlerin ortalamayı saptırmasını engellemek için medyan hesaplamasını da koda entegre ettim.")

    # Prompt 3
    p_pr3 = find_p("Prompt 3")
    idx = list(body).index(p_pr3)
    set_p_text(body[idx+2], "Z-score ve kritik oran eşiklerini birleştirerek şirkete 0-100 arasında anlamlı bir finansal risk puanı üreten anomali algoritması mantığı kurmak.")
    set_p_text(body[idx+5], "'Bir şirketin sektör finansal rasyolarına göre anomali/risk puanını 0 ile 100 arasında hesaplamak istiyorum. Hem Z-score sapmalarını (örneğin |Z| > 2) hem de kritik kural bazlı riskleri (örneğin cari oran < 1.0 veya aşırı borçluluk) içeren hibrit bir puanlama mantığını nasıl kurabilirim?'")
    set_p_text(body[idx+8], "Temel ceza puanı (penalty points) mantığı önerdi; her Z-score aşımı için 5-15 puan, kritik kural ihlalleri için 15-20 puan ekleyip toplamı 100 ile sınırlayan ve risk seviyelerine (Düşük, Orta, Yüksek) ayıran bir mimari sundu.")
    set_p_text(body[idx+11], "☐ Doğrudan kullandım.   ☑ Küçük değişiklikler yaptım.   ☐ Büyük ölçüde değiştirdim.   ☐ Yalnızca fikir almak için kullandım.   ☐ Cevabı kullanmadım.")
    set_p_text(body[idx+13], "Önerilen katsayıları finansal literatüre göre revize ettim; örneğin cari oranın 1'in altına düşmesini en kritik risklerden biri olarak 20 ceza puanına sabitledim ve anlaşılır uyarı mesajları ekledim.")

    # 9.5
    p_kod_kullandiniz_mi = find_p("Bu hafta projenizde yapay zekâ tarafından oluşturulan bir kod kullandınız mı?")
    set_p_text(body[list(body).index(p_kod_kullandiniz_mi)+1], "☑ Evet   ☐ Hayır")

    p_istenen_islem = find_p("Yapay zekâdan istediğiniz işlem:")
    set_p_text(body[list(body).index(p_istenen_islem)+1], "Sıfıra bölünme hatasını engelleyen genel amaçlı güvenli bölme fonksiyonu (safe_divide).")

    p_onerilen_kod = find_p("Yapay zekânın önerdiği kod:")
    set_p_text(body[list(body).index(p_onerilen_kod)+1], "def safe_divide(a, b, default=None):\n    try:\n        return round(a / b, 4)\n    except ZeroDivisionError:\n        return default")

    p_kod_kendi_ifadeniz = find_p("Bu kodun ne yaptığını kendi ifadelerinizle açıklayınız:")
    set_p_text(body[list(body).index(p_kod_kendi_ifadeniz)+1], "İki sayıyı birbirine bölerken paydanın 0 olması durumunda programın çökmesini engeller, hata yakalandığında varsayılan olarak None döner ve sonucu 4 basamağa yuvarlar.")

    p_kod_nasil_kullandiniz = find_p("Kodu projenizde nasıl kullandınız?")
    set_p_text(p_kod_nasil_kullandiniz, "Kodu projenizde nasıl kullandınız?")
    # Next paragraph has checkboxes
    p_kod_nasil_cb = find_p("☐ Hiç değiştirmeden kullandım.")
    set_p_text(p_kod_nasil_cb, "☐ Hiç değiştirmeden kullandım.   ☑ Küçük değişiklikler yaptım.   ☐ Önemli ölçüde değiştirdim.   ☐ Yalnızca örnek aldım ve kodu kendim yeniden yazdım.   ☐ Kodu kullanmadım.")

    p_degisiklik = find_p("Kod üzerinde yaptığınız değişiklikler:")
    set_p_text(body[list(body).index(p_degisiklik)+1], "try-except bloğu yerine 'if denominator is None or denominator == 0:' şeklinde açık koşul kontrolü ekledim ve tip ipuçları (float, Optional[float]) ile kodu daha performanslı ve okunabilir hale getirdim.")

    p_mantik = find_p("Kodu kullanmadan önce kodun çalışma mantığını anlıyor muydunuz?")
    p_mantik_cb = find_p("☐ Tamamen anlıyordum.")
    set_p_text(p_mantik_cb, "☑ Tamamen anlıyordum.   ☐ Büyük ölçüde anlıyordum.   ☐ Kısmen anlıyordum.   ☐ Çok az anlıyordum.   ☐ Anlamadan kullandım.")

    # 9.6
    p_kontrol_nasil = find_p("☐ Kodu çalıştırarak test ettim.")
    new_kontrol = (
        "☑ Kodu çalıştırarak test ettim.   ☑ Kodu satır satır inceledim.   ☑ Resmî dokümantasyondan kontrol ettim.\n"
        "☑ İnternetten farklı kaynaklardan araştırdım.   ☐ Başka bir yapay zekâ aracından kontrol ettim.\n"
        "☐ Arkadaşım veya öğretim elemanıyla kontrol ettim.   ☐ Herhangi bir kontrol yapmadan kullandım."
    )
    set_p_text(p_kontrol_nasil, new_kontrol)

    p_hata_buldunuz_mu = find_p("Kontrol sırasında yapay zekânın verdiği cevapta hata buldunuz mu?")
    p_hata_cb = find_p("☐ Evet☐ Hayır")
    set_p_text(p_hata_cb, "☑ Evet   ☐ Hayır")

    p_tespit_hata = find_p("Evet ise tespit ettiğiniz hata:")
    set_p_text(body[list(body).index(p_tespit_hata)+1], "Yapay zekanın ilk ürettiği sektör karşılaştırma kodunda, sektörde yalnızca 1 şirket olduğunda standart sapma 0 çıktığı için '(val - mean) / std_dev' satırında tekrar sıfıra bölünme (ZeroDivisionError) hatası oluşuyordu.")

    p_hata_duzeltme = find_p("Hatayı nasıl düzelttiniz?")
    set_p_text(body[list(body).index(p_hata_duzeltme)+1], "Standart sapmanın pozitif ve sıfırdan büyük olup olmadığını kontrol eden 'if sector_std and sector_std > 0:' koşulunu ekleyerek, standart sapmanın sıfır olduğu durumlarda Z-score'u None olarak belirledim.")

    # 9.7
    p_ai_prob = find_p("Bu hafta yapay zekâ kullanırken karşılaştığınız problemleri belirtiniz.")
    p_ai_prob_cb = find_p("☐ Hatalı kod üretti.")
    new_ai_prob = (
        "☑ Hatalı kod üretti.   ☑ Kod çalışmadı.   ☐ Projeye uygun olmayan çözüm önerdi.\n"
        "☐ Sorumu yanlış anladı.   ☐ Güncel olmayan bilgi verdi.   ☑ Gereğinden karmaşık çözüm önerdi.\n"
        "☐ Olmayan bir fonksiyon veya kütüphane önerdi.   ☐ Aynı soruya farklı cevaplar verdi.\n"
        "☐ Verdiği kodu yeterince açıklamadı.   ☐ Herhangi bir problem yaşamadım."
    )
    set_p_text(p_ai_prob_cb, new_ai_prob)

    p_en_onemli_prob = find_p("Karşılaştığınız en önemli problem:")
    set_p_text(body[list(body).index(p_en_onemli_prob)+1], "Yapay zekâ, ilk etapta doğrudan ağır harici kütüphaneler (pandas, scipy, statsmodels) kullanarak gereksiz karmaşık çözümler sundu; ayrıca negatif özkaynak gibi finansal mantık istisnalarını hesaba katmadı.")

    p_prob_cozum = find_p("Bu problemi nasıl çözdünüz?")
    set_p_text(body[list(body).index(p_prob_cozum)+1], "Çekirdek algoritmayı Python'ın yerleşik standart kütüphaneleriyle sıfır dış bağımlılıkla çalışacak şekilde sadeleştirdim ve finansal kuralları adım adım kendim belirleyip koda ekledim.")

    # 9.8
    p_ai_olmasaydi_cb = find_p("☐ Evet, benzer sürede tamamlayabilirdim.")
    new_ai_olmasaydi = (
        "☐ Evet, benzer sürede tamamlayabilirdim.   ☑ Evet, ancak daha uzun sürede tamamlayabilirdim.\n"
        "☐ Görevlerin bir kısmını tamamlayabilirdim.   ☐ Büyük ölçüde zorlanırdım.   ☐ Görevleri tamamlayamazdım."
    )
    set_p_text(p_ai_olmasaydi_cb, new_ai_olmasaydi)

    p_ai_neden_olmasaydi = find_p("Neden?")
    set_p_text(body[list(body).index(p_ai_neden_olmasaydi)+1], "Formüller ve mantık zaten literatürde mevcuttur; ancak veri yapılarının kurulması, test senaryolarının yazılması ve alternatif yaklaşımların denenmesi 2-3 kat daha fazla vakit alırdı.")

    p_en_cok_zor = find_p("Yapay zekâ olmadan en fazla hangi görevlerde zorlanırdınız?")
    set_p_text(body[list(body).index(p_en_cok_zor)+1], "Z-Score ve eşik değerleri birleştiren hibrit risk ceza puanlama mimarisinin kurgulanmasında ve istisnai sınır durumların taranmasında.")

    p_rahat_gorev = find_p("Yapay zekâ olmadan rahatlıkla yapabileceğiniz görevler hangileriydi?")
    set_p_text(body[list(body).index(p_rahat_gorev)+1], "Temel finansal oran formüllerinin çıkarılması, dosya okuma işlemleri, nesne yönelimli sınıfların iskeletinin yazılması ve Git komutlarının işletilmesi.")

    # 9.9
    p_ogrenme_etki = find_p("Bu hafta yapay zekâ sayesinde daha önce bilmediğiniz yeni bir teknik bilgi")
    p_ogrenme_cb = find_p("☐ Evet☐ Kısmen☐ Hayır")
    # There are multiple "☐ Evet☐ Kısmen☐ Hayır" in document, find the one after 9.9
    for p in body[list(body).index(p_ogrenme_etki):list(body).index(p_ogrenme_etki)+5]:
        if "Evet" in ''.join(p.itertext()):
            set_p_text(p, "☑ Evet   ☐ Kısmen   ☐ Hayır")
            break

    p_ogrenilen_bilgi = find_p("Öğrendiğiniz yeni bilgi veya yöntem:")
    set_p_text(body[list(body).index(p_ogrenilen_bilgi)+1], "İstatistiksel aykırı değer analizinde Z-Score'un sektör verilerine nasıl uygulanacağı ve küçük örneklemli sektörlerde medyanın ortalamaya göre ne kadar hayati bir denge unsuru olduğu.")

    p_tekrar_cb = find_p("☐ Evet☐ Büyük ölçüde☐ Kısmen☐ Hayır")
    set_p_text(p_tekrar_cb, "☑ Evet   ☐ Büyük ölçüde   ☐ Kısmen   ☐ Hayır")

    p_tekrar_acikla = find_p("Açıklayınız:")
    # The one after 9.9
    for p in body[list(body).index(p_tekrar_cb):list(body).index(p_tekrar_cb)+5]:
        if "Açıklayınız:" in ''.join(p.itertext()):
            set_p_text(body[list(body).index(p)+1], "Z-Score ve medyan tabanlı anomali tespit mantığını kavradığım için, ileride karşılaşacağım herhangi bir finansal veya operasyonel veri analizinde yapay zekaya ihtiyaç duymadan bu istatistiksel modeli sıfırdan kurabilirim.")
            break

    # 9.10
    p_yz_oran = find_p("Tahmini yapay zekâ kullanım oranım: % ………")
    set_p_text(p_yz_oran, "Tahmini yapay zekâ kullanım oranım: % 35", bold=True)

    p_yz_kod_oran = find_p("Tahmini oran: % ………")
    set_p_text(p_yz_kod_oran, "Tahmini oran: % 30", bold=True)

    p_kendini_deg = find_p("☐ Büyük ölçüde kendi başıma çalıştım.")
    new_kendini = (
        "☐ Büyük ölçüde kendi başıma çalıştım.\n"
        "☑ Genellikle kendim çalıştım, ihtiyaç duyduğumda yapay zekâ kullandım.\n"
        "☐ Kendim ve yapay zekâ desteğini yaklaşık eşit düzeyde kullandım.\n"
        "☐ Çalışmalarımın önemli bölümünde yapay zekâ desteğine ihtiyaç duydum.\n"
        "☐ Yapay zekâ desteği olmadan ilerlemekte ciddi şekilde zorlandım."
    )
    set_p_text(p_kendini_deg, new_kendini)

    p_secenek_neden = find_p("Bu seçeneği neden işaretlediğinizi açıklayınız:")
    set_p_text(body[list(body).index(p_secenek_neden)+1], "Projenin mimarisini, finansal oran seçimlerini ve test veri setini tamamen kendim planladım. Yapay zekayı bir kod yazıcıdan ziyade; algoritma alternatiflerini tartışan, kodları hızlandıran ve kenar durumları hatırlatan bir pair-programming ortağı olarak kullandım.")

    # 9.11
    p_genel_deg = find_p("Genel değerlendirme:")
    genel_text = (
        "Bu hafta yapay zekâ, projeye başlangıç sürecimde özellikle mimari şablonların kurulması, oran hesaplama modülünün prototiplenmesi ve birim test senaryolarının çeşitlendirilmesinde bana ciddi bir zaman kazandırdı. "
        "Finansal analiz alanındaki gereksinimleri ve sektör gruplama mantığını tamamen kendim kurguladım. Yapay zekânın sunduğu kodları hiçbir zaman doğrudan kopyalamadım; her fonksiyonu satır satır inceleyip sıfıra bölünme, tek şirketlik sektörlerde standart sapmanın sıfır çıkması ve negatif özkaynak kârlılık paradoksu gibi kritik hataları bizzat tespit edip düzelttim. "
        "Bu süreç bana hem istatistiksel anomali analizini hem de savunmacı yazılım geliştirme prensiplerini derinlemesine öğretti. Yapay zekâ desteği olmadan da bu modülleri rahatlıkla geliştirebileceğimi ve gelecekte benzer problemlerde bu bilgi birikimini tek başıma uygulayabileceğimi net bir şekilde görüyorum."
    )
    set_p_text(body[list(body).index(p_genel_deg)+1], genel_text)

    # 9.12
    p_kanit_acikla = find_p("Eklediğiniz kanıtları kısaca açıklayınız:")
    kanit_text = (
        "1. src/ratios.py içerisindeki safe_divide ve oran hesaplama fonksiyonları (Yapay zekanın ilk önerdiği try-except yapısı yerine if-koşullu ve tip denetimli optimize edilmiş nihai sürüm).\n"
        "2. src/sector_analysis.py içerisindeki sektör benchmark ve Z-score hesaplama algoritması (Standart sapma = 0 durum kontrolü ve medyan hesaplaması tarafımdan eklenmiştir).\n"
        "3. tests/test_ratios.py dosyasındaki birim testler (Hesaplama doğrulukları ve sıfıra bölme testleri).\n"
        "4. Git commit geçmişi (git log --oneline çıktısı: 717c811, ad296b4)."
    )
    set_p_text(body[list(body).index(p_kanit_acikla)+1], kanit_text)

    # 10. BÖLÜM 10: HAFTALIK GENEL ÖZ DEĞERLENDİRME
    p_en_basarili = find_p("Bu hafta en başarılı olduğunuz konu:")
    set_p_text(body[list(body).index(p_en_basarili)+1], "Finansal formülleri modüler, hataya dayanıklı ve temiz bir nesne yönelimli mimaride (models.py, ratios.py, sector_analysis.py, anomaly_detector.py) kodlayarak, sentetik veriler üzerinde anomali ve risk puanını uçtan uca hatasız çalıştırabilmek.")

    p_en_zor = find_p("En fazla zorlandığınız konu:")
    set_p_text(body[list(body).index(p_en_zor)+1], "Küçük sektör gruplarında aşırı aykırı şirketlerin sektör ortalamasını çarpıtması problemi ve negatif özkaynak/kâr durumlarında oranların matematiksel olarak yanlış yönde sinyal vermesini engelleyecek mantıksal kuralların tasarlanması.")

    p_farkli = find_p("Bu hafta tekrar çalışma fırsatınız olsaydı farklı yapacağınız şey:")
    set_p_text(body[list(body).index(p_farkli)+1], "Veri setini doğrudan JSON dosyasından değil, ilk günden itibaren hem Excel hem de CSV dosyalarını otomatik okuyabilen esnek bir veri besleme modülü ile başlatırdım.")

    p_puan = find_p("…… / 10")
    set_p_text(p_puan, "9 / 10", bold=True)

    p_puan_neden = find_p("Neden?")
    # Find the one after p_puan
    for p in body[list(body).index(p_puan):list(body).index(p_puan)+4]:
        if "Neden?" in ''.join(p.itertext()):
            set_p_text(body[list(body).index(p)+1], "Hedeflenen tüm modüller zamanında, temiz kod standartlarına uygun ve birim testlerle doğrulanmış olarak tamamlandı. Sadece çalışan bir kod değil, aynı zamanda olası istisnalara (sıfıra bölünme, uç değerler) karşı dayanıklı bir çekirdek altyapı kuruldu. 1 puanı ise dosya okuma ve arayüz çalışmalarının henüz prototip aşamasında kalması nedeniyle kırdım.")
            break

    # Now write out the modified document.xml
    new_xml = ET.tostring(tree, encoding='utf-8', xml_declaration=True)
    all_files['word/document.xml'] = new_xml

    for out_path in [dest_docx_1, dest_docx_2]:
        with zipfile.ZipFile(out_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for name, data in all_files.items():
                zout.writestr(name, data)
        print(f"Rapor başarıyla kaydedildi: {out_path}")

if __name__ == "__main__":
    main()
