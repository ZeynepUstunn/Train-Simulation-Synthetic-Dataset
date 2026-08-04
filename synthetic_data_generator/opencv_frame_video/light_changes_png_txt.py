import bpy
import os
import math
import mathutils

# --- GENEL AYARLAR (DENEME İSMİ) ---
experiment_name = "exp8"  
dataset_dir = r"D:/opencv_video/dataset_master" 
image_dir = os.path.join(dataset_dir, "images")
label_dir = os.path.join(dataset_dir, "labels")

os.makedirs(image_dir, exist_ok=True)
os.makedirs(label_dir, exist_ok=True)

scene = bpy.context.scene
camera = scene.camera
render = scene.render

render.image_settings.file_format = 'PNG'

# --- FRAME STEP (KARE ATLAMA ADIMI) ---
frame_step = 5 

# --- 4 ANOMALİNİN KARE ARALIKLARI VE SINIF ID'LERİ ---
anomaly_configs = [
      {
              "obj_name": "Wood",
              "class_id": 2,
              "start": 50,
              "end": 171
          },
]

# --- AKŞAMÜSTÜ GÖLGE VE IŞIK YÖNÜ AYARI (TEK SEFERLİK) ---
print("--- Akşamüstü ışık yönü ve skybox ayarlanıyor... ---")
if scene.world and scene.world.node_tree:
    world_nodes = scene.world.node_tree.nodes
    world_links = scene.world.node_tree.links
    
    background_node = None
    env_node = None
    
    for node in world_nodes:
        if node.type == 'BACKGROUND':
            background_node = node
        elif node.type == 'TEX_ENVIRONMENT':
            env_node = node
            
    if background_node:
        background_node.inputs['Strength'].default_value = 0.7  
        
    if env_node:
        mapping_node = world_nodes.get("Sunset_Mapping")
        coord_node = world_nodes.get("Sunset_Coord")
        
        if not mapping_node:
            mapping_node = world_nodes.new(type='ShaderNodeMapping')
            mapping_node.name = "Sunset_Mapping"
            
        if not coord_node:
            coord_node = world_nodes.new(type='ShaderNodeTexCoord')
            coord_node.name = "Sunset_Coord"
            
        world_links.new(coord_node.outputs['Generated'], mapping_node.inputs['Vector'])
        world_links.new(mapping_node.outputs['Vector'], env_node.inputs['Vector'])
        
        sun_rotation_degrees = 120.0 
        mapping_node.inputs['Rotation'].default_value[2] = math.radians(sun_rotation_degrees)

def get_yolo_bbox(obj, scene):
    mesh = obj.data
    matrix_world = obj.matrix_world
    pts = [matrix_world @ mathutils.Vector(v.co) for v in mesh.vertices]
    cam_eval = camera.evaluated_get(bpy.context.evaluated_depsgraph_get())
    
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    
    from bpy_extras.object_utils import world_to_camera_view
    
    for pt in pts:
        co_ndc = world_to_camera_view(scene, cam_eval, pt)
        if co_ndc.z < 0:
            return None 
        
        x = co_ndc.x
        y = 1.0 - co_ndc.y
        
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        
    min_x = max(0.0, min(1.0, min_x))
    max_x = max(0.0, min(1.0, max_x))
    min_y = max(0.0, min(1.0, min_y))
    max_y = max(0.0, min(1.0, max_y))
    
    if max_x <= min_x or max_y <= min_y:
        return None
        
    x_center = (min_x + max_x) / 2.0
    y_center = (min_y + max_y) / 2.0
    w = max_x - min_x
    h = max_y - min_y
    
    return (x_center, y_center, w, h)

print(f"--- ({experiment_name}) Sadece Belirtilen Aralık ve O Anki Anomali İçin Render Başladı ---")

rendered_frames_count = 0

for config in anomaly_configs:
    start_f = config["start"]
    end_f = config["end"]
    target_obj_name = config["obj_name"]
    target_class_id = config["class_id"]
    
    # Her anomalinin kendi aralığında dön
    for f in range(start_f, end_f + 1, frame_step):
        scene.frame_set(f)
        
        file_prefix = f"{experiment_name}_{f:04d}"
        img_path = os.path.join(image_dir, file_prefix + ".png")
        txt_path = os.path.join(label_dir, file_prefix + ".txt")
        
        # 1. Karenin PNG çıktısını al
        render.filepath = img_path
        bpy.ops.render.render(write_still=True)
        rendered_frames_count += 1
        
        # 2. SADECE bu döngünün ait olduğu o anki hedef objeyi kontrol et ve kaydet
        boxes_to_write = []
        obj = bpy.data.objects.get(target_obj_name)
        if obj:
            bbox = get_yolo_bbox(obj, scene)
            if bbox:
                xc, yc, w, h = bbox
                boxes_to_write.append(f"{target_class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")
        
        # Etiket dosyasını oluştur
        if boxes_to_write:
            with open(txt_path, "w") as f_txt:
                f_txt.writelines(boxes_to_write)

print(f"--- İşlem Tamamlandı! Toplam {rendered_frames_count} kare, sadece ilgili anomali etiketleriyle kaydedildi. ---")
