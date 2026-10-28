# HAFTALIK YAZILIM PROJESİ GELİŞİM RAPORU

- **Ders:** Yazılım Geliştirme I
- **Proje Adı:** Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi
- **Öğrenci Adı Soyadı:** Muhammet Mustafa Kırmızı
- **Öğrenci No:** 24130766
- **Hafta No:** 1
- **Tarih:** 14 / 10 / 2026

---

## 1. BU HAFTANIN HEDEFLERİ
**Bu hafta proje kapsamında gerçekleştirmeyi planladığınız çalışmaları yazınız:**
1. Proje konusunun ("Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi") kapsamının, fonksiyonel ve teknik gereksinimlerinin netleştirilmesi.
2. Şirketlerin Bilanço ve Gelir Tablosu finansal kalemleri için veri modellerinin (`models.py`) tasarlanması ve test veri setinin (`sample_companies.json`) hazırlanması.
3. Temel finansal oran hesaplayıcı motorunun (`FinancialRatioCalculator`: Likidite, Borçluluk, Kârlılık, Faaliyet) kodlanması ve güvenli bölme kontrollerinin (`safe_divide`) eklenmesi.
4. Sektör ortalamaları ve standart sapmalarını hesaplayan `SectorAnalyzer` ile Z-Score tabanlı anomali/risk puanlama motorunun (`FinancialAnomalyDetector`) prototiplenmesi.

**Bu hedeflerin proje açısından neden önemli olduğunu kısaca açıklayınız:**
> **Açıklama:**  
> Projenin temel amacı, ham finansal tablolardan (bilanço ve gelir tablosu) anlamlı finansal rasyolar türeterek şirketleri sektörleriyle kıyaslamak ve anormal finansal sapmaları (risk) otomatik tespit etmektir. İlk haftada veri modellerinin, oran hesaplama mantığının ve istatistiksel karşılaştırma çekirdeğinin hatasız kurulması; sonraki haftalarda eklenecek olan makine öğrenmesi modelleri (Isolation Forest), veritabanı yapısı ve web analiz ekranı (dashboard) için sağlam bir temel oluşturması açısından kritik öneme sahiptir.

---

## 2. BU HAFTA YAPILAN ÇALIŞMALAR
**Bu hafta gerçekleştirilen çalışmalar:**  
Bu hafta, projenin iş analizi ve çekirdek geliştirme fazı başarıyla yürütüldü. İlk olarak finansal tablolardaki temel kalemler incelenerek Bilanço ve Gelir Tablosu için Python dataclass yapıları kuruldu. 4 ana kategoride 14 farklı finansal oranı hesaplayan `FinancialRatioCalculator` sınıfı yazıldı. Matematiksel hesaplamalarda sıfıra bölünme ve negatif kâr/özkaynak gibi istisnaları yönetmek için `safe_divide` mekanizması entegre edildi. Farklı sektörlerden şirketlere ait finansal veriler JSON formatında modellendi. Bu veriler üzerinden sektör ortalaması, medyanı ve standart sapmasını dinamik hesaplayan `SectorAnalyzer` geliştirildi. Son olarak, Z-Score ve kritik eşik ihlallerine göre 0-100 arasında Risk Puanı üreten `FinancialAnomalyDetector` prototipi kodlanarak uçtan uca test edildi.

**Geliştirilen veya güncellenen modüller / özellikler:**
1. `src/models.py`: Bilanço (`BalanceSheet`), Gelir Tablosu (`IncomeStatement`) ve Şirket (`Company`) veri modelleri oluşturuldu; toplam varlık, borç, brüt ve faaliyet kârı gibi dinamik property hesaplamaları eklendi.
2. `src/ratios.py`: Likidite, Finansal Kaldıraç, Kârlılık ve Faaliyet oranlarını hesaplayan `FinancialRatioCalculator` sınıfı ve `safe_divide` güvenlik fonksiyonu kodlandı.
3. `src/sector_analysis.py`: Şirketleri sektörlerine göre gruplayıp ortalama, medyan, standart sapma metriklerini çıkaran ve Z-score hesaplayan `SectorAnalyzer` sınıfı geliştirildi.
4. `src/anomaly_detector.py` & `tests/test_ratios.py`: Anomali ve risk puanlama motoru kodlandı; hesaplamaları ve sınır durumları doğrulayan birim testler yazıldı.

