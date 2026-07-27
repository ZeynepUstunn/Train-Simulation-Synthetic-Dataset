import bpy
import bpy_extras
import random
import os
import mathutils

# --- 1. KLASÖR VE ÇIKTI YAPISI AYARLARI ---
BASE_DIR = r"D:\Blender_Output\dataset"
IMAGE_DIR = os.path.join(BASE_DIR, "images", "train")
LABEL_DIR = os.path.join(BASE_DIR, "labels", "train")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(LABEL_DIR, exist_ok=True)

# --- 2. VARYANT VE NESNE TANIMLAMALARI ---
# En dıştaki klasörün adını yazman yeterli, kod asıl modeli kendi bulacak.
TARGET_OBJECT_NAME = "box"  
NESNE_TIPI = "koli"
VARYANT = "v1"
CLASS_ID = 0

scene = bpy.context.scene
cam = scene.camera

# --- 3. GPU VE RENDER AYARLARI ---
scene.render.image_settings.file_format = 'PNG'
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU'
scene.cycles.samples = 32
scene.cycles.use_denoising = True

# --- 4. İÇ İÇE KLASÖRLERDEKİ ASIL MODELİ BULAN ALGORİTMA ---
def find_real_mesh(obj):
    if obj.type == 'MESH':  
        return obj
    for child in obj.children: 
        found = find_real_mesh(child)
        if found:
            return found
    return None

# --- 5. KESİN ÇÖZÜM: YOLO KUTUSU HESAPLAYAN FONKSİYON ---
def get_yolo_bbox(scene, cam, obj):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    obj_eval = obj.evaluated_get(depsgraph)
    
    bound_box = [obj_eval.matrix_world @ mathutils.Vector(corner) for corner in obj_eval.bound_box]
    corners_2d = [bpy_extras.object_utils.world_to_camera_view(scene, cam, c) for c in bound_box]
    
    valid_corners = [c for c in corners_2d if c.z > 0]
    if not valid_corners:
        return None
        
    x_coords = [c.x for c in valid_corners]
    y_coords = [c.y for c in valid_corners]
    
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    if max_x < 0.0 or min_x > 1.0 or max_y < 0.0 or min_y > 1.0:
        return None
        
    min_x = max(0.0, min_x)
    max_x = min(1.0, max_x)
    min_y = max(0.0, min_y)
    max_y = min(1.0, max_y)
    
    width = max_x - min_x
    height = max_y - min_y
    
    if width <= 0.0001 or height <= 0.0001:
        return None
        
    x_center = min_x + (width / 2.0)
    y_center = 1.0 - (min_y + (height / 2.0))
    
    return (x_center, y_center, width, height)

# --- 6. GÜNEŞ IŞIĞI HAZIRLIĞI ---
sun_light_obj = None
for obj in scene.objects:
    if obj.type == 'LIGHT' and obj.data.type == 'SUN':
        sun_light_obj = obj
        break

if not sun_light_obj:
    light_data = bpy.data.lights.new(name="RandomSun", type='SUN')
    sun_light_obj = bpy.data.objects.new(name="RandomSun", object_data=light_data)
    scene.collection.objects.link(sun_light_obj)

# --- 7. ANİMASYON DÖNGÜSÜ ---
START_FRAME = 960
END_FRAME = 1080
FRAME_STEP = 5

print(f"--- YOLO Etiketli Render Başlatılıyor: Kare {START_FRAME} - {END_FRAME} ---")

# Objeyi sahnede bul ve gerçek 3D modelini (Mesh) ayıkla
base_obj = bpy.data.objects.get(TARGET_OBJECT_NAME)
target_obj = None

if base_obj:
    target_obj = find_real_mesh(base_obj)
    if target_obj:
        print(f"BİLGİ: Gerçek 3D model '{target_obj.name}' başarıyla bulundu!")
    else:
        print(f"HATA: '{TARGET_OBJECT_NAME}' içinde hiçbir fiziksel yüzey (MESH) bulunamadı!")
else:
    print(f"HATA: '{TARGET_OBJECT_NAME}' adında bir obje sahnede hiç bulunamadı!")

# Eğer obje sorunsuz bulunduysa döngüye gir
if target_obj:
    for frame in range(START_FRAME, END_FRAME + 1, FRAME_STEP):
        scene.frame_set(frame)
        
        # Kameranın ve sahnenin yeni konumunu arka planda zorla günceller
        bpy.context.view_layer.update()
        
        # Çeşitlilik (Augmentation) için ışık ayarları
        sun_light_obj.rotation_euler = (
            random.uniform(0.2, 1.2), 
            random.uniform(-1.0, 1.0), 
            random.uniform(0.0, 6.28) 
        )
        sun_light_obj.data.energy = random.uniform(1.5, 6.0)
        sun_light_obj.data.color = (
            random.uniform(0.8, 1.0),
            random.uniform(0.8, 0.95),
            random.uniform(0.7, 1.0)
        )
        
        file_name = f"{NESNE_TIPI}_{VARYANT}_frame_{frame:04d}"
        img_path = os.path.join(IMAGE_DIR, f"{file_name}.png")
        txt_path = os.path.join(LABEL_DIR, f"{file_name}.txt")
        
        print(f"[{frame}/{END_FRAME}] Render alınıyor: {file_name}")
        
        # Görseli render al ve kaydet
        scene.render.filepath = img_path
        bpy.ops.render.render(write_still=True)
        
        # YOLO kutusunu hesapla ve yaz
        bbox = get_yolo_bbox(scene, cam, target_obj)
        with open(txt_path, 'w') as f:
            if bbox:
                f.write(f"{CLASS_ID} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}\n")
            else:
                f.write(f"{CLASS_ID} 0.500000 0.500000 0.200000 0.200000\n")
                print(f"Uyarı: Frame {frame} için nesne kamerada yok, varsayılan etiket basıldı.")

    print("--- Tüm İşlem Başarıyla Tamamlandı! ---")