import bpy
from math import radians

### HARP HAMMERS ###
def animate_hammer_harp(obj, notes, swing_deg, rebound_deg, axis, pre_frames=4):
    """
    Animate a hammer object based on note events

    - obj: Blender object representing the specific hammer
    - notes: List of Note objects to animate
    - pre_frames: hammer winds up before the note start
    - swing_deg: degrees the hammer swings down on hit
    - rebound_deg: degrees the hammer rebounds after hit
    - axis: rotation axis ('X', 'Y', or 'Z')
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
        else:
            return

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

### HARP ###
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

### DRUM HAMMERS ###
def animate_hammer(obj, notes, swing_deg, rebound_deg, axis, pre_frames=4):
    """
    Animate a hammer object based on note events (FOR DRUMS ONLY NOW)

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
        hold_frame = max(pre_frame - 12, 1) # 

        # Copies of the rest rotation for each phase
        up_rot = rest_rot.copy()
        down_rot = rest_rot.copy()
        rebound_rot = rest_rot.copy()

        # Apply swing angles (not sure which axis yet or multiple?, so I added all three)
        if axis == 'Y':
            up_rot.x += radians(rebound_deg) # little pre-wind/rebound
            down_rot.x += radians(-swing_deg)      # swing down
            rebound_rot.x += radians(rebound_deg+4)  # little rebound
        else:
            return
  
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

### DRUMS ###
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

### ORGAN PISTONS ###
def animate_piston(obj, notes, z_rest=1.1, z_up=1.33, pre_frames=6):
    notes = sorted(notes, key=lambda n: n.start_frame)
    for note in notes:
        on_frame = note.start_frame
        hold_frame = note.end_frame
        off_frame = hold_frame + 48

        # Move to rest position
        obj.location.z = z_rest
        obj.keyframe_insert("location", frame=max(on_frame - pre_frames, 1))

        # Move up on note on
        obj.location.z = z_up
        obj.keyframe_insert("location", frame=on_frame)

        obj.location.z = z_up
        obj.keyframe_insert("location", frame=hold_frame)

        # Move back to rest position
        obj.location.z = z_rest
        obj.keyframe_insert("location", frame=off_frame)

### ORGAN ###
def animate_organ(track_list, organ_track_idx):
    """
    organ animation based on note events
    """
    organ_notes = track_list[organ_track_idx]
    # Implementation would go here
    
    organ_mapping = {
        # Map organ pitches to Blender objects
        57: {"piston": "Piston.014", "glow": "Filament.014"}, # A3
        58: {"piston": "Piston.010", "glow": "Filament.010"}, # A#3
        59: {"piston": "Piston.008", "glow": "Filament.008"}, # B3
        60: {"piston": "Piston.012", "glow": "Filament.012"}, # C4
        61: {"piston": "Piston.016", "glow": "Filament.016"}, # C#4

        62: {"piston": "Piston.028", "glow": "Filament.028"}, # D4
        63: {"piston": "Piston.026", "glow": "Filament.026"}, # D#4
        64: {"piston": "Piston.024", "glow": "Filament.024"}, # E4
        65: {"piston": "Piston.022", "glow": "Filament.022"}, # F4
        66: {"piston": "Piston.020", "glow": "Filament.020"}, # F#4
        67: {"piston": "Piston.018", "glow": "Filament.018"}, # G4

        68: {"piston": "Piston.006", "glow": "Filament.006"}, # G#4
        69: {"piston": "Piston.004", "glow": "Filament.004"}, # A4
        70: {"piston": "Piston.002", "glow": "Filament.002"}, # A#4
        71: {"piston": "Piston.001", "glow": "Filament.001"}, # B4
        72: {"piston": "Piston.003", "glow": "Filament.003"}, # C5
        73: {"piston": "Piston.005", "glow": "Filament.005"}, # C#5
        74: {"piston": "Piston.007", "glow": "Filament.007"}, # D5

        75: {"piston": "Piston.019", "glow": "Filament.019"}, # D#5
        76: {"piston": "Piston.021", "glow": "Filament.021"}, # E5
        77: {"piston": "Piston.023", "glow": "Filament.023"}, # F5
        78: {"piston": "Piston.025", "glow": "Filament.025"}, # F#5
        79: {"piston": "Piston.027", "glow": "Filament.027"}, # G5
        80: {"piston": "Piston.029", "glow": "Filament.029"}, # G#5

        81: {"piston": "Piston.015", "glow": "Filament.015"}, # A5
        82: {"piston": "Piston.011", "glow": "Filament.011"}, # A#5
        83: {"piston": "Piston.009", "glow": "Filament.009"}, # B5
        84: {"piston": "Piston.013", "glow": "Filament.013"}, # C6
        85: {"piston": "Piston.017", "glow": "Filament.017"}, # C#6
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
        slot=0,
        on_strength=100.0,
        off_strength=0.0,
        pre_frames=2,
        copy_material=True
    )