**Bu çalışmalar sonucunda projede meydana gelen değişiklikler:**  
Proje şartname aşamasından çıkarılarak; nesne yönelimli mimariye sahip, birim testleri geçen ve konsol üzerinden tam finansal kıyaslama ve anomali analizi yapabilen somut bir çekirdek yazılım prototipine dönüştürüldü. Git versiyon kontrolü başlatılarak ilk commit'ler atıldı.

---

## 3. PROJENİN TAMAMLANMA DURUMU
**Tamamlanan çalışmalar:**
- Bilanço, Gelir Tablosu ve Şirket veri modellerinin oluşturulması (`models.py`)
- Likidite, Borçluluk, Kârlılık ve Faaliyet oranlarını hesaplayan rasyo motorunun kodlanması (`ratios.py`)
- Sektör ortalaması, medyanı ve standart sapması hesaplama modülü (`sector_analysis.py`)
- Z-Score ve eşik değer bazlı anomali/risk puanlayıcı algoritması (`anomaly_detector.py`)
- Örnek sektör ve şirket test veri seti (`sample_companies.json`)
- Matematiksel ve sınır durum birim testleri (`tests/test_ratios.py`)
- Uçtan uca çalışan konsol demosu (`main.py`) ve Git repository kurulumu.

**Devam eden çalışmalar:**
- Şirket finansal tablolarını harici Excel/CSV dosyalarından otomatik içeri aktaracak veri okuyucu (Parser/ETL) modülünün tasarımı.
- Makine öğrenmesi tabanlı anomali tespiti (`Isolation Forest` / `LOF`) için veri hazırlığı ve kütüphane araştırması.

**Başlanamayan veya ertelenen çalışmalar:**
- Web tabanlı görselleştirme arayüzü (`Streamlit Dashboard`) ve interaktif grafikler (2. ve 3. haftalara planlandı).
- SQLite / PostgreSQL veritabanı şeması ve kayıt kalıcılığı (ilerleyen haftalara planlandı).

**Projenin tahmini genel tamamlanma oranı:** **% 20**  
**Bu oranı neye göre belirlediğinizi kısaca açıklayınız:**  
Dönem boyunca yapılacak çalışmalar 5 ana aşamaya ayrılmıştır: (1) Gereksinim analizi ve çekirdek matematiksel hesaplama motoru [%20], (2) Veri aktarımı ve Makine Öğrenmesi anomali modeli [%25], (3) Veritabanı ve API entegrasyonu [%20], (4) Arayüz ve Görselleştirme Ekranı [%20], (5) Test, optimizasyon ve dokümantasyon [%15]. Çekirdek matematiksel motor ve prototip eksiksiz tamamlandığı için genel ilerleme %20 olarak belirlenmiştir.

---

## 4. TEKNİK ÇALIŞMALAR
**İlgili alanlar:**
- [ ] Arayüz / UI geliştirme
- [ ] Veritabanı işlemleri
- [x] Backend geliştirme
- [ ] API geliştirme / API kullanımı
- [ ] Kullanıcı giriş ve yetkilendirme
- [x] Dosya işlemleri
- [x] Test işlemleri
- [x] Hata düzeltme / Debugging
- [x] Git / GitHub kullanımı
- [x] Kod iyileştirme / Refactoring
- [x] Dokümantasyon
- [x] Diğer: Finansal Matematik ve İstatistiksel Analiz

**Bu hafta kullandığınız programlama dili / dilleri:**  
Python 3.12

**Kullandığınız teknoloji, framework, kütüphane veya araçlar:**  
Python Standart Kütüphanesi (`dataclasses`, `json`, `math`, `collections`, `typing`, `os`), `unittest` test çatısı, Git & GitHub, VS Code IDE, Google Gemini / Antigravity AI Asistanı.

