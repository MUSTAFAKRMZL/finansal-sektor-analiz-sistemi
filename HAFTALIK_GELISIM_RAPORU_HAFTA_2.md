# HAFTALIK YAZILIM PROJESİ GELİŞİM RAPORU (HAFTA 2)

- **Ders:** Yazılım Geliştirme I
- **Proje Adı:** Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi
- **Öğrenci Adı Soyadı:** Muhammet Mustafa Kırmızı
- **Öğrenci No:** 24130766
- **Hafta No:** 2
- **Tarih:** 21 / 10 / 2026

---

## 1. BU HAFTANIN HEDEFLERİ
**Bu hafta proje kapsamında gerçekleştirmeyi planladığınız çalışmaları yazınız:**
1. Şirketlerin finansal tablolarını (Bilanço ve Gelir Tablosu) harici CSV ve JSON dosyalarından sisteme otomatik olarak aktaran ve şema doğrulayan `FinancialDataLoader` modülünün (`src/data_loader.py`) geliştirilmesi.
2. BIST yapısına uygun 3 farklı sektörden (Savunma ve Bilişim, Otomotiv ve Yan Sanayi, Perakende Ticaret) 10 şirkete ait kapsamlı finansal veri setinin (`data/companies_financials.csv`) hazırlanması.
3. Şirket kayıtları, bilanço, rasyolar ve anomali sonuçlarını kalıcı olarak saklamak üzere SQLite tabanlı ilişkisel veritabanı yönetim modülünün (`src/database.py`) kurulması ve tabloların tasarlanması.
4. Z-Score analizine ek olarak sektör ağırlık merkezine çok boyutlu Öklid uzaklığı (Multi-dimensional Normalized Distance) ve negatif özkaynak kuralını içeren hibrit anomali motorunun (`src/anomaly_detector.py`) geliştirilmesi.

**Bu hedeflerin proje açısından neden önemli olduğunu kısaca açıklayınız:**
> **Açıklama:**  
> İlk haftada kodlanan çekirdek rasyo motorunun çalışan gerçek bir sisteme dönüşmesi için verilerin dinamik dosyalardan (CSV/Excel) okunması ve veritabanında kalıcı saklanması zorunludur. Ayrıca çok boyutlu Öklid uzaklığı ve negatif özkaynak gibi kritik iflas kurallarının modele eklenmesi, projenin en temel çıktısı olan şirket risk/anomali puanının finansal hassasiyetini ve güvenilirliğini ciddi ölçüde artırmaktadır.

---

## 2. BU HAFTA YAPILAN ÇALIŞMALAR
**Bu hafta gerçekleştirilen çalışmalar:**  
Bu hafta projenin veri entegrasyonu, kalıcı depolama ve çok boyutlu risk analizi katmanları tamamlandı. İlk olarak `FinancialDataLoader` modülü geliştirilerek bilanço ve gelir tablosundaki 21 zorunlu alanı denetleyen şema doğrulama mekanizması yazıldı. 3 sektör ve 10 şirketi içeren `companies_financials.csv` veri seti oluşturuldu. Veri kalıcılığı için SQLite tabanlı `DatabaseManager` sınıfı yazılarak 4 ilişkisel tablo ve güvenli bağlantı yönetimi (`contextmanager`) kuruldu. Anomali tespit motoruna Çok Boyutlu Öklid Sapma Mesafesi ve negatif özkaynak kuralı eklendi. Tüm veri akışı `main.py` dosyasında birleştirilerek CSV'den veritabanına aktarım, sektör analizi ve formatlı risk özet tablosu uçtan uca çalıştırıldı. Yazılan 4 yeni birim test ile toplam test sayısı 8'e çıkarıldı ve tümü başarıyla geçti.

