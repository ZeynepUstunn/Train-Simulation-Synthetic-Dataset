import cv2
import os

# --- AYARLAR ---
dataset_dir = r"D:/opencv_video/dataset_master_2"
image_dir = os.path.join(dataset_dir, "images")
label_dir = os.path.join(dataset_dir, "labels")
output_video_path = r"D:/opencv_video/anomaly_output_video_deneme2.mp4"

# --- DOĞRU SINIF ID VE İSİM EŞLEŞMELERİ (Blender Scriptin ile Birebir) ---
class_names = {
    0: {"name": "Box",    "alert": "DIKKAT: KUTU TESPIT EDILDI!",        "color": (255, 255, 0)},   # Sarı / Camgöbeği
    1: {"name": "Rock",   "alert": "DIKKAT: KAYA TESPIT EDILDI!",        "color": (0, 0, 255)},     # Kırmızı
    2: {"name": "Wood",   "alert": "DIKKAT: ODUN / TAHTA TESPIT EDILDI!", "color": (0, 165, 255)},   # Turuncu
    3: {"name": "Animal", "alert": "DIKKAT: HAYVAN / CANLI TESPIT EDILDI!", "color": (0, 255, 0)}   # Yeşil
}

start_frame = 1
end_frame = 890
fps = 30  # Videonun saniyedeki kare hızı

# İlk görselden genişlik ve yükseklik bilgilerini alalım
sample_img_path = os.path.join(image_dir, f"{start_frame:04d}.png")
sample_img = cv2.imread(sample_img_path)

if sample_img is None:
    print(f"Hata: Örnek görsel okunamadı! Yol: {sample_img_path}")
    exit()

height, width, _ = sample_img.shape

# Video Yazıcı (VideoWriter) Tanımlaması
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

print("--- OpenCV ile Uyarı Mesajlı ve Sayaçlı Video Üretimi Başladı ---")

# Etiket okunan kare sayısını takip etmek için sayaç
labeled_frame_count = 0

for f in range(start_frame, end_frame + 1):
    frame_name = f"{f:04d}"
    img_path = os.path.join(image_dir, frame_name + ".png")
    txt_path = os.path.join(label_dir, frame_name + ".txt")
    
    if not os.path.exists(img_path):
        continue
        
    frame = cv2.imread(img_path)
    active_classes_in_frame = []
    
    # Eğer bu kareye ait bir etiket (.txt) dosyası varsa oku
    if os.path.exists(txt_path):
        labeled_frame_count += 1  # Etiket okunan kare sayısını 1 artır
        
        with open(txt_path, "r") as f_txt:
            lines = f_txt.readlines()
            
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
                
            class_id = int(parts[0])
            xc, yc, w, h = map(float, parts[1:])
            
            # YOLO normalized formatından piksel koordinatlarına çevrim
            box_w = int(w * width)
            box_h = int(h * height)
            x_center = int(xc * width)
            y_center = int(yc * height)
            
            xmin = int(x_center - box_w / 2)
            ymin = int(y_center - box_h / 2)
            xmax = int(x_center + box_w / 2)
            ymax = int(y_center + box_h / 2)
            
            # Doğru sınıf sözlüğünden veriyi al
            cfg = class_names.get(class_id, {"name": "Unknown", "alert": "ANOMALI", "color": (255, 255, 255)})
            color = cfg["color"]
            
            # 1. Nesnenin etrafına Bounding Box çiz
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 3)
            
            # Nesne kutusu üzerine isim yazısı
            cv2.putText(frame, cfg["name"], (xmin, max(35, ymin - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)
            
            # Çakışmalar dahil o karedeki tüm aktif sınıfları listeye ekle
            if cfg not in active_classes_in_frame:
                active_classes_in_frame.append(cfg)

    # 2. Üst Kısımda Uyarı Mesajı Oluşturma (Eğer karede anomali varsa)
    if active_classes_in_frame:
        alert_texts = [item["alert"] for item in active_classes_in_frame]
        combined_alert_text = " | ".join(alert_texts)
        
        # Üst uyarı bandı arkaplanı (Siyah kutu)
        cv2.rectangle(frame, (0, 0), (width, 60), (0, 0, 0), -1)
        
        # Uyarı Yazısı
        cv2.putText(frame, combined_alert_text, (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    # İşlenen kareyi videoya yaz
    video_writer.write(frame)

# Kaynakları serbest bırak
video_writer.release()

print("--- İşlem Tamamlandı! ---")
print(f"Toplam {end_frame} kare tarandı.")
print(f"İçinde anomali (etiket) bulunan toplam kare sayısı: {labeled_frame_count}")
print(f"Video başarıyla kaydedildi: {output_video_path}")