**Bu teknolojileri hangi amaçlarla kullandığınızı açıklayınız:**
- `dataclasses` & `typing`: Bilanço ve gelir tablosu finansal kalemlerini tip güvenli ve nesne yönelimli şekilde modellemek için.
- `math` & `collections`: Sektör ortalaması, standart sapma ve Z-score hesaplamalarını harici bağımlılık olmadan hızlıca yürütmek için.
- `json`: Test veri setini yapılandırılmış dosya formatında okumak için.
- `unittest`: Oran formüllerinin ve sıfıra bölme güvenliğinin hatasız çalıştığını otomatize birim testlerle doğrulamak için.
- `Git`: Kod sürümlerini ve geliştirme adımlarını commit'ler ile kayıt altında tutmak için.

---

## 5. KARŞILAŞILAN PROBLEMLER VE ÇÖZÜMLER
### Problem 1
- **Karşılaşılan problem:** Finansal oranlar hesaplanırken bazı borçsuz şirketlerde veya sıfır stoklu dönemlerde paydanın 0 olması sebebiyle `ZeroDivisionError` hatası meydana geldi. Ayrıca geçmiş yıl zararları nedeniyle negatif özkaynak durumlarında Borç/Özkaynak ve ROE oranlarının ters yönde anlamsız sonuçlar üretmesi.
- **Problemin nedeni:** Finansal formüller bölme işlemlerine dayanır; payda sıfır olduğunda çalışma zamanı hatası fırlatılır. Negatif kâr ile negatif özkaynak bölündüğünde ise matematiksel olarak pozitif kârlılık gibi yanıltıcı bir sonuç oluşmaktadır.
- **Çözüm yöntemi:** Paydayı kontrol eden ve sıfır/None durumunda güvenli şekilde `None` döndüren `safe_divide` yardımcı fonksiyonu geliştirildi. Negatif özkaynak durumu için ise kural bazlı risk kontrolleri eklenerek şirkete doğrudan anomali ceza puanı uygulandı.
- **Sonuç:** Sıfıra bölünme kaynaklı çökmeler tamamen engellendi; negatif özkaynak gibi uç durumlarda rasyoların sistemi yanıltması engellenerek risk raporuna kritik uyarı olarak yansıtıldı. Birim testlerle doğrulandı.

### Problem 2
- **Karşılaşılan problem:** Sektördeki şirket sayısının az olduğu durumlarda (örneğin 3 şirket), aşırı borçlu veya aşırı kârlı tek bir uç değerin (outlier) sektörün aritmetik ortalamasını ve standart sapmasını aşırı saptırması; bu nedenle normal şirketlerin haksız yere anomalili çıkması riski.
- **Problemin nedeni:** Aritmetik ortalama ve standart sapma uç değerlere karşı çok hassastır. Az sayıda şirket bulunan bir sektörde tek bir dev veya batık şirket tüm sektör normunu bozmaktadır.
- **Çözüm yöntemi:** Sektör kıyaslama motoruna aritmetik ortalamanın yanı sıra aykırı değerlerden etkilenmeyen `medyan` (ortanca) hesaplaması entegre edildi. Sektörde tek şirket olduğunda standart sapmanın sıfır çıkması durumu da koruma altına alındı.
- **Sonuç:** Sektör benchmark raporlarında hem ortalama hem de medyan birlikte sunularak tekil şirketlerin sektörü saptırmasının önüne geçildi; çok daha dengeli ve güvenilir bir kıyaslama tabanı oluşturuldu.

---

## 6. KOD VE PROJE KANITLARI
- **GitHub Bağlantısı:** https://github.com/MUSTAFAKRMZL/finansal-sektor-analiz-sistemi
- **Commit Sayısı:** 2 commit
- **Önemli Commitler:**
  - `717c811`: feat: proje baslangici, veri modelleri, finansal oran hesaplayici ve anomali tespiti prototipi
  - `ad296b4`: chore: gitignore eklendi ve pycache temizlendi
