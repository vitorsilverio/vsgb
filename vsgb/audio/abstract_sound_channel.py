#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

from vsgb.audio.length_counter import LengthCounter

class AbstractSoundChannel:

    def __init__(self, offset, length, cgb_mode):
        self.offset = offset
        self.length = LengthCounter(length)
        self.cgb_mode = cgb_mode

        self._nr0 = 0
        self._nr1 = 0
        self._nr2 = 0
        self._nr3 = 0
        self._nr4 = 0

        self.channel_enabled = False
        self.dac_enabled = False

    def accepts(self, address):
        return self.offset <= address < self.offset + 5

    def step(self, ticks):
        pass

    def trigger(self):
        pass

    def is_enabled(self):
        return self.channel_enabled and self.dac_enabled

    def write_byte(self, address, value):
        address = address - self.offset
        if address == 0:
            self.set_nr0(value)
            return
        if address == 1:
            self.set_nr1(value)
            return
        if address == 2:
            self.set_nr2(value)
            return
        if address == 3:
            self.set_nr3(value)
            return
        if address == 4:
            self.set_nr4(value)
            return

    def read_byte(self, address):
        address = address - self.offset
        if address == 0:
            return self.get_nr0()
        if address == 1:
            return self.get_nr1()
        if address == 2:
            return self.get_nr2()
        if address == 3:
            return self.get_nr3()
        if address == 4:
            return self.get_nr4()

    def set_nr0(self, value):
        self._nr0 = value

    def set_nr1(self, value):
        self._nr1 = value

    def set_nr2(self, value):
        self._nr2 = value

    def set_nr3(self, value):
        self._nr3 = value

    def set_nr4(self, value):
        self._nr4 = value
        self.length.set_nr4(value)
        if (value & (1 << 7)) != 0:
            self.channel_enabled = self.dac_enabled
            self.trigger()

    def get_nr0(self):
        return self._nr0

    def get_nr1(self):
        return self._nr1

    def get_nr2(self):
        return self._nr2

    def get_nr3(self):
        return self._nr3

    def get_nr4(self):
        return self._nr4

    def get_frequency(self):
        return 2048 - (self.get_nr3() | ((self.get_nr4() & 0b00000111) << 8))

    def update_length(self, ticks):
        self.length.step(ticks)
        if not self.length.enabled:
            return self.channel_enabled
        if self.channel_enabled and self.length.length == 0:
            self.channel_enabled = False
        return self.channel_enabled


