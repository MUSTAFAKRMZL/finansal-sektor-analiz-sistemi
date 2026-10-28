# HAFTALIK YAZILIM PROJESİ GELİŞİM RAPORU (HAFTA 3)

- **Ders:** Yazılım Geliştirme I
- **Proje Adı:** Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi
- **Öğrenci Adı Soyadı:** Mustafa Kırmızı
- **Öğrenci No:** 24130766
- **Hafta No:** 3
- **Tarih:** 28 / 10 / 2026

---

## 1. BU HAFTANIN HEDEFLERİ
**Bu hafta proje kapsamında gerçekleştirmeyi planladığınız çalışmaları yazınız:**
1. Finansal rasyo vektörlerini makine öğrenmesi algoritmalarına hazırlamak amacıyla Min-Max \([0, 1]\) veri normalizasyonu modülünün (`DataNormalizer`) geliştirilmesi.
2. Denetimsiz makine öğrenmesi tabanlı `Isolation Forest` (İzolasyon Ormanı) ve `k-NN` (k-En Yakın Komşu) aykırı değer tespit algoritmalarının (`src/ml_anomaly.py`) kodlanması.
3. İstatistiksel Z-Score, finansal iflas kuralları ve makine öğrenmesi skorlarını ağırlıklı birleştiren Hibrit Anomali Motorunun (`HybridAnomalyEngine`) oluşturulması.
4. Şirket-sektör kıyaslamalarını SVG Radar Grafiği (Örümcek Ağı), Sütun Grafikleri ve Canlı Bilanço Simülatörü ile sunan İnteraktif Web Görsel Analiz Ekranının (`src/web_dashboard.py` & `dashboard.html`) tasarlanması.

**Bu hedeflerin proje açısından neden önemli olduğunu kısaca açıklayınız:**
> **Açıklama:**  
> Proje şartnamesinin en kritik çıktıları olan *"veri normalizasyonu, makine öğrenmesi uygulamaları ve görsel analiz ekranı"* bu haftanın hedefleriyle doğrudan hayata geçirilmektedir. Özellikle perakende gibi yapısal olarak düşük cari oranla çalışan sektörlerde salt kural bazlı sistemlerin ürettiği yanlış pozitif (false-positive) alarmları önlemek için Isolation Forest ve k-NN kümeleme modellerinin entegrasyonu hayati önem taşımaktadır.

---

## 2. BU HAFTA YAPILAN ÇALIŞMALAR
**Bu hafta gerçekleştirilen çalışmalar:**  
Bu hafta projenin makine öğrenmesi katmanı ve görsel analiz arayüzü (Web Dashboard) tamamlandı. İlk olarak 13 temel finansal rasyoyu \([0, 1]\) aralığına çeken `DataNormalizer` sınıfı geliştirildi ve sıfır varyanslı sütunlar için güvenli koruma eklendi. Ardından Liu vd. (2008) makalesindeki matematiksel formülasyona (Euler sabiti ve harmonik yol uzunluğu düzeltmesi \(c(n)\)) sadık kalınarak 100 ağaçlı `IsolationForestDetector` ve komşuluk mesafesini ölçen `KNNOutlierDetector` sınıfları saf Python ile kodlandı. İstatistiksel Z-Score (%55), Isolation Forest (%30) ve k-NN (%15) skorlarını harmanlayan `HybridAnomalyEngine` oluşturuldu. Görsel analiz için HTML5, CSS Grid ve dinamik SVG grafik motoru kullanan `DashboardGenerator` yazılarak Radar Grafiği, Sektör Karşılaştırma Bar Grafiği ve tarayıcı üzerinde anlık yeni şirket testi yapılabilen Canlı Bilanço Simülatörü (`dashboard.html`) üretildi. Son olarak 4 yeni birim test (`test_ml_anomaly.py`) eklenerek toplam 12 testin tamamı başarıyla çalıştırıldı.