- **Çalışan Uygulama / Demo:** Yerel konsol uygulaması (`python main.py` komutuyla terminalde uçtan uca çalıştırılabilmektedir).

### Kod Bölümü
**Kodun Amacı:** Şirketin kısa vadeli borçlarını ödeme kabiliyetini ölçen temel likidite rasyolarını (Cari Oran, Likit/Asit-Test Oranı, Nakit Oran) sıfıra bölünme hatalarına karşı korumalı olarak hesaplayan `FinancialRatioCalculator.calculate_liquidity_ratios` metodu.

```python
@staticmethod
def calculate_liquidity_ratios(bs: BalanceSheet) -> Dict[str, Optional[float]]:
    """
    Likidite Oranları: Şirketin kısa vadeli borçlarını ödeme gücünü gösterir.
    """
    cur_assets = bs.total_current_assets
    short_liab = bs.total_short_term_liabilities
    inventories = bs.inventories
    cash = bs.cash_and_equivalents

    # 1. Cari Oran = Dönen Varlıklar / KVYK (İdeal: 1.5 - 2.0)
    current_ratio = safe_divide(cur_assets, short_liab)

    # 2. Asit-Test / Likit Oran = (Dönen Varlıklar - Stoklar) / KVYK (İdeal: >= 1.0)
    acid_test_ratio = safe_divide(cur_assets - inventories, short_liab)

    # 3. Nakit Oran = Nakit ve Benzerleri / KVYK (İdeal: >= 0.20)
    cash_ratio = safe_divide(cash, short_liab)

    return {
        "current_ratio": current_ratio,
        "acid_test_ratio": acid_test_ratio,
        "cash_ratio": cash_ratio
    }
```

**Kodun Nasıl Çalıştığı:**  
Bu metot, parametre olarak aldığı `BalanceSheet` nesnesinden dönen varlıklar, kısa vadeli borçlar, stoklar ve nakit kalemlerini okur. Cari oran ile şirketin kısa vadeli borçlarını dönen varlıklarıyla kaç kat karşılayabildiğini bulur. Asit-test oranında ise satılması zaman alan stokları çıkararak gerçek likit gücü ölçer. Nakit oranında ise şirketin anında nakde dönebilecek varlıklarının borçlara oranını hesaplar. Paydanın sıfır olması durumunda programın çökmemesi için doğrudan bölme operatörü yerine `safe_divide` yardımcı fonksiyonu kullanılır.

---

## 7. BU HAFTA ÖĞRENİLEN YENİ BİLGİLER
1. Finansal analizde tek bir şirketin oranlarının soyut kaldığını, mutlaka sektör ortalaması ve medyanı ile normalize edilerek karşılaştırılması gerektiğini kavradım.
2. İstatistikte Z-Score (standart skor) yönteminin finansal anomalileri tespit etmekte nasıl kullanıldığını ve sektör ortalamasından 2 standart sapma uzaklaşan değerlerin kritik anomali sinyali olduğunu öğrendim.
3. Python `dataclasses` yapısının nesne yönelimli modellemede `@property` dekoratörleriyle birleştiğinde karmaşık bilanço hiyerarşilerini ne kadar sadeleştirdiğini öğrendim.

- **En Önemli Bilgi:** Yazılım geliştirirken sadece formülleri kodlamanın yetmediği; iş dünyasına ait özel kısıtların (sıfır borç, negatif kâr, aşırı aykırı şirketler) yazılım mimarisinde savunmacı hata kontrolleri ve medyan gibi sağlam istatistiklerle desteklenmesi gerektiğidir.
- **Yeniden Kullanılabilirlik:** Evet. Z-Score normalizasyonu, medyan tabanlı aykırı değer analizi ve savunmacı bölme/veri doğrulama pratikleri; ileride geliştireceğim tüm veri analitiği, makine öğrenmesi ve finansal mühendislik projelerinde doğrudan yeniden kullanabileceğim temel prensiplerdir.

---

