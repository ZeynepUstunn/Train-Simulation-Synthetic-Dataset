import bpy
import random
import os

# --- 1. ÇIKTI KLASÖRÜ AYARI ---
OUTPUT_DIR = r"D:\Blender_Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

scene = bpy.context.scene

# --- 2. GPU VE RENDER AYARLARI ---
scene.render.image_settings.file_format = 'PNG'
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU' # YOLO modeli eğitimi için renderları RTX ile hızlandıralım
scene.cycles.samples = 64   # Hızlı veri üretimi için optimize örnekleme
scene.cycles.use_denoising = True

# --- 3. SAHNEYE TEK BİR GÜNEŞ IŞIĞI EKLE ---
sun_light_obj = None
# Sahnede zaten bir güneş ışığı varsa onu bul
for obj in scene.objects:
    if obj.type == 'LIGHT' and obj.data.type == 'SUN':
        sun_light_obj = obj
        break

# Yoksa yeni bir güneş ışığı yarat
if not sun_light_obj:
    light_data = bpy.data.lights.new(name="RandomSun", type='SUN')
    sun_light_obj = bpy.data.objects.new(name="RandomSun", object_data=light_data)
    scene.collection.objects.link(sun_light_obj)

# --- 4. ANİMASYON KARE ARALIĞI (Anomali Bölgesi) ---
START_FRAME = 960
END_FRAME = 1080
FRAME_STEP = 5

print(f"--- Render Başlatılıyor: Kare {START_FRAME} ile {END_FRAME} Arası (Adım: {FRAME_STEP}) ---")

# --- 5. OTONOM RENDER DÖNGÜSÜ ---
for frame in range(START_FRAME, END_FRAME + 1, FRAME_STEP):
    # A) Blender sahnesini ilgili animasyon karesine getir
    # (Kamera animasyonlu olduğu için otomatik olarak doğru yere geçecektir)
    scene.frame_set(frame)
    
    # B) Işığın konumunu rastgele değiştir (Numpy yerine standart Python random modülü)
    new_x = random.uniform(-15.0, 15.0)
    new_y = random.uniform(-15.0, 15.0)
    new_z = random.uniform(10.0, 25.0)
    sun_light_obj.location = (new_x, new_y, new_z)
    
    # C) Işığın enerjisini (parlaklığını) değiştir
    # BlenderProc'taki 700-2000 arası değerler Blender'ın kendi güneş ışığı için çok yüksektir.
    # Saf Blender'da Güneş ışığı için 1.0 ile 5.0 arası değerler genellikle idealdir.
    sun_light_obj.data.energy = random.uniform(1.0, 5.0)
    
    # D) Render Dosya Yolu
    output_filename = f"train_anomali_frame_{frame:04d}.png"
    scene.render.filepath = os.path.join(OUTPUT_DIR, output_filename)
    
    print(f"[{frame}/{END_FRAME}] Render alınıyor: {output_filename}")
    
    # E) Render Al
    bpy.ops.render.render(write_still=True)

print("--- Tüm Render İşlemi Başarıyla Tamamlandı! ---")