**Geliştirilen veya güncellenen modüller / özellikler:**
- `src/ml_anomaly.py`: `DataNormalizer`, `IsolationForestDetector` (100 ağaçlı izolasyon ormanı), `KNNOutlierDetector` ve `HybridAnomalyEngine` sınıfları sıfırdan geliştirildi.
- `src/web_dashboard.py` & `dashboard.html`: SVG Radar (Örümcek Ağı) grafiği, grup sütun grafikleri, KPI kartları, sektör filtreleri ve canlı bilanço simülatörü içeren Web Dashboard modülü kodlandı.
- `main.py`: Hibrit ML motorunu çalıştırıp sonuçları SQLite veritabanına kaydeden ve tek komutla `dashboard.html` üreten entegre sürüme (`v0.3.0`) yükseltildi.
- `tests/test_ml_anomaly.py`: Normalizasyon sınır durumlarını, Isolation Forest aykırı değer sıralamasını, k-NN dedektörünü ve HTML üretimini doğrulayan 4 yeni birim test eklendi (Toplam 12/12 test başarılı).

**Bu çalışmalar sonucunda projede meydana gelen değişiklikler:**  
Proje, sadece arka uçta çalışan bir konsol uygulaması olmaktan çıkarak; makine öğrenmesi (Isolation Forest & k-NN) ile çok boyutlu anomali tespiti yapan ve kullanıcıya tarayıcı üzerinde interaktif Radar/Bar grafikleri ile canlı bilanço simülasyonu sunan tam teşekküllü bir Görsel Karar Destek Sistemine dönüştü.

---

## 3. PROJENİN TAMAMLANMA DURUMU
- **Tamamlanan çalışmalar:**
  - Min-Max veri normalizasyonu ve özellik vektörü çıkarımı (`DataNormalizer`)
  - Isolation Forest (İzolasyon Ormanı) makine öğrenmesi anomali modeli (`IsolationForestDetector`)
  - k-NN komşuluk mesafesi tabanlı aykırı değer dedektörü (`KNNOutlierDetector`)
  - İstatistiksel + Kural + ML ağırlıklı Hibrit Risk Motoru (`HybridAnomalyEngine`)
  - SVG Radar ve Bar grafikli İnteraktif Web Dashboard ve Canlı Bilanço Simülatörü (`web_dashboard.py` & `dashboard.html`)
  - Makine öğrenmesi ve görsel arayüz birim testleri (12/12 test başarılı)
- **Devam eden çalışmalar:**
  - Çok dönemli (2021, 2022, 2023) tarihsel trend analizi ve dönemler arası rasyo değişim grafiklerinin arayüze eklenmesi.
  - Analiz sonuçlarının tek tıkla yazdırılabilir kurumsal PDF/HTML özet raporu olarak dışa aktarılması.
- **Başlanamayan veya ertelenen çalışmalar:**
  - Kullanıcı bazlı oturum yönetimi ve özel portföy kaydetme özelliği (sonraki haftalara planlandı).
- **Projenin tahmini genel tamamlanma oranı:** **% 75**  
- **Bu oranı neye göre belirlediğinizi kısaca açıklayınız:**  
  5 aşamalı proje planımızda: (1) Çekirdek matematiksel rasyo motoru [%20 - Tamamlandı], (2) CSV/JSON Veri aktarımı ve SQLite veritabanı [%25 - Tamamlandı], (3) Veri normalizasyonu ve Makine Öğrenmesi (Isolation Forest) anomali modeli [%15 - Bu hafta tamamlandı], (4) İnteraktif Görsel Analiz Ekranı / Web Dashboard [%15 - Bu hafta tamamlandı], (5) Çok dönemli trend analizi, PDF raporlama, genel optimizasyon ve final dokümantasyonu [%25 - Kalan kısım]. İlk 4 ana hedef tamamlandığı için proje %75 oranına ulaşmıştır.

---

## 4. TEKNİK ÇALIŞMALAR
- [x] Arayüz / UI geliştirme
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
- [x] Diğer: Makine Öğrenmesi (Isolation Forest & k-NN) ve Veri Normalizasyonu

