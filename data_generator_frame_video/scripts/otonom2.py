"""
TEK SEFERLİK HIZLANDIRILMIŞ VE HASSAS PİPELINE (1 - 700 KARE)
--------------------------------------------------------------
1. Akıllı Multi-Point Raycasting: Tüm köşeler yerine sadece merkez ve 3 kritik köşeye 
   bakarak render hızını büyük ölçüde artırır.
2. Frustum Culling: Kamera görüş alanı dışındakileri ve arkadakileri anında eler.
3. Tek seferde çalışır, 1-700 kareyi işleyip doğrulama videosunu üretir.
"""

import bpy
import os
import cv2
import mathutils
from bpy_extras.object_utils import world_to_camera_view

# --- KULLANICI AYARLARI ---
base_output_dir = r"D:\datasets_videos_all\multi_dataset\video_seti_varyasyon_3"
img_dir = os.path.join(base_output_dir, "images")
lbl_dir = os.path.join(base_output_dir, "labels")
os.makedirs(img_dir, exist_ok=True)
os.makedirs(lbl_dir, exist_ok=True)

GLOBAL_START = 1
GLOBAL_END = 700
STEP_SIZE = 1

TARGET_CLASSES = {
    "Active_Box": 0, "Active_Rock": 1, "Active_Wood": 2, "Active_Animal": 3,
    "Other_Box": 4, "Other_Rock": 5, "Other_Wood": 6, "Other_Animal": 7,
    "Edge_Box": 8, "Edge_Rock": 9, "Edge_Wood": 10, "Edge_Animal": 11,
}

CLASS_NAMES = {v: k for k, v in TARGET_CLASSES.items()}

def get_class_id(obj_name):
    for key, class_id in TARGET_CLASSES.items():
        if key.lower() in obj_name.lower(): return class_id
    return 1

def find_mesh_recursive(obj):
    if obj.type == 'MESH' and obj.data: return obj
    for child in obj.children:
        found = find_mesh_recursive(child)
        if found: return found
    return None

def is_object_visible_by_raycast(scene, camera, target_mesh):
    """Sadece merkez ve en kritik 3 köşeye bakarak hem hız kazandırır hem arkada kalanı eler."""
    depsgraph = bpy.context.evaluated_depsgraph_get()
    cam_pos = camera.matrix_world.translation
    
    mat_world = target_mesh.matrix_world
    corners = [mat_world @ mathutils.Vector(c) for c in target_mesh.bound_box]
    
    # 9 nokta yerine sadece: Merkez + 3 kritik köşe (0, 2, 6)
    test_points = [target_mesh.matrix_world.translation, corners[0], corners[2], corners[6]]
    
    hits = 0
    for pt in test_points:
        direction = pt - cam_pos
        dist = direction.length
        direction.normalize()
        
        result, hit_loc, _, _, hit_obj, _ = scene.ray_cast(depsgraph, cam_pos, direction, distance=dist - 0.01)
        
        # Eğer ışın hiçbir şeye çarpmadıysa veya doğrudan hedef nesneye çarptıysa görünürdür
        if not result or (hit_obj and (hit_obj == target_mesh or hit_obj.parent == target_mesh)):
            hits += 1
            
    # Kritik noktalardan en az 1 tanesi bile görünüyorsa kabul et
    return hits >= 1

def get_bounding_box_2d(scene, camera, obj):
    target_mesh = find_mesh_recursive(obj)
    if not target_mesh: return None
    
    # 1. Görünürlük ve Arkada Kalma Kontrolü (Hızlandırılmış Raycast)
    if not is_object_visible_by_raycast(scene, camera, target_mesh):
        return None

    # 2. 2D Kamera İz Düşümü ve Frustum Culling
    corners = [target_mesh.matrix_world @ mathutils.Vector(c) for c in target_mesh.bound_box]
    cam_coords = [world_to_camera_view(scene, camera, co) for co in corners]
    
    if any(cc.z < 0 for cc in cam_coords): return None
    
    min_x = min(cc.x for cc in cam_coords)
    max_x = max(cc.x for cc in cam_coords)
    min_y = min(cc.y for cc in cam_coords)
    max_y = max(cc.y for cc in cam_coords)

    if max_x < 0 or min_x > 1 or max_y < 0 or min_y > 1: return None

    w = max_x - min_x
    h = max_y - min_y
    res_x, res_y = scene.render.resolution_x, scene.render.resolution_y
    if (w * res_x) < 10 or (h * res_y) < 10: return None

    return (min_x + w/2, 1 - (min_y + h/2), w, h)

def generate_validation_video():
    image_files = sorted([f for f in os.listdir(img_dir) if f.endswith(".png")])
    if not image_files: return

    sample_img = cv2.imread(os.path.join(img_dir, image_files[0]))
    if sample_img is None: return
    height, width, _ = sample_img.shape
    output_video_path = os.path.join(base_output_dir, "dogrulama_video_tekrar.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, 30, (width, height))

    for img_file in image_files:
        img_path = os.path.join(img_dir, img_file)
        base_name = os.path.splitext(img_file)[0]
        txt_path = os.path.join(lbl_dir, f"{base_name}.txt")

        img = cv2.imread(img_path)
        if img is None: continue

        if os.path.exists(txt_path):
            with open(txt_path, "r") as f:
                for line in f.readlines():
                    parts = line.strip().split()
                    if len(parts) == 5:
                        cid = int(parts[0])
                        xc, yc, w, h = map(float, parts[1:])
                        
                        xmin = int((xc - w / 2) * width)
                        xmax = int((xc + w / 2) * width)
                        ymin = int((yc - h / 2) * height)
                        ymax = int((yc + h / 2) * height)

                        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 165, 255), 2)
                        cname = CLASS_NAMES.get(cid, "Object")
                        cv2.putText(img, cname, (xmin, max(20, ymin - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

        video_writer.write(img)
    video_writer.release()
    print(f">>> Doğrulama Videosu Kaydedildi: {output_video_path}")

def run_pipeline():
    scene = bpy.context.scene
    camera = scene.camera
    if not camera: return

    print("\n================ HIZLANDIRILMIŞ SAHNE RENDERI BAŞLIYOR ================")
    
    for frame in range(GLOBAL_START, GLOBAL_END + 1, STEP_SIZE):
        scene.frame_set(frame)
        file_name = f"frame_{frame:04d}"
        txt_content = []
        detected_objects_log = []

        for obj in bpy.data.objects:
            if obj.hide_render or not any(k.lower() in obj.name.lower() for k in TARGET_CLASSES.keys()):
                continue
            
            bbox = get_bounding_box_2d(scene, camera, obj)
            if bbox:
                cid = get_class_id(obj.name)
                cname = CLASS_NAMES.get(cid, "Unknown")
                txt_content.append(f"{cid} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}")
                detected_objects_log.append(f"{cname} (ID:{cid})")

        with open(os.path.join(lbl_dir, f"{file_name}.txt"), "w") as f:
            f.write("\n".join(txt_content))

        scene.render.filepath = os.path.join(img_dir, f"{file_name}.png")
        bpy.ops.render.render(write_still=True)
        print(f"Kare {frame} işlendi. Toplam Etiket: {len(txt_content)} -> Etiketlenenler: {detected_objects_log}")

    print("\n>>> RENDER SÜRECİ TAMAMLANDI, VİDEO HAZIRLANIYOR... <<<")
    generate_validation_video()
    print("\n>>> TÜM İŞLEMLER BAŞARIYLA BİTTİ! <<<")

if __name__ == "__main__":
    run_pipeline()