**Geliştirilen veya güncellenen modüller / özellikler:**
- `src/data_loader.py`: CSV ve JSON formatındaki finansal tabloları okuyan, eksik sütunları ve veri tiplerini denetleyen `FinancialDataLoader` sınıfı sıfırdan geliştirildi.
- `src/database.py`: SQLite veritabanı şemasını oluşturan, şirketleri, finansal tabloları, hesaplanan oranları ve anomali değerlendirmelerini saklayan `DatabaseManager` modülü kodlandı.
- `src/anomaly_detector.py`: Çok boyutlu uzaklık (Multi-dimensional Euclidean Distance of Z-Scores) ve negatif özkaynak kuralı eklenerek anomali motoru v0.2'ye yükseltildi.
- `data/companies_financials.csv` & `tests/`: 3 sektörlü 10 şirketlik veri seti hazırlandı; veritabanı ve veri yükleyici için 4 yeni birim test yazılarak toplam 8 teste ulaşıldı.

**Bu çalışmalar sonucunda projede meydana gelen değişiklikler:**  
Proje, yalnızca bellekte çalışan izole bir prototip olmaktan çıkarak; harici CSV dosyalarından veri aktaran, ilişkisel SQLite veritabanında tüm hesaplamaları kalıcı saklayan, çok boyutlu matematiksel anomali analizi yapan ve şirketleri sektörel bazda sıralayan tam entegre bir arka uç (backend) analiz sistemine dönüştü.

---

## 3. PROJENİN TAMAMLANMA DURUMU
**Tamamlanan çalışmalar:**
- CSV ve JSON veri yükleyici modülü (`FinancialDataLoader`)
- 10 şirketli ve 3 sektörlü genişletilmiş finansal veri seti (`companies_financials.csv`)
- SQLite ilişkisel veritabanı mimarisi ve CRUD servisleri (`DatabaseManager`)
- Çok boyutlu Öklid sapma mesafesi ve negatif özkaynak risk kuralları (`FinancialAnomalyDetector`)
- Veritabanı ve veri yükleyici birim testleri (toplam 8 testin tamamı başarılı)
- Konsol üzerinden çalışan entegre versiyon 0.2 demosu (`main.py`)

**Devam eden çalışmalar:**
- Çok boyutlu mesafe analizini scikit-learn kütüphanesindeki `Isolation Forest` ve `Local Outlier Factor (LOF)` makine öğrenmesi modelleriyle kıyaslama ve model optimizasyonu.
- Veritabanındaki verileri ve sektör kıyaslamalarını dinamik grafiklerle gösterecek Web Dashboard (`Streamlit`) arayüz tasarımı.

**Başlanamayan veya ertelenen çalışmalar:**
- Kullanıcı giriş/yetkilendirme sistemi ve rol bazlı erişim (sonraki haftalara planlandı).
- Canlı BIST/KAP veri çekme API entegrasyonu (veri sağlayıcı sınırlamaları nedeniyle simüle veri setiyle devam edildi).

**Projenin tahmini genel tamamlanma oranı:** **% 45**  
**Bu oranı neye göre belirlediğinizi kısaca açıklayınız:**  
5 aşamalı yol haritamızda: (1) Çekirdek matematiksel rasyo motoru [%20 - Tamamlandı], (2) Veri aktarımı (ETL), SQLite veritabanı kalıcılığı ve gelişmiş çok boyutlu risk motoru [%25 - Bu hafta tamamlandı], (3) Makine öğrenmesi modeli optimizasyonu ve API katmanı [%20], (4) Web Arayüzü / Görsel Analiz Dashboard'u [%20], (5) Test, optimizasyon ve dokümantasyon [%15]. İlk iki aşama eksiksiz tamamlandığı için toplam tamamlanma oranı %45'e yükselmiştir.

---

## 4. TEKNİK ÇALIŞMALAR
**İlgili alanlar:**
- [ ] Arayüz / UI geliştirme
- [x] Veritabanı işlemleri
- [x] Backend geliştirme
- [ ] API geliştirme / API kullanımı
- [ ] Kullanıcı giriş ve yetkilendirme
- [x] Dosya işlemleri
- [x] Test işlemleri
- [x] Hata düzeltme / Debugging
- [x] Git / GitHub kullanımı
- [x] Kod iyileştirme / Refactoring
- [x] Dokümantasyon
- [x] Diğer: Çok Boyutlu İstatistiksel Analiz ve Veri Normalizasyonu

