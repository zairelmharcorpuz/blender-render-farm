"""Apply workflow render settings to the loaded scene.

Reads SAMPLES / RES_X / RES_Y from the environment (set by render.yml),
then lets the CLI flags (-o, -s, -e, -a) do the actual rendering.

Run headless:  blender -b scene.blend -P scripts/apply_settings.py -o ... -s N -e M -a
"""
import os

import bpy

scene = bpy.context.scene

# Runners have no GPU: always render with Cycles on CPU.
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = int(os.environ.get("SAMPLES", "32"))
scene.cycles.use_denoising = False

scene.render.resolution_x = int(os.environ.get("RES_X", "640"))
scene.render.resolution_y = int(os.environ.get("RES_Y", "360"))
scene.render.resolution_percentage = 100

scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.render.film_transparent = False
scene.render.use_overwrite = True

print(
    "render settings: engine=%s samples=%dx%d res=%dx%d"
    % (
        scene.render.engine,
        scene.cycles.samples,
        scene.render.resolution_x,
        scene.render.resolution_y,
        scene.render.resolution_percentage,
    )
)