## 8. GELECEK HAFTANIN PLANI
1. Şirketlerin finansal tablolarını harici Excel (`.xlsx`) ve CSV dosyalarından otomatik okuyup doğrulayan bir dosya içe aktarma (Ingestion / ETL) modülü geliştirmek.
2. `scikit-learn` kütüphanesini projeye dahil ederek `Isolation Forest` ve `Local Outlier Factor (LOF)` makine öğrenmesi algoritmalarını sektör rasyoları üzerinde eğitmek.
3. Hesaplanan rasyoları ve şirket anomali puanlarını kalıcı olarak saklamak için SQLite veritabanı şemasını oluşturmak ve CRUD servislerini yazmak.
4. Görsel analiz ekranı için Streamlit tabanlı interaktif web dashboard arayüzünün prototip tasarımına başlamak.

- **Öncelikli Problem/Özellik:** Öncelikli hedefim; kullanıcıların kendi Excel veya CSV formatındaki mali tablolarını sisteme yükleyebilmesini sağlamak ve istatistiksel Z-score analizini scikit-learn Isolation Forest makine öğrenmesi modeliyle destekleyerek çok boyutlu anomali tespitini tamamlamaktır.

---

## 9. YAPAY ZEKÂ DESTEKLİ PROJE GELİŞTİRME SÜRECİ

### 9.1. Bu Hafta Kullandığınız Yapay Zekâ Araçları
- **Kullandığım araçlar:** Google Gemini, ChatGPT, Antigravity AI Asistanı
- **Kullanım süresi:** [x] 1–3 saat

### 9.2. Yapay Zekâyı Hangi Amaçlarla Kullandınız?
- **Başlıca amaçlar:** Finansal oran formüllerinin algoritma haline getirilmesi, nesne yönelimli mimaride veri sınıflarının (`dataclasses`) tasarımı, sıfıra bölme ve sınır durumların hata yönetimi, Z-Score istatistiksel sektör karşılaştırma mantığı ve birim test senaryolarının türetilmesi.
- **En çok kullanılan konu:** Finansal oranların matematiksel hesaplanmasında ve Z-Score istatistiğinin sektör verilerine uygulanmasında.
- **Neden ihtiyaç duyuldu:** 14 farklı finansal rasyonun sektör dinamiklerine göre nasıl yorumlandığına ve negatif özkaynak / sıfır borç gibi uç durumlarda standart finansal yaklaşımların nasıl kodlanabileceğine dair alternatif yaklaşımları hızlıca görmek ve hata payını azaltmak için.

### 9.3. Yapay Zekâya Başvurmadan Önce Ne Yaptınız?
- **Problemi önce kendim çözmeye çalıştım:** [x] Evet
- **Yapılan araştırmalar:** Finansal yönetim ders notlarından ve BIST finansal tablo rehberlerinden temel likidite, kârlılık, kaldıraç oranlarının tanımlarını çıkardım; formülleri bir kâğıda yazarak hangi bilanço/gelir tablosu kalemlerinin birbirine bölüneceğini belirledim.
- **Başvurma nedenleri:**
  - [x] Yazdığım kod hata verdi.
  - [x] Daha hızlı bir çözüm üretmek istedim.
  - [x] Alternatif bir çözüm aradım.
  - [x] Yazdığım kodu kontrol ettirmek istedim.
  - [x] Konuyu öğrenmek istedim.

### 9.4. Bu Hafta Kullandığınız Önemli Promptlar
#### Prompt 1
- **Çözmeye çalıştığım problem:** Bilanço ve Gelir tablosundaki kalemlerden likidite, borçluluk, kârlılık ve devir hızı oranlarını hesaplayan modüler bir Python sınıf yapısının kurulması.
- **Yapay zekâya yazdığım prompt:** *"Python 3'te bilanço ve gelir tablosu verilerini tutacak bir veri modeli ve bu verilerden Likidite (Cari, Asit-Test, Nakit), Kaldıraç (Borç/Varlık, Borç/Özkaynak), Kârlılık (ROA, ROE, Kâr Marjları) oranlarını hesaplayan FinancialRatioCalculator sınıfı tasarla. Sıfıra bölünme hatalarını güvenli şekilde yönetecek bir yapı kur."*
- **Yapay zekânın cevabının özeti:** Dataclass yapılarıyla bilanço ve gelir tablosunu modelleyen, statik metotlarla oranları sözlük (dict) olarak döndüren ve sıfır kontrolü yapan bir kod şablonu sundu.
- **Cevabı nasıl kullandım:** [x] Küçük değişiklikler yaptım.
- **Açıklama:** Projemizin veri gereksinimlerine göre kalemleri detaylandırdım, `safe_divide` fonksiyonunun dönüş tiplerini netleştirdim ve Türkçe finansal terminolojiye uyarladım.