- **Programlama Dili:** Python 3.12, HTML5, CSS3, JavaScript (ES6+), SVG
- **Teknoloji ve Araçlar:** Python Standart Kütüphanesi (`math`, `random`, `json`, `sqlite3`, `http.server`, `unittest`), HTML5/CSS3 Grid, Dinamik SVG Grafik Motoru (Radar & Bar Chart), VS Code IDE, Google Gemini / Antigravity AI Asistanı.
- **Kullanım Amaçları:**
  - `math` & `random`: Isolation Forest ağaç bölümlemelerini, Euler harmonik yol uzunluğu fonksiyonunu \(c(n)\) ve k-NN Öklid mesafelerini deterministik (`seed=42`) olarak hesaplamak için.
  - `HTML5`, `CSS3` & `JavaScript`: Kullanıcının sektör ve şirket seçerek anlık analiz yapabileceği ve yeni bilanço simüle edebileceği interaktif arayüz için.
  - `Dinamik SVG`: Harici grafik kütüphanesi bağımlılığı olmadan yüksek çözünürlüklü Örümcek Ağı (Radar) ve Sütun (Bar) karşılaştırma grafiklerini çizmek için.
  - `http.server` & `unittest`: Yerel web sunucusu başlatmak ve ML algoritmalarını 12 birim testle doğrulamak için.

---

## 5. KARŞILAŞILAN PROBLEMLER VE ÇÖZÜMLER
### Problem 1
- **Karşılaşılan problem:** Finansal oranların ölçeklerinin birbirinden çok farklı olması (örneğin Stok Devir Hızı `15.0` iken ROA `0.08` veya Borç/Özkaynak `-2.38`) nedeniyle k-NN mesafe algoritmasında büyük ölçekli oranların küçük ölçekli kârlılık oranlarını tamamen domine etmesi ve sabit değerli sütunlarda normalizasyon sırasında sıfıra bölünme oluşması.
- **Problemin nedeni:** Mesafe tabanlı makine öğrenmesi algoritmaları (k-NN, LOF) özelliklerin mutlak büyüklüğüne duyarlıdır. Normalizasyon yapılmadığında sayısal aralığı geniş olan değişken tek başına mesafeyi belirler; ayrıca tüm şirketlerde aynı çıkan bir oranda (`max == min`) Min-Max paydası 0 olur.
- **Problemi çözmek için neler yaptınız:** `DataNormalizer.min_max_normalize` metodu yazılarak tüm 13 finansal rasyo `[0.0, 1.0]` aralığına ölçeklendi. `abs(c_max - c_min) < 1e-9` kontrolü eklenerek varyansı sıfır olan sütunlara güvenli şekilde nötr `0.5` değeri atandı.
- **Sonuç:** Tüm finansal göstergeler eşit ağırlıkla modele katıldı, sıfıra bölünme hatası engellendi ve birim test (`test_min_max_normalization_and_zero_variance`) ile doğrulandı.

### Problem 2
- **Karşılaşılan problem:** Perakende sektöründeki sağlıklı şirketlerin (BİM, Migros) yapısal olarak düşük cari oranla çalışmaları sebebiyle Hafta 2'deki kural bazlı sistemde 30-50 arası risk puanı alması; buna karşın yazılımda stoksuz çalışan şirketlerin (Logo) aşırı yüksek stok devir hızı nedeniyle ML modelinde tek başına anomali görünmesi.
- **Problemin nedeni:** Tek başına kural bazlı sistemler sektör içi kümeleşmeyi göremez; tek başına denetimsiz ML (Isolation Forest) ise pozitif yönlü aşırı performansı (çok yüksek likidite veya kârlılık) negatif finansal riskten ayırt edemez.
- **Problemi çözmek için neler yaptınız:** İstatistiksel/Kural skoru (%55), Isolation Forest (%30) ve k-NN (%15) çıktıları `HybridAnomalyEngine` içinde birleştirildi. Perakende şirketleri kendi aralarında sıkı kümelendiği için ML skorları düşük çıktı (`7.4 - 11.6`) ve BİM'in hibrit riski `19.8`'e (Düşük Risk) gerilerken, gerçekten batık olan `RISKY_TECH` hem kural (`100`) hem ML (`78.4`) hem k-NN (`85.0`) modellerinde yakalanarak `95.7` Hibrit Risk puanı aldı.
- **Sonuç:** Yanlış pozitif (false-positive) uyarılar azaltıldı ve hem sektörel kümeleşmeyi hem de finansal iflas kurallarını dikkate alan çok daha isabetli bir karar destek mekanizması elde edildi.

