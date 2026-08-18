## otonom.py :

TEK SEFERLİK OTONOM VE HASSAS PİPELINE (1 - 700 KARE)
------------------------------------------------------
1. Mevcut sahne, skybox ve orijinal konumlar birebir korunur.
2. Multi-Point Raycasting ve Frustum Culling ile kusursuz etiketleme yapar.
3. Bir nesnenin görünürlüğünü doğrulamak için toplam 9 ışın yollanıyor.
4. Tek seferde çalışır, 1-700 kareyi işleyip doğrulama videosunu üretir.

Not: Eğer sahnede çok fazla nesne varsa veya donanım üzerinde yük oluşturuyorsa, bu 9 noktalı kontrol sistemi her karede hesaplandığı için süreci yavaşlatabilir.

## otonom2.py :

TEK SEFERLİK HIZLANDIRILMIŞ VE HASSAS PİPELINE (1 - 700 KARE)
--------------------------------------------------------------
1. Akıllı Multi-Point Raycasting: Tüm köşeler yerine sadece merkez ve 3 kritik köşeye 
   bakarak render hızını büyük ölçüde artırır.
2. Frustum Culling: Kamera görüş alanı dışındakileri ve arkadakileri anında eler.
3. Tek seferde çalışır, 1-700 kareyi işleyip doğrulama videosunu üretir.

Not: Daha hızlı ancak OpencCV ile çizilen kare biraz geniş kalabiliyor.
## otonom3.py :

TEK SEFERLİK HIZLANDIRILMIŞ VE YÜKSEK DOĞRULUKLU PİPELINE (1 - 720 KARE)
------------------------------------------------------------------------
1. Optimizasyonlu Multi-Point Raycasting (5 Nokta): Nesne merkezine ek olarak 4 köşeyi kontrol ederek, örtünme (occlusion) durumlarında yüksek doğruluk ve hız dengesi sağlar.
2. Dinamik Frustum Culling: Kamera görüş alanı dışındaki veya arkasında kalan nesneleri en düşük işlem maliyetiyle tespit edip eler.
3. Tam Otomasyon: 720 karelik render, etiketleme ve sonuçların görselleştirildiği doğrulama videosu üretimini tek bir döngüde tamamlar.

Not: Hız ve doğruluk arasında kurulan en dengeli mimaridir; yüksek render performansı sunarken aynı zamanda nesnelerin örtünme durumlarında bile etiket hassasiyetini koruyarak en verimli veri üretim sürecini sağlar.
