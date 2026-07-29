import bpy
import os
import mathutils
import random

OUTPUT_IMAGE_DIR = r"D:\Blender_Output\dataset\images\train"
OUTPUT_LABEL_DIR = r"D:\Blender_Output\dataset\labels\train"

EXPERIMENT_ID = 3  

TARGET_OBJECTS = {
    "Koli": 0,     
    "Rock": 1,     
    "Wood": 2,     
    "Wood_2": 2    
}

FRAME_STEP = 3  

# Sadece düzeltme yapılan koli aralığı
SCENARIOS = [
    {
        "name": "koli",                
        "target_obj": "Koli",          
        "start_frame": 620,            
        "end_frame": 810               
    }
]

os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)

scene = bpy.context.scene
camera = scene.camera
if not camera: raise Exception("Kamera bulunamadı!")

from bpy_extras.object_utils import world_to_camera_view

mapping_node, bg_node = None, None
if scene.world:
    scene.world.use_nodes = True
    for node in scene.world.node_tree.nodes:
        if node.type == 'BACKGROUND': bg_node = node
        if node.type == 'MAPPING': mapping_node = node
    if not mapping_node and bg_node:
        mapping_node = scene.world.node_tree.nodes.new(type='ShaderNodeMapping')
        tex_coord = scene.world.node_tree.nodes.new(type='ShaderNodeTexCoord')
        scene.world.node_tree.links.new(tex_coord.outputs['Generated'], mapping_node.inputs['Vector'])

current_sky_rot = random.uniform(0.0, 6.28)
original_transforms = {k: {"object": bpy.data.objects.get(k), "location": bpy.data.objects.get(k).location.copy(), "rotation_z": bpy.data.objects.get(k).rotation_euler[2]} for k in TARGET_OBJECTS.keys() if bpy.data.objects.get(k)}

for scenario in SCENARIOS:
    for frame in range(scenario["start_frame"], scenario["end_frame"] + 1, FRAME_STEP):
        scene.frame_set(frame)
        current_sky_rot = (current_sky_rot + random.uniform(0.4, 1.2)) % 6.28
        if mapping_node: mapping_node.inputs['Rotation'].default_value[2] = current_sky_rot
        if bg_node: bg_node.inputs['Strength'].default_value = random.uniform(0.7, 1.4)

        for obj_name, data in original_transforms.items():
            obj = data["object"]
            if obj:
                obj.rotation_euler[2] = data["rotation_z"] + random.uniform(0.0, 6.28)
                obj.location.x = data["location"].x + random.uniform(-0.15, 0.15)
                obj.location.y = data["location"].y + random.uniform(-0.15, 0.15)
                for child in obj.children: child.rotation_euler[2] = obj.rotation_euler[2]

        bpy.context.view_layer.update()
        bpy.context.evaluated_depsgraph_get().update()

        base_filename = f"rail_anomaly_exp{EXPERIMENT_ID}_{scenario['name']}_frame_{frame:04d}"
        image_path = os.path.join(OUTPUT_IMAGE_DIR, base_filename + ".png")
        txt_path = os.path.join(OUTPUT_LABEL_DIR, base_filename + ".txt")
        
        scene.render.filepath = image_path
        bpy.ops.render.render(write_still=True)
        
        annotations = []
        target_obj_name = scenario["target_obj"]
        if target_obj_name in TARGET_OBJECTS:
            class_id = TARGET_OBJECTS[target_obj_name]
            obj = bpy.data.objects.get(target_obj_name)
            if obj and not obj.hide_render:
                bbox_corners = [obj.matrix_world @ mathutils.Vector(c) for c in obj.bound_box]
                min_x, max_x, min_y, max_y, is_visible = 1.0, 0.0, 1.0, 0.0, False
                for corner in bbox_corners:
                    co_2d = world_to_camera_view(scene, camera, corner)
                    if co_2d is not None:
                        is_visible = True
                        min_x, max_x = min(min_x, co_2d.x), max(max_x, co_2d.x)
                        min_y, max_y = min(min_y, co_2d.y), max(max_y, co_2d.y)
                if is_visible:
                    w, h = max_x - min_x, max_y - min_y
                    if w > 0.001 and h > 0.001:
                        annotations.append(f"{class_id} {min_x + w/2:.6f} {(1.0 - max_y) + h/2:.6f} {w:.6f} {h:.6f}")

        with open(txt_path, 'w') as f:
            if annotations: f.write("\n".join(annotations) + "\n")
