# 🗓️ HAFTA 3: Sahne Detaylandırma, Studio Sürücüsü Optimizasyonu ve Hız Senaryosu

Bu döküman, projenin üçüncü haftasında sahneye eklenen istasyon ve güvenlik elemanlarını, render darboğazını çözmek adına uygulanan sürücü (driver) mimarisi geçişini ve kesin zaman çizelgesi (timeline) hesaplamalarını içmektedir.

## 1. Sahne Genişletme ve Detay Modelleme (Asset Pipeline)
* **Geometri ve Hat Düzenlemesi:** Ray altı ve kenarındaki balast taşları `Array Modifier` ile optimize edilerek hizalanmış ve `Realize Instances` kapatılarak bellek optimizasyonu korunmuştur. Tren rayları tünel sonrasına doğru uzatılmıştır.
* **İstasyon ve Çevre Tasarımı:** Sahneye yolcu durağı, istasyon binası, bekleyen yolcu modelleri, uyarı levhaları ve bariyerler eklenmiştir. Tünel çıkışına derinlik algısını desteklemek için ot ve ağaçlar yerleştirilmiştir.
* **Ufuk Çizgisi Optimizasyonu:** Rayların havada kesilme problemini çözmek adına dağ, ağaç ve kıvrılan ray modelleriyle pürüzsüz bir ufuk noktası (horizon) görünümü elde edilmiştir.
* **Katener Sistemi:** Ray ortalarına elektrik direkleri yerleştirilmiş ve direkler arası gergin hat (katener telleri) dökümantasyona uygun olarak çekilmiştir.

## 2. Grafik İşlemci (GPU) Donanım ve Sürücü Değişimi
Sahnede `Sampling` (64), `Light Paths` (Diffuse/Glossy limitleri 3'e düşürüldü) ve `Denoise (OptiX)` ayarları kısılmasına rağmen tek karenin **5-6 dakika** sürmesi üzerine mimari bir darboğaz analizi yapılmıştır.

* **Sorun Tespiti:** Oyun odaklı *Game Ready* sürücülerinin Blender gibi ağır render yüklerinde GPU'yu tam güce (Boost frekansına) kaldırmadığı, OptiX kütüphanesini kilitlediği ve arka planda rölantide çalıştığı saptanmıştır.
* **Çözüm (NVIDIA Studio Sürücüsü):** Donanım, **NVIDIA Studio Sürücüsü** mimarisine geçirilmiştir. Studio sürücüsü, Blender'ın kullandığı OptiX kütüphanesini doğrudan ekran kartının donanmsal ışın izleme (RT) ve yapay zeka (Tensor) çekirdeklerine kilitlemiştir. Ayrıca NVIDIA Denetim Masası üzerinden *Doku Süzme - Kalite* ayarı *Yüksek Performans* moduna çekilmiştir.
* **Performans Kazanımı (Benchmark):**
  * ❌ **Eski Sürücü Süresi:** `06:38.85` (6 dakika 38 saniye)
  *  **Yeni Studio Sürücüsü Süresi:** `00:42.79` (42 saniye)
  * *Sonuç:* Donanım verimliliğinde yaklaşık **10 kat (10x) performans artışı** sağlanmıştır.

## 3. Render Analizi ve Karşılaşılan Kısıtlamalar
* **Kırılma Noktası Darboğazı:** Kare başı süre stabil olarak 40-50 saniye bandında giderken, kameranın tünel girişine yaklaştığı **178. kareden sonra** süre 1 dakikanın üzerine çıkmıştır. Tünel içi ışık ve gölge matrislerinin (Ray Tracing) hesaplama yükünü artırdığı tespit edilmiştir.
* **Veri Kaybı (Overwrite):** Yanlışlıkla video üzerine yazma (*Overwrite*) hatası nedeniyle bir önceki animasyon çıktısı kaybedilmiş, bu durum risk yönetimi adına projenin `PNG Sequence` olarak alınması kararını kesinleştirmiştir.

## 4. Matematiksel Zaman Çizelgesi (Timeline) ve Hız Planı
Trenin gerçek dünya ivmesine ve banliyö hız standartlarına uyması adına, kameranın toplam rotası için planlanan yeni hız senaryosu grafik editörü (Graph Editor) için şu şekilde hesaplanmıştır:

| Sahne Bölümü | Kamera Mesafesi | Ayrılan Kare (Frame) | Süre (Saniye) |
| :--- | :--- | :--- | :--- |
| **1. İlk Düzlük** | 330 Metre | 480 Frame | 16 Saniye |
| **2. Tünel Giriş / Çıkış (Viraj)** | 120 Metre | 240 Frame | 8 Saniye |
| **3. Son Düzlük (İstasyon Durağı)** | 330 Metre | 390 Frame | 13 Saniye |
| **TOPLAM** | **780 Metre** | **1110 Frame** | **37 Saniye** |

## 5. Gelecek Çalışmalar ve Sentetik Veri Çeşitliliği (Bonus)
* [ ] Kamera keyframe rotalarının sarsıntısız akış için eğriler üzerinden yeniden çizilmesi.
* [ ] Yapay zeka veri çeşitliliğini (data augmentation) artırmak adına ilerleyen aşamalarda; farklı hava durumları (yağmur, kar), farklı ışık kaynakları (gece/gündüz) ve ters yönden dönüş hatlarının simüle edilmesi.