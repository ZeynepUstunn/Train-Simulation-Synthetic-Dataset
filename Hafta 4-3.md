# 🚉 Anomali ve Sentetik Veri Senaryoları

Durak yakınlarında insan hareketi ve yerleşim yoğun olduğu için bu bölgede kurgulanacak anomali senaryoları hem sahne gerçekçiliğini artırır hem de yapay zeka (YOLO) modelinin farklı geometri, materyal ve boyutlardaki engelleri tanımasını sağlar.

---

## 📦 1. İnsan / Yolcu Kaynaklı Anomaliler
Durak yakınlarında yolcuların veya taşıma işlemlerinin düşürebileceği objeler:

* **Bavul / Valiz / Çanta:** Durakta bekleyen birinin düşürdüğü kumaş veya deri bavul. *(Modelin prizmatik/kutu benzeri geometrileri öğrenmesi için idealdir.)*
* **Karton Koli / Taşıma Kutusu:** Köy yerinde kargo veya erzak taşınırken raya düşmüş büyük bir karton koli.
* **Bisiklet / Scooter:** Durağa yanaştırılmış veya raya devrilmiş bir bisiklet. *(İnce metalik iskeleti ve tekerlek hatlarıyla model için zorlu ve değerli bir test verisidir.)*

## 🚜 2. Tarım ve Köy Yaşamı Kaynaklı Anomaliler
Köy atmosferine tam oturan ve ray üzerine taşabilecek nesneler:

* **Saman Balyası:** Köy alanından raya yuvarlanmış silindir veya dikdörtgen saman balyası. *(Sarı/kahve tonları ve organik dokusuyla harika bir test objesidir.)*
* **Ahşap Meyve / Sebze Kasası:** Raya devrilmiş ve dağılmış tahta kasalar.
* **Ahşap Çit Parçası / Plaka:** Sahneye eklenen çitlerden kopmuş veya raya devrilmiş bir ahşap çit modülü. *(Sahne temasıyla tam uyumludur.)*
* **El Arabası (Wheelbarrow):** Rayın hemen kenarında duran veya tek tekerleği raya taşmış paslı bir el arabası.


## 🛠️ 3. Altyapı ve Bakım Kaynaklı Anomaliler
Saha çalışması ve durak bakım süreçlerini simüle eden nesneler:

* **Yağ Varili (Metal Drum):** Ray kenarında duran paslı sarı/kırmızı varil. *(Silindirik yapısı ve yüksek metalik yansımalarıyla ışık testleri sağlar.)*
* **Beton Blok / Trafik Konisi:** Durak yakınındaki bir tadilattan kalmış turuncu trafik konisi veya küçük beton blok.

## 💡 Yapay Zeka (YOLO) Açısından Kritik Yerleşim Tavsiyesi

* **Kısmi Engel (Partial Obstacle):** Objeyi doğrudan rayın tam ortasına koymak yerine **bir kısmını raya, bir kısmını peron veya toprağa değecek şekilde** yerleştir.
* **Katkısı:** Model sadece hattı tam bloklayan nesneleri değil, **aktif rotaya taşan potansiyel tehlikeleri** de (Sınır/Tehdit Algılama) tespit etmeyi öğrenir.

<img width="1920" height="1080" alt="b6" src="https://github.com/user-attachments/assets/1f2c86cb-fc33-4286-bfb8-af299f84e6d8" />
<img width="1920" height="1080" alt="b1" src="https://github.com/user-attachments/assets/15bd0c72-25f5-40ac-b9fe-56d5905e406a" />
<img width="1920" height="1080" alt="b2" src="https://github.com/user-attachments/assets/01c4008f-7c2b-47bb-97e7-02bc96b00a20" />
<img width="1920" height="1080" alt="b3" src="https://github.com/user-attachments/assets/a7513460-b361-4bf1-b6af-a80c2206cbb6" />
<img width="1920" height="1080" alt="a" src="https://github.com/user-attachments/assets/3cd4f715-c9c5-4077-8d02-233df397a741" />
<img width="1920" height="1080" alt="b4" src="https://github.com/user-attachments/assets/3462707b-6415-45de-b4e3-449dfc71be3d" />
<img width="1920" height="1080" alt="b5" src="https://github.com/user-attachments/assets/cb1fc70e-99e8-4567-bb19-4113640e7ecc" />
<img width="1920" height="1080" alt="b6" src="https://github.com/user-attachments/assets/3a835acf-77a7-4bf4-9f92-010dd2a2daef" />