### BASS ###
def animate_bass(track_list, bass_track_idx):
    """
    bass animation based on note events, BELOW ORGAN
    """
    # Implementation would go here
    bass_notes = track_list[bass_track_idx]

    bass_mapping = {
        47: "Core.001", # A2
        48: "Core.002", # A#2
        49: "Core.003", # B2
        50: "Core.004", # C3
        51: "Core.005", # C#3
        52: "Core.006", # D3
        53: "Core.007", # D#3
        54: "Core.008", # E3
        55: "Core.009", # F3
        56: "Core.010", # F#3
        57: "Core.011", # G3
        58: "Core.012", # G#3
        59: "Core.013", # A3
        60: "Core.014", # A#3
        61: "Core.015", # B3
        62: "Core.016", # C4
        63: "Core.017", # C#4
        64: "Core.018", # D4
        65: "Core.019", # D#4
        66: "Core.020", # E4
        67: "Core.021", # F4
        68: "Core.022", # F#4
        69: "Core.023", # G4
        70: "Core.024"  # G#4
    }

    # bucket notes by pitch
    notes_by_pitch = {}
    for note in bass_notes:
        notes_by_pitch.setdefault(note.pitch, []).append(note)

    for pitch, obj_name in bass_mapping.items():
        if pitch not in notes_by_pitch:
            continue

        obj = bpy.data.objects.get(obj_name)
        if obj is None:
            print(f"[WARN] Bass object {obj_name!r} not found, skipping.")
            continue

        # one material, slot 0, glow it
        animate_glow(
            obj=obj,
            notes=notes_by_pitch[pitch],
            slot=0,
            on_strength=100.0,   # tweak
            off_strength=0.0,
            pre_frames=2,
            copy_material=True
        )

### TRUMPET LASER helper ###
def map_pitch(p, pmin, pmax, amin, amax):
    # Map pitch p in [pmin, pmax] to value in [amin, amax]
    if pmax == pmin:
        t = 0.5
    else:
        t = (p - pmin) / (pmax - pmin)
        t = max(0.0, min(1.0, t))
    return amin + t * (amax - amin)

