# 🗓️ HAFTA 1: Sahne Tasarımı ve Donanım Optimizasyonu

Bu döküman, projenin ilk haftasında sentetik veri setinin oluşturulacağı 3D ortamın kurulmasını, karşılaşılan donanım kısıtlamalarını ve uygulanan optimizasyon süreçlerini içermektedir.

## 1. Geometrik Altyapı ve Model Entegrasyonu
* **Format Standartlaştırması:** `.blend` formatındaki ham kaynakların aktarımında yaşanan hiyerarşi ve mesh sorunları nedeniyle, asset boru hattı **`.gltf` / `.fbx`** standartlarına çekilmiştir.
* **Varlık (Asset) Entegrasyonu:** Sahne dinamiğine uygun hazır tren rayları (`Train Rail`) ve katener direkleri yerleştirilmiş; ray sonuna derinlik algısı yaratması amacıyla tünel giriş yapısı eklenmiştir.

## 2. Bellek ve Donanım Optimizasyonu (Performans)
* **VRAM ve Nesne Klonlama:** Çevresel varlıkların (ağaç, taş vb.) `Ctrl + C` / `Ctrl + V` ile kopyalanmasının poligon sayısını şişirdiği ve donanımı kilitlediği saptanmıştır. Tüm varlıklar silinerek **`Alt + D` (Linked Duplicate / Instancing)** yöntemiyle yeniden klonlanmış ve ekran kartı belleği (VRAM) optimize edilmiştir.
* **Geçici Dosya (Cache) Yönetimi:** C diskinin dolmasından kaynaklı Cycles/Eevee render motoru hatalarını çözmek adına Blender **`Temporary Path` (Geçici Dosya Yolu)** dizini D diskine taşınmış ve render süreleri normale döndürülmüştür.

## 3. Görsel Gerçekçilik ve Yapay Zeka (AI) Veri Analizi
* **Çevre Aydınlatması:** Raylar üzerinde metalik yansımalar (`ray parlaması`), balast taşları ve genel ortam aydınlatması için **`Skybox / HDRI`** kurulumu tamamlanmıştır.
* **Veri Kalitesi Ölçümü:** Kaplamalardaki (texture) ot, çalı ve taş detaylarının yapay zeka modellerinde gürültü (noise) yaratıp yaratmayacağı analize alınmıştır. **Görsel gerçekçilik ile ham veri dengesi** optimize edilmektedir.
* 

## 4. Kamera, Aydınlatma ve Stratejik Hedefler
* **Kamera ve Kadraj:** 10 saniyelik ilk simülasyon testi için alt düzlem (`Plane`) ölçeklendirilmiş ve kameranın başlangıç rotası çizilmiştir.
* **Işık Dinamiği:** Nesne tespitini (Object Detection) zorlaştıracak dik öğlen gölgeleri yerine, daha dengeli gölgeler üreten yatay bir aydınlatma açısı belirlenmiştir.
* **Proje Hedefleri:** Geliştirilen bu sentetik veri simülasyonunun **Saha Expo**, **IDEF** fuarları ile **AVIES Yapay Zeka ve Bakanlık Projesi** standartlarına uygun seviyede yapılandırılması hedeflenmiştir.
  
<img width="1024" height="500" alt="landscape" src="https://github.com/user-attachments/assets/02d0292e-1577-4e90-8139-ea98e68bdba1" />

<img width="1017" height="915" alt="curve" src="https://github.com/user-attachments/assets/1a87876a-80cb-4fe1-90c0-022e19003a26" />

<img width="1421" height="707" alt="gerçekçi ama düz" src="https://github.com/user-attachments/assets/7ea81920-3f8d-4c4e-b61e-70ef28edad6c" />

<img width="1024" height="547" alt="render ekranı" src="https://github.com/user-attachments/assets/c72848dd-aab2-4a0c-8696-39a99badb48b" />

<img width="1367" height="841" alt="kk" src="https://github.com/user-attachments/assets/53ac6902-3b50-4e89-9136-b75ba97fc5c7" />


