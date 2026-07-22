# 📌 HAFTA 4: Sahne Optimizasyonları, Ray Hattı Genişletmesi ve Veri Çeşitlendirme (Data Augmentation)

## 🎯 Hafta 4 Hedefleri ve Gerçekleştirilen Çalışmalar

Bu hafta kapsamında, önceki render çıktılarında tespit edilen fiziksel ve geometrik tutarsızlıkların giderilmesi, sahne alanının büyütülmesi ve yapay zeka modelinin eğitim kalitesini artıracak anomali senaryolarının (Edge Case) sahneye entegrasyonu üzerine çalışılmıştır.

### 1. ⚡ Elektrifikasyon ve Katener Sistemleri (Direk ve Tel Düzenlemeleri)
* **Konumlandırma Optimizasyonu:** Rayların ortasında yer alan ve fiziksel çakışmaya sebep olan katener direkleri kaldırıldı. Direkler, gerçek demiryolu standartlarına uygun olarak hattın **sağ ve sol kenarlarına** hizalandı.
* **Geometri Değişimi:** Tipik ahşap/üçgen yapılı destek direkleri sahneye entegre edilerek gerçekçilik artırıldı.
* **Tünel ve Tel Entegrasyonu:** Tünel üstünü delip geçen hatalı tel rotaları düzeltilerek; katener tellerinin tünel içi izolatör bağlantıları ve hat boyunca gerilim hatları fiziksel kurallara uygun hale getirildi.

### 2. 🗺️ Sahne Genişletme ve Çevre Tasarımı (Köy & Balast)
* **Sahne Ölçeği (Terrain Expansion):** Yapay zeka modelinin uzun menzilli hat takibi yapabilmesi adına mevcut hat mesafesi genişletildi, toplam render süresi ve kapsama alanı artırıldı.
* **Çakıl Taşları (Balast Düzenlemesi):** Ray altı taban kalınlığı ve kenar şev genişlikleri belirlenen oranlarda ($25/34$ kademeli dağılımı) Geometry Nodes / instancing ile yeniden düzenlendi.
* **Çevre ve Köy Bölgesi Revizyonu:** Sahnenin son kısmında yer alan istasyon/köy yerleşkesindeki model ölçeklendirmeleri (Scale) $1:1$ gerçek boyutlara getirildi; ufuk çizgisindeki (horizon gap) boşluklar arazi elemanlarıyla kapatıldı.

### 3. 🎥 Kamera Hareketi ve Dinamik Hız Ayarı (FPS & Frame Scaling)
* **Hız Algısı Düzeltmesi:** İlk prototipte görsel olarak yavaş algılanan kamera hareketi yeniden kalibre edildi.
* **Frame Aralığı Kısaltması:** Kameranın viraj ve düzlüklerdeki ivmelenmesi (Inertia & Spline Interpolation) güncellenerek frame aralığı kısaltıldı. Böylece daha dinamik ve gerçekçi bir tren sürüş açı/hız profili elde edildi.

### 4. 🚨 Yapay Zeka Anomali Senaryoları (Obstacle & Anomaly Detection)
* **Ray Üstünde Yabancı Nesne (Obstacle Detection):** Yapay zeka modelinin acil durum frenleme ve engel tanıma kabiliyetini ölçmek amacıyla ray üzerine nesne/engel senaryoları entegre edildi.

<img width="1692" height="902" alt="image" src="https://github.com/user-attachments/assets/d05f393c-4f58-46d6-a956-ac5ab93a5eaa" />
<img width="1687" height="897" alt="image" src="https://github.com/user-attachments/assets/c27d6ceb-2b54-4be7-9490-ad6fdbf49a43" />
<img width="1920" height="1080" alt="a" src="https://github.com/user-attachments/assets/25ab1f91-ef0d-4987-a40d-d9711d10ceee" />
<img width="1920" height="1080" alt="a1" src="https://github.com/user-attachments/assets/e9389cb1-346e-4029-89c4-7a08bca34201" />
<img width="1920" height="1080" alt="a2" src="https://github.com/user-attachments/assets/7ac5c1b0-8dde-4a18-8bce-3cecba0f91f3" />
<img width="1920" height="1080" alt="a3" src="https://github.com/user-attachments/assets/3a6d4fed-a51a-4c36-a906-7008c5ead907" />
<img width="1920" height="1080" alt="a4" src="https://github.com/user-attachments/assets/4f93eb9e-2f5d-473d-9bc0-a41f527d8184" />
<img width="1920" height="1080" alt="a5" src="https://github.com/user-attachments/assets/13182be8-f6f0-400c-a6c4-669e1e3b616e" />
<img width="1920" height="1080" alt="a6" src="https://github.com/user-attachments/assets/fa380a7f-c53b-4cb6-baa4-7b64fd811d27" />
<img width="1920" height="1080" alt="a7" src="https://github.com/user-attachments/assets/9af2e578-b466-43ab-af02-548100c855ab" />

