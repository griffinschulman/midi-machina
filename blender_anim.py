import bpy
from math import radians

# Animate a hammer object in Blender based on note events
# perhaps send swing deg and rebound deg per object later, and make animate hammer one function
def animate_hammer_harp(obj, notes, swing_deg, rebound_deg, axis, pre_frames=4):
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

    notes = sorted(notes, key=lambda n: n.start_frame)

    # iterate over notes to create keyframes
    for note in notes:
        hit_frame = note.start_frame
        pre_frame = max(hit_frame - pre_frames, 1) # ensure frame is at least 1 (first hit)
        rebound_frame = hit_frame + 8 # 
        settle_frame = hit_frame + 20 # 
        hold_frame = max(pre_frame - 24, 1)

        # Copies of the rest rotation for each phase
        up_rot = rest_rot.copy()
        down_rot = rest_rot.copy()
        rebound_rot = rest_rot.copy()

        # Apply swing angles (not sure which axis yet or multiple?, so I added all three)
        if axis == 'X':
            up_rot.x += radians(rebound_deg) # little pre-wind/rebound
            down_rot.x += radians(-swing_deg)      # swing down
            rebound_rot.x += radians(rebound_deg+4)  # little rebound
        elif axis == 'Y':
            up_rot.y += radians(rebound_deg) # little pre-wind/rebound
            down_rot.y += radians(-swing_deg)      # swing down
            rebound_rot.y += radians(rebound_deg)  # little rebound
        else: # 'Z'
            up_rot.z += radians(rebound_deg) # little pre-wind/rebound
            down_rot.z += radians(-swing_deg)      # swing down
            rebound_rot.z += radians(rebound_deg)  # little rebound

        # Hold at rest until just before windup
        obj.rotation_euler = rest_rot
        obj.keyframe_insert("rotation_euler", frame=hold_frame)

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

def animate_hammer(obj, notes, swing_deg, rebound_deg, axis, pre_frames=4):
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

    notes = sorted(notes, key=lambda n: n.start_frame)

    # iterate over notes to create keyframes
    for note in notes:
        hit_frame = note.start_frame
        pre_frame = max(hit_frame - pre_frames, 1) # ensure frame is at least 1 (first hit)
        rebound_frame = hit_frame + 6 # 
        settle_frame = hit_frame + 10 # 
        hold_frame = max(pre_frame - 12, 1)

        # Copies of the rest rotation for each phase
        up_rot = rest_rot.copy()
        down_rot = rest_rot.copy()
        rebound_rot = rest_rot.copy()

        # Apply swing angles (not sure which axis yet or multiple?, so I added all three)
        if axis == 'X':
            up_rot.x += radians(rebound_deg) # little pre-wind/rebound
            down_rot.x += radians(-swing_deg)      # swing down
            rebound_rot.x += radians(rebound_deg+4)  # little rebound
        elif axis == 'Y':
            up_rot.y += radians(rebound_deg) # little pre-wind/rebound
            down_rot.y += radians(-swing_deg)      # swing down
            rebound_rot.y += radians(rebound_deg)  # little rebound
        else: # 'Z'
            up_rot.z += radians(rebound_deg) # little pre-wind/rebound
            down_rot.z += radians(-swing_deg)      # swing down
            rebound_rot.z += radians(rebound_deg)  # little rebound

        # Hold at rest until just before windup
        obj.rotation_euler = rest_rot
        obj.keyframe_insert("rotation_euler", frame=hold_frame)
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
        36: {"obj": "Kick_Stick", "swing_deg": 14.0, "rebound_deg": 10.0, "pre_frames": 24},
        40: {"obj": "Snare_Stick", "swing_deg": -13.0, "rebound_deg": -11.0, "pre_frames": 24},
        42: {"obj": "HiHat_Stick", "swing_deg": -27.0, "rebound_deg": -12.0, "pre_frames": 24},
        43: {"obj": "TomLo_Stick", "swing_deg": 35.0, "rebound_deg": 14.0, "pre_frames": 24},
        45: {"obj": "TomHi_Stick", "swing_deg": -35.0, "rebound_deg": -14.0, "pre_frames": 24},
        49: {"obj": "Crash_Stick", "swing_deg": 30.0, "rebound_deg": 14.0, "pre_frames": 24},
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
                       pre_frames=4)
                       # pre_frames=cfg["pre_frames"])