#### Prompt 2
- **Çözmeye çalıştığım problem:** Bir sektördeki tüm şirketlerin oranlarını toplayıp ortalama, medyan ve standart sapma hesaplayarak hedef şirketin Z-Score değerini bulmak.
- **Yapay zekâya yazdığım prompt:** *"Elimde farklı şirketlerin finansal oran sözlükleri var. Bunları sektörlerine göre gruplayıp her bir oran için sektör ortalamasını ve standart sapmasını hesaplayan, ardından belirli bir şirketin sektöründen kaç standart sapma saptığını (Z-score) bulan bir algoritma yazar mısın?"*
- **Yapay zekânın cevabının özeti:** `defaultdict` ve `math.sqrt` kullanarak sektör bazlı metrikleri toplayan ve `(değer - ortalama) / standart_sapma` formülüyle Z-Score hesaplayan bir fonksiyon önerdi.
- **Cevabı nasıl kullandım:** [x] Büyük ölçüde değiştirdim.
- **Açıklama:** Yapay zekânın verdiği kodda sektörde tek şirket olduğunda standart sapmanın 0 olması durumunda tekrar sıfıra bölünme oluşuyordu. Bu kontrolü ekledim ve ayrıca uç değerlerin ortalamayı saptırmasını engellemek için medyan hesaplamasını da koda entegre ettim.

#### Prompt 3
- **Çözmeye çalıştığım problem:** Z-score ve kritik oran eşiklerini birleştirerek şirkete 0-100 arasında anlamlı bir finansal risk puanı üreten anomali algoritması mantığı kurmak.
- **Yapay zekâya yazdığım prompt:** *"Bir şirketin sektör finansal rasyolarına göre anomali/risk puanını 0 ile 100 arasında hesaplamak istiyorum. Hem Z-score sapmalarını (örneğin |Z| > 2) hem de kritik kural bazlı riskleri (örneğin cari oran < 1.0 veya aşırı borçluluk) içeren hibrit bir puanlama mantığını nasıl kurabilirim?"*
- **Yapay zekânın cevabının özeti:** Temel ceza puanı (penalty points) mantığı önerdi; her Z-score aşımı için 5-15 puan, kritik kural ihlalleri için 15-20 puan ekleyip toplamı 100 ile sınırlayan ve risk seviyelerine (Düşük, Orta, Yüksek) ayıran bir mimari sundu.
- **Cevabı nasıl kullandım:** [x] Küçük değişiklikler yaptım.
- **Açıklama:** Önerilen katsayıları finansal literatüre göre revize ettim; örneğin cari oranın 1'in altına düşmesini en kritik risklerden biri olarak 20 ceza puanına sabitledim ve anlaşılır uyarı mesajları ekledim.

### 9.5. Yapay Zekâ Tarafından Üretilen Kodlar
- **Yapay zekâ kodu kullanıldı mı:** [x] Evet
- **İstenen işlem:** Sıfıra bölünme hatasını engelleyen genel amaçlı güvenli bölme fonksiyonu (`safe_divide`).
- **Önerilen kod:**
  ```python
  def safe_divide(a, b, default=None):
      try:
          return round(a / b, 4)
      except ZeroDivisionError:
          return default
  ```
