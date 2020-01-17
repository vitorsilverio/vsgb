#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

from vsgb.audio.abstract_sound_channel import AbstractSoundChannel
from vsgb.audio.frequency_sweep import FrequencySweep
from vsgb.audio.volume_envelope import VolumeEnvelope
from vsgb.io_registers import IO_Registers

class SoundChannel1(AbstractSoundChannel):

    def __init__(self, cgb_mode):
        super().__init__(IO_Registers.NR_10, 64, cgb_mode)
        self.freq_divider = 0
        self.frequency_sweep = FrequencySweep()
        self.volume_envelope = VolumeEnvelope()

    def start(self):
        self.i = 0
        if self.cgb_mode:
            self.length.reset()
        self.length.start()
        self.frequency_sweep.start()
        self.volume_envelope.start()

    def trigger(self):
        self.i = 0
        self.freq_divider = 1
        self.volume_envelope.trigger()

    def step(self, ticks):
        self.volume_envelope.step(ticks)
        e = self.update_length(ticks) and self.update_sweep(ticks) and self.dac_enabled
        if not e:
            return 0
        self.freq_divider -= 1
        if self.freq_divider == 0:
            self.reset_freq_divider()
            self.last_output = (self.get_duty() & (1 >> self.i)) >> self.i
            self.i = (self.i + ticks) % 8
        return self.last_output * self.volume_envelope.get_volume()

    def set_nr0(self, value):
        super().set_nr0(value)
        self.frequency_sweep.set_nr10(value)

    def set_nr1(self, value):
        super().set_nr1(value)
        self.length.set_length(64 - (value & 0b00111111))

    def set_nr2(self, value):
        super().set_nr2(value)
        self.volume_envelope.set_nr2(value)
        self.dac_enabled = (value & 0b11111000) != 0

    def set_nr3(self, value):
        super().set_nr3(value)
        self.frequency_sweep.set_nr13(value)

    def set_nr4(self, value):
        super().set_nr4(value)
        self.frequency_sweep.set_nr14(value)

    def get_nr3(self):
        return self.frequency_sweep.get_nr13()

    def get_nr4(self):
        return (super().get_nr4() & 0b11111000) | (self.frequency_sweep.get_nr14() & 0b00000111)

    def get_duty(self):
        return {
            0: 0b00000001,
            1: 0b10000001,
            2: 0b10000111,
            3: 0b01111110
        }.get(self.get_nr1() >> 6)

    def reset_freq_divider(self):
        self.freq_divider = self.get_frequency() * 4

    def update_sweep(self, ticks):
        self.frequency_sweep.step(ticks)
        if self.channel_enabled and not self.frequency_sweep.is_enabled():
            self.channel_enabled = False
        return self.channel_enabled
        