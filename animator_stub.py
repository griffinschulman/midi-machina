from parser import parse_midi_file
import mido

def animate_stub(midi_path):
    mid = mido.MidiFile(midi_path)
    track_list = parse_midi_file(mid)

    print(f"Total tracks (including meta): {len(track_list)}")

    # Skip track 0 (meta) and just inspect the musical tracks
    for i, track_notes in enumerate(track_list[1:], start=1):
        print(f"\nTrack {i}: {len(track_notes)} notes")
        for note in track_notes[:60]:
            print(
                f"  Pitch={note.pitch}, "
                f"start_frame={note.start_frame}, end_frame={note.end_frame}"
            )

if __name__ == "__main__":
    animate_stub("solarpunkex2.mid")