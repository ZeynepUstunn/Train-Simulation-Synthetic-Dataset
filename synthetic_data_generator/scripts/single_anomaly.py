import bpy
import os
import mathutils
import random

# ==================== GENEL AYARLAR VE VERSİYON YÖNETİMİ ====================
OUTPUT_IMAGE_DIR = r"D:\Blender_Output\dataset\images\train"
OUTPUT_LABEL_DIR = r"D:\Blender_Output\dataset\labels\train"

# Başlangıç testleri için temiz bir deney ID'si
EXPERIMENT_ID = 1  

# Sınıf ID Eşleştirmeleri
TARGET_OBJECTS = {
    "Box": 0,      # 0 -> Kutu / Koli / Valiz
    "Rock": 1,     # 1 -> Rock (Taş/Kaya)
    "Rock_2": 1,   # 1 -> İkinci Kaya nesnesi
    "Wood": 2,     # 2 -> Wood (Ahşap/Kütük)   
    "Animal": 3,   # 3 -> Animal (Hayvan)
}

FRAME_STEP = 3  # Kaç karede bir render alınacağı

# ==================== BAŞ KISIM TEKİL ANOMALİ SENARYOSU ====================
SCENARIOS = [
    {
        "name": "initial_rock_test",        # Dosya adında görünecek açıklayıcı etiket
        "target_obj": "Rock_2",             # En baştaki test etmek istediğiniz nesne
        "start_frame": 1,                   # Animasyonun başı (Başlangıç karesi)
        "end_frame": 136                    # İlk aralığın bitiş karesi
    }
]
# ==============================================================================

os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)

scene = bpy.context.scene
camera = scene.camera

if not camera:
    raise Exception("HATA: Sahnede aktif bir kamera bulunamadı!")

from bpy_extras.object_utils import world_to_camera_view

# ==================== WORLD NODELERİNİ OTOMATİK KURMA ====================
mapping_node = None
bg_node = None

if scene.world:
    scene.world.use_nodes = True
    nodes = scene.world.node_tree.nodes
    links = scene.world.node_tree.links
    
    for node in nodes:
        if node.type == 'BACKGROUND':
            bg_node = node
            break
            
    for node in nodes:
        if node.type == 'MAPPING':
            mapping_node = node
            break
            
    if not mapping_node and bg_node:
        print("BİLGİ: Gölge ve ışık değişimi için Mapping düğümleri otomatik ekleniyor...")
        mapping_node = nodes.new(type='ShaderNodeMapping')
        tex_coord_node = nodes.new(type='ShaderNodeTexCoord')
        
        env_tex_node = None
        for link in bg_node.inputs['Color'].links:
            env_tex_node = link.from_node
            break
            
        if env_tex_node:
            links.new(tex_coord_node.outputs['Generated'], mapping_node.inputs['Vector'])
            links.new(mapping_node.outputs['Vector'], env_tex_node.inputs['Vector'])

current_sky_rot = random.uniform(0.0, 6.28)

# Tüm nesnelerin orijinal konum ve rotasyonlarını kaydediyoruz
original_transforms = {}
for obj_name in TARGET_OBJECTS.keys():
    obj = bpy.data.objects.get(obj_name)
    if obj:
        original_transforms[obj_name] = {
            "object": obj,
            "location": obj.location.copy(),
            "rotation_z": obj.rotation_euler[2]
        }

print(f"=== BAŞ KISIM TEK ANOMALİ DENEMESİ BAŞLADI (EXP {EXPERIMENT_ID}) ===")

