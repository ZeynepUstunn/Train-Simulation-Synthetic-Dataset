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
* [**🚀 PROJENİN SON DURUMU VE ANALİZ RAPORU**]
  * Nihai render görselleri, istasyon ve katener sistemlerinin son hali, 42 saniyelik kesin zaman çizelgesi tablosu ve donanım benchmark çıktıları.

## 🎯 Gelecek Çalışmalar ve Veri Çeşitliliği (Data Augmentation)
Yaygın yapay zeka modellerinin (AVIES, Bakanlık standartları, Saha Expo / IDEF vizyonu) sınırlarını ve dayanıklılığını test etmek amacıyla sonraki aşamalarda aynı kamera rotası sabit tutularak şu varyasyonların üretilmesi planlanmaktadır:
* [ ] **Zorlu Hava Şartları:** Şiddetli yağmur parçacıkları, karlı zemin kaplamaları ve yoğun sis (Mist Pass) simülasyonu.
* [ ] **Işık Kaynağı Değişimleri:** Gece / Alacakaranlık seyrinde tren far ışığının nesne tespiti üzerindeki etkisinin test edilmesi.
