## `bpy` (Blender Python API) Nedir ve Açılımı Nedir?

- **Açılımı:** `bpy`, **"Blender Python"** (Blender Python API) ifadesinin kısaltmasıdır.
- **Tanımı:** Blender yazılımının dahili Python modülüdür. Sahneler, 3D nesneler, kameralar, ışıklar, materyaller ve render motoru gibi Blender içindeki her türlü bileşeni harici bir arayüze gerek kalmadan kod aracılığıyla tamamen kontrol etmeyi ve otomatikleştirmeyi sağlar.

# 📦 Demiryolu Anomali Tespiti - Sentetik Veri Üretim Pipeline'ı

Bu repo, Blender Python API (`bpy`) ve YOLO nesne tespiti formatı kullanılarak demiryolu sahneleri için otomatik sentetik veri (görsel ve `.txt` etiketleri) üreten Python betiklerini barındırmaktadır.

---

## 🚀 Script Açıklamaları ve Sürüm Geçmişi

### 1. `run_pipeline.py` (Tekli Nesne & Kapsamlı Optimizasyon Sürümü)
* **Açıklama:** İçi içe geçmiş gruplu/klasörlü karmaşık 3D modelleri (`box` vb.) Outliner yapısında kaybolmadan bulabilmek için geliştirilmiş **özyürümeli (recursive) `find_real_mesh`** algoritmasını içerir. 
* **Öne Çıkan Özellikler:**
  * Cycles motoru ve GPU hızlandırma desteği ile yüksek kaliteli render.
  * `get_yolo_bbox` fonksiyonu ile nesnenin kamera açısındaki 3D sınır kutusunu (bounding box) hatasız bir şekilde 2D YOLO formatına (`class_id x_center y_center width height`) dönüştürür.
  * Aydınlatma çeşitliliği (Random Sun) ile modelin farklı ışık koşullarını öğrenmesini sağlar.

### 2. `exp1.py` (Temel Altyapı & İlk Sürüm)
* **Açıklama:** Projenin temel prototipidir. `Koli`, `Rock` ve `Wood` sınıfları tanımlanmış; skybox dönüşleri ve temel sahne animasyon döngüsü bu sürümde kurulmuştur.

### 3. `exp2.py` (Çoklu Parça & Sınıf Gruplama Desteği)
* **Açıklama:** Blender'da çakışma yaratmamak adına ikinci ahşap nesnesine `Wood_2` adı verilmiş ve kod tarafında ana sınıf ID'sine (`2`) bağlanarak çoklu parça desteği genişletilmiştir.

### 4. `exp3.py` (Hata Düzeltme & Odaklanmış Render)
* **Açıklama:** Yanlış nesne adından dolayı boş kalan koli (box) etiket aralığını düzeltmek amacıyla sadece ilgili kare aralığını (`620-810`) hedefleyen özel düzeltme betiğidir.

### 5. `exp4.py` (Standartlaştırma & Final Sürüm)
* **Açıklama:** Sınıf adlandırmalarında standartlaşmaya gidilerek `Koli` terimi **`Box`** olarak güncellenmiştir. Parçalı zaman aralıkları ve optimize edilmiş nesne isimleriyle güncel kararlı üretim kodudur.

### 6. `single_anomaly.py` (Tekli Anomali & Kırpma Filtreli Test Sürümü)
* **Açıklama:** Belirli bir kare aralığında (örn. başlangıç veya özel test aralıkları) tek bir anomali nesnesini izole ederek test etmek için kullanılan sürümüdür.
* **Öne Çıkan Özellikler:**
  * Nesne kameranın dışına çıkmaya başladığında veya sınır kutusu çok küçüldüğünde hatalı etiket oluşmasını önleyen `width > 0.01` filtreleme mantığına sahiptir.
  * Sahnedeki hedef nesnenin her karede kendi ekseni etrafında (`rotation_z`) rastgele dönmesini ve hafif konum varyasyonları kazanmasını sağlar.

### 7. `veri_dagilimi.py` (Dataset Analiz ve Dağılım Raporu)
* **Açıklama:** Üretilen YOLO etiket klasörünü (`labels/train`) tarayarak veri setindeki sınıfların dengesini ve toplam dosya sayısını raporlayan yardımcı Python betiğidir.
* **Öne Çıkan Özellikler:**
  * Toplam etiket dosyası ile içinde nesne bulunmayan (boş) arka plan karelerinin sayısını tespit eder.
  * Her bir sınıf ID'sini (Box, Rock, Wood, Animal) isimleriyle eşleştirerek kaçar adet örnek üretildiğini terminale yazar.
  * Model eğitimi öncesi veri dengesizliğini kontrol etmek için hızlı ve pratik bir özet sunar.
---

## 🛠️ Kullanım (Nasıl Çalıştırılır?)

PowerShell üzerinden Blender'ı arayüzsüz (background mode) çağırarak ilgili Python betiğini şu komutla çalıştırabilirsiniz:

```powershell
& "D:\Blender\blender-5.1.2-windows-x64\blender-5.1.2-windows-x64\blender.exe" -b "D:\opencv\Rail_Road8.blend" -P "D:\opencv\single_box_detect.py"
