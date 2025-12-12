import bpy
import mido
from parser import parse_midi_file
from math import radians

def animate_hammer(obj, notes, pre_frames=3, swing_deg=25.0, rebound_deg=10.0):
    """
    Animate a hammer object based on note events

    - obj: Blender object representing the specific hammer
    - notes: List of Note objects to animate
    - pre_frames: hammer winds up before the note start
    - hit_offset: offset for the hammer hit frame (subject to change)
    - rebound_offset: offset for the hammer rebound frame (subject to change)
    """
    # assume obj is at rest position
    rest_loc = obj.location.copy()
    rest_rot = obj.rotation_euler.copy()
    axis = 'X'  # assuming hammer swings around X axis THIS MAY CHANGE

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
        if axis == "X":
            down_rot.x += radians(-swing_deg)      # swing down
            up_rot.x += radians(rebound_deg)       # little pre-wind/rebound
            rebound_rot.x += radians(rebound_deg)  # little rebound
        elif axis == "Y":
            down_rot.y += radians(-swing_deg)
            up_rot.y += radians(rebound_deg)
            rebound_rot.y += radians(rebound_deg)
        else:  # "Z"
            down_rot.z += radians(-swing_deg)
            up_rot.z += radians(rebound_deg)
            rebound_rot.z += radians(rebound_deg)

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

def animate_drums(midi_path, drum_track_idx):
    mid = mido.MidiFile(midi_path)
    track_list = parse_midi_file(mid)
    drum_notes = track_list[drum_track_idx]

    # need to map drum pitches to hammer objects in Blender
    # separate pitches for different drums, loop over, call animate_hammer
