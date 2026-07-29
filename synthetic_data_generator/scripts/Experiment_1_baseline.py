import bpy
import os
import mathutils
import random

# ==================== GENEL AYARLAR VE VERSİYON YÖNETİMİ ====================
OUTPUT_IMAGE_DIR = r"D:\Blender_Output\dataset\images\train"
OUTPUT_LABEL_DIR = r"D:\Blender_Output\dataset\labels\train"

EXPERIMENT_ID = 1  

# Sınıf ID Eşleştirmeleri
TARGET_OBJECTS = {
    "Koli": 0,     # 0 -> Kutu/Koli
    "Rock": 1,     # 1 -> Rock (Taş/Kaya)
    "Wood": 2      # 2 -> Wood (Ahşap/Kütük)
}

FRAME_STEP = 3  

SCENARIOS = [
    {
        "name": "rock_part1",          
        "target_obj": "Rock",        
        "start_frame": 1,
        "end_frame": 115
    },
    {
        "name": "wood",
        "target_obj": "Wood",
        "start_frame": 320,
        "end_frame": 380
    },
    {
        "name": "koli",
        "target_obj": "Koli",
        "start_frame": 660,
        "end_frame": 820
    },
    {
        "name": "rock_part2",          
        "target_obj": "Rock_2",        
        "start_frame": 1080,
        "end_frame": 1240
    }
]

os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)

scene = bpy.context.scene
camera = scene.camera

if not camera:
    raise Exception("HATA: Sahnede aktif bir kamera bulunamadı!")

from bpy_extras.object_utils import world_to_camera_view

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
original_transforms = {}
for obj_name in TARGET_OBJECTS.keys():
    obj = bpy.data.objects.get(obj_name)
    if obj:
        original_transforms[obj_name] = {
            "object": obj,
            "location": obj.location.copy(),
            "rotation_z": obj.rotation_euler[2]
        }

for scenario in SCENARIOS:
    scenario_name = scenario["name"]
    target_obj_name = scenario["target_obj"]
    start_frame = scenario["start_frame"]
    end_frame = scenario["end_frame"]
    
    for frame in range(start_frame, end_frame + 1, FRAME_STEP):
        scene.frame_set(frame)
        current_sky_rot += random.uniform(0.4, 1.2)
        if current_sky_rot > 6.28: current_sky_rot -= 6.28
        if mapping_node: mapping_node.inputs['Rotation'].default_value[2] = current_sky_rot

        if bg_node:
            bg_node.inputs['Strength'].default_value = random.uniform(0.7, 1.4)
            bg_node.inputs['Color'].default_value = (random.uniform(0.9, 1.0), random.uniform(0.9, 1.0), random.uniform(0.95, 1.05), 1.0)

        for obj_name, data in original_transforms.items():
            obj = data["object"]
            if obj:
                obj.rotation_euler[2] = data["rotation_z"] + random.uniform(0.0, 6.28)
                obj.location.x = data["location"].x + random.uniform(-0.15, 0.15)
                obj.location.y = data["location"].y + random.uniform(-0.15, 0.15)
                for child in obj.children:
                    child.rotation_euler[2] = obj.rotation_euler[2]

        bpy.context.view_layer.update()
        bpy.context.evaluated_depsgraph_get().update()

        base_filename = f"rail_anomaly_exp{EXPERIMENT_ID}_{scenario_name}_frame_{frame:04d}"
        image_path = os.path.join(OUTPUT_IMAGE_DIR, base_filename + ".png")
        txt_path = os.path.join(OUTPUT_LABEL_DIR, base_filename + ".txt")
        
        scene.render.filepath = image_path
        bpy.ops.render.render(write_still=True)
        
        annotations = []
        if target_obj_name in TARGET_OBJECTS:
            class_id = TARGET_OBJECTS[target_obj_name]
            obj = bpy.data.objects.get(target_obj_name)
            if obj and not obj.hide_render:
                bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
                min_x, max_x, min_y, max_y, is_visible = 1.0, 0.0, 1.0, 0.0, False
                for corner in bbox_corners:
                    co_2d = world_to_camera_view(scene, camera, corner)
                    if co_2d is not None:
                        is_visible = True
                        min_x, max_x = min(min_x, co_2d.x), max(max_x, co_2d.x)
                        min_y, max_y = min(min_y, co_2d.y), max(max_y, co_2d.y)
                if is_visible:
                    min_x, max_x = max(0.0, min(1.0, min_x)), max(0.0, min(1.0, max_x))
                    min_y, max_y = max(0.0, min(1.0, min_y)), max(0.0, min(1.0, max_y))
                    width, height = max_x - min_x, max_y - min_y
                    x_center = min_x + (width / 2.0)
                    y_center = (1.0 - max_y) + (height / 2.0)
                    if width > 0.001 and height > 0.001:
                        annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        with open(txt_path, 'w') as f:
            if annotations: f.write("\n".join(annotations) + "\n")