- **Kodun yaptığı iş:** İki sayıyı birbirine bölerken paydanın 0 olması durumunda programın çökmesini engeller, hata yakalandığında varsayılan olarak `None` döner ve sonucu 4 basamağa yuvarlar.
- **Nasıl kullanıldı:** [x] Küçük değişiklikler yaptım.
- **Yapılan değişiklikler:** `try-except` bloğu yerine `if denominator is None or denominator == 0:` şeklinde açık koşul kontrolü ekledim ve tip ipuçları (`float`, `Optional[float]`) ile kodu daha performanslı ve okunabilir hale getirdim.
- **Çalışma mantığı anlaşılıyor muydu:** [x] Tamamen anlıyordum.

### 9.6. Yapay Zekâ Çıktılarının Kontrolü
- **Kontrol yöntemleri:**
  - [x] Kodu çalıştırarak test ettim.
  - [x] Kodu satır satır inceledim.
  - [x] Resmî dokümantasyondan kontrol ettim.
  - [x] İnternetten farklı kaynaklardan araştırdım.
- **Hata bulundu mu:** [x] Evet
- **Tespit edilen hata:** Yapay zekanın ilk ürettiği sektör karşılaştırma kodunda, sektörde yalnızca 1 şirket olduğunda standart sapma 0 çıktığı için `(val - mean) / std_dev` satırında tekrar sıfıra bölünme (`ZeroDivisionError`) hatası oluşuyordu.
- **Nasıl düzeltildi:** Standart sapmanın pozitif ve sıfırdan büyük olup olmadığını kontrol eden `if sector_std and sector_std > 0:` koşulunu ekleyerek, standart sapmanın sıfır olduğu durumlarda Z-score'u `None` olarak belirledim.

### 9.7. Yapay Zekâ Kullanırken Karşılaşılan Problemler
- **Yaşanan problemler:**
  - [x] Hatalı kod üretti.
  - [x] Kod çalışmadı.
  - [x] Gereğinden karmaşık çözüm önerdi.
- **En önemli problem:** Yapay zekâ, ilk etapta doğrudan ağır harici kütüphaneler (pandas, scipy, statsmodels) kullanarak gereksiz karmaşık çözümler sundu; ayrıca negatif özkaynak gibi finansal mantık istisnalarını hesaba katmadı.
- **Problemin çözümü:** Çekirdek algoritmayı Python'ın yerleşik standart kütüphaneleriyle sıfır dış bağımlılıkla çalışacak şekilde sadeleştirdim ve finansal kuralları adım adım kendim belirleyip koda ekledim.

### 9.8. Yapay Zekâ Olmasaydı Ne Olurdu?
- **Görevler tamamlanabilir miydi:** [x] Evet, ancak daha uzun sürede tamamlayabilirdim.
- **Gerekçe:** Formüller ve mantık zaten literatürde mevcuttur; ancak veri yapılarının kurulması, test senaryolarının yazılması ve alternatif yaklaşımların denenmesi 2-3 kat daha fazla vakit alırdı.
- **En fazla zorlanılacak görevler:** Z-Score ve eşik değerleri birleştiren hibrit risk ceza puanlama mimarisinin kurgulanmasında ve istisnai sınır durumların taranmasında.
- **Rahatlıkla yapılabilecek görevler:** Temel finansal oran formüllerinin çıkarılması, dosya okuma işlemleri, nesne yönelimli sınıfların iskeletinin yazılması ve Git komutlarının işletilmesi.

### 9.9. Öğrenmeye Etkisi
- **Yeni bilgi öğrenildi mi:** [x] Evet
- **Öğrenilen bilgi:** İstatistiksel aykırı değer analizinde Z-Score'un sektör verilerine nasıl uygulanacağı ve küçük örneklemli sektörlerde medyanın ortalamaya göre ne kadar hayati bir denge unsuru olduğu.
- **Tekrar kullanılabilirlik:** [x] Evet
- **Açıklama:** Z-Score ve medyan tabanlı anomali tespit mantığını kavradığım için, ileride karşılaşacağım herhangi bir finansal veya operasyonel veri analizinde yapay zekaya ihtiyaç duymadan bu istatistiksel modeli sıfırdan kurabilirim.

