#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

from vsgb.audio.sound_driver import SoundDriver

class VolumeEnvelope:

    def __init__(self):
        self.i = 0
        self.volume = 0
        self.initial_volume = 0
        self.sweep = 0
        self.envelope_direction = 0
        self.finished = False

    def set_nr2(self, value):
        self.initial_volume = value >> 4
        self.envelope_direction = -1 if (value & 0b00001000 == 0) else 1
        self.sweep = value & 0b00000111

    def is_enabled(self):
        return self.sweep > 0

    def start(self):
        self.finished = True
        self.i = 8192

    def trigger(self):
        self.volume = self.initial_volume
        self.i = 0
        self.finished = False

    def step(self, ticks):
        if self.finished:
            return

        if (self.volume == 0 and self.envelope_direction == -1 ) or (self.volume == 15 and self.envelope_direction == 1):
            self.finished = True
            return
        self.i += ticks
        if self.i >= self.sweep * SoundDriver.TICKS_PER_SEC / 64:
            self.i = 0
            self.volume += self.envelope_direction

    def get_volume(self):
        if self.is_enabled():
            return self.volume
        else:
            return self.initial_volume
