# Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi (v0.4.0)

Bu proje, şirketlerin bilanço ve gelir tablosu verilerini kullanarak finansal oranlarını otomatik olarak hesaplayan, sektör ortalamaları ve medyanları ile karşılaştıran, Min-Max veri normalizasyonu ve makine öğrenmesi (`Isolation Forest` + `k-NN`) ile olağandışı sapmaları tespit eden, 3 yıllık zaman serisi trend analizi ve **Altman Z-Score** iflas tahmin modeli yürüten, doğal dil tabanlı **Akıllı Finansal Yorum Asistanı** ve tek tıkla yazdırılabilir/PDF şirket karnesi sunan interaktif bir karar destek sistemidir.

## Haftalara Göre Gelişim Özeti
- **Hafta 1:** Gereksinim analizi, veri modelleme (`models.py`), 14 finansal oran hesaplama motoru (`ratios.py`), Z-Score sektör analizi (`sector_analysis.py`) ve ilk risk puanlayıcı.
- **Hafta 2:** CSV/JSON şema doğrulamalı veri yükleyici (`data_loader.py`), 3 sektör / 10 şirketlik veri seti (`companies_financials.csv`), 4 tablolu ilişkisel SQLite veritabanı (`database.py`) ve çok boyutlu Öklid uzaklığı.
- **Hafta 3:** Min-Max veri normalizasyonu, `Isolation Forest` (İzolasyon Ormanı) ve `k-NN` makine öğrenmesi anomali modelleri (`ml_anomaly.py`), Hibrit Risk Motoru ve SVG Radar/Bar grafikli İnteraktif Web Dashboard + Canlı Bilanço Simülatörü (`web_dashboard.py` & `dashboard.html`).
- **Hafta 4:** Çok dönemli zaman serisi analizi (`trend_analysis.py`: 2021-2023 3 yıllık veri seti, CAGR ve Altman Z-Score İflas Modeli), Akıllı Finansal Yorum ve Yönetici Özeti Motoru (`executive_commentary.py`), Dashboard'da 3 yıllık trend ve AI karne paneli, tek tıkla yazdırılabilir / PDF çıktı özelliği (`@media print`).

## Kurulum ve Çalıştırma

Proje sıfır dış bağımlılıkla doğrudan **Python 3.12** standart kütüphanesiyle çalışır:

```powershell
# Analizi çalıştırmak, veritabanını güncellemek ve dashboard.html üretmek için:
python main.py

# Yerel web sunucusunu (http://127.0.0.1:8080/dashboard.html) başlatmak için:
python main.py --serve

# Tüm birim testleri (17 test) çalıştırmak için:
python -m unittest discover tests
```

## Proje Mimarisi
- `src/models.py`: Bilanço, Gelir Tablosu ve Şirket veri modelleri
- `src/ratios.py`: Likidite, Borçluluk, Kârlılık ve Faaliyet oranları hesaplama motoru
- `src/sector_analysis.py`: Sektör ortalaması, medyan, standart sapma ve Z-Score kıyaslama modülü
- `src/anomaly_detector.py`: Z-Score, çok boyutlu Öklid mesafesi ve finansal iflas eşikleri motoru
- `src/ml_anomaly.py`: Min-Max Normalizasyon, Isolation Forest (100 ağaç), k-NN ve Hibrit Risk Motoru
- `src/trend_analysis.py`: 3 yıllık çok dönemli zaman serisi, CAGR büyüme oranları ve Altman Z-Score iflas modeli
- `src/executive_commentary.py`: Akıllı Finansal Yorum Asistanı, güçlü/zayıf yönler ve CFO seviyesi aksiyon önerileri
- `src/data_loader.py`: CSV ve JSON finansal tablo okuyucu ve şema doğrulayıcı
- `src/database.py`: SQLite ilişkisel veritabanı yöneticisi
- `src/web_dashboard.py`: İnteraktif HTML5/SVG Radar, Bar grafikli görsel analiz ekranı ve yazdırılabilir karne üreticisi
- `dashboard.html`: Tarayıcıda doğrudan açılabilen interaktif görsel analiz ekranı
- `tests/`: 17 adet birim ve entegrasyon testi (%100 Başarılı)
