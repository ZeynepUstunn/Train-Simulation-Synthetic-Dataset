import os

# Doğru ve tam klasör yollarını buraya yazmalısın:
image_dir = r"D:/Blender_Output/dataset/images/train"  
label_dir = r"D:/Blender_Output/dataset/labels/train"  

images = {os.path.splitext(f)[0] for f in os.listdir(image_dir) if f.endswith('.png')}
labels = {os.path.splitext(f)[0] for f in os.listdir(label_dir) if f.endswith('.txt')}

extra_labels = labels - images

if extra_labels:
    print(f"Fazla olan .txt dosyaları (karşılığı resim yok): {extra_labels}")
else:
    print("Hiç fazlalık yok, sayılar tam eşleşiyor.")
