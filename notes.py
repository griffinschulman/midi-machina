class Note:
    """Represents a single musical note event for one instrument"""
    def __init__(self, start_tick, end_tick, pitch, velocity, start_sec, end_sec, start_frame, end_frame):
        self.start_tick = start_tick    # start time in ticks
        self.end_tick = end_tick        # end time in ticks
        self.pitch = pitch              # MIDI pitch number (0-127)
        self.velocity = velocity        # note velocity (0-127)
        
        self.start_sec = start_sec      # start time in seconds
        self.end_sec = end_sec          # end time in seconds
        self.start_frame = start_frame  # start time in frames
        self.end_frame = end_frame      # end time in frames
