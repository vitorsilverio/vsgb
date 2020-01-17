#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

from vsgb.audio.abstract_sound_channel import AbstractSoundChannel
from vsgb.audio.lfsr import Lfsr
from vsgb.audio.polynomial_counter import PolynomialCounter
from vsgb.audio.volume_envelope import VolumeEnvelope
from vsgb.io_registers import IO_Registers

class SoundChannel4(AbstractSoundChannel):

    def __init__(self, cgb_mode):
        super().__init__(IO_Registers.NR_41 - 1, 64, cgb_mode)
        self.volume_envelope = VolumeEnvelope()
        self.last_result = 0
        self.polynominal_counter = PolynomialCounter()
        self.lfsr = Lfsr()

    def start(self):
        self.i = 0
        if self.cgb_mode:
            self.length.reset()
        self.length.start()
        self.lfsr.start()
        self.volume_envelope.start()

    def trigger(self):
        self.lfsr.reset()
        self.volume_envelope.trigger()

    def step(self, ticks):
        self.volume_envelope.step(ticks)
        if not self.update_length(ticks):
            return 0
        if not self.dac_enabled:
            return 0
        
        if self.polynominal_counter.step(ticks):
            self.last_result = self.lfsr.next_bit((self._nr3 & (1 << 3)) != 0)

        return self.last_result * self.volume_envelope.get_volume()


    def set_nr1(self, value):
        super().set_nr1(value)
        self.length.set_length(64 - (value & 0b00111111))

    def set_nr2(self, value):
        super().set_nr2(value)
        self.volume_envelope.set_nr2(value)
        self.dac_enabled = (value & 0b11111000) != 0
        self.channel_enabled = self.channel_enabled and self.dac_enabled

    def set_nr3(self, value):
        super().set_nr3(value)
        self.polynominal_counter.set_nr43(value)
