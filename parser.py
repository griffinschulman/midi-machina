# import mido
import mido

# reference: https://youtu.be/MUFNS5sNICI?si=CoaxxkgSqs1W5Z5j
# load a MIDI file
mid = mido.MidiFile('solarpunkex.mid')
print("Loaded MIDI file:", mid)

# print the tracks in the MIDI file
print("Tracks in the MIDI file:")
for i, track in enumerate(mid.tracks):
    print(f"Track {i}: {track.name}")
    for message in track:
        print(message)