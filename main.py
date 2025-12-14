# main.py
#
# This script is intended to be run inside Blender's scripting environment.
#
# Setup sys.path for Blender to find project and vendor modules

import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/griffinschulman/Desktop/Princeton Courses/COS426/MIDI-MACHINA/midi-machina")
VENDOR_DIR = PROJECT_ROOT / "vendor"

# Make sure Blender can import project modules + vendored deps
for p in (PROJECT_ROOT, VENDOR_DIR):
    sp = str(p)
    if sp not in sys.path:
        sys.path.insert(0, sp)

import mido
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
ORGAN_OBJECTS = [
    "Tube.014", "Tube.010", "Tube.008", "Tube.012", "Tube.016",
    "Tube.028", "Tube.026", "Tube.024", "Tube.022", "Tube.020",
    "Tube.018", "Tube.006", "Tube.004", "Tube.002", "Tube.001",
    "Tube.003", "Tube.005", "Tube.007", "Tube.019", "Tube.021",
    "Tube.023", "Tube.025", "Tube.027", "Tube.029", "Tube.015",
    "Tube.011", "Tube.009", "Tube.013", "Tube.017"
]
BASS_OBJECTS = [
    "Core.001", "Core.002", "Core.003", "Core.004", "Core.005",
    "Core.006", "Core.007", "Core.008", "Core.009", "Core.010",
    "Core.011", "Core.012", "Core.013", "Core.014", "Core.015",
    "Core.016", "Core.017", "Core.018", "Core.019", "Core.020",
    "Core.021", "Core.022", "Core.023", "Core.024"
]
TRUMPET_OBJECTS = [
    "Laser.001", "Beam.001",
    "Laser.002", "Beam.002"
]

clear_animation_for_objects(DRUM_OBJECTS)
clear_animation_for_objects(HARP_OBJECTS)
clear_animation_for_objects(ORGAN_OBJECTS)
clear_animation_for_objects(BASS_OBJECTS)
clear_animation_for_objects(TRUMPET_OBJECTS)

import importlib

import parser
import blender_anim

# Reload modules to pick up recent edits in Blender without restarting
importlib.reload(parser)
importlib.reload(blender_anim)

MIDI_PATH = str(PROJECT_ROOT / "solarpunkFIN.mid")
mid = mido.MidiFile(MIDI_PATH)
track_list = parser.parse_midi_file(mid)

blender_anim.animate_drums(track_list=track_list, drum_track_idx=1)
blender_anim.animate_harp(track_list=track_list, harp_track_idx=2)
blender_anim.animate_organ(track_list=track_list, organ_track_idx=3)
blender_anim.animate_bass(track_list=track_list, bass_track_idx=4)
blender_anim.animate_trumpet_laser(track_list=track_list, trumpet_track_idx=5, trumpet_name="Laser.001", laser_name="Beam.001")
blender_anim.animate_trumpet_laser(track_list=track_list, trumpet_track_idx=6, trumpet_name="Laser.002", laser_name="Beam.002")
