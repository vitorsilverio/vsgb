#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

from vsgb.audio.sound_driver import SoundDriver

class FrequencySweep:

    DIVIDER = int(SoundDriver.TICKS_PER_SEC / 128)

    def __init__(self):
        self.period = 0
        self.negate = False
        self.shift = 0
        self.timer = 0
        self.shadow_freq = 0
        self._nr13 = 0
        self._nr14 = 0
        self.i = 0
        self.overflow = False
        self.counter_enabled = False
        self.negging = False

    def start(self):
        self.counter_enabled = False
        self.i = 8192

    def trigger(self):
        self.negging = False
        self.overflow = False

        self.shadow_freq = self._nr13 | ((self._nr14 & 0b00000111) << 8)
        self.timer = 8 if self.period == 0 else self.period
        self.counter_enabled = self.period != 0 or self.shift != 0

        if self.shift > 0:
            self.calculate()

    def set_nr10(self, value):
        self.period = (value >> 4) & 0b00000111
        self.negate = (value & (1 << 3)) != 0
        self.shift = value & 0b111
        if self.negging and not self.negate:
            self.overflow = True

    def set_nr13(self, value):
        self._nr13 = value

    def set_nr14(self, value):
        self._nr14 = value
        if (value & (1 << 7)) != 0:
            self.trigger()

    def get_nr13(self):
        return self._nr13

    def get_nr14(self):
        return self._nr14
    
    def step(self, ticks):
        self.i += ticks
        if self.i >= FrequencySweep.DIVIDER:
            self.i = 0
            if not self.counter_enabled:
                return
            self.timer -= 1
            if self.timer == 0:
                self.timer = 8 if self.period == 0 else self.period
                if self.period != 0:
                    new_freq = self.calculate()
                    if not self.overflow and self.shift != 0:
                        self.shadow_freq = new_freq
                        self._nr13 = self.shadow_freq & 0xff
                        self._nr14 = (self.shadow_freq & 0x700) >> 8
                        self.calculate()

    def calculate(self):
        freq = self.shadow_freq >> self.shift
        if self.negate:
            freq = self.shadow_freq - freq
            self.negging = True
        else:
            freq = self.shadow_freq + freq
        if freq > 2047:
            self.overflow = True
        return freq
    
    def is_enabled(self):
        return not self.overflow
        