---

## 6. KOD VE PROJE KANITLARI
- **GitHub / Repository:** https://github.com/mustafakirmizi/finansal-sektor-analiz-sistemi
- **Commit Sayısı:** 3 commit
- **Önemli Commitler:**
  - `feat: Hafta 3 - Min-Max veri normalizasyonu, Isolation Forest ve k-NN ML anomali modelleri (src/ml_anomaly.py)`
  - `feat: Interaktif SVG Radar/Bar grafikli Web Dashboard ve canli bilanco simulatoru (src/web_dashboard.py & dashboard.html)`
  - `test: ML modelleri ve dashboard uretimi icin 4 yeni birim test eklendi (Toplam 12 test OK)`
- **Çalışan Demo:** `c:\Users\MONSTER\Desktop\yazılımgeliştirme1ödev\dashboard.html`

### Kod Örneği:
**Kodun Amacı:** Eğitilen 100 adet İzolasyon Ağacı (Isolation Tree) üzerinden şirketlerin ortalama izolasyon yol uzunluğunu \(E(h(x))\) hesaplayan ve Euler harmonik sabiti \(c(n)\) ile normalize ederek 0-100 aralığında makine öğrenmesi anomali skoru üreten `IsolationForestDetector.score_samples` metodu.

```python
def score_samples(self, X: List[List[float]]) -> List[float]:
    """
    Her bir örnek için [0, 100] aralığında Isolation Forest anomali skoru döndürür.
    Kısa ortalama yol uzunluğu (hızlı izolasyon) -> Yüksek anomali skoru.
    """
    if not self.trees or self.n_samples <= 1:
        return [0.0 for _ in X]

    c_n = _c_factor(self.n_samples)
    if c_n <= 0:
        return [0.0 for _ in X]

    scores = []
    for x in X:
        avg_path = sum(self._path_length(x, t, 0) for t in self.trees) / len(self.trees)
        # Standart IF skoru: s = 2^(-E(h(x)) / c(n)), aralık (0, 1)
        raw_if_score = math.pow(2.0, -avg_path / c_n)
        # 0-100 ölçeğine kalibrasyon
        calibrated = max(0.0, min(100.0, (raw_if_score - 0.35) / 0.45 * 100.0))
        scores.append(round(calibrated, 1))
    return scores
```

**Kodun Nasıl Çalıştığı:**  
Isolation Forest algoritmasında aykırı (anomalili) bir şirket, normal şirket kümesinden çok uzakta olduğu için rastgele özellik bölmeleriyle kök düğüme çok yakın seviyelerde (kısa yol uzunluğu ile) izole edilir. Bu metot, her şirket vektörü `x` için 100 ağaçtaki yol uzunluklarının ortalamasını (`avg_path`) alır ve teorik ortalama ağaç derinliği `c(n)` ile oranlayarak \(2^{-\text{avg\_path} / c(n)}\) formülünü uygular. Yol kısaldıkça üs sıfıra yaklaşır ve skor 1'e (100 puana) yükselir.

---

