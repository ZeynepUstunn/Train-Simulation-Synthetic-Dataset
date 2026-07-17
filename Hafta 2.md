# 🗓️ HAFTA 2: Çevre Tasarımı, Bellek Yönetimi ve İşletim Sistemi Optimizasyonları

Bu döküman, projenin ikinci haftasında ray altı çakıl taşlarının (balast) modellenmesi sırasında karşılaşılan yüksek bellek (RAM/VRAM) kısıtlamalarını çözmek adına uygulanan sistem, donanım ve render optimizasyonlarını içermektedir.

## 1. Çevre Tasarımı ve Sahne Mimarisi
* **Sürücü Optimizasyonu:** Donanım performansını artırmak adına **NVIDIA Game Ready** sürücüleri güncellenmiş ve render sürelerinde optimizasyon sağlanmıştır.
* **Ufuk Çizgisi ve Skybox:** Sahne arka planına **Skybox ve dağ modelleri** entegre edilmiştir. Rayların ufuk çizgisinde aniden kesilmesini önlemek ve derinlik algısını korumak adına sahne geometrisi yatay eksende genişletilmiştir.
* **Ray ve Tünel Düzenlemeleri:** Kısıtlı model kaynakları nedeniyle ahşap traversli ray modeli seçilmiş ve metalik parlama (specular) efektleri eklenmiştir. Çeşitli kamera dönüşleri eklenerek rota güncellenmiş ve sol taraftaki ek hattın sonuna derinlik hissi vermesi için karanlık bir tünel silueti entegre edilmiştir.

## 2. Yüksek Yoğunluklu Nesne Yönetimi (Çakıl Taşları & Geometry Nodes)
* **Geometri Yönetimi:** Ray altındaki milyonlarca balast taşını simüle etmek için kullanılan **Geometry Nodes** sisteminde `Realize Instances` düğümünün sistemi kilitlediği (crash) saptanmıştır. 
* **Topoloji Optimizasyonu:** Dönüşlü/kıvrımlı hatların poligon yükünü artırması nedeniyle ray yapısı düz bir hatta çekilmiştir. Taş modelleri `Make Single User` ve `Convert to Mesh` işlemleriyle optimize edilmeye çalışılmış, işlem hacmini düşürmek adına taşlık alan ray altı tabanıyla eşitlenerek kademeli yerleşim yapılmıştır.

## 3. Sistem ve Bellek (RAM / Sanal Bellek) Optimizasyonları
* **Darboğaz Analizi:** Render esnasında RAM kullanımının **%97** seviyelerine çıkarak Blender'ın çökmesine (OOM - Out of Memory) neden olduğu Görev Yöneticisi üzerinden tespit edilmiştir.
* **Sistem Hafifletme:** Arka planda yüksek kaynak tüketen **WSL (Linux), Docker, Ubuntu ve Qt** gibi geliştirici araçları geçici olarak durdurulmuş veya sistemden kaldırılmıştır.
* **Sanal Bellek (Paging File) Kurulumu:** C diskinin doluluk oranını azaltmak adına, Windows işletim sisteminin **Sanal Bellek (Paging File)** dizini ikincil depolama birimi olan **D diskine** taşınmış ve genişletilmiştir. 
* **Disk Temizliği:** Sistemdeki `temp` ve `appdata` geçici dosyaları, Chrome önbelleği temizlenerek C diskinde **55 GB** boş alan açılmıştır.
  > *Not: Önbellek (Cache) temizliği sonrası ham modda (Solid Mode) yaşanan anlık ekran donmaları, ekran kartının (GPU) milyonlarca taşın ışık, gölge ve matris verilerini sıfırdan derlemesinden (shader compilation) kaynaklanmış olup geçicidir.*

## 4. Render ve Çıktı Optimizasyonu (Cycles & GPU)
* **Doku Sınırlandırması:** Render motorundaki yüksek bellek tüketimini kısmak için `Simplify` sekmesinden maksimum doku boyutu **128px** seviyesine sınırlandırılmıştır.
* **İşlemci Mimarisi Seçimi:** Eevee motorundan **Cycles (Path Tracing)** motoruna geçiş yapılmıştır. Sahnede GPU compute birimindeki anlık bellek darboğazını aşmak adına, hibrit ve CPU tabanlı render denemeleri yapılarak Blender'ın çökmeden kararlı (stable) bir şekilde görsel üretmesi sağlanmıştır.
* **Görsel Karıncalanma (Denoising):** Render başlangıcındaki karıncalanma efektinin Cycles motorunun çalışma prensibinden (Işın takibi örneklemesi) kaynaklandığı saptanmış, sonraki karelerde **Denoise** filtresinin devreye girmesiyle pürüzsüz görüntü elde edilmiştir.

## 5. Gelecek Çalışmalar
* [ ] Alt tabanın kenarlık hizalamasının milimetrik olarak eşitlenmesi.
* [ ] Kamera hareketinin curve (eğri) ve hız grafiklerinin (Graph Editor) düzenlenmesi.

<img width="1920" height="1080" alt="deneme2" src="https://github.com/user-attachments/assets/22de102e-725e-4cb4-b9d6-c748e8ed3dcb" />

<img width="1920" height="1080" alt="deneme4" src="https://github.com/user-attachments/assets/d174ebbd-c57d-48ae-b920-206f82133245" />

<img width="1920" height="1080" alt="deneme6" src="https://github.com/user-attachments/assets/1f3b3e5a-c9d0-49f2-8bd9-e7f203de561d" />

<img width="1917" height="712" alt="deneme8" src="https://github.com/user-attachments/assets/60d09a0b-296e-4451-bb1f-b5c324d295ab" />

