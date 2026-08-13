# 🚂 Yapay Zeka İçin Sentetik Tren Hattı Simülasyonu

Bu depo (repository), bilgisayar mühendisliği staj projem kapsamında geliştirilen, nesne tespiti (Object Detection), hat takibi ve sinyalizasyon yapay zeka modellerini eğitmek amacıyla tasarlanmış **"Gerçek Dünya Fiziğine Uygun Sentetik Tren Simülasyonu Veri Seti"** projesinin geliştirme adımlarını, teknik notlarını ve optimizasyon süreçlerini içermektedir.

---

## 📌 Proje Özeti & Mühendislik Standartları
* **Mekansal Modelleme:** Yaklaşık **780 metrelik** katener direkli ve tünelli banliyö tren hattı, istasyon yapısı ve peron detayları gerçek dünya ölçeğine (1:1 Metric System) uygun olarak Blender ortamında simüle edilmiştir.
* **Matematiksel Zaman Akışı:** Trenin virajlarda yavaşlaması ve istasyona pürüzsüz yaklaşması esasına dayalı olarak **42 saniyelik (1260 Frame / 30 FPS)** kesin bir hız senaryosu grafik editörü (Graph Editor) üzerinde kilitlenmiştir.

## 📂 Proje İlerleme Günlüğü & Son Durum (Progress Logs)

Şirket içi değerlendirme, iş takibi ve dökümantasyon disiplini amacıyla sürecin teknik detayları, karşılaşılan donanım/RAM darboğazları, üretime yönelik mühendislik çözümleri ve projenin nihai çıktısı aşağıda listelenmiştir:

* [**🗓️ HAFTA 1: Sahne Tasarımı & Donanım Optimizasyonu**]
  * `.gltf` model entegrasyonu, `Alt+D` instancing ile VRAM yükü hafifletme, Temporary Path ve disk yönetimi.
* [**🗓️ HAFTA 2: Çevre Tasarımı & İşletim Sistemi Optimizasyonları**]
  * Geometry Nodes balast taşları yönetimi, Windows Sanal Bellek (Paging File) kurulumu, RAM darboğazı analizleri ve Cycles render denemeleri.
* [**🗓️ HAFTA 3: Grafik İşlemci Sürücü Değişimi & Hız Senaryosu**]
  * NVIDIA Studio Sürücüsü mimarisine geçiş ile **10x render hızlanması** (6 dk'dan 42 sn'ye düşüş), 1260 karelik hız senaryosu tablosu ve katener telleri modellemesi.
* [**🎯 HAFTA 4-5: Otonom Veri Üretim Pipeline'ı ve Sınıf Mimarisi**]
 * **Aşama 1 (4 Sınıflı Temel Pipeline):** Sürecin ilk etabında, nesne kategorileri daha sade tutularak (Box, Rock, Wood, Animal) temel otonom etiketleme ve video üretim pipeline'ı (`.png` görseller + YOLO `.txt` etiketleri + OpenCV doğrulama videoları) başarıyla kurgulandı ve ilk test veri seti üretildi.
  * **Aşama 2 (12 Sınıflı Gelişmiş Mimarisi):** Modelin nesnelerin konumsal bağlamını (hat üstü, hat dışı vb.) daha iyi öğrenebilmesi amacıyla sınıf yapısı detaylandırılarak **12 Sınıflı YOLO Mimarisine** geçildi. Otonom rastgele yerleştirmedeki çakışma ve kot farkı sorunları kontrollü yaklaşımla aşılarak şu sınıf matrisi oluşturuldu:
    * `0-3`: Active_Box, Active_Rock, Active_Wood, Active_Animal (Aktif hat bölgesi)
    * `4-7`: Other_Box, Other_Rock, Other_Wood, Other_Animal (Diğer/uzaktaki bölge)
    * `8-11`: Edge_Box, Edge_Rock, Edge_Wood, Edge_Animal (Kenar/hat dışı bölge)
  * **Video Çeşitliliği ve Atmosfer Varyasyonları:** Ham veri üretiminden video çeşitliliğine odaklanılarak anomali varyasyonları ve farklı skybox (gün batımı/gece) entegrasyonları test edildi.
* [**🎯 HAFTA 6: Otonom Veri Üretim Pipeline Optimizasyonu**]
  * **Algoritmik ve Performans Optimizasyonları:** Raycast yükünü azaltmak amacıyla tarama noktaları 9 noktadan **merkez ve 3 kritik köşeye** indirgendi. Frustum Culling ile birleştirilerek arkada kalan/görünmeyen nesnelerin etiketlenmesi engellendi ve render süresi optimize edildi. 
* [**🚀 PROJENİN SON DURUMU VE ANALİZ RAPORU**]
  * Nihai render görselleri, otomatik YOLO etiketleme (`.txt`) ve OpenCV tabanlı doğrulama videoları (`dogrulama_video_tekrar.mp4`) ile desteklenen entegrasyon süreçleri.
 
## 🎯 Gelecek Çalışmalar ve Veri Çeşitliliği (Data Augmentation)
Yaygın yapay zeka modellerinin sınırlarını ve dayanıklılığını test etmek amacıyla sonraki aşamalarda aynı kamera rotası sabit tutularak şu varyasyonların üretilmesi planlanmaktadır:
* [ ] **Zorlu Hava Şartları:** Şiddetli yağmur parçacıkları, karlı zemin kaplamaları ve yoğun sis (Mist Pass) simülasyonu.
* [ ] **Işık Kaynağı Değişimleri:** Gece / Alacakaranlık seyrinde tren far ışığının nesne tespiti üzerindeki etkisinin test edilmesi.
