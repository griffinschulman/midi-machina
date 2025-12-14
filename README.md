# Midi Machina (Princeton COS426 Computer Graphics Final Project)

**Midi Machina** is a Blender-based music visualizer that takes **MIDI input** and generates an **Animusic-style** animation by programmatically keyframing objects in a stylized scene (Solarpunk aesthetic).

---

## Repository Overview

### Key files
- `main.py`  
  Runs **inside Blender’s Python interpreter** and orchestrates the pipeline:
  1) loads the MIDI, 2) parses it, 3) calls instrument animators, and 4) clears old animation.

- `parser.py`  
  The **main MIDI parsing file**. Uses `mido` to parse note events into per-track lists of `Note` objects, converting MIDI ticks -> seconds -> **frame numbers**.

- `notes.py`  
  Defines the `Note` class used throughout the project (start/end tick, pitch, velocity, plus precomputed seconds and frame indices).

- `blender_anim.py`  
  Contains the **bulk of the animation code** (drum sticks, harp hammers + vibrating strings, organ pistons + glow, bass glow, trumpet lasers, glow helpers).

- `animator_stub.py`  
  Small helper script to sanity-check parsing and print note events (useful outside Blender).

### MIDI / audio assets
- `solarpunkFIN.mid` — MIDI used for the animation
- `solarpunkFIN.mp3` — reference audio

### Vendored dependencies
Because Blender ships with its own Python environment (and `pip` installs don’t always land where Blender can import them), **`mido` and `packaging` are vendored in this repo**:

- `vendor/mido/`
- `vendor/packaging/`

`main.py` adds both the project root and `vendor/` to `sys.path` so Blender can import them.

---

## Requirements

- **Blender** (with scripting workspace enabled)
- Python dependencies (already vendored in `vendor/`):
  - `mido==1.3.3`
  - `packaging==25.0`

> Note: If you remove `vendor/`, you’ll need to install these packages into Blender’s Python site-packages or re-vendor them (see below).

---

## How to Run (Blender UI)

1. Open your **Blender scene** (the Solarpunk .blend that contains the instrument objects).
2. In Blender, go to the **Scripting** workspace.
3. Open `main.py` in the text editor panel.
4. **Edit the path constants at the top of `main.py`:**
   - `PROJECT_ROOT = Path("...")` -> set this to the folder containing this repo on your machine
5. Press **Run Script**.

This will:
- clear existing keyframes for the expected instrument objects
- parse the MIDI into track note-lists
- call animation functions in `blender_anim.py` for drums/harp/organ/bass/trumpet lasers

## Blender Scene (.blend)

The Solarpunk Blender scene is hosted on Google Drive (too large for GitHub):

[Download MMscene.blend (Google Drive)](https://drive.google.com/file/d/1DJscowy0yCSSnnoUrkMaS_OEhJakyYh1/view?usp=sharing)