def animate_harp(track_list, harp_track_idx):
    """
    Animate harp hammers based on note events
    """
    harp_notes = track_list[harp_track_idx]

    # map harp pitches to harp string objects in Blender (3 octaves from C3 to B5)
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

    # parameters for harp hammer animation
    harp_params = {
        "swing_deg": -7.0,    # degrees the hammer swings down on hit
        "rebound_deg": -15.0, # degrees the hammer rebounds after hit
        "axis": "X",          # rotation axis
        "pre_frames": 4       # frames before hit to start windup
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
        animate_hammer_harp(
            obj=obj,
            notes=notes_by_pitch[pitch],
            **harp_params
        )

def animate_piston(obj, notes, z_rest=1.1, z_down=1.33, pre_frames=6):
    notes = sorted(notes, key=lambda n: n.start_frame)
    for note in notes:
        on_frame = int(note.start_frame)
        off_frame = int(note.end_frame)

        obj.location.z = z_rest
        obj.keyframe_insert("location", frame=max(on_frame - pre_frames, 1))

        obj.location.z = z_down
        obj.keyframe_insert("location", frame=on_frame)

        obj.location.z = z_rest
        obj.keyframe_insert("location", frame=off_frame)

def animate_organ(track_list, organ_track_idx):
    """
    Placeholder for organ animation based on note events
    """
    organ_notes = track_list[organ_track_idx]
    # Implementation would go here
    
    organ_mapping = {
        # Map organ pitches to Blender objects
        57: {"piston": "Piston.014", "glow": "Cylinder.284"}, # A3
        58: {"piston": "Piston.010", "glow": "Cylinder.280"}, # A#3
        59: {"piston": "Piston.008", "glow": "Cylinder.278"}, # B3
        60: {"piston": "Piston.012", "glow": "Cylinder.282"}, # C4
        61: {"piston": "Piston.016", "glow": "Cylinder.286"}, # C#4

        62: {"piston": "Piston.028", "glow": "Cylinder.298"}, # D4
        63: {"piston": "Piston.026", "glow": "Cylinder.296"}, # D#4
        64: {"piston": "Piston.024", "glow": "Cylinder.294"}, # E4
        65: {"piston": "Piston.022", "glow": "Cylinder.292"}, # F4
        66: {"piston": "Piston.020", "glow": "Cylinder.290"}, # F#4
        67: {"piston": "Piston.018", "glow": "Cylinder.288"}, # G4

        68: {"piston": "Piston.006", "glow": "Cylinder.276"}, # G#4
        69: {"piston": "Piston.004", "glow": "Cylinder.274"}, # A4
        70: {"piston": "Piston.002", "glow": "Cylinder.272"}, # A#4
        71: {"piston": "Piston.001", "glow": "Cylinder.271"}, # B4
        72: {"piston": "Piston.003", "glow": "Cylinder.273"}, # C5
        73: {"piston": "Piston.005", "glow": "Cylinder.375"}, # C#5
        74: {"piston": "Piston.007", "glow": "Cylinder.377"}, # D5

        75: {"piston": "Piston.019", "glow": "Cylinder.389"}, # D#5
        76: {"piston": "Piston.021", "glow": "Cylinder.391"}, # E5
        77: {"piston": "Piston.023", "glow": "Cylinder.393"}, # F5
        78: {"piston": "Piston.025", "glow": "Cylinder.395"}, # F#5
        79: {"piston": "Piston.027", "glow": "Cylinder.397"}, # G5
        80: {"piston": "Piston.029", "glow": "Cylinder.399"}, # G#5

        81: {"piston": "Piston.015", "glow": "Cylinder.385"}, # A5
        82: {"piston": "Piston.011", "glow": "Cylinder.381"}, # A#5
        83: {"piston": "Piston.009", "glow": "Cylinder.379"}, # B5
        84: {"piston": "Piston.013", "glow": "Cylinder.383"}, # C6
        85: {"piston": "Piston.017", "glow": "Cylinder.387"}, # C#6
    }

    # bucket notes by pitch once
    notes_by_pitch = {}
    for note in organ_notes:
        notes_by_pitch.setdefault(note.pitch, []).append(note)

    # piston motion
    for pitch, cfg in organ_mapping.items():
        if pitch not in notes_by_pitch:
            continue

        piston_name = cfg.get("piston")
        if piston_name and piston_name in bpy.data.objects:
            animate_piston(bpy.data.objects[piston_name], notes_by_pitch[pitch])
        elif piston_name:
            print(f"[WARN] Piston object {piston_name!r} not found.")

    # glow pass (reuse your glow code!)
    animate_glow_group(
        notes=organ_notes,
        mapping=organ_mapping,
        on_strength=10.0,
        off_strength=0.0,
        pre_frames=4,
        copy_material=True
    )

def animate_glow(obj, notes, on_strength=10.0, off_strength=0.0, pre_frames=4, copy_material=True):
    """
    Keyframe Principled BSDF Emission Strength for one object:
    - off until right before note-on
    - on at note-on
    - off at note-off
    """
    if not obj.material_slots or obj.material_slots[0].material is None:
        print(f"[WARN] {obj.name!r} has no material in slot {0}, skipping.")
        return

    mat = obj.material_slots[0].material
    if copy_material and mat.users > 1:
        mat = mat.copy()
        obj.material_slots[0].material = mat

    nodes = mat.node_tree.nodes
    bsdf = nodes["Principled BSDF"]
    sock = bsdf.inputs["Emission Strength"]

    notes = sorted(notes, key=lambda n: n.start_frame)

    for note in notes:
        on_frame = note.start_frame
        off_frame = note.end_frame
        hold_f = max(on_frame - pre_frames, 1)

        sock.default_value = off_strength
        sock.keyframe_insert(data_path="default_value", frame=max(hold_f - 1, 1))

        sock.default_value = on_strength
        sock.keyframe_insert(data_path="default_value", frame=on_frame)

        sock.default_value = off_strength
        sock.keyframe_insert(data_path="default_value", frame=off_frame)


def animate_glow_group(notes, mapping, on_strength=10.0, off_strength=0.0, pre_frames=4, copy_material=True):
    notes_by_pitch = {}
    for note in notes:
        notes_by_pitch.setdefault(note.pitch, []).append(note)

    for pitch, cfg in mapping.items():
        if pitch not in notes_by_pitch:
            continue

        # NEW: allow cfg to be {"glow": "..."} or {"piston": "...", "glow": "..."}
        obj_name = cfg.get("glow")

        obj = bpy.data.objects.get(obj_name)
        if obj is None:
            print(f"[WARN] Object {obj_name!r} not found, skipping.")
            continue

        animate_glow(
            obj=obj,
            notes=notes_by_pitch[pitch],
            on_strength=on_strength,
            off_strength=off_strength,
            pre_frames=pre_frames,
            copy_material=copy_material
        )