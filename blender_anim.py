import bpy
from math import radians

### HARP HAMMERS ###
def animate_hammer_harp(obj, notes, swing_deg, rebound_deg, axis):
    """
    Animate a hammer object based on note events

    - obj: Blender object representing the specific hammer
    - notes: List of Note objects to animate
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
        hold_frame = hit_frame - 24 #  
        pre_frame = hit_frame - 4 # 
        rebound_frame = hit_frame + 8 # 
        settle_frame = hit_frame + 16 # 

        # copies of the rest rotation for each phase
        up_rot = rest_rot.copy()
        down_rot = rest_rot.copy()
        rebound_rot = rest_rot.copy()

        # apply swing angles by axis
        if axis == 'X':
            up_rot.x += radians(rebound_deg)
            down_rot.x += radians(-swing_deg)
            rebound_rot.x += radians(rebound_deg+5)
        elif axis == 'Y':
            up_rot.y += radians(rebound_deg)
            down_rot.y += radians(-swing_deg)
            rebound_rot.y += radians(rebound_deg+5)
        elif axis == 'Z':
            up_rot.z += radians(rebound_deg)
            down_rot.z += radians(-swing_deg)
            rebound_rot.z = radians(rebound_deg+5)
        else:
            return

        # gold at rest until just before windup
        obj.rotation_euler = rest_rot
        obj.keyframe_insert("rotation_euler", frame=hold_frame)

        # pre-wind
        obj.rotation_euler = up_rot
        obj.keyframe_insert("rotation_euler", frame=pre_frame)

        # hit
        obj.rotation_euler = down_rot
        obj.keyframe_insert("rotation_euler", frame=hit_frame)

        # rebound
        obj.rotation_euler = rebound_rot
        obj.keyframe_insert("rotation_euler", frame=rebound_frame)

        # settle
        obj.rotation_euler = rest_rot
        obj.keyframe_insert("rotation_euler", frame=settle_frame)

### STRING VIBRATION ###
def animate_string_vibrate_2keys(obj, notes, key_up=1, key_down=2,
                                 amp=0.8, cycles=4, step=2):
    """
    Alternates two shape keys (one bends up, one bends down) with decay.
    - key_up driven on even ticks
    - key_down driven on odd ticks
    """
    mesh = obj.data
    sk = mesh.shape_keys
    kb = sk.key_blocks

    up = kb[key_up]
    down = kb[key_down]

    notes = sorted(notes, key=lambda n: n.start_frame)

    for note in notes:
        hit_frame = int(note.start_frame)

        # ensure both start at rest right before hit
        up.value = 0.0
        down.value = 0.0
        up.keyframe_insert("value", frame=hit_frame - 1)
        down.keyframe_insert("value", frame=hit_frame - 1)

        # alternating pulses: up, down, up, down...
        total_ticks = cycles * 2
        for i in range(total_ticks):
            f = hit_frame + i * step
            # decay from 1.0 to 0.0 over total_ticks
            decay = 1.0 - (i / max(1, total_ticks)) # avoid div by zero
            a = amp * decay

            if i % 2 == 0:
                up.value = a
                down.value = 0.0
            else:
                up.value = 0.0
                down.value = a

            up.keyframe_insert("value", frame=f)
            down.keyframe_insert("value", frame=f)

        # settle back to rest
        end_f = hit_frame + total_ticks * step + step
        up.value = 0.0
        down.value = 0.0
        up.keyframe_insert("value", frame=end_f)
        down.keyframe_insert("value", frame=end_f)

### HARP ###
def animate_harp(track_list, track_id):
    """
    Animate harp hammers based on note events
    """
    harp_notes = track_list[track_id]

    # map harp pitches to harp string objects in Blender (3 octaves from C3 to B5)
    harp_mapping = {
        60: {"hammer": "Hammer.001", "string": "String.001"}, # C3
        61: {"hammer": "Hammer.002", "string": "String.002"}, # C#3
        62: {"hammer": "Hammer.003", "string": "String.003"}, # D3
        63: {"hammer": "Hammer.004", "string": "String.004"}, # D#3
        64: {"hammer": "Hammer.005", "string": "String.005"}, # E3
        65: {"hammer": "Hammer.006", "string": "String.006"}, # F3
        66: {"hammer": "Hammer.007", "string": "String.007"}, # F#3
        67: {"hammer": "Hammer.008", "string": "String.008"}, # G3
        68: {"hammer": "Hammer.009", "string": "String.009"}, # G#3
        69: {"hammer": "Hammer.010", "string": "String.010"}, # A3
        70: {"hammer": "Hammer.011", "string": "String.011"}, # A#3
        71: {"hammer": "Hammer.012", "string": "String.012"}, # B3
        72: {"hammer": "Hammer.013", "string": "String.013"}, # C4
        73: {"hammer": "Hammer.014", "string": "String.014"}, # C#4
        74: {"hammer": "Hammer.015", "string": "String.015"}, # D4
        75: {"hammer": "Hammer.016", "string": "String.016"}, # D#4
        76: {"hammer": "Hammer.017", "string": "String.017"}, # E4
        77: {"hammer": "Hammer.018", "string": "String.018"}, # F4
        78: {"hammer": "Hammer.019", "string": "String.019"}, # F#4
        79: {"hammer": "Hammer.020", "string": "String.020"}, # G4
        80: {"hammer": "Hammer.021", "string": "String.021"}, # G#4
        81: {"hammer": "Hammer.022", "string": "String.022"}, # A4
        82: {"hammer": "Hammer.023", "string": "String.023"}, # A#4
        83: {"hammer": "Hammer.024", "string": "String.024"}, # B4
        84: {"hammer": "Hammer.025", "string": "String.025"}, # C5
        85: {"hammer": "Hammer.026", "string": "String.026"}, # C#5
        86: {"hammer": "Hammer.027", "string": "String.027"}, # D5
        87: {"hammer": "Hammer.028", "string": "String.028"}, # D#5
        88: {"hammer": "Hammer.029", "string": "String.029"}, # E5
        89: {"hammer": "Hammer.030", "string": "String.030"}, # F5
        90: {"hammer": "Hammer.031", "string": "String.031"}, # F#5
        91: {"hammer": "Hammer.032", "string": "String.032"}, # G5
        92: {"hammer": "Hammer.033", "string": "String.033"}, # G#5
        93: {"hammer": "Hammer.034", "string": "String.034"}, # A5
        94: {"hammer": "Hammer.035", "string": "String.035"}, # A#5
        95: {"hammer": "Hammer.036", "string": "String.036"}  # B5
    }

    # parameters for harp hammer animation
    harp_params = {
        "swing_deg": -7.0,    # degrees the hammer swings down on hit
        "rebound_deg": -15.0, # degrees the hammer rebounds after hit
        "axis": "X",          # rotation axis
    }

    notes_by_pitch = {}
    for note in harp_notes:
        notes_by_pitch.setdefault(note.pitch, []).append(note)

    # for each pitch that we know how to animate, apply animations
    for pitch, cfg in harp_mapping.items():
        if pitch not in notes_by_pitch:
            continue # skip unmapped pitches

        # skip if obj not found in blender scene
        hammer_name = cfg["hammer"]
        if cfg["hammer"] not in bpy.data.objects:
            print(f"[WARN] Object {hammer_name!r} not found in Blender scene, skipping.")
            continue
        string_name = cfg["string"]
        if cfg["hammer"] not in bpy.data.objects:
            print(f"[WARN] Object {string_name!r} not found in Blender scene, skipping.")
            continue

        # animate hammer
        hammer_obj = bpy.data.objects[hammer_name]
        animate_hammer_harp(
            obj=hammer_obj,
            notes=notes_by_pitch[pitch],
            **harp_params
        )
        
        # animate string
        string_obj = bpy.data.objects[string_name]
        animate_string_vibrate_2keys(
            obj=string_obj,
            notes=notes_by_pitch[pitch],
            key_up="Key 1",
            key_down="Key 2",
            amp=0.7,
            cycles=4,
            step=2
        )

### DRUM HAMMERS ###
def animate_drum_hammer(obj, notes, swing_deg, rebound_deg, axis):
    """
    Animate a hammer object based on note events (FOR DRUMS ONLY NOW)

    - obj: Blender object representing the specific hammer
    - notes: List of Note objects to animate
    - swing_deg: degrees the hammer swings down on hit
    - rebound_deg: degrees the hammer rebounds after hit
    """
    # assume obj is at rest position, rotate around Y axis
    rest_rot = obj.rotation_euler.copy()

    notes = sorted(notes, key=lambda n: n.start_frame)

    # iterate over notes to create keyframes
    for note in notes:
        hit_frame = note.start_frame
        hold_frame = hit_frame - 16 #
        pre_frame = hit_frame - 4 #
        rebound_frame = hit_frame + 6 # 
        settle_frame = hit_frame + 10 # 

        # copies of the rest rotation for each phase
        up_rot = rest_rot.copy()
        down_rot = rest_rot.copy()
        rebound_rot = rest_rot.copy()

        # apply swing angles by axis
        if axis == 'X':
            up_rot.x += radians(rebound_deg)
            down_rot.x += radians(-swing_deg) 
            rebound_rot.x += radians(rebound_deg) 
        elif axis == 'Y':
            up_rot.y += radians(rebound_deg)
            down_rot.y += radians(-swing_deg)
            rebound_rot.y += radians(rebound_deg)
        elif axis == "Z":
            up_rot.z += radians(rebound_deg)
            down_rot.z += radians(-swing_deg)
            rebound_rot.z += radians(rebound_deg)
        else: 
            return
  
        # hold at rest until just before windup
        obj.rotation_euler = rest_rot
        obj.keyframe_insert("rotation_euler", frame=hold_frame)
        
        # pre-wind
        obj.rotation_euler = up_rot
        obj.keyframe_insert("rotation_euler", frame=pre_frame)

        # hit
        obj.rotation_euler = down_rot
        obj.keyframe_insert("rotation_euler", frame=hit_frame)

        # rebound
        obj.rotation_euler = rebound_rot
        obj.keyframe_insert("rotation_euler", frame=rebound_frame)

        # settle
        obj.rotation_euler = rest_rot
        obj.keyframe_insert("rotation_euler", frame=settle_frame)

### DRUM BODIES ###
def animate_drum_body(obj, notes, hit_dist, rebound_dist, axis):
    """
    Animate a drum object based on note events

    - obj: Blender object representing the specific drum
    - notes: List of Note objects to animate
    - hit_dist: distance to move on impact
    - rebound_dist: distance to bounce back 
    """
    # assume obj is at rest position, rotate around Y axis
    rest_loc = obj.location.copy()

    notes = sorted(notes, key=lambda n: n.start_frame)

    # iterate over notes to create keyframes
    for note in notes:
        hit_frame = note.start_frame
        down_frame = hit_frame + 2 #
        rebound_frame = hit_frame + 4 # 
        settle_frame = hit_frame + 6 # 

        # copies of the rest rotation for each phase
        down_loc = rest_loc.copy()
        rebound_loc = rest_loc.copy()

        # apply swing angles by axis
        if axis == 'X':
            down_loc.x -= hit_dist
            rebound_loc.x += rebound_dist
        elif axis == 'Y':
            down_loc.y -= hit_dist
            rebound_loc.y += rebound_dist
        elif axis == 'Z':
            down_loc.z -= hit_dist
            rebound_loc.z += rebound_dist
        else: 
            return
  
        # hold at rest until just before hit
        obj.location = rest_loc
        obj.keyframe_insert("location", frame=hit_frame)

        # hit
        obj.location = down_loc
        obj.keyframe_insert("location", frame=down_frame)

        # rebound
        obj.location = rebound_loc
        obj.keyframe_insert("location", frame=rebound_frame)

        # settle
        obj.location = rest_loc
        obj.keyframe_insert("location", frame=settle_frame)

### DRUMS ###
def animate_drums(track_list, track_id):
    """
    Animate drum hammers based on note events
    """
    drum_notes = track_list[track_id]

    # map drum pitches to drum objects in Blender
    drum_mapping = {
        36: {"hammer": "Kick_Stick", "swing_deg": 14.0, "rebound_deg": 10.0,
                "drum": "Kick", "hit_dist": 0.01, "rebound_dist": 0.005},

        40: {"hammer": "Snare_Stick", "swing_deg": -12.0, "rebound_deg": -10.0,
                "drum": "Snare", "hit_dist": 0.01, "rebound_dist": 0.005},

        42: {"hammer": "HiHat_Stick", "swing_deg": -15.0, "rebound_deg": -11.0,
                "drum": "HiHat", "hit_dist": 0.01, "rebound_dist": 0.005},

        43: {"hammer": "TomLo_Stick", "swing_deg": 18.0, "rebound_deg": 14.0,
                "drum": "TomLo", "hit_dist": 0.01, "rebound_dist": 0.005},

        45: {"hammer": "TomHi_Stick", "swing_deg": 18.0, "rebound_deg": 10.0,
                "drum": "TomHi", "hit_dist": 0.01, "rebound_dist": 0.005},

        49: {"hammer": "Crash_Stick", "swing_deg": -17.0, "rebound_deg": -14.0,
                "drum": "Crash", "hit_dist": 0.01, "rebound_dist": 0.005}
    }

    notes_by_pitch = {}
    for note in drum_notes:
        notes_by_pitch.setdefault(note.pitch, []).append(note)

    # for each pitch that we know how to animate, apply animations
    for pitch, cfg in drum_mapping.items():
        if pitch not in notes_by_pitch:
            continue # skip unmapped pitches

        # skip if obj not found in blender scene
        hammer_name = cfg["hammer"]
        if hammer_name not in bpy.data.objects:
            print(f"[WARN] Object {hammer_name!r} not found in Blender scene, skipping.")
            continue
        drum_name = cfg["drum"]
        if drum_name not in bpy.data.objects:
            print(f"[WARN] Object {drum_name!r} not found in Blender scene, skipping.")
            continue

        # animate hammer
        hammer_obj = bpy.data.objects[hammer_name]
        animate_drum_hammer(
            obj=hammer_obj,
            notes=notes_by_pitch[pitch],
            swing_deg=cfg["swing_deg"],
            rebound_deg=cfg["rebound_deg"],
            axis="X"
        )
        
        # animate drum
        drum_obj = bpy.data.objects[drum_name]
        animate_drum_body(
            obj=drum_obj,
            notes=notes_by_pitch[pitch],
            hit_dist=cfg["hit_dist"],
            rebound_dist=cfg["rebound_dist"],
            axis="Z"
        )


### ORGAN PISTONS ###
def animate_piston(obj, notes, dist):
    notes = sorted(notes, key=lambda n: n.start_frame)
    for note in notes:
        on_frame = note.start_frame
        hold_frame = on_frame - 6
        off_frame = note.end_frame
        settle_frame = note.end_frame + 6

        # reference z position
        z_rest = obj.location.z
        z_up = z_rest + dist

        # move to rest position
        obj.location.z = z_rest
        obj.keyframe_insert("location", frame=hold_frame)

        # move up and stay up on note
        obj.location.z = z_up
        obj.keyframe_insert("location", frame=on_frame)
        obj.keyframe_insert("location", frame=off_frame)

        # move back to rest position
        obj.location.z = z_rest
        obj.keyframe_insert("location", frame=settle_frame)

### ORGAN ###
def animate_organ(track_list, track_id):
    """
    organ animation based on note events
    """
    organ_notes = track_list[track_id]
    
    organ_mapping = {
        # map organ pitches to Blender objects
        57: {"piston": "Piston.001", "glow": "Filament.001"}, # A3
        58: {"piston": "Piston.002", "glow": "Filament.002"}, # A#3
        59: {"piston": "Piston.003", "glow": "Filament.003"}, # B3
        60: {"piston": "Piston.004", "glow": "Filament.004"}, # C4
        61: {"piston": "Piston.005", "glow": "Filament.005"}, # C#4

        62: {"piston": "Piston.006", "glow": "Filament.006"}, # D4
        63: {"piston": "Piston.007", "glow": "Filament.007"}, # D#4
        64: {"piston": "Piston.008", "glow": "Filament.008"}, # E4
        65: {"piston": "Piston.009", "glow": "Filament.009"}, # F4
        66: {"piston": "Piston.010", "glow": "Filament.010"}, # F#4
        67: {"piston": "Piston.011", "glow": "Filament.011"}, # G4

        68: {"piston": "Piston.012", "glow": "Filament.012"}, # G#4
        69: {"piston": "Piston.013", "glow": "Filament.013"}, # A4
        70: {"piston": "Piston.014", "glow": "Filament.014"}, # A#4
        71: {"piston": "Piston.015", "glow": "Filament.015"}, # B4
        72: {"piston": "Piston.016", "glow": "Filament.016"}, # C5
        73: {"piston": "Piston.017", "glow": "Filament.017"}, # C#5
        74: {"piston": "Piston.018", "glow": "Filament.018"}, # D5

        75: {"piston": "Piston.019", "glow": "Filament.019"}, # D#5
        76: {"piston": "Piston.020", "glow": "Filament.020"}, # E5
        77: {"piston": "Piston.021", "glow": "Filament.021"}, # F5
        78: {"piston": "Piston.022", "glow": "Filament.022"}, # F#5
        79: {"piston": "Piston.023", "glow": "Filament.023"}, # G5
        80: {"piston": "Piston.024", "glow": "Filament.024"}, # G#5

        81: {"piston": "Piston.025", "glow": "Filament.025"}, # A5
        82: {"piston": "Piston.026", "glow": "Filament.026"}, # A#5
        83: {"piston": "Piston.027", "glow": "Filament.027"}, # B5
        84: {"piston": "Piston.028", "glow": "Filament.028"}, # C6
        85: {"piston": "Piston.029", "glow": "Filament.029"}, # C#6
    }

    # bucket notes by pitch once
    notes_by_pitch = {}
    for note in organ_notes:
        notes_by_pitch.setdefault(note.pitch, []).append(note)

    # piston motion
    for pitch, cfg in organ_mapping.items():
        if pitch not in notes_by_pitch:
            continue
        
        # skip if obj not found in blender scene
        piston_name = cfg["piston"]
        if piston_name not in bpy.data.objects:
            print(f"[WARN] Object {piston_name!r} not found in Blender scene, skipping.")
            continue
        glow_name = cfg["glow"]
        if glow_name not in bpy.data.objects:
            print(f"[WARN] Object {glow_name!r} not found in Blender scene, skipping.")
            continue

        # piston motion
        piston_obj = bpy.data.objects[piston_name]
        animate_piston(
            obj=piston_obj,
            notes=notes_by_pitch[pitch],
            dist=0.23
        )

        # filament glow
        glow_obj = bpy.data.objects[glow_name]
        animate_glow(
            obj=glow_obj,
            notes=notes_by_pitch[pitch],
            slot=0,
            on_strength=100.0,
            off_strength=1.0,
        )

### BASS ###
def animate_bass(track_list, track_id):
    """
    bass animation based on note events, BELOW ORGAN
    """
    # Implementation would go here
    bass_notes = track_list[track_id]

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

        animate_glow(
            obj=obj,
            notes=notes_by_pitch[pitch],
            slot=0,
            on_strength=100.0,
            off_strength=1.0,
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
def animate_trumpet_laser(track_list, track_id, obj_num):
    """
    - Laser appears on note-on, disappears on note-off (viewport + render)
    - Trumpet + laser rotate on X and Z within bounds, then return to rest after note-off
    """

    # define object names
    trumpet_names = [
        "Gyro_X" + obj_num,
        "Gyro_Z" + obj_num,
        "Beam" + obj_num   
    ]

    # get objs, skip if obj not found in blender scene
    trumpet_objects = []
    for name in trumpet_names:
        obj = bpy.data.objects.get(name)
        if obj is None:
            print(f"[WARN] Missing objects: trumpet={trumpet_name!r} laser={laser_name!r}")
            return
        else: trumpet_objects.append(obj)

    GX = trumpet_objects[0]
    GZ = trumpet_objects[1]
    L = trumpet_objects[2]

    notes = sorted(track_list[track_id], key=lambda n: n.start_frame)

    # start laser hidden
    L.hide_viewport = True
    L.hide_render = True
    L.keyframe_insert("hide_viewport", frame=1)
    L.keyframe_insert("hide_render", frame=1)

    # reference rotations
    rest_GX = GX.rotation_euler.copy()
    rest_GZ = GZ.rotation_euler.copy()

    for i in range(len(notes)):
        # relevant frames of note before and after
        prev_end_frame = None
        next_start_frame = None
        if (i-1 >= 0):
            prev_end_frame = notes[i-1].end_frame
        if (i+1 < len(notes)):
            next_start_frame = notes[i+1].start_frame

        # relevant frames of this note
        on_frame = notes[i].start_frame
        hold_frame = on_frame - 3
        off_frame = notes[i].end_frame
        settle_frame = off_frame + 3
        threshhold = 7 # min number of frames between notes for rotation


        # --- Laser visibility ---
        L.hide_viewport = True
        L.hide_render = True
        L.keyframe_insert("hide_viewport", frame=on_frame)
        L.keyframe_insert("hide_render", frame=on_frame)

        L.hide_viewport = False
        L.hide_render = False
        L.keyframe_insert("hide_viewport", frame=on_frame+1)
        L.keyframe_insert("hide_render", frame=on_frame+1)
        L.keyframe_insert("hide_viewport", frame=off_frame-1)
        L.keyframe_insert("hide_render", frame=off_frame-1)

        L.hide_viewport = True
        L.hide_render = True
        L.keyframe_insert("hide_viewport", frame=off_frame)
        L.keyframe_insert("hide_render", frame=off_frame)
        
        # --- Rotation (fixed pose) ---
        pmin, pmax = 38, 57
        x_deg = map_pitch(notes[i].pitch, pmin, pmax, -30.0, 30.0)
        z_deg = map_pitch(notes[i].pitch, pmin, pmax, -50.0, 50.0) 

        # GX
        on_GX = rest_GX.copy()
        on_GX.x = rest_GX.x + radians(x_deg)
        # GZ
        on_GZ = rest_GZ.copy()
        on_GZ.z = rest_GZ.z + radians(z_deg)

        # hold until just before rotation
        if (prev_end_frame is None):
            GX.rotation_euler = rest_GX
            GX.keyframe_insert("rotation_euler", frame=hold_frame)
            GZ.rotation_euler = rest_GZ
            GZ.keyframe_insert("rotation_euler", frame=hold_frame)
        elif (on_frame - prev_end_frame > threshhold):
            GX.rotation_euler = rest_GX
            GX.keyframe_insert("rotation_euler", frame=hold_frame)
            GZ.rotation_euler = rest_GZ
            GZ.keyframe_insert("rotation_euler", frame=hold_frame)

        # rotate and stay rotated
        GX.rotation_euler = on_GX
        GX.keyframe_insert("rotation_euler", frame=on_frame)
        GX.keyframe_insert("rotation_euler", frame=off_frame)
        GZ.rotation_euler = on_GZ
        GZ.keyframe_insert("rotation_euler", frame=on_frame)
        GX.keyframe_insert("rotation_euler", frame=off_frame)

        # return to rest rotation
        if (next_start_frame is None):
            GX.rotation_euler = rest_GX
            GX.keyframe_insert("rotation_euler", frame=settle_frame)
            GZ.rotation_euler = rest_GZ
            GZ.keyframe_insert("rotation_euler", frame=settle_frame)
        elif (next_start_frame - off_frame > threshhold):
            GX.rotation_euler = rest_GX
            GX.keyframe_insert("rotation_euler", frame=settle_frame)
            GZ.rotation_euler = rest_GZ
            GZ.keyframe_insert("rotation_euler", frame=settle_frame)
        
    bpy.context.view_layer.update()

### GLOW ANIMATION ###
def animate_glow(obj, notes, slot, on_strength, off_strength):
    # get material from specified material slot
    if not obj.material_slots or obj.material_slots[slot].material is None:
        print(f"[WARN] {obj.name!r} has no material in slot {slot}, skipping.")
        return

    # find Principled BSDF node
    node_tree = obj.material_slots[slot].material.node_tree
    bsdf = next((n for n in node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf is None:
        print(f"[WARN] {mat.name!r}: no Principled BSDF node found, skipping.")
        return

    # emission socket name depends on blender version/material setup
    if "Emission Strength" in bsdf.inputs:
        socket = bsdf.inputs["Emission Strength"]

    notes = sorted(notes, key=lambda n: n.start_frame)

    for note in notes:
        on_frame = note.start_frame
        hold_frame = on_frame - 6
        off_frame = note.end_frame
        settle_frame = note.end_frame + 6

        # keyframe off at hold frame
        socket.default_value = off_strength
        socket.keyframe_insert("default_value", frame=hold_frame)

        # turn on and stay on
        socket.default_value = on_strength
        socket.keyframe_insert("default_value", frame=on_frame)
        socket.keyframe_insert("default_value", frame=off_frame)

        # turn off at settle frame
        socket.default_value = off_strength
        socket.keyframe_insert("default_value", frame=settle_frame)