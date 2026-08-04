import bpy
import os
import math
import mathutils

# --- GENEL AYARLAR ---
dataset_dir = r"D:/opencv_video/dataset_master_2" 
image_dir = os.path.join(dataset_dir, "images")
label_dir = os.path.join(dataset_dir, "labels")

os.makedirs(image_dir, exist_ok=True)
os.makedirs(label_dir, exist_ok=True)

scene = bpy.context.scene
camera = scene.camera
render = scene.render

render.image_settings.file_format = 'PNG'
start_frame = 1
end_frame = 890  # Toplam kare sayısı 890 olarak güncellendi

# --- YENİ ANOMALİ VE KARE ARALIKLARI (ÇAKIŞMALAR DAHİL) ---
anomaly_configs = [
    {
        "obj_name": "Rock",         
        "class_id": 1,              
        "start": 72,                
        "end": 230                  
    },
    {
        "obj_name": "Wood",
        "class_id": 2,
        "start": 20,
        "end": 94                   # 72-94 aralığında Rock ile çakışır, ikisi de yazılır
    },
    {
        "obj_name": "Box",
        "class_id": 0,
        "start": 650,
        "end": 890
    },
    {
        "obj_name": "Animal",
        "class_id": 3,
        "start": 350,
        "end": 605
    }
]

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
            return None # Kamera arkasında kalıyorsa atla
        
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

print("--- 1 - 890 Kare Kesintisiz Render ve Çakışma Uyumlu Etiketleme Başladı ---")

for f in range(start_frame, end_frame + 1):
    scene.frame_set(f)
    frame_name = f"{f:04d}"
    
    img_path = os.path.join(image_dir, frame_name + ".png")
    txt_path = os.path.join(label_dir, frame_name + ".txt")
    
    # 1. Her karenin PNG çıktısı mutlaka alınır (Video oluşturabilmek için)
    render.filepath = img_path
    bpy.ops.render.render(write_still=True)
    
    # 2. O karede aktif olan TÜM nesneler taranır (Çakışanlar dahil alt alta yazılır)
    boxes_to_write = []
    for config in anomaly_configs:
        if config["start"] <= f <= config["end"]:
            obj = bpy.data.objects.get(config["obj_name"])
            if obj:
                bbox = get_yolo_bbox(obj, scene)
                if bbox:
                    xc, yc, w, h = bbox
                    boxes_to_write.append(f"{config['class_id']} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")
    
    # 3. Eğer o karede herhangi bir nesne varsa .txt dosyası oluşturulur, yoksa dosya açılmaz (boş bırakılır)
    if boxes_to_write:
        with open(txt_path, "w") as f_txt:
            f_txt.writelines(boxes_to_write)

print("--- İşlem Tamamlandı! 890 Kare PNG ve Çakışma Kurallarına Uygun Etiketler Hazır ---")
