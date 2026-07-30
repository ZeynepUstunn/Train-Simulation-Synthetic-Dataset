import os
from collections import Counter

# Etiket klasörünün yolu
LABEL_DIR = r"D:\Blender_Output\dataset\labels\train"

# Sınıf ID'lerini kendi projenle eşleştirebilirsin
CLASS_NAMES = {
    0: "Box (Koli/Valiz)",
    1: "Rock (Taş/Kaya)",
    2: "Wood (Ahşap)",
    3: "Animal (Hayvan)"
}

class_counts = Counter()
empty_files = 0
total_files = 0

if os.path.exists(LABEL_DIR):
    for filename in os.listdir(LABEL_DIR):
        if filename.endswith(".txt"):
            total_files += 1
            file_path = os.path.join(LABEL_DIR, filename)
            
            with open(file_path, 'r') as f:
                lines = f.readlines()
                if not lines:
                    empty_files += 1
                for line in lines:
                    parts = line.strip().split()
                    if parts:
                        class_id = int(parts[0])
                        class_counts[class_id] += 1

    print("=== VERİ DAĞILIMI RAPORU ===")
    print(f"Toplam Etiket Dosyası: {total_files}")
    print(f"İçinde Hiç Nesne Olmayan (Boş) Dosya Sayısı: {empty_files}\n")
    
    print("Sınıf Bazında Nesne Adetleri:")
    for cid, count in sorted(class_counts.items()):
        name = CLASS_NAMES.get(cid, f"Bilinmeyen Sınıf ({cid})")
        print(f" - {name} (ID {cid}): {count} adet")
else:
    print(f"HATA: Belirtilen klasör bulunamadı: {LABEL_DIR}")