for scenario in SCENARIOS:
    scenario_name = scenario["name"]
    target_obj_name = scenario["target_obj"]
    start_frame = scenario["start_frame"]
    end_frame = scenario["end_frame"]
    
    print(f"\n--- İşleniyor: {scenario_name} (Kareler: {start_frame} - {end_frame}) ---")
    
    for frame in range(start_frame, end_frame + 1, FRAME_STEP):
        scene.frame_set(frame)
        
        # 1. SKYBOX YÖNÜ VE GÖLGE AÇISINI DEĞİŞTİRME
        current_sky_rot += random.uniform(0.4, 1.2)
        if current_sky_rot > 6.28:
            current_sky_rot -= 6.28
            
        if mapping_node:
            mapping_node.inputs['Rotation'].default_value[2] = current_sky_rot

        # 2. ARKA PLAN IŞIK KUVVETİ VE RENGİNİ DEĞİŞTİRME
        if bg_node:
            bg_node.inputs['Strength'].default_value = random.uniform(0.7, 1.4)
            r_tint = random.uniform(0.9, 1.0)
            g_tint = random.uniform(0.9, 1.0)
            b_tint = random.uniform(0.95, 1.05)
            bg_node.inputs['Color'].default_value = (r_tint, g_tint, b_tint, 1.0)

        # 3. TÜM NESNELERİ VE ALT PARÇALARINI KENDİ ETRAFINDA DÖNDÜRME VE KAYDIRMA
        for obj_name, data in original_transforms.items():
            obj = data["object"]
            orig_loc = data["location"]
            orig_rot_z = data["rotation_z"]
            
            if obj:
                new_rot_z = orig_rot_z + random.uniform(0.0, 6.28)
                new_loc_x = orig_loc.x + random.uniform(-0.15, 0.15)
                new_loc_y = orig_loc.y + random.uniform(-0.15, 0.15)
                
                obj.rotation_euler[2] = new_rot_z
                obj.location.x = new_loc_x
                obj.location.y = new_loc_y
                
                for child in obj.children:
                    child.rotation_euler[2] = new_rot_z

        bpy.context.view_layer.update()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        depsgraph.update()

        # Benzersiz dosya adı formatı
        base_filename = f"rail_anomaly_exp{EXPERIMENT_ID}_{scenario_name}_frame_{frame:04d}"
        image_path = os.path.join(OUTPUT_IMAGE_DIR, base_filename + ".png")
        txt_path = os.path.join(OUTPUT_LABEL_DIR, base_filename + ".txt")
        
        # 4. Görüntüyü Render Al
        scene.render.filepath = image_path
        bpy.ops.render.render(write_still=True)
        
        # 5. Etiketleri Hesapla
        annotations = []
        
        if target_obj_name in TARGET_OBJECTS:
            class_id = TARGET_OBJECTS[target_obj_name]
            obj = bpy.data.objects.get(target_obj_name)
            
            if obj and not obj.hide_render:
                bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
                
                min_x, max_x = 1.0, 0.0
                min_y, max_y = 1.0, 0.0
                is_visible = False
                
                for corner in bbox_corners:
                    co_2d = world_to_camera_view(scene, camera, corner)
                    if co_2d is not None:
                        is_visible = True
                        min_x = min(min_x, co_2d.x)
                        max_x = max(max_x, co_2d.x)
                        min_y = min(min_y, co_2d.y)
                        max_y = max(max_y, co_2d.y)
                
                if is_visible:
                    # Sınırları 0 ile 1 arasına kırp
                    min_x = max(0.0, min(1.0, min_x))
                    max_x = max(0.0, min(1.0, max_x))
                    min_y = max(0.0, min(1.0, min_y))
                    max_y = max(0.0, min(1.0, max_y))
                    
                    width = max_x - min_x
                    height = max_y - min_y
                    
                    # Eğer nesne tamamen kameranın dışına çıktıysa veya çok küçükse yoksay
                    if width > 0.01 and height > 0.01:
                        x_center = min_x + (width / 2.0)
                        y_min_yolo = 1.0 - max_y
                        y_center = y_min_yolo + (height / 2.0)
                        annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        # Kareler için txt dosyasını oluştur
        with open(txt_path, 'w') as f:
            if annotations:
                f.write("\n".join(annotations) + "\n")

print(f"\n=== BAŞ KISIM TEK ANOMALİ DENEMESİ BAŞARIYLA TAMAMLANDI! ===")