### 9.10. Değerlendirme ve Oranlar
- **Tahmini yapay zekâ kullanım oranım:** **% 35**
- **Yapay zekâ tarafından oluşturulan kod oranı:** **% 30**
- **Kendini değerlendirme:** [x] Genellikle kendim çalıştım, ihtiyaç duyduğumda yapay zekâ kullandım.
- **Gerekçe:** Projenin mimarisini, finansal oran seçimlerini ve test veri setini tamamen kendim planladım. Yapay zekayı bir kod yazıcıdan ziyade; algoritma alternatiflerini tartışan, kodları hızlandıran ve kenar durumları hatırlatan bir pair-programming ortağı olarak kullandım.

### 9.11. Genel Değerlendirme
Bu hafta yapay zekâ, projeye başlangıç sürecimde özellikle mimari şablonların kurulması, oran hesaplama modülünün prototiplenmesi ve birim test senaryolarının çeşitlendirilmesinde bana ciddi bir zaman kazandırdı. Finansal analiz alanındaki gereksinimleri ve sektör gruplama mantığını tamamen kendim kurguladım. Yapay zekânın sunduğu kodları hiçbir zaman doğrudan kopyalamadım; her fonksiyonu satır satır inceleyip sıfıra bölünme, tek şirketlik sektörlerde standart sapmanın sıfır çıkması ve negatif özkaynak kârlılık paradoksu gibi kritik hataları bizzat tespit edip düzelttim. Bu süreç bana hem istatistiksel anomali analizini hem de savunmacı yazılım geliştirme prensiplerini derinlemesine öğretti. Yapay zekâ desteği olmadan da bu modülleri rahatlıkla geliştirebileceğimi ve gelecekte benzer problemlerde bu bilgi birikimini tek başıma uygulayabileceğimi net bir şekilde görüyorum.

### 9.12. Kanıtlar
1. `src/ratios.py` içerisindeki `safe_divide` ve oran hesaplama fonksiyonları (Yapay zekanın ilk önerdiği try-except yapısı yerine if-koşullu ve tip denetimli optimize edilmiş nihai sürüm).
2. `src/sector_analysis.py` içerisindeki sektör benchmark ve Z-score hesaplama algoritması (Standart sapma = 0 durum kontrolü ve medyan hesaplaması tarafımdan eklenmiştir).
3. `tests/test_ratios.py` dosyasındaki birim testler (Hesaplama doğrulukları ve sıfıra bölme testleri).
4. Git commit geçmişi (`git log --oneline` çıktısı: `717c811`, `ad296b4`).

---

## 10. HAFTALIK GENEL ÖZ DEĞERLENDİRME
- **En başarılı olunan konu:** Finansal formülleri modüler, hataya dayanıklı ve temiz bir nesne yönelimli mimaride (`models.py`, `ratios.py`, `sector_analysis.py`, `anomaly_detector.py`) kodlayarak, sentetik veriler üzerinde anomali ve risk puanını uçtan uca hatasız çalıştırabilmek.
- **En fazla zorlanılan konu:** Küçük sektör gruplarında aşırı aykırı şirketlerin sektör ortalamasını çarpıtması problemi ve negatif özkaynak/kâr durumlarında oranların matematiksel olarak yanlış yönde sinyal vermesini engelleyecek mantıksal kuralların tasarlanması.
- **Farklı yapılacak şey:** Veri setini doğrudan JSON dosyasından değil, ilk günden itibaren hem Excel hem de CSV dosyalarını otomatik okuyabilen esnek bir veri besleme modülü ile başlatırdım.
- **Haftalık Puan:** **9 / 10**
- **Puan Gerekçesi:** Hedeflenen tüm modüller zamanında, temiz kod standartlarına uygun ve birim testlerle doğrulanmış olarak tamamlandı. Sadece çalışan bir kod değil, aynı zamanda olası istisnalara (sıfıra bölünme, uç değerler) karşı dayanıklı bir çekirdek altyapı kuruldu. 1 puanı ise dosya okuma ve arayüz çalışmalarının henüz prototip aşamasında kalması nedeniyle kırdım.
