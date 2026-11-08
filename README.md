# Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi (v0.5.0)

Bu proje, şirketlerin bilanço ve gelir tablosu verilerini kullanarak finansal oranlarını otomatik olarak hesaplayan, sektör ortalamaları ve medyanları ile karşılaştıran, Min-Max veri normalizasyonu ve makine öğrenmesi (`Isolation Forest` + `k-NN`) ile olağandışı sapmaları tespit eden, 3 yıllık zaman serisi trend analizi ve **Altman Z-Score** iflas tahmin modeli yürüten, doğal dil tabanlı **Akıllı Finansal Yorum Asistanı**, canlı **REST API** sunucusu ve tek tıkla yazdırılabilir/PDF şirket karnesi sunan interaktif bir karar destek platformudur.

## Haftalara Göre Gelişim Özeti

### Faz 1: Çekirdek Sistem (MVP)
- **Hafta 1:** Gereksinim analizi, veri modelleme (`models.py`), 14 finansal oran hesaplama motoru (`ratios.py`), Z-Score sektör analizi (`sector_analysis.py`) ve ilk risk puanlayıcı.
- **Hafta 2:** CSV/JSON şema doğrulamalı veri yükleyici (`data_loader.py`), 3 sektör / 10 şirketlik veri seti (`companies_financials.csv`), 4 tablolu ilişkisel SQLite veritabanı (`database.py`) ve çok boyutlu Öklid uzaklığı.
- **Hafta 3:** Min-Max veri normalizasyonu, `Isolation Forest` (İzolasyon Ormanı) ve `k-NN` makine öğrenmesi anomali modelleri (`ml_anomaly.py`), Hibrit Risk Motoru ve SVG Radar/Bar grafikli İnteraktif Web Dashboard + Canlı Bilanço Simülatörü (`web_dashboard.py` & `dashboard.html`).
- **Hafta 4:** Çok dönemli zaman serisi analizi (`trend_analysis.py`: 2023-2025 3 yıllık veri seti, CAGR ve Altman Z-Score İflas Modeli), Akıllı Finansal Yorum ve Yönetici Özeti Motoru (`executive_commentary.py`), Dashboard'da 3 yıllık trend ve AI karne paneli, tek tıkla yazdırılabilir / PDF çıktı özelliği (`@media print`).

### Faz 2: Kurumsal & İleri Analitik Modüller (11 Haftalık Genişletilmiş Plan)
- **Hafta 5:** SQLite'dan dinamik nesne geri yükleme (`load_companies_from_db`), sıfır bağımlılıklı çoklu iş parçacıklı canlı **REST API** sunucusu (`src/api_server.py`), `/api/health`, `/api/companies`, `/api/sectors`, `POST /api/analyze` uç noktaları ve Web Dashboard ile canlı API haberleşmesi.

## Kurulum ve Çalıştırma

Proje sıfır dış bağımlılıkla doğrudan **Python 3.12** standart kütüphanesiyle çalışır:

```powershell
# Analizi çalıştırmak, SQLite veritabanını güncellemek ve dashboard.html üretmek için:
python main.py

# Canlı REST API & Web Dashboard sunucusunu (http://127.0.0.1:8080/dashboard.html) başlatmak için:
python main.py --serve

# Tüm birim ve REST API testlerini (22 test) çalıştırmak için:
python -m unittest discover tests
```

## REST API Uç Noktaları (`python main.py --serve`)
- `GET /api/health` — Sunucu sağlığı, sürüm (`v0.5.0`), veritabanı kayıt istatistikleri
- `GET /api/dashboard-data` — Tüm şirket, benchmark, trend ve yapay zekâ yorum verileri
- `GET /api/companies` — Şirket özet listesi ve hibrit risk sıralaması
- `GET /api/companies/{code}` — Tekil şirket detaylı bilançosu, rasyoları ve karnesi
- `GET /api/sectors` — Sektör bazlı ortalama, medyan ve standart sapma benchmarkları
- `POST /api/analyze` — Ham bilanço/gelir tablosu göndererek Python motorlarında gerçek zamanlı analiz

## Proje Mimarisi
- `src/models.py`: Bilanço, Gelir Tablosu ve Şirket veri modelleri
- `src/ratios.py`: Likidite, Borçluluk, Kârlılık ve Faaliyet oranları hesaplama motoru
- `src/sector_analysis.py`: Sektör ortalaması, medyan, standart sapma ve Z-Score kıyaslama modülü
- `src/anomaly_detector.py`: Z-Score, çok boyutlu Öklid mesafesi ve finansal iflas eşikleri motoru
- `src/ml_anomaly.py`: Min-Max Normalizasyon, Isolation Forest (100 ağaç), k-NN ve Hibrit Risk Motoru
- `src/trend_analysis.py`: 3 yıllık çok dönemli zaman serisi, CAGR büyüme oranları ve Altman Z-Score iflas modeli
- `src/executive_commentary.py`: Akıllı Finansal Yorum Asistanı, güçlü/zayıf yönler ve CFO seviyesi aksiyon önerileri
- `src/data_loader.py`: CSV ve JSON finansal tablo okuyucu ve şema doğrulayıcı
- `src/database.py`: SQLite ilişkisel veritabanı yöneticisi ve `load_companies_from_db()` geri yükleyici
- `src/api_server.py`: ThreadingHTTPServer tabanlı güvenli REST API sunucusu ve `FinancialAnalysisService`
- `src/web_dashboard.py`: Canlı API destekli HTML5/SVG Radar & Bar grafikli görsel analiz ekranı
- `dashboard.html`: Hem çevrimdışı (`file://`) hem de canlı API modunda çalışan Web Dashboard
- `tests/`: 22 adet birim ve REST API entegrasyon testi (%100 Başarılı)
