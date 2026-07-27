# Sentetik Veri Üretimi ve YOLO Optimizasyonu: Alınan Kararlar ve Süreç Notları

## 1. Veri Üretiminde Yöntem ve Araç Tercihi (Karar Verildi)
- **BlenderProc Kullanımından Vazgeçildi:** Ağır harici kütüphaneler ve sürüm çakışmaları yaratan BlenderProc aracı tamamen dışarıda bırakıldı.
- **Saf Blender API (`bpy`) Tercih Edildi:** Blender'ın kendi yerleşik Python altyapısı (`bpy` ve `bpy_extras`) kullanılarak dış bağımlılıklardan arındırılmış, tam kontrollü ve sade bir pipeline (`run_pipeline.py`) benimsendi.

## 2. Proje Gereksinimleri ve Ekip İletişimi (Karar Verildi)
- **Model Mimarisi:** Nesne tespiti projelerinin standart standardı olan **YOLO** altyapısının (YOLOv8 vb.) kullanılacağı varsayımıyla hazırlık yapılmasına karar verildi.
- **Sınıf (Class) Yönetimi ve Genişleme Payı:** İleride eklenebilecek olası anomaliler (taş, insan, yabancı cisim vb.) göz önünde bulundurularak, ID karmaşası yaşamamak adına esnek ve mantıksal bir sınıf listesi yapısı kurulması kararlaştırıldı:
  - `0`: Koli / Kutu (Anomali)
  - `1`: Taş / Kaya (Anomali)
  - `2`: İnsan / Canlı (Anomali)
  - `3`: Ray Üzerindeki Yabancı Cisim (Genel)
  - `4`: Diğer / Bilinmeyen Anomali
- **Dinamik Sınıf ID Ataması:** Kod içerisindeki `CLASS_ID` değişkeninin render alınan nesnenin türüne göre kolayca değiştirilebilecek dinamik bir yapıda tutulması kararlaştırıldı.

## 3. Etiketleme ve Koordinat Mantığı (Karar Verildi)
- **Otomatik Etiketleme:** Manuel olarak Roboflow, LabelImg veya CVAT gibi araçlarla uğraşmak yerine, etiketleme sürecinin tamamen Blender içindeki matematiksel hesaplarla otomatikleştirilmesi sağlandı.
- **Perspektif İzdüşümü:** 3D dünyadaki gerçek konumların (metrik değerler), `world_to_camera_view` fonksiyonu ve kameranın Z derinliği kullanılarak 2D ekran piksellerine (`0.0` ile `1.0` arası oranlar) dönüştürülmesi kuralı benimsendi.
- **Çoklu Nesne Kuralı:** Fotoğraf içerisindeki nesne sayısına bağlı olarak `.txt` dosyalarının tek satır (tek nesne) veya alt alta çoklu satır (her nesne yeni bir sınıf ve koordinat satırı) formatında yazılması standartlaştırıldı.

## 4. Veri Seti Klasör Hiyerarşisi (Karar Verildi)
- Üretilen tüm verilerin gelecekteki model eğitimi ve ekip paylaşımı için standart YOLO dosya düzenine uygun olarak konumlandırılması kesinleştirildi:
  ```text
  dataset/
  │
  ├── images/
  │   ├── train/  <-- Render alınan tüm .png resimler
  │   └── val/    <-- Model testleri için ayrılan resimler
  │
  └── labels/
      ├── train/  <-- Resimlerle birebir ada sahip .txt koordinat dosyaları
      └── val/    <-- Val resimlerine ait .txt dosyaları
