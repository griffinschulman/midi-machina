import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/griffinschulman/Desktop/Princeton Courses/COS426/MIDI-MACHINA/midi-machina")
VENDOR_DIR = PROJECT_ROOT / "vendor"

# Make sure Blender can import project modules + vendored deps
for p in (PROJECT_ROOT, VENDOR_DIR):
    sp = str(p)
    if sp not in sys.path:
        sys.path.insert(0, sp)

# Sanity check: fail fast with useful info
try:
    import mido
except ModuleNotFoundError as e:
    import site
    print("[ERROR] Blender Python cannot import mido.")
    print("sys.executable:", sys.executable)
    print("site.getusersitepackages():", site.getusersitepackages())
    print("First sys.path entries:", sys.path[:10])
    raise

import bpy

def clear_animation_for_objects(names):
    for name in names:
        obj = bpy.data.objects.get(name)
        if obj:
            obj.animation_data_clear()
            scn = bpy.context.scene
            scn.frame_set(1)

            obj.rotation_mode = 'XYZ'
            obj.rotation_euler = (0.0, 0.0, 0.0)

    bpy.context.view_layer.update()

DRUM_OBJECTS = ["Kick_Stick","Snare_Stick","HiHat_Stick","TomLo_Stick","TomHi_Stick","Crash_Stick"]
HARP_OBJECTS = [
    "HarpHammer_C3","HarpHammer_C#3","HarpHammer_D3","HarpHammer_D#3","HarpHammer_E3",
    "HarpHammer_F3","HarpHammer_F#3","HarpHammer_G3","HarpHammer_G#3","HarpHammer_A3",
    "HarpHammer_A#3","HarpHammer_B3","HarpHammer_C4","HarpHammer_C#4","HarpHammer_D4",
    "HarpHammer_D#4","HarpHammer_E4","HarpHammer_F4","HarpHammer_F#4","HarpHammer_G4",
    "HarpHammer_G#4","HarpHammer_A4","HarpHammer_A#4","HarpHammer_B4","HarpHammer_C5",
    "HarpHammer_C#5","HarpHammer_D5","HarpHammer_D#5","HarpHammer_E5","HarpHammer_F5",
    "HarpHammer_F#5","HarpHammer_G5","HarpHammer_G#5","HarpHammer_A5","HarpHammer_A#5",
    "HarpHammer_B5"
]
clear_animation_for_objects(DRUM_OBJECTS)
clear_animation_for_objects(HARP_OBJECTS)

import importlib

import parser
import blender_anim

# Reload modules to pick up recent edits in Blender without restarting
importlib.reload(parser)
importlib.reload(blender_anim)

MIDI_PATH = str(PROJECT_ROOT / "solarpunkex2.mid")
mid = mido.MidiFile(MIDI_PATH)
track_list = parser.parse_midi_file(mid)

import blender_anim

blender_anim.animate_drums(track_list=track_list, drum_track_idx=1)
blender_anim.animate_harp(track_list=track_list, harp_track_idx=2)
blender_anim.animate_organ(track_list=track_list, organ_track_idx=3)
print("Animation complete.")