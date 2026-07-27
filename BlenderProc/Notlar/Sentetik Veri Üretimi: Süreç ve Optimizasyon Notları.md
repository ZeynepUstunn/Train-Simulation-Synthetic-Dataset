# Sentetik Veri Üretimi: Süreç ve Optimizasyon Notları

## 1. Karşılaşılan Sorunlar (BlenderProc)
- **Paket Hataları:** Otonom üretim için BlenderProc denendi, sürekli eksik modül (`requests`, `trimesh` vb.) hataları alındı.
- **İzole Ortam Çıkmazı:** BlenderProc'un, arka planda çalışırken sistemdeki paketleri yok sayıp sadece kendi oluşturduğu özel klasöre (`custom-python-packages`) baktığı tespit edildi.
- **Sürüm Çakışması:** BlenderProc sorunu aşmak için 4.2 sürümüne dönmeye çalıştı fakat 5.1.2 ile kaydedilen yeni `.blend` dosyası açılamadı.
- **Eklenti Hatası:** Arayüzsüz (headless) açılışta `poliigon` eklentisi çökmeye (crash) neden oldu (klasör adı değiştirilip devre dışı bırakılarak çözüldü).

## 2. Strateji Değişikliği
- Sürekli devam eden paket ve sürüm uyumsuzluklarından tamamen kurtulmak için **BlenderProc aracısını kullanmaktan vazgeçildi**.

## 3. Saf Blender API (`bpy`) Çözümü
- Süreç, hiçbir dış kütüphane (pip paketleri) gerektirmeyen %100 saf `bpy` koduna (`run_pipeline.py`) çevrildi.
- **Animasyon:** Mevcut kamera animasyonu kullanıldı; BlenderProc'taki gibi kamerayı her karede manuel kopyalama işlemi gereksiz kılındı.
- **Veri Çeşitliliği (Data Diversity):** YOLO eğitimi için gereken ışık konumu ve parlaklık varyasyonları, Python'ın standart `random` modülüyle otonom hale getirildi.
- **Performans:** Cycles render motoru ve GPU (RTX 3050) ayarları doğrudan koda entegre edildi.

## 4. Nihai Çalıştırma Komutu
Artık hiçbir paket derdi olmadan, doğrudan arka planda (background mode) render başlatan tek satırlık ilk standart komut:

```powershell
& "D:\Blender\blender-5.1.2-windows-x64\blender-5.1.2-windows-x64\blender.exe" -b "D:\Blender Study\rail\Rail_Road_V2.blend" -P "D:\Blender Study\rail\run_pipeline.py"
