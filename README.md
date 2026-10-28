# Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi (v0.3.0)

Bu proje, şirketlerin bilanço ve gelir tablosu verilerini kullanarak finansal oranlarını otomatik olarak hesaplayan, sektör ortalamalarıyla karşılaştıran, Min-Max veri normalizasyonu ve makine öğrenmesi (`Isolation Forest` + `k-NN`) ile olağandışı sapmaları tespit ederek hibrit anomali/risk puanı üreten ve interaktif görsel analiz ekranı (`dashboard.html`) sunan bir karar destek sistemidir.

## Haftalara Göre Gelişim Özeti
- **Hafta 1:** Gereksinim analizi, veri modelleme (`models.py`), 14 finansal oran hesaplama motoru (`ratios.py`), Z-Score sektör analizi (`sector_analysis.py`) ve ilk risk puanlayıcı.
- **Hafta 2:** CSV/JSON şema doğrulamalı veri yükleyici (`data_loader.py`), 3 sektör / 10 şirketlik veri seti (`companies_financials.csv`), 4 tablolu ilişkisel SQLite veritabanı (`database.py`) ve çok boyutlu Öklid uzaklığı.
- **Hafta 3:** Min-Max veri normalizasyonu, `Isolation Forest` (İzolasyon Ormanı) ve `k-NN` makine öğrenmesi anomali modelleri (`ml_anomaly.py`), Hibrit Risk Motoru ve SVG Radar/Bar grafikli İnteraktif Web Dashboard + Canlı Bilanço Simülatörü (`web_dashboard.py` & `dashboard.html`).

## Kurulum ve Çalıştırma

Proje sıfır dış bağımlılıkla doğrudan Python 3.12 standart kütüphanesiyle çalışır:

```powershell
# Analizi çalıştırmak, veritabanını güncellemek ve dashboard.html üretmek için:
python main.py

# Yerel web sunucusunu (http://127.0.0.1:8080/dashboard.html) başlatmak için:
python main.py --serve

# Tüm birim testleri (12 test) çalıştırmak için:
python -m unittest discover tests
```

## Proje Yapısı
- `src/models.py`: Bilanço, Gelir Tablosu ve Şirket veri modelleri
- `src/ratios.py`: Likidite, Borçluluk, Kârlılık ve Faaliyet oranları hesaplama motoru
- `src/sector_analysis.py`: Sektör ortalaması, medyan, standart sapma ve Z-Score kıyaslama modülü
- `src/anomaly_detector.py`: Z-Score, çok boyutlu Öklid mesafesi ve finansal iflas eşikleri motoru
- `src/ml_anomaly.py`: Min-Max Normalizasyon, Isolation Forest (100 ağaç), k-NN ve Hibrit Risk Motoru
- `src/data_loader.py`: CSV ve JSON finansal tablo okuyucu ve şema doğrulayıcı
- `src/database.py`: SQLite ilişkisel veritabanı yöneticisi
- `src/web_dashboard.py`: İnteraktif HTML5/SVG Radar & Bar grafikli görsel analiz ekranı üreticisi
- `dashboard.html`: Tarayıcıda doğrudan açılabilen interaktif görsel analiz ekranı
- `tests/`: 12 adet birim ve entegrasyon testi