**Bu hafta kullandığınız programlama dili / dilleri:**  
Python 3.12

**Kullandığınız teknoloji, framework, kütüphane veya araçlar:**  
Python Standart Kütüphanesi (`sqlite3`, `csv`, `json`, `math`, `contextlib`, `unittest`, `dataclasses`, `os`), Git, VS Code IDE, Google Gemini / Antigravity AI Asistanı.

**Bu teknolojileri hangi amaçlarla kullandığınızı açıklayınız:**
- `sqlite3`: Şirketler, finansal tablolar, rasyolar ve anomali sonuçları arasında ilişkisel veri modeli kurarak kalıcı depolama sağlamak için.
- `csv` & `json`: Harici kaynaklardan sağlanan finansal verileri tablo formatında sisteme güvenle aktarmak (ETL) için.
- `contextlib`: Veritabanı bağlantılarını güvenli açıp kapatmak, Windows üzerinde dosya kilitleme ve sızıntı hatalarını önlemek için.
- `math`: Çok boyutlu Z-Score vektörlerinin Öklid normunu hesaplayarak sektörden genel sapma mesafesini bulmak için.
- `unittest`: Yeni eklenen veri yükleyici ve veritabanı modüllerinin doğruluğunu otomatik testlerle teyit etmek için.

---

## 5. KARŞILAŞILAN PROBLEMLER VE ÇÖZÜMLER
### Problem 1
- **Karşılaşılan problem:** Windows işletim sisteminde birim testler (`test_database.py`) çalıştırılırken, `tearDown` metodunda test veritabanı dosyası silinmek istendiğinde `PermissionError: [WinError 32] Dosya başka bir işlem tarafından kullanıldığından bu işlem dosyaya erişemiyor` hatası alındı ve testler başarısız oldu.
- **Problemin nedeni:** SQLite bağlantısı standart `with conn:` bloğunda kullanıldığında; `with` yapısı yalnızca işlemleri (commit/rollback) yönetir, bağlantıyı fiziksel olarak kapatmaz (`close`). Açık kalan bağlantı nedeniyle Windows dosya kilidi aktif kaldı ve dosya silinemedi.
- **Problemi çözmek için neler yaptınız:** `src/database.py` içerisinde `contextlib.contextmanager` dekoratörü kullanılarak `get_connection()` metodu yazıldı. `try-finally` bloğuyla her veritabanı işleminden sonra `conn.close()` çağrısı garanti altına alındı.
- **Sonuç:** Veritabanı bağlantı sızıntıları ve dosya kilitlenme hataları tamamen ortadan kaldırıldı; birim testler başarıyla geçti.

### Problem 2
- **Karşılaşılan problem:** Perakende sektöründeki şirketlerin (Migros, BİM, Şok) doğaları gereği vadeli mal alıp günlük nakit satmaları nedeniyle cari oranlarının 1.0'ın altında çıkması ve sistemin bu şirketlere haksız yere aşırı yüksek likidite riski ataması.
- **Problemin nedeni:** Farklı sektörlerin finansal operasyon modelleri birbirinden tamamen farklıdır; perakende sektöründe negatif işletme sermayesi normal bir finansman modeliyken, teknoloji sektöründe cari oranın 1'in altında olması ciddi bir kriz belirtisidir.
- **Problemi çözmek için neler yaptınız:** Kural bazlı risk kontrollerine ek olarak "Çok Boyutlu Sektörel Uzaklık" metriği entegre edildi ve perakende şirketlerinin sektör kendi içindeki ortalamalarıyla kıyaslanması sağlandı. Ayrıca risk etiketleri Düşük, Orta, Yüksek ve Kritik Risk olarak yeniden kalibre edildi.
- **Sonuç:** Şirketlerin sadece genel ezber kurallarla değil, kendi sektör dinamiklerine göre göreceli olarak değerlendirilmesi sağlandı; perakende şirketleri iflas riski yerine sektör normlarına uygun olarak "Orta Risk / Takip Edilmeli" şeklinde sınıflandırıldı.