### TRUMPET LASER ###
def animate_trumpet_laser(track_list, trumpet_track_idx, trumpet_name, 
                          laser_name, x_on_deg=25.0, z_on_deg=-12.0,
                          pre_frames=1, settle_frames=3):
    """
    - Laser appears on note-on, disappears on note-off (viewport + render)
    - Trumpet + laser rotate on X and Z within bounds, then return to rest after note-off
    """

    notes = sorted(track_list[trumpet_track_idx], key=lambda n: n.start_frame)

    trumpet = bpy.data.objects.get(trumpet_name)
    laser = bpy.data.objects.get(laser_name)
    if trumpet is None or laser is None:
        print(f"[WARN] Missing objects: trumpet={trumpet_name!r} laser={laser_name!r}")
        return

    trumpet.rotation_mode = 'XYZ'
    laser.rotation_mode = 'XYZ'
    rest_tr = trumpet.rotation_euler.copy()
    rest_lr = laser.rotation_euler.copy()

    # start laser hidden
    laser.hide_viewport = True
    laser.hide_render = True
    laser.keyframe_insert("hide_viewport", frame=1)
    laser.keyframe_insert("hide_render", frame=1)

    for note in notes:
        on_f = int(note.start_frame)
        off_f = int(note.end_frame)
        hold_f = max(on_f - pre_frames, 1)
        settle_f = off_f + settle_frames

        # --- Laser visibility ---
        laser.hide_viewport = True
        laser.hide_render = True
        laser.keyframe_insert("hide_viewport", frame=max(hold_f - 1, 1))
        laser.keyframe_insert("hide_render", frame=max(hold_f - 1, 1))

        laser.hide_viewport = False
        laser.hide_render = False
        laser.keyframe_insert("hide_viewport", frame=on_f)
        laser.keyframe_insert("hide_render", frame=on_f)

        laser.hide_viewport = True
        laser.hide_render = True
        laser.keyframe_insert("hide_viewport", frame=off_f)
        laser.keyframe_insert("hide_render", frame=off_f)

        # --- Rotation (fixed pose) ---
        pmin, pmax = 38, 57
        x_deg = map_pitch(note.pitch, pmin, pmax, -50.0, 50.0)
        z_deg = map_pitch(note.pitch, pmin, pmax,  30.0, -30.0) 

        on_tr = rest_tr.copy()
        on_lr = rest_lr.copy()
        on_tr.x = rest_tr.x + radians(x_deg)
        on_tr.z = rest_tr.z + radians(z_deg)
        on_lr.x = rest_lr.x + radians(x_deg)
        on_lr.z = rest_lr.z + radians(z_deg)

        trumpet.rotation_euler = rest_tr
        trumpet.keyframe_insert("rotation_euler", frame=max(hold_f - 1, 1))
        laser.rotation_euler = rest_lr
        laser.keyframe_insert("rotation_euler", frame=max(hold_f - 1, 1))

        trumpet.rotation_euler = on_tr
        trumpet.keyframe_insert("rotation_euler", frame=on_f)
        laser.rotation_euler = on_lr
        laser.keyframe_insert("rotation_euler", frame=on_f)

        trumpet.rotation_euler = rest_tr
        trumpet.keyframe_insert("rotation_euler", frame=settle_f)
        laser.rotation_euler = rest_lr
        laser.keyframe_insert("rotation_euler", frame=settle_f)

    bpy.context.view_layer.update()

### GLOW ANIMATION ###
def animate_glow(obj, notes, slot, on_strength=10.0, off_strength=0.0, pre_frames=4, copy_material=True):
    """
    Keyframe Principled BSDF Emission Strength for one object:
    - off until right before note-on
    - on at note-on
    - off at note-off
    """
    # get material from specified material slot
    if not obj.material_slots or obj.material_slots[slot].material is None:
        print(f"[WARN] {obj.name!r} has no material in slot {slot}, skipping.")
        return
    
    mat = obj.material_slots[slot].material
    # make a copy of the material to avoid affecting other objects
    if copy_material and mat.users > 1:
        mat = mat.copy()
        obj.material_slots[slot].material = mat

    # find Principled BSDF node
    nodes = mat.node_tree.nodes
    bsdf = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf is None:
        print(f"[WARN] {mat.name!r}: no Principled BSDF node found, skipping.")
        return

    # Emission socket name depends on Blender version/material setup
    if "Emission Strength" in bsdf.inputs:
        sock = bsdf.inputs["Emission Strength"]

    notes = sorted(notes, key=lambda n: n.start_frame)

    for note in notes:
        on_frame = note.start_frame
        off_frame = note.end_frame
        hold_f = max(on_frame - pre_frames, 1)

        # Keyframe off at hold frame
        sock.default_value = off_strength
        sock.keyframe_insert(data_path="default_value", frame=max(hold_f - 1, 1))

        # turn on at note on
        sock.default_value = on_strength
        sock.keyframe_insert(data_path="default_value", frame=on_frame+4)

        # turn off at note off
        sock.default_value = off_strength
        sock.keyframe_insert(data_path="default_value", frame=off_frame)


def animate_glow_group(notes, mapping, slot, on_strength=10.0, off_strength=0.0, pre_frames=4, copy_material=True):
    notes_by_pitch = {}
    for note in notes:
        notes_by_pitch.setdefault(note.pitch, []).append(note)

    for pitch, cfg in mapping.items():
        if pitch not in notes_by_pitch:
            continue

        # get object name from mapping
        obj_name = cfg.get("glow")

        obj = bpy.data.objects.get(obj_name)
        if obj is None:
            print(f"[WARN] Object {obj_name!r} not found, skipping.")
            continue

        # animate glow for this object for this note
        animate_glow(
            obj=obj,
            notes=notes_by_pitch[pitch],
            slot=slot,
            on_strength=on_strength,
            off_strength=off_strength,
            pre_frames=pre_frames,
            copy_material=copy_material
        )