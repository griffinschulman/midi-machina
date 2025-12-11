class Note:
    """Represents a single musical note event for one instrument"""
    def __init__(self, start_tick, end_tick, pitch, velocity, start_sec, end_sec, start_frame, end_frame):
        self.start_tick = start_tick
        self.end_tick = end_tick
        self.pitch = pitch
        self.velocity = velocity
        
        self.start_sec = start_sec
        self.end_sec = end_sec
        self.start_frame = start_frame
        self.end_frame = end_frame