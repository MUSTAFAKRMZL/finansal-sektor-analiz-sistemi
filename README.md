# Şirketlerin Finansal Performansını Sektörleriyle Karşılaştıran Akıllı Analiz Sistemi

Bu proje, şirketlerin bilanço ve gelir tablosu verilerini kullanarak finansal oranlarını otomatik olarak hesaplayan, sektör ortalamalarıyla karşılaştıran ve olağandışı sapmaları tespit ederek anomali/risk puanı üreten bir karar destek sistemidir.

## Hafta 1 Özeti
- **Kapsam:** Gereksinim analizi, veri modelleme, finansal oran hesaplama motoru ve kural/istatistik tabanlı anomali puanlayıcı prototipi.
- **Teknoloji:** Python 3.12 (Standart kütüphaneler ile sıfır dış bağımlılıkla çalışabilir prototip).

## Kurulum ve Çalıştırma

```bash
# Projeyi çalıştırmak için:
python main.py

# Testleri çalıştırmak için:
python -m unittest discover tests
```

## Proje Yapısı
- `src/models.py`: Bilanço, Gelir Tablosu ve Şirket veri modelleri
- `src/ratios.py`: Likidite, Borçluluk, Kârlılık ve Faaliyet oranları hesaplama motoru
- `src/sector_analysis.py`: Sektör ortalamaları ve kıyaslama modülü
- `src/anomaly_detector.py`: Z-Score ve eşik değer tabanlı anomali/risk motoru
- `data/sample_companies.json`: Örnek sektör ve şirket finansal verileri
- `main.py`: Konsol prototip demosu
- `tests/test_ratios.py`: Birim testler
