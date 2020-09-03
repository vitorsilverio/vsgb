#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

from vsgb.audio.sound_driver import SoundDriver

class LengthCounter:

    DIVIDER = int(SoundDriver.TICKS_PER_SEC / 256)

    def __init__(self, full_length):
        self.full_length = full_length
        self.length = 0
        self.i = 0
        self.enabled = False

    def start(self):
        self.i = 8192

    def step(self, ticks):
        self.i += ticks
        if self.i >= LengthCounter.DIVIDER:
            self.i = 0
            if self.enabled and self.length > 0:
                self.length -= 1

    def set_length(self, length):
        if length == 0:
            self.length = self.full_length
        else:
            self.length = length

    def set_nr4(self, value):
        enable = (value & (1 << 6)) != 0
        trigger = (value & (1 << 7)) != 0

        if self.enabled:
            if self.length == 0 and trigger:
                if enable and self.i < LengthCounter.DIVIDER / 2:
                    self.set_length(self.full_length -1)
                else:
                    self.set_length(self.full_length)
        elif enable:
            if self.length > 0 and self.i < LengthCounter.DIVIDER / 2:
                self.length -= 1
            if self.length == 0 and trigger and self.i < LengthCounter.DIVIDER / 2:
                self.set_length(self.full_length -1)
        else:
            if self.length == 0 and trigger:
                self.set_length(self.full_length)
        self.enabled = enable

    def reset(self):
        self.enabled = True
        self.i = 0
        self.length = 0
