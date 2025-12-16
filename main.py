# main.py
#
# This script is intended to be run inside Blender's scripting environment.
#
# Setup sys.path for Blender to find project and vendor modules

import sys
from pathlib import Path

PROJECT_ROOT = Path("H:/My Drive/Courses/2025F/COS 426/Final Project/midi-machina")
VENDOR_DIR = PROJECT_ROOT / "vendor"

# make sure Blender can import project modules + vendored deps
for p in (PROJECT_ROOT, VENDOR_DIR):
    sp = str(p)
    if sp not in sys.path:
        sys.path.insert(0, sp)

import bpy
import mido

# helper function for clearing animations
def clear_animation_for_objects(names):
    for name in names:
        obj = bpy.data.objects.get(name)
        if obj:
            # clear animations
            obj.animation_data_clear()
            scn = bpy.context.scene
            scn.frame_set(1)

            # reset obj
            obj.rotation_mode = 'XYZ'
            obj.rotation_euler = (0.0, 0.0, 0.0)
            obj.location = (0.0, 0.0, 0.0)

    bpy.context.view_layer.update()

# helper function for clearing glow animations
def clear_animation_for_glow(names):
    for name in names:
        obj = bpy.data.objects.get(name)
        if obj:
            # clear animations
            node_tree = obj.material_slots[0].material.node_tree
            node_tree.animation_data_clear()
            scn = bpy.context.scene
            scn.frame_set(1)

            # reset glow value
            bsdf = next((n for n in node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
            socket = bsdf.inputs["Emission Strength"]
            socket.default_value = 1.0

# helper function for clearing shape key animations
def clear_animation_for_shapekeys(names):
    for name in names:
        obj = bpy.data.objects.get(name)
        if obj:
            # clear animations
            shape_keys = obj.data.shape_keys
            shape_keys.animation_data_clear()
            scn = bpy.context.scene
            scn.frame_set(1)

            # reset shape key values
            kb = shape_keys.key_blocks
            kb[1].value = 0.0
            kb[2].value = 0.0

# define scene objects
DRUM_OBJECTS = [
    "Kick_Stick", "Kick",
    "Snare_Stick", "Snare",
    "HiHat_Stick", "HiHat",
    "TomLo_Stick", "TomLo",
    "TomHi_Stick", "TomHi",
    "Crash_Stick", "Crash"
]
HARP_HAMMERS = [
    "Hammer.001", "Hammer.002", "Hammer.003", "Hammer.004", 
    "Hammer.005", "Hammer.006", "Hammer.007", "Hammer.008", 
    "Hammer.009", "Hammer.010", "Hammer.011", "Hammer.012", 
    "Hammer.013", "Hammer.014", "Hammer.015", "Hammer.016", 
    "Hammer.017", "Hammer.018", "Hammer.019", "Hammer.020", 
    "Hammer.021", "Hammer.022", "Hammer.023", "Hammer.024", 
    "Hammer.025", "Hammer.026", "Hammer.027", "Hammer.028", 
    "Hammer.029", "Hammer.030", "Hammer.031", "Hammer.032", 
    "Hammer.033", "Hammer.034", "Hammer.035", "Hammer.036",
]
HARP_STRINGS = [
    "String.001", "String.002", "String.003", "String.004", 
    "String.005", "String.006", "String.007", "String.008", 
    "String.009", "String.010", "String.011", "String.012", 
    "String.013", "String.014", "String.015", "String.016", 
    "String.017", "String.018", "String.019", "String.020", 
    "String.021", "String.022", "String.023", "String.024", 
    "String.025", "String.026", "String.027", "String.028", 
    "String.029", "String.030", "String.031", "String.032", 
    "String.033", "String.034", "String.035", "String.036"
]
ORGAN_PISTONS = [
    "Piston.001", "Piston.002", "Piston.003", "Piston.004", "Piston.005",
    "Piston.006", "Piston.007", "Piston.008", "Piston.009", "Piston.010",
    "Piston.011", "Piston.012", "Piston.013", "Piston.014", "Piston.015",
    "Piston.016", "Piston.017", "Piston.018", "Piston.019", "Piston.020",
    "Piston.021", "Piston.022", "Piston.023", "Piston.024", "Piston.025",
    "Piston.026", "Piston.027", "Piston.028", "Piston.029",
]
ORGAN_FILAMENTS = [
    "Filament.001", "Filament.002", "Filament.003", "Filament.004", "Filament.005",
    "Filament.006", "Filament.007", "Filament.008", "Filament.009", "Filament.010",
    "Filament.011", "Filament.012", "Filament.013", "Filament.014", "Filament.015",
    "Filament.016", "Filament.017", "Filament.018", "Filament.019", "Filament.020",
    "Filament.021", "Filament.022", "Filament.023", "Filament.024", "Filament.025",
    "Filament.026", "Filament.027", "Filament.028", "Filament.029"
]
BASS_OBJECTS = [
    "Core.001", "Core.002", "Core.003", "Core.004", "Core.005",
    "Core.006", "Core.007", "Core.008", "Core.009", "Core.010",
    "Core.011", "Core.012", "Core.013", "Core.014", "Core.015",
    "Core.016", "Core.017", "Core.018", "Core.019", "Core.020",
    "Core.021", "Core.022", "Core.023", "Core.024"
]
TRUMPET_OBJECTS = [
    "Gyro_X.001", "Gyro_Z.001", "Beam.001",
    "Gyro_X.002", "Gyro_Z.002", "Beam.002",
]

# clear all animations
clear_animation_for_objects(DRUM_OBJECTS)
clear_animation_for_objects(HARP_HAMMERS)
clear_animation_for_objects(ORGAN_PISTONS)
clear_animation_for_objects(TRUMPET_OBJECTS)
clear_animation_for_glow(ORGAN_FILAMENTS)
clear_animation_for_glow(BASS_OBJECTS)
clear_animation_for_shapekeys(HARP_STRINGS)

#----------------------------------
import importlib

import parser
import blender_anim

# reload modules to pick up recent edits in Blender without restarting
importlib.reload(parser)
importlib.reload(blender_anim)

# parse file
MIDI_PATH = str(PROJECT_ROOT / "solarpunkFIN.mid")
mid = mido.MidiFile(MIDI_PATH)
track_list = parser.parse_midi_file(mid)

# animate instruments
blender_anim.animate_drums(track_list=track_list, track_id=1)
blender_anim.animate_harp(track_list=track_list, track_id=2)
blender_anim.animate_organ(track_list=track_list, track_id=3)
blender_anim.animate_bass(track_list=track_list, track_id=4)
blender_anim.animate_trumpet_laser(track_list=track_list, track_id=5, obj_num=".001")
blender_anim.animate_trumpet_laser(track_list=track_list, track_id=6, obj_num=".002")