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

## 4. Kamera, Aydınlatma ve Stratejik Hedefler
* **Kamera ve Kadraj:** 10 saniyelik ilk simülasyon testi için alt düzlem (`Plane`) ölçeklendirilmiş ve kameranın başlangıç rotası çizilmiştir.
* **Işık Dinamiği:** Nesne tespitini (Object Detection) zorlaştıracak dik öğlen gölgeleri yerine, daha dengeli gölgeler üreten yatay bir aydınlatma açısı belirlenmiştir.
* **Proje Hedefleri:** Geliştirilen bu sentetik veri simülasyonunun **Saha Expo**, **IDEF** fuarları ile **AVIES Yapay Zeka ve Bakanlık Projesi** standartlarına uygun seviyede yapılandırılması hedeflenmiştir.