---

## 6. KOD VE PROJE KANITLARI
- **GitHub / Repository:** https://github.com/MUSTAFAKRMZL/finansal-sektor-analiz-sistemi
- **Commit Sayısı:** 3 commit
- **Önemli Commitler:**
  - `feat: Hafta 2 - CSV veri yukleyici, SQLite veritabani ve cok boyutlu anomali motoru`
  - `fix: SQLite contextmanager baglanti yonetimi ve WinError 32 dosya kilidi cozumu`
  - `test: Veritabani ve veri yukleyici icin birim testlerin yazilmasi (8 test OK)`
- **Çalışan Demo:** `python main.py` ile çalışan konsol veri tabanı & sektör analiz dashboard'u.

### Kod Örneği:
**Kodun Amacı:** Çok boyutlu Z-Score sapma mesafesini (Multi-dimensional Euclidean Distance) ve negatif özkaynak kuralını hesaplayarak 0-100 bileşik risk skoru üreten `FinancialAnomalyDetector.evaluate_risk` metodu.

```python
def evaluate_risk(self, comparison_data: Dict[str, Any]) -> Dict[str, Any]:
    comparisons = comparison_data.get("comparisons", [])
    anomalies, critical_flags = [], []
    total_penalty = 0.0
    squared_deviations = []

    for item in comparisons:
        cat, metric, val, z = item["category"], item["metric"], item["company_value"], item.get("z_score")
        if val is None:
            continue

        # 1. Z-Score Bazlı Sapma Kontrolü (|Z| >= threshold)
        if z is not None:
            squared_deviations.append(z ** 2)
            if abs(z) >= self.z_threshold:
                direction = "Aşırı Yüksek" if z > 0 else "Aşırı Düşük"
                anomalies.append({
                    "metric": f"{cat}.{metric}", "value": val, "z_score": z,
                    "message": f"Sektör ortalamasından {abs(z):.2f} standart sapma kadar {direction}."
                })
                total_penalty += min(abs(z) * 5.0, 15.0)

        # 2. Kritik Kural Eşikleri
        if metric == "current_ratio" and val < 1.0:
            critical_flags.append(f"Kritik Likidite Riski: Cari oran ({val}) 1.0 altında.")
            total_penalty += 20.0
        elif metric == "financial_leverage" and val > 0.80:
            critical_flags.append(f"Yüksek Borçluluk Riski: Kaldıraç oranı ({val}) %80 üzerinde.")
            total_penalty += 20.0
        elif metric == "equity_ratio" and val < 0.0:
            critical_flags.append("Negatif Özkaynak: Sermaye kaybı ve teknik iflas riski.")
            total_penalty += 25.0

    # 3. Çok Boyutlu Öklid Uzaklığı
    multi_dim_distance = 0.0
    if squared_deviations:
        multi_dim_distance = round(math.sqrt(sum(squared_deviations) / len(squared_deviations)), 2)
        if multi_dim_distance > 1.8:
            total_penalty += (multi_dim_distance - 1.8) * 10.0

    risk_score = round(min(max(total_penalty, 0.0), 100.0), 1)
    return {
        "company_code": comparison_data["company_code"],
        "risk_score": risk_score,
        "multi_dim_distance": multi_dim_distance,
        "anomalies": anomalies,
        "critical_flags": critical_flags
    }
```

**Kodun Nasıl Çalıştığı:**  
Bu metot, bir şirketin tüm finansal rasyolarını sektörün ortalamalarıyla kıyaslar. Her bir göstergenin Z-Score değerinin karesini toplayarak çok boyutlu uzayda sektörün merkezinden ne kadar uzaklaşıldığını gösteren ortalama Öklid sapmasını hesaplar. Aynı zamanda cari oranın 1'in altına inmesi, kaldıracın %80'i aşması ve özkaynakların eksiye düşmesi gibi hayati finansal riskleri kontrol ederek ceza puanları uygular. Sonuç olarak 0 ile 100 arasında normalize edilmiş güvenilir bir risk skoru ve tespit edilen anomali listesini üretir.

