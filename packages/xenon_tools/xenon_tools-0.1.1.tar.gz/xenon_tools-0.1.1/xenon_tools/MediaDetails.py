#! /usr/bin/env python
from utils import human_time


class MediaDetails:
    duration_seconds = 0
    duration_human = ''
    frame_rate = 0
    no_channels = 0
    frame_width = 0

    def __init__(self, duration_seconds=0, frame_rate=0, no_channels=0, frame_width=0):
        self.duration_seconds = duration_seconds
        self.duration_human = human_time(duration_seconds)
        self.frame_width = frame_width
        self.frame_rate = frame_rate
        self.no_channels = no_channels
