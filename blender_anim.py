import bpy
from math import radians

# Animate a hammer object in Blender based on note events
# perhaps send swing deg and rebound deg per object later, and make animate hammer one function
def animate_hammer(obj, notes, swing_deg, rebound_deg, axis, pre_frames):
    """
    Animate a hammer object based on note events

    - obj: Blender object representing the specific hammer
    - notes: List of Note objects to animate
    - pre_frames: hammer winds up before the note start
    - swing_deg: degrees the hammer swings down on hit
    - rebound_deg: degrees the hammer rebounds after hit
    """
    # assume obj is at rest position, rotate around Y axis
    rest_rot = obj.rotation_euler.copy()

    # iterate over notes to create keyframes
    for note in notes:
        hit_frame = note.start_frame
        pre_frame = max(hit_frame - pre_frames, 1) # ensure frame is at least 1 (first hit)
        rebound_frame = hit_frame + 2 # subject to change
        settle_frame = hit_frame + 5 # subject to change

        # Copies of the rest rotation for each phase
        up_rot = rest_rot.copy()
        down_rot = rest_rot.copy()
        rebound_rot = rest_rot.copy()


        # Apply swing angles (not sure which axis yet or multiple?, so I added all three)
        if axis == 'X':
            up_rot.x += radians(rebound_deg) # little pre-wind/rebound
            down_rot.x += radians(-swing_deg)      # swing down
            rebound_rot.x += radians(rebound_deg)  # little rebound
        elif axis == 'Y':
            up_rot.y += radians(rebound_deg) # little pre-wind/rebound
            down_rot.y += radians(-swing_deg)      # swing down
            rebound_rot.y += radians(rebound_deg)  # little rebound
        else: # 'Z'
            up_rot.z += radians(rebound_deg) # little pre-wind/rebound
            down_rot.z += radians(-swing_deg)      # swing down
            rebound_rot.z += radians(rebound_deg)  # little rebound

        # Pre-wind
        obj.rotation_euler = up_rot
        obj.keyframe_insert("rotation_euler", frame=pre_frame)

        # Hit
        obj.rotation_euler = down_rot
        obj.keyframe_insert("rotation_euler", frame=hit_frame)

        # Rebound
        obj.rotation_euler = rebound_rot
        obj.keyframe_insert("rotation_euler", frame=rebound_frame)

        # Settle
        obj.rotation_euler = rest_rot
        obj.keyframe_insert("rotation_euler", frame=settle_frame)

def animate_drums(track_list, drum_track_idx):
    """
    Animate drum hammers based on note events
    """
    drum_notes = track_list[drum_track_idx]

    # map drum pitches to hammer objects in Blender
    # separate pitches for different drums, loop over, call animate_hammer
    # save rotation axis to object or have a mapping here
    drum_mapping = {
        36: {"obj": "Kick_Stick", "swing_deg": 14.0, "rebound_deg": 10.0, "pre_frames": 3},
        40: {"obj": "Snare_Stick", "swing_deg": -14.0, "rebound_deg": -14.0, "pre_frames": 3},
        42: {"obj": "HiHat_Stick", "swing_deg": -27.0, "rebound_deg": -6.0, "pre_frames": 3},
        43: {"obj": "TomLo_Stick", "swing_deg": 35.0, "rebound_deg": 14.0, "pre_frames": 3},
        45: {"obj": "TomHi_Stick", "swing_deg": 35.0, "rebound_deg": 14.0, "pre_frames": 3},
        49: {"obj": "Crash_Stick", "swing_deg": 30.0, "rebound_deg": 10.0, "pre_frames": 3},
    }

    notes_by_pitch = {}
    for note in drum_notes:
        notes_by_pitch.setdefault(note.pitch, []).append(note)

    # For each pitch that we know how to animate, apply hammer animation
    for pitch, cfg in drum_mapping.items():
        if pitch not in notes_by_pitch:
            continue # skip unmapped pitches

        obj_name = cfg["obj"]
        # skip if obj_name not found in blender scene
        if obj_name not in bpy.data.objects:
            print(f"[WARN] Object {obj_name!r} not found in Blender scene, skipping.")
            continue

        # get blender object
        obj = bpy.data.objects[obj_name]
        # animate drum hammers
        animate_hammer(obj=obj,
                       notes=notes_by_pitch[pitch],
                       swing_deg=cfg["swing_deg"],
                       rebound_deg=cfg["rebound_deg"],
                       axis='Y',
                       pre_frames=cfg["pre_frames"])


def animate_harp(track_list, harp_track_idx):
    """
    Animate harp hammers based on note events
    """
    # 
    harp_notes = track_list[harp_track_idx]

    # map harp pitches to harp string objects in Blender
    harp_mapping = {
        60: "HarpHammer_C3",
        61: "HarpHammer_C#3",
        62: "HarpHammer_D3",
        63: "HarpHammer_D#3",
        64: "HarpHammer_E3",
        65: "HarpHammer_F3",
        66: "HarpHammer_F#3",
        67: "HarpHammer_G3",
        68: "HarpHammer_G#3",
        69: "HarpHammer_A3",
        70: "HarpHammer_A#3",
        71: "HarpHammer_B3",
        72: "HarpHammer_C4",
        73: "HarpHammer_C#4",
        74: "HarpHammer_D4",
        75: "HarpHammer_D#4",
        76: "HarpHammer_E4",
        77: "HarpHammer_F4",
        78: "HarpHammer_F#4",
        79: "HarpHammer_G4",
        80: "HarpHammer_G#4",
        81: "HarpHammer_A4",
        82: "HarpHammer_A#4",
        83: "HarpHammer_B4",
        84: "HarpHammer_C5",
        85: "HarpHammer_C#5",
        86: "HarpHammer_D5",
        87: "HarpHammer_D#5",
        88: "HarpHammer_E5",
        89: "HarpHammer_F5",
        90: "HarpHammer_F#5",
        91: "HarpHammer_G5",
        92: "HarpHammer_G#5",
        93: "HarpHammer_A5",
        94: "HarpHammer_A#5",
        95: "HarpHammer_B5"
    }

    harp_params = {
        "swing_deg": -7.0,
        "rebound_deg": -10.0,
        "axis": "X",
        "pre_frames": 3
    }

    notes_by_pitch = {}
    for note in harp_notes:
        notes_by_pitch.setdefault(note.pitch, []).append(note)

    # For each pitch that we know how to animate, apply hammer animation
    for pitch, obj_name in harp_mapping.items():
        if pitch not in notes_by_pitch:
            continue # skip unmapped pitches

        # skip if obj_name not found in blender scene
        if obj_name not in bpy.data.objects:
            print(f"[WARN] Object {obj_name!r} not found in Blender scene, skipping.")
            continue

        # get blender object
        obj = bpy.data.objects[obj_name]
        # print(f"Animating pitch {pitch} on object {obj_name} with {len(notes_by_pitch[pitch])} notes.")
        animate_hammer(
            obj=obj,
            notes=notes_by_pitch[pitch],
            **harp_params
        )