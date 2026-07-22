<img width="1920" height="1080" alt="1" src="https://github.com/user-attachments/assets/6604d52d-4818-4da4-9b1d-5c121400d501" />
<img width="1920" height="1080" alt="2" src="https://github.com/user-attachments/assets/4c42e6c4-6c79-4f88-8f7f-daa24f02b31e" />
<img width="1920" height="1080" alt="3" src="https://github.com/user-attachments/assets/c44011e3-37e1-49a6-9100-ecf54eea04ae" />
<img width="1920" height="1080" alt="4" src="https://github.com/user-attachments/assets/0295836d-be32-4cad-a26a-5f01bd796160" />
<img width="1920" height="1080" alt="5" src="https://github.com/user-attachments/assets/4c23e744-6b86-4088-be22-a5d1063144fe" />
<img width="1920" height="1080" alt="6" src="https://github.com/user-attachments/assets/9cd98ad3-2109-4dc4-a644-24aa33870535" />
<img width="1920" height="1080" alt="7" src="https://github.com/user-attachments/assets/86884fca-9068-4f88-a5c4-0491661ef6cc" />
<img width="1920" height="1080" alt="8" src="https://github.com/user-attachments/assets/ccf29e15-b7fd-4cf1-982e-1a236a5b24ab" />

# 🚨 Yan Hat ve Aktif Hat Eş Zamanlı Anomali Senaryosu (Multi-Track Edge Case)

🎯 Durum Özeti

Kamera açısına aynı anda hem trenin ilerlediği aktif hat (kendi rayımız) hem de yan hat (komşu ray) üzerindeki yabancı nesnelerin girmesi durumu kurgulanmıştır.

⚙️ Yapay Zeka Mantığı ve Önceliklendirme (Threat Prioritization)
Görsel Algılama (YOLO): Model ekrandaki her iki engeli de tespit eder ve Bounding Box ile etiketler.

Rota Ayrımı (ROI / Rail Segmentation): Yapay zeka, aktif tren hattı ile komşu hattı birbirinden ayırır.

Karar Mekanizması:

🛑 Aktif Raydaki Engel: Doğrudan çarpma rotasında olduğu için Acil Fren (E-Brake) uyarısı tetiklenir.

⚠️ Yan Raydaki Engel: Trenin güvenliğini doğrudan tehdit etmediği için Bilgi/Uyarı (Traffic Warning) olarak merkeze raporlanır.

💡 Veri Setine Katkısı

Bu sentetik veri senaryosu, modele sadece engel tanımayı değil; "Ekrandaki engellerden hangisi benim rotam üzerinde?" sorusunu yanıtlayarak tehdit önceliklendirme kabiliyeti kazandırır.

<img width="1920" height="1080" alt="9" src="https://github.com/user-attachments/assets/2b2d827b-bb78-4f0a-b624-a9f79bdf50b3" />
<img width="1920" height="1080" alt="10" src="https://github.com/user-attachments/assets/e9faa2ad-feac-4c2b-80da-427d77b8c706" />
<img width="1920" height="1080" alt="10" src="https://github.com/user-attachments/assets/a6b7626e-40e6-46f4-820c-5768ffa1b0b4" />
<img width="1920" height="1080" alt="11" src="https://github.com/user-attachments/assets/e5a9bda0-cbd5-445c-8109-d8ec2c1e3b8e" />

# 📋 Render Bölme ve Modüler İşleme Planı (Hafta Sonu Birleştirme)

## 🎯 Amaç
Sahnede artan obje ve geometri yoğunluğuna bağlı olarak yükselen render süresini yönetmek, VRAM/RAM kaynaklı çökme (crash) risklerini sıfırlamak ve donanımı korumak amacıyla **1500 karelik (frame)** simülasyonu 3 modüler parçada render almak.

## 🟩 Yapılacaklar (Checklist)

- [ ] **1. Parça Render Alımı:** Frame aralığını `1 - 500` olarak ayarla ve `render_part1` olarak çıktı al.
- [ ] **2. Parça Render Alımı:** Frame aralığını `501 - 1000` olarak ayarla ve `render_part2` klasörüne çıktı al. *(500. kareyi tekrarlama!)*
- [ ] **3. Parça Render Alımı:** Frame aralığını `1001 - 1500` olarak ayarla ve `render_part3` klasörüne çıktı al.
- [ ] **Işık & Çevre Kontrolü:** Parçalar arasında renk/ışık tonu farkı oluşmaması için HDRI, gün ışığı ve kamera hızı ayarlarına müdahale etme.

# Trenin tahtanın üstünden geçip gitmesi fiziksel bir kaza değil, nesne tespiti modelinin kameraya sıfır mesafeye kadar olan yaklaşma verisini toplama sürecidir.
"Ray üstü anomali senaryolarında (Obstacle Detection), kameranın yabancı nesneye yaklaşma ve temas anına kadarki tüm açısal verilerini (Continuous Spatial Data) toplamak amacıyla sürekli hat hareketi sürdürülmüştür."

# 🚀 Yapay Zeka Veri Seti İçin Anomali ve Edge Case Senaryoları 

## 1. 🪨 Nesne Türü ve Boyut Çeşitlendiricileri (Object Diversity)
Modelin sadece tahta blokları değil, farklı geometri ve materyalleri tanıması için:
* **Metal / Yansıtıcı Cisimler:** Ray üstünde birikmiş hurda, metal parçası veya araç aksamı (Işığı yansıttığı için parlama/glare testi yapar).
* **Doğal Engeller:** Ray üzerine düşmüş kaya/taş yığını veya devrilmiş ağaç dalı.
* **Organik / Hareketli Nesneler (Canlı Tespiti):** Ray üzerinde duran insan, hayvan (sığır/köpek) veya hat bakım işçisi maketleri.
* **Küçük / Alçak Engeller:** Ray seviyesini çok az aşan küçük taş veya alet çantası (Modelin düşük piksel boyutlu nesne algılama hassasiyetini ölçer).

## 2. 📍 Konumsel ve Geometrik Senaryolar (Spatial & Geometry Edge Cases)
* **Kısmi Engel (Partially Blocking):** Engelin tamamı değil, sadece bir kısmı (örn: sadece sağ/sol raya taşan tahta) aktif hatta duruyor.
* **Viraj İçi Anomali (Curve Detection):** Kameranın görüş açısının kısıtlandığı keskin virajların tam çıkışına konulan engeller (Modelin açısal algılama mesafesini test eder).
* **Tünel Giriş/Çıkış Anomalisi (High Contrast / Blind Spot):** Işık seviyesinin aniden değiştiği tünel ağzına yerleştirilen engeller.
* **Makas Geçişleri (Switching Tracks):** Trenin ray değiştirdiği (makas) noktalarda her iki hatta dağılmış çoklu engeller.

## 3. 🌧️ Çevre, Hava ve Işık Koşulları (Environmental Augmentation)
Blender içinde sadece nesneleri değil, sahne ortamını değiştirerek elde edilecek senaryolar:
* **Gece / Düşük Işık (Night Vision):** Trenin kendi farının (Spotlight) aydınlattığı alanda engel tespiti.
* **Sis / Puslu Hava (Volumetric Fog):** Görüş mesafesinin düştüğü durumlarda derinlik (depth) ve engel tanıma testi.
* **Gölge Yanılsamaları (Hard Shadows):** Ağaçların veya katener direklerinin ray üzerine düşürdüğü dik gölgeler (Modelin gölgeyi engel sanmasını / False Positive engeller).
* **Kamera Merceği Paraziti:** Ekran kartı renderında hafif gren (noise), motion blur veya mercek lekesi ekleyerek gerçek kamera kusurlarını simüle etmek.

## 4. 🛤️ Altyapısal Anomaliler (Structural Defects)
Yabancı nesne dışında ray hattının kendisindeki bozulmalar:
* **Eksik / Kırık Ray (Rail Break):** Rayın bir kısmının kopuk veya kırık olması.
* **Hizası Bozulmuş Travers:** Ahşap/beton traverslerin yerinden oynaması veya eksik olması.