## 7. BU HAFTA ÖĞRENİLEN YENİ BİLGİLER
1. Isolation Forest algoritmasının çalışma prensibini, ikili arama ağaçlarında ortalama başarısız arama yolu uzunluğu formülü olan \(c(n) = 2H(n-1) - 2(n-1)/n\) eşitliğini ve denetimsiz anomali tespitinin matematiksel temellerini öğrendim.
2. Çok boyutlu veri analizinde Min-Max normalizasyonunun k-NN gibi Öklid mesafesi kullanan algoritmalar üzerindeki belirleyici etkisini ve sıfır varyans (sabit sütun) istisnalarının nasıl yönetileceğini deneyimledim.
3. Harici bir grafik kütüphanesine ihtiyaç duymadan trigonometrik birim çember koordinatlarıyla (\(\cos, \sin\)) dinamik SVG Radar (Örümcek Ağı) grafiği çizmeyi öğrendim.

- **En Önemli Bilgi:** Denetimsiz makine öğrenmesi modellerinin "farklı olanı" bulmakta çok güçlü olduğunu, ancak bu farklılığın finansal açıdan "iyi bir ayrışma mı (yüksek likidite/kâr)" yoksa "tehlikeli bir risk mi (iflas sinyali)" olduğunu ayırt etmek için alan bilgisi (domain rules) ile hibritlenmesi gerektiğini kavramaktı.
- **Yeniden Kullanılabilirlik:** Evet. Kurduğumuz hibrit anomali mimarisi (Normalizasyon + Isolation Forest + Kural Motoru) siber güvenlikte saldırı tespitinden kredi kartı dolandırıcılığı (fraud) analizine ve sensör arıza tespitine kadar her alanda doğrudan yeniden kullanılabilir.

---

## 8. GELECEK HAFTANIN PLANI
1. Şirketlerin birden fazla dönemini (2021, 2022, 2023) karşılaştıran tarihsel zaman serisi / trend analizi modülünün eklenmesi.
2. Web Dashboard üzerine şirketlerin finansal sağlık gidişatını özetleyen otomatik sözel yorumlayıcı (Akıllı Finansal Yorum Asistanı) bölümünün entegre edilmesi.
3. Analiz sonuçlarının ve şirket karnesinin tek tıkla dışa aktarılabilir/yazdırılabilir rapor formatına dönüştürülmesi.
4. Uçtan uca sistem entegrasyon testlerinin genişletilmesi ve proje teknik dokümantasyonunun güncellenmesi.

- **Öncelikli Problem/Özellik:** Öncelikli hedefim; tek dönemlik anlık fotoğraf çekmenin ötesine geçerek şirketin önceki dönemlerine göre rasyolarının iyileşip kötüleştiğini analiz eden çok dönemli trend analizini ve otomatik finansal karne yorumlayıcısını tamamlamaktır.

---

## 9. YAPAY ZEKÂ DESTEKLİ PROJE GELİŞTİRME SÜRECİ

### 9.1. Bu Hafta Kullandığınız Yapay Zekâ Araçları
- **Kullandığım araçlar:** Google Gemini, ChatGPT, Antigravity AI Asistanı
- **Kullanım süresi:** [x] 1–3 saat

### 9.2. Yapay Zekâyı Hangi Amaçlarla Kullandınız?
- **Başlıca amaçlar:** Isolation Forest algoritmasının saf Python ile ağaç veri yapısı olarak gerçeklenmesi, SVG Radar grafiğinin trigonometrik poligon koordinatlarının hesaplanması, hibrit ağırlıklandırma kalibrasyonu ve birim test senaryolarının oluşturulması.
- **En çok kullanılan konu:** Isolation Forest yol uzunluğu normalizasyon fonksiyonu \(c(n)\) ve SVG Radar grafiğinin açısal koordinat dönüşümleri konusunda.
- **Neden ihtiyaç duyuldu:** Harici kütüphane kurulum sorunlarından bağımsız, her ortamda anında çalışan saf Python Isolation Forest uygulaması ve tarayıcıda pürüzsüz çalışan SVG Radar grafiği oluşturmak için.