---

## 7. BU HAFTA ÖĞRENİLEN YENİ BİLGİLER
1. Python'da `sqlite3` kullanırken `with connection:` bloğunun bağlantıyı kapatmadığını, sadece transaction yönettiğini; bağlantıyı kapatmak için `contextlib.contextmanager` ve `conn.close()` yapısının şart olduğunu öğrendim.
2. Finansal anomali analizinde tek tek rasyolara bakmanın sektörel özellikleri (örneğin perakendede düşük cari oran) kaçırabileceğini, çok boyutlu uzaklık (Multi-dimensional Euclidean Distance) ile şirketin tüm göstergelerinin bir arada değerlendirilmesinin doğruluğu katbekat artırdığını kavradım.
3. CSV dosyalarında Türkçe karakter ve başlık hatalarını önlemek için `utf-8-sig` kodlamasının ve `DictReader` ile zorunlu alan doğrulamasının endüstriyel standart olduğunu deneyimledim.

- **En Önemli Bilgi:** Veritabanı kaynak yönetiminde (resource management) bağlantıların düzgün kapatılmamasının özellikle dosya tabanlı veritabanlarında (SQLite) işletim sistemi seviyesinde kilitlenmelere yol açtığını ve bunu `contextmanager` ile temiz şekilde çözmeyi öğrenmekti.
- **Yeniden Kullanılabilirlik:** Evet. SQLite veritabanı mimarisi, veri yükleyici şablonu ve çok boyutlu aykırı değer analizi tüm yazılım ve veri bilimi projelerinde doğrudan uygulanabilir standart yöntemlerdir.

---

## 8. GELECEK HAFTANIN PLANI
1. Streamlit kütüphanesi kullanarak web tabanlı interaktif görsel analiz dashboard'unun (Arayüz / UI) kodlanması.
2. Şirketlerin rasyolarını sektör ortalamalarıyla görselleştiren Radar Grafikleri (Spider Chart) ve Bar Grafikleri bileşenlerinin entegre edilmesi.
3. scikit-learn tabanlı `Isolation Forest` anomali tespit modelinin çok boyutlu veri setimiz üzerinde eğitilerek mevcut Z-Score motoruyla karşılaştırılması.
4. Kullanıcının arayüzden yeni bir şirkete ait bilanço verilerini girerek anlık analiz ve risk raporu alabilmesini sağlayan dinamik form ekranının tasarlanması.

- **Öncelikli Problem/Özellik:** Öncelikli hedefim; konsolda çalışan tüm bu analiz çıktısını Streamlit web arayüzüne taşıyarak kullanıcının tek tıkla şirket seçip sektör karşılaştırma grafiklerini ve anomali radarını interaktif görebileceği görsel arayüzü tamamlamaktır.

---

## 9. YAPAY ZEKÂ DESTEKLİ PROJE GELİŞTİRME SÜRECİ

### 9.1. Bu Hafta Kullandığınız Yapay Zekâ Araçları
- **Kullandığım araçlar:** Google Gemini, ChatGPT, Antigravity AI Asistanı
- **Kullanım süresi:** [x] 1–3 saat

### 9.2. Yapay Zekâyı Hangi Amaçlarla Kullandınız?
- **Başlıca amaçlar:** SQLite ilişkisel veritabanı şema tasarımı, Windows SQLite dosya kilitlenme hatasının (`WinError 32`) çözümü, çok boyutlu Öklid uzaklığı formülasyonu ve CSV veri okuma doğrulama mekanizması.
- **En çok kullanılan konu:** SQLite ilişkisel tablo şeması (`foreign key`, `unique constraint`) ve bağlantı yönetiminde `contextmanager` kullanımı.
- **Neden ihtiyaç duyuldu:** Çok tablolu bir yapıda veri bütünlüğünü koruyan ve testlerde dosya kilitleme yapmayan temiz bir Pythonic veritabanı mimarisi kurmak için.

