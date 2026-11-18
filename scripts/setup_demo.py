"""Generate a small demo scene (scene.blend) when no blend file is provided.

Run headless:  blender -b --python scripts/setup_demo.py
"""
import math
import os

import bpy

# Start from a guaranteed-clean scene.
bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 32
scene.render.resolution_x = 640
scene.render.resolution_y = 360
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 48

# Ground plane.
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"
mat_g = bpy.data.materials.new("GroundMat")
mat_g.use_nodes = True
principled = mat_g.node_tree.nodes["Principled BSDF"]
principled.inputs["Base Color"].default_value = (0.25, 0.28, 0.32, 1)
principled.inputs["Roughness"].default_value = 0.8
ground.data.materials.append(mat_g)

# Spinning Suzanne as the render subject.
bpy.ops.mesh.primitive_monkey_add(location=(0, 0, 1.2))
suzanne = bpy.context.active_object
suzanne.name = "Suzanne"
subsurf = suzanne.modifiers.new("Subsurf", "SUBSURF")
subsurf.levels = 1
subsurf.render_levels = 2
bpy.ops.object.shade_smooth()
mat_s = bpy.data.materials.new("SuzanneMat")
mat_s.use_nodes = True
bsdf = mat_s.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.85, 0.2, 0.15, 1)
bsdf.inputs["Roughness"].default_value = 0.35
suzanne.data.materials.append(mat_s)

# One full revolution across the frame range, linear interpolation.
suzanne.rotation_euler = (0, 0, 0)
suzanne.keyframe_insert("rotation_euler", frame=1)
suzanne.rotation_euler = (0, 0, 2 * math.pi)
suzanne.keyframe_insert("rotation_euler", frame=49)
for fcurve in suzanne.animation_data.action.fcurves:
    for keyframe in fcurve.keyframe_points:
        keyframe.interpolation = "LINEAR"

# Camera aimed at the subject via a track constraint.
bpy.ops.object.camera_add(location=(6.5, -6.5, 4.2))
camera = bpy.context.active_object
scene.camera = camera
target = bpy.data.objects.new("Target", None)
scene.collection.objects.link(target)
target.location = (0, 0, 1.1)
constraint = camera.constraints.new("TRACK_TO")
constraint.target = target
constraint.track_axis = "TRACK_NEGATIVE_Z"
constraint.up_axis = "UP_Y"

# Sun light.
bpy.ops.object.light_add(type="SUN", location=(4, -3, 8))
sun = bpy.context.active_object
sun.data.energy = 4.0
sun.data.angle = math.radians(15)
sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(30))

# Sky-ish world background.
world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
background = world.node_tree.nodes["Background"]
background.inputs["Color"].default_value = (0.55, 0.7, 0.95, 1)
background.inputs["Strength"].default_value = 1.0

out = os.path.join(os.getcwd(), "scene.blend")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("demo scene saved to", out)
