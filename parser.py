# import mido
import mido
from notes import Note

# reference: https://youtu.be/MUFNS5sNICI?si=CoaxxkgSqs1W5Z5j
# load a MIDI file
# mid = mido.MidiFile('test.mid')
# print("Loaded MIDI file:", mid)

# print the tracks in the MIDI file
# print("Tracks in the MIDI file:")
# for i, track in enumerate(mid.tracks):
#     print(f"Track {i}: {track.name}")
#     for message in track:
#         print(message)

def get_tempo(mid):
    """Extract tempo from the MIDI file. Defaults to 500000 μs/beat if not found"""
    tempo = None
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                return msg.tempo  # Tempo in microseconds per beat
    return 500000  # Default tempo (120 bpm) if no tempo message is found

def ticks_to_frames(ticks, ticks_per_beat, tempo, fps=24):
    """Convert ticks to frames based on tempo and sample rate"""
    seconds = mido.tick2second(ticks, ticks_per_beat, tempo)
    frames = int(round(seconds * fps))
    return frames

# found reference on Carnegie Mellon ? (http://course.ece.cmu.edu/~ece500/projects/f24-teamc5/wp-content/uploads/sites/332/2024/11/current-python-midi-parsing-code.pdf)
def parse_track(track, ticks_per_beat, tempo):
    """Parse a MIDI track and extract note events"""
    notes = []
    # Keep track of the current time in ticks (no abolute time in mido)
    current_time = 0
    note_on_events = {}

    for msg in track:
        # Update current time in ticks
        current_time += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            note_on_events[msg.note] = (current_time, msg.velocity)
        elif (msg.type == 'note_off') or (msg.type == 'note_on' and msg.velocity == 0):
            if msg.note in note_on_events:
                start_time, velocity = note_on_events[msg.note]
                end_time = current_time
                note_obj = Note(
                    start_tick=start_time,
                    end_tick=end_time,
                    pitch=msg.note,
                    velocity=velocity,
                    start_sec=mido.tick2second(start_time, ticks_per_beat, tempo),
                    end_sec=mido.tick2second(end_time, ticks_per_beat, tempo),
                    start_frame=ticks_to_frames(start_time, ticks_per_beat, tempo),
                    end_frame=ticks_to_frames(end_time, ticks_per_beat, tempo)
                )
                notes.append(note_obj)
                del note_on_events[msg.note]

    return notes

def parse_midi_file(mid):
    """Parse the entire MIDI file and extract notes from all tracks"""
    all_notes = []
    ticks_per_beat = mid.ticks_per_beat 
    tempo = get_tempo(mid) # get tempo from the MIDI file

    for track in mid.tracks:
        track_notes = parse_track(track, ticks_per_beat, tempo)
        all_notes.extend(track_notes)

    return all_notes

# parse midi file and print notes
def main():
    mid = mido.MidiFile("test.mid")
    notes = parse_midi_file(mid)
    print(f"Total notes parsed: {len(notes)}")
    print("First 5 notes:")
    for note in notes[:5]:
        print(f"Pitch: {note.pitch}, Start Tick: {note.start_tick}, End Tick: {note.end_tick}, "
              f"Velocity: {note.velocity}, Start Sec: {note.start_sec:.2f}, End Sec: {note.end_sec:.2f}, "
              f"Start Frame: {note.start_frame}, End Frame: {note.end_frame}")


if __name__ == "__main__":
    main()