### 9.3. Yapay Zekâya Başvurmadan Önce Ne Yaptınız?
- **Problemi önce kendim çözmeye çalıştım:** [x] Evet
- **Yapılan araştırmalar:** Python resmi SQLite dokümantasyonunu ve `unittest` yaşam döngüsünü inceledim; testlerde neden dosyanın silinemediğini hata kodundan (`WinError 32`) araştırdım.
- **Başvurma nedenleri:**
  - [x] Yazdığım kod hata verdi.
  - [x] Daha hızlı bir çözüm üretmek istedim.
  - [x] Alternatif bir çözüm aradım.
  - [x] Yazdığım kodu kontrol ettirmek istedim.
  - [x] Konuyu öğrenmek istedim.

### 9.4. Bu Hafta Kullandığınız Önemli Promptlar
- **Prompt 1:** *"Python sqlite3 ile şirketler, finansal tablolar, rasyolar ve anomali sonuçlarını tutacak ilişkisel bir veritabanı sınıfı yaz. Şirket ve periyot bazında mükerrer kayıtları engelleyecek ON CONFLICT yapıları içersin."*  
  *(Cevap: SQLite DDL tabloları ve UPSERT sorguları önerdi. [x] Küçük değişiklikler yaparak modellerimizin alanlarına göre uyarladım).*
- **Prompt 2:** *"unittest içinde test_database çalıştırırken tearDown metodunda os.remove(db_path) WinError 32 veriyor. with conn bloğu kullanmama rağmen dosya neden kilitli kalıyor ve nasıl çözülür?"*  
  *(Cevap: with sqlite3.connect yapısının bağlantıyı kapatmadığını, sadece commit yaptığını açıkladı ve contextmanager ile close garantisi sağlayan yapıyı sundu. [x] Doğrudan uyguladım).*
- **Prompt 3:** *"Bir şirketin 14 farklı rasyosunun sektör Z-score değerlerini tek bir çok boyutlu sapma skorunda birleştirmek için matematiksel olarak Öklid normu nasıl uygulanır?"*  
  *(Cevap: Z-skorlarının karelerinin ortalamasının karekökünü (Root Mean Square Z-score) alarak sektör merkezine uzaklığı hesaplama formülü sundu. [x] Küçük değişiklikler yaparak risk ceza puanına entegre ettim).*

### 9.5. Yapay Zekâ Tarafından Üretilen Kodlar
- **Kullanılan kod:** `get_connection` context manager fonksiyonu:
  ```python
  @contextmanager
  def get_connection(self):
      conn = sqlite3.connect(self.db_path)
      conn.row_factory = sqlite3.Row
      try:
          yield conn
      finally:
          conn.close()
  ```
- **Kodun yaptığı iş:** Veritabanı işlemlerinde bağlantıyı açar ve işlem bittiğinde veya beklenmedik bir hata fırlatıldığında `finally` bloğu ile bağlantıyı mutlaka kapatır; Windows üzerinde dosya kilitleme oluşmasını engeller.
- **Nasıl kullanıldı:** [x] Küçük değişiklikler yaptım.
- **Yapılan değişiklikler:** Bağlantıya `conn.row_factory = sqlite3.Row` ayarını ekleyerek sonuçların sözlük gibi sütun isimleriyle okunabilmesini sağladım.
- **Çalışma mantığı anlaşılıyor muydu:** [x] Tamamen anlıyordum.

### 9.6. Yapay Zekâ Çıktılarının Kontrolü
- **Kontrol:** Kodu çalıştırarak test ettim, satır satır inceledim, resmi Python `contextlib` dokümantasyonundan doğruladım.
- **Tespit edilen hata:** Yapay zekanın ilk önerdiği CSV okuyucuda Türkçe karakterli sütunlarda (`ş`, `ı`, `ğ`) UTF-8 BOM kaynaklı ilk sütun adı okuma hatası oluşuyordu; bunu `encoding='utf-8-sig'` kullanarak düzelttim.

