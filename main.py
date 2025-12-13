import sys
from pathlib import Path

# Point Python to your project folder
PROJECT_ROOT = Path("/Users/griffinschulman/Desktop/Princeton Courses/COS426/MIDI-MACHINA/midi-machina")  # <-- change this
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import blender_anim

MIDI_PATH = "/Users/griffinschulman/Desktop/Princeton Courses/COS426/MIDI-MACHINA/midi-machina/solarpunkex.mid"

# Example: assume track 1 is drums,
# and your hammer object names in Blender are "Hammer_Kick" and "Hammer_Snare"
pitch_to_obj = {
    36: "Hammer_Kick",   # C1 (GM: Bass Drum 1)
    40: "Hammer_Snare",  # E1 (Snare)
}

blender_anim.animate_drums_from_midi(
    midi_path=MIDI_PATH,
    drum_track_idx=1      # track 1 if 0 is meta
)
