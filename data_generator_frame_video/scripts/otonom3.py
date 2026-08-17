"""
TEK SEFERLİK HIZLANDIRILMIŞ VE HASSAS PİPELINE (1 - 720 KARE)
--------------------------------------------------------------
1. Multi-Point Raycasting (5 Nokta): Merkez + 4 köşe kontrolü ile yüksek doğruluk ve hız.
2. Frustum Culling: Kamera dışındakileri ve arkadakileri anında eler.
3. Otomatik Video: 720 kare sonunda doğrulama videosunu otomatik oluşturur.
"""

import bpy
import os
import cv2
import mathutils
from bpy_extras.object_utils import world_to_camera_view

# --- KULLANICI AYARLARI ---
base_output_dir = r"D:\dataset_video_3"
img_dir = os.path.join(base_output_dir, "images")
lbl_dir = os.path.join(base_output_dir, "labels")
os.makedirs(img_dir, exist_ok=True)
os.makedirs(lbl_dir, exist_ok=True)

GLOBAL_START = 1
GLOBAL_END = 720
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
    """Merkez ve 4 köşeye ışın fırlatarak görünürlüğü doğrular."""
    depsgraph = bpy.context.evaluated_depsgraph_get()
    cam_pos = camera.matrix_world.translation
    
    mat_world = target_mesh.matrix_world
    corners = [mat_world @ mathutils.Vector(c) for c in target_mesh.bound_box]
    
    # Merkez + 4 köşe (toplam 5 nokta kontrolü)
    test_points = [
        target_mesh.matrix_world.translation, 
        corners[0], corners[2], corners[4], corners[6]
    ]
    
    hits = 0
    for pt in test_points:
        direction = pt - cam_pos
        dist = direction.length
        direction.normalize()
        
        result, hit_loc, _, _, hit_obj, _ = scene.ray_cast(depsgraph, cam_pos, direction, distance=dist - 0.01)
        
        if not result or (hit_obj and (hit_obj == target_mesh or hit_obj.parent == target_mesh)):
            hits += 1
            
    return hits >= 1

def get_bounding_box_2d(scene, camera, obj):
    target_mesh = find_mesh_recursive(obj)
    if not target_mesh: return None
    
    # 1. Görünürlük Kontrolü
    if not is_object_visible_by_raycast(scene, camera, target_mesh):
        return None

    # 2. 2D Projeksiyon
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
    height, width, _ = sample_img.shape
    output_video_path = os.path.join(base_output_dir, "dogrulama_video_final.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, 30, (width, height))

    for img_file in image_files:
        img = cv2.imread(os.path.join(img_dir, img_file))
        txt_path = os.path.join(lbl_dir, os.path.splitext(img_file)[0] + ".txt")

        if os.path.exists(txt_path):
            with open(txt_path, "r") as f:
                for line in f:
                    parts = list(map(float, line.strip().split()))
                    cid, xc, yc, w, h = int(parts[0]), *parts[1:]
                    xmin, xmax = int((xc - w/2)*width), int((xc + w/2)*width)
                    ymin, ymax = int((yc - h/2)*height), int((yc + h/2)*height)
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 165, 255), 2)
                    cv2.putText(img, CLASS_NAMES.get(cid, "Obj"), (xmin, max(20, ymin-10)), 0, 0.6, (0, 165, 255), 2)
        video_writer.write(img)
    video_writer.release()
    print(f">>> Video Kaydedildi: {output_video_path}")

def run_pipeline():
    scene = bpy.context.scene
    if not scene.camera: return

    for frame in range(GLOBAL_START, GLOBAL_END + 1, STEP_SIZE):
        scene.frame_set(frame)
        txt_content = []
        
        for obj in bpy.data.objects:
            if obj.hide_render or not any(k.lower() in obj.name.lower() for k in TARGET_CLASSES.keys()):
                continue
            bbox = get_bounding_box_2d(scene, scene.camera, obj)
            if bbox:
                txt_content.append(f"{get_class_id(obj.name)} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}")

        with open(os.path.join(lbl_dir, f"frame_{frame:04d}.txt"), "w") as f:
            f.write("\n".join(txt_content))

        scene.render.filepath = os.path.join(img_dir, f"frame_{frame:04d}.png")
        bpy.ops.render.render(write_still=True)
        print(f"Kare {frame}/{GLOBAL_END} tamamlandı. Etiketlenenler: {len(txt_content)} nesne.")

    generate_validation_video()

if __name__ == "__main__":
    run_pipeline()
