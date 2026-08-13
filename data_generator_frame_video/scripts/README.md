## otonom.py :

TEK SEFERLİK OTONOM VE HASSAS PİPELINE (1 - 700 KARE)
------------------------------------------------------
1. Mevcut sahne, skybox ve orijinal konumlar birebir korunur.
2. Multi-Point Raycasting ve Frustum Culling ile kusursuz etiketleme yapar.
3. Tek seferde çalışır, 1-700 kareyi işleyip doğrulama videosunu üretir.

## otonom_video.py :

TEK SEFERLİK HIZLANDIRILMIŞ VE HASSAS PİPELINE (1 - 700 KARE)
--------------------------------------------------------------
1. Akıllı Multi-Point Raycasting: Tüm köşeler yerine sadece merkez ve 3 kritik köşeye 
   bakarak render hızını büyük ölçüde artırır.
2. Frustum Culling: Kamera görüş alanı dışındakileri ve arkadakileri anında eler.
3. Tek seferde çalışır, 1-700 kareyi işleyip doğrulama videosunu üretir.