### 9.7. Karşılaşılan Problemler
- **En önemli problem:** Yapay zekanın ilk etapta veritabanı için gereksiz yere ağır bir harici ORM kütüphanesi (`SQLAlchemy`) önermesi.
- **Çözüm:** Projeyi hafif, hızlı ve harici bağımlılıksız tutmak adına Python'ın yerleşik `sqlite3` kütüphanesiyle temiz bir `DatabaseManager` sınıfı yazdım.

### 9.8. Yapay Zekâ Olmasaydı Ne Olurdu?
- [x] Evet, ancak daha uzun sürede tamamlayabilirdim. WinError 32 bağlantı kilidi hatasını tespit etmek ve çok boyutlu istatistiksel uzaklık formülünü kalibre etmek daha fazla araştırma süresi gerektirirdi.

### 9.9. Öğrenmeye Etkisi
- [x] Evet. SQLite transaction yönetimi ile connection yaşam döngüsü arasındaki kritik farkı ve çok boyutlu vektör sapması analizini öğrendim.

### 9.10. Değerlendirme ve Oranlar
- **Yapay Zekâ Kullanım Oranım:** **% 30**
- **Kodun Yapay Zekâ Tarafından Oluşturulma Oranı:** **% 25**
- **Değerlendirme:** [x] Genellikle kendim çalıştım, ihtiyaç duyduğumda yapay zekâ kullandım.
- **Gerekçe:** Mimariyi, veri tablolarını, perakende sektörü risk kalibrasyonunu ve test senaryolarını kendim tasarladım. Yapay zekayı sadece bağlantı hatası debugging'i ve SQL UPSERT syntax desteği için danışman olarak kullandım.

### 9.11. Genel Değerlendirme
Bu hafta yapay zekâ, özellikle veritabanı şemasının optimizasyonu ve Windows ortamındaki dosya kilitleme (WinError 32) sorununun çözülmesinde bana ciddi zaman kazandırdı. Bununla birlikte finansal mantık, perakende sektöründeki negatif işletme sermayesi kalibrasyonu ve veri yükleyici doğrulamaları tamamen kendi denetimimde şekillendirildi. Yapay zekanın önerdiği kodların iç mantığını ve işletim sistemi seviyesindeki etkilerini anlayarak kullandım; bu sayede projenin arka uç güvenilirliği ve test kapsamı en üst seviyeye ulaştı.

### 9.12. Kanıtlar
1. `src/database.py` (SQLite `DatabaseManager` ve `contextmanager` bağlantı yönetimi)
2. `src/data_loader.py` (CSV/JSON ayrıştırıcı ve şema doğrulama)
3. `src/anomaly_detector.py` (Çok boyutlu Öklid uzaklığı metriği)
4. `tests/` klasöründeki 8 adet başarılı birim test çıktısı (`Ran 8 tests in 0.062s - OK`)

---

## 10. HAFTALIK GENEL ÖZ DEĞERLENDİRME
- **En başarılı olunan konu:** SQLite veritabanı ile dosya yükleme katmanını sıfır dış bağımlılıkla ve tüm birim testlerden başarıyla geçecek şekilde entegre etmek.
- **En fazla zorlanılan konu:** Windows üzerinde SQLite bağlantılarının açık kalarak dosya kilidi oluşturması ve perakende sektöründeki yapısal bilanço farklılıklarının anomali puanına etkisi.
- **Farklı yapılacak şey:** Veritabanı bağlantılarını en başından contextmanager ile tasarlamak.
- **Haftalık Puan:** **9.5 / 10**
- **Puan Gerekçesi:** Planlanan tüm veri yükleme, SQLite kalıcılık, çok boyutlu anomali analizi ve test hedefleri eksiksiz tamamlandı; sistem uçtan uca hatasız çalışmaktadır.