### 9.3. Yapay Zekâya Başvurmadan Önce Ne Yaptınız?
- **Problemi önce kendim çözmeye çalıştım:** [x] Evet
- **Yapılan araştırmalar:** Isolation Forest makalesindeki (Liu et al., 2008) ikili ağaç derinlik formüllerini inceledim ve radar grafiği için 6 eksenli poligonun (\(2\pi i / N\)) açılarını kağıt üzerinde modelledim.
- **Başvurma nedenleri:**
  - [x] Yazdığım kod hata verdi.
  - [x] Daha hızlı bir çözüm üretmek istedim.
  - [x] Alternatif bir çözüm aradım.
  - [x] Yazdığım kodu kontrol ettirmek istedim.
  - [x] Konuyu öğrenmek istedim.

### 9.4. Bu Hafta Kullandığınız Önemli Promptlar
- **Prompt 1:** *"Python standart kütüphaneleriyle (math, random) Isolation Forest algoritmasını gerçekle. Ağaç düğümlerini, c(n) Euler harmonik düzeltme faktörünü ve 2^(-E(h(x))/c(n)) anomali skorunu içersin."*  
  *(Cevap: Özyinelemeli `_IsolationNode` yapısı ve `c(n)` fonksiyonu ile ağaç topluluğu oluşturan bir sınıf şablonu sundu. [x] Küçük değişiklikler yaparak sabit sütun varyans korumasını ekledim).*
- **Prompt 2:** *"JavaScript ile harici kütüphane kullanmadan `<svg>` içinde 6 finansal göstergeyi (Cari Oran, Asit-Test, Özkaynak Oranı, Net Kâr Marjı, ROA, Aktif Devir) çizen bir Radar Chart fonksiyonu yaz. Sektör ortalamasını referans poligon olarak göstersin."*  
  *(Cevap: Trigonometrik cos ve sin fonksiyonlarıyla merkez etrafında poligon noktaları üreten bir JS fonksiyonu verdi. [x] Büyük ölçüde değiştirdim; negatif oranlarda poligonun ters tarafa taşmasını önleyen bağıl ölçekleme ekledim).*
- **Prompt 3:** *"Finansal analizde kural bazlı risk skoru, Isolation Forest skoru ve k-NN mesafe skorunu birleştirirken perakende sektörü gibi yanlış pozitifleri azaltacak ama teknik iflas durumlarını kaçırmayacak ağırlıklandırma nasıl kurulmalıdır?"*  
  *(Cevap: Ağırlıklı ortalama (%55 Kural/İstatistik, %30 IForest, %15 k-NN) ve kritik eşik koruma kuralı önerdi. [x] Küçük değişiklikler yaparak uyguladım).*

### 9.5. Yapay Zekâ Tarafından Üretilen Kodlar
- **Kullanılan kod:** `_c_factor(n)` fonksiyonu:
  ```python
  def _c_factor(n: int) -> float:
      if n <= 1:
          return 0.0
      if n == 2:
          return 1.0
      euler_gamma = 0.5772156649
      h = math.log(n - 1.0) + euler_gamma
      return 2.0 * h - (2.0 * (n - 1.0) / n)
  ```
- **Kodun yaptığı iş:** `n` elemanlı bir veri kümesinde ikili arama ağacının beklenen derinliğini Euler sabiti ve harmonik sayı yaklaşımıyla hesaplar; skoru normalize eder.
- **Nasıl kullanıldı:** [x] Küçük değişiklikler yaptım.
- **Yapılan değişiklikler:** `n == 2` sınır durumunu açık koşul olarak ekledim ve tip bildirimlerini tamamladım.
- **Çalışma mantığı anlaşılıyor muydu:** [x] Tamamen anlıyordum.

### 9.6. Yapay Zekâ Çıktılarının Kontrolü
- **Kontrol:** Kodu çalıştırarak test ettim, satır satır inceledim, makale formülleriyle karşılaştırdım.
- **Tespit edilen hata:** Yapay zekanın ilk önerdiği Isolation Tree bölme kodunda, alt düğümdeki tüm örneklerin belirli bir özellikte aynı değere sahip olması durumunda (`min == max`) boş alt-ağaç oluşuyordu; `valid_attrs` varyans kontrolü ile düzeltildi.

### 9.7. Karşılaşılan Problemler
- **En önemli problem:** Radar grafiğinde negatif finansal oranların (örneğin `RISKY_TECH` şirketinde `-%53.3` net kâr marjı) yarıçapı negatif yaparak grafiğin karşı eksenine taşması.
- **Çözüm:** Negatif oranlar için minimum yarıçap sınırı (`0.12`) tanımladım ve sektör ortalamasını `0.60` referans çemberine sabitleyerek görsel bozulmayı giderdim.

### 9.8. Yapay Zekâ Olmasaydı Ne Olurdu?
- [x] Evet, ancak daha uzun sürede tamamlayabilirdim. Isolation Forest ağaç derinlik matematiğini ve SVG poligon çizimlerini sıfırdan kodlamak çok daha uzun sürerdi.

### 9.9. Öğrenmeye Etkisi
- [x] Evet. Isolation Forest algoritmasının iç çalışma mekanizmasını ve trigonometrik SVG veri görselleştirmesini öğrendim.

### 9.10. Değerlendirme ve Oranlar
- **Yapay Zekâ Kullanım Oranım:** **% 35**
- **Kodun Yapay Zekâ Tarafından Oluşturulma Oranı:** **% 30**
- **Değerlendirme:** [x] Genellikle kendim çalıştım, ihtiyaç duyduğumda yapay zekâ kullandım.

### 9.11. Genel Değerlendirme
Bu hafta yapay zekâ, özellikle Isolation Forest algoritmasının saf Python ile ağaç yapısında kodlanması ve SVG tabanlı interaktif Radar/Bar grafiklerinin matematiksel koordinatlarının oluşturulmasında geliştirme hızımı büyük ölçüde artırdı. Veri normalizasyonundaki sıfır varyans korumalarını, perakende sektörü yanlış pozitif kalibrasyonunu ve hibrit model ağırlıklarını bizzat kendim tasarlayıp doğruladım.

### 9.12. Kanıtlar
1. `src/ml_anomaly.py` (`DataNormalizer`, `IsolationForestDetector`, `KNNOutlierDetector` ve `HybridAnomalyEngine`)
2. `src/web_dashboard.py` & `dashboard.html` (SVG Radar/Bar grafikleri ve Canlı Bilanço Simülatörü içeren görsel analiz ekranı)
3. `tests/test_ml_anomaly.py` (Toplam 12/12 başarılı birim test çıktısı)

---

## 10. HAFTALIK GENEL ÖZ DEĞERLENDİRME
- **En başarılı olunan konu:** Harici hiçbir paket kurulumuna ihtiyaç duymadan saf Python ile çalışan Isolation Forest makine öğrenmesi modelini ve tarayıcıda interaktif çalışan SVG Radar/Bar grafikli Web Dashboard ekranını (`dashboard.html`) uçtan uca entegre etmek.
- **En fazla zorlanılan konu:** Denetimsiz makine öğrenmesi modelinin yüksek kârlı/likit şirketleri de "sektörden farklı" olduğu için anomali sayması problemini, istatistiksel iflas kurallarıyla hibritleyerek dengelemek.
- **Farklı yapılacak şey:** Veri setine en baştan her şirket için 3 yıllık geçmiş dönem verisi ekleyerek Radar grafiğinin yanında yıllar arası trend çizgisini de aynı anda çıkarmak olurdu.
- **Haftalık Puan:** **9.5 / 10**
- **Puan Gerekçesi:** Proje şartnamesindeki tüm temel gereksinimler (oran analizi, veri normalizasyonu, sektör karşılaştırması, makine öğrenmesi anomali tespiti ve görsel analiz ekranı) 3. hafta itibarıyla çalışır ve 12 birim testle doğrulanmış şekilde tamamlandı.
