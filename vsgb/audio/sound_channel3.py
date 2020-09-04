#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

from vsgb.audio.abstract_sound_channel import AbstractSoundChannel
from vsgb.io_registers import IO_Registers

class SoundChannel3(AbstractSoundChannel):


    def __init__(self, cgb_mode):
        super().__init__(IO_Registers.NR_31 - 1, 256, cgb_mode)
        self.freq_divider = 0
        if cgb_mode:
            self.wave_ram = [
                0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff,
                0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff
            ]
        else:
            self.wave_ram = [
                0x84, 0x40, 0x43, 0xaa, 0x2d, 0x78, 0x92, 0x3c,
                0x60, 0x59, 0x59, 0xb0, 0x34, 0xb8, 0x2e, 0xda
            ]
        self.last_output = 0
        self.ticks_since_read = 65536
        self.last_read_addr = 0
        self.buffer = 0
        self.triggered = False

    def accepts(self, address):
        return super().accepts(address) or IO_Registers.WAVE_PATTERN_0 <= address <= IO_Registers.WAVE_PATTERN_F

    def read_byte(self, address):
        if IO_Registers.WAVE_PATTERN_0 <= address <= IO_Registers.WAVE_PATTERN_F:
            if not self.is_enabled():
                return self.wave_ram[address - IO_Registers.WAVE_PATTERN_0]
            if IO_Registers.WAVE_PATTERN_0 <= self.last_read_addr <= IO_Registers.WAVE_PATTERN_F and (self.cgb_mode or self.ticks_since_read < 2):
                return self.wave_ram[self.last_read_addr - IO_Registers.WAVE_PATTERN_0]
        return super().read_byte(address)

    def write_byte(self, address, value):
        if IO_Registers.WAVE_PATTERN_0 <= address <= IO_Registers.WAVE_PATTERN_F:
            if not self.is_enabled():
                self.wave_ram[address - IO_Registers.WAVE_PATTERN_0] = value
                return
            if IO_Registers.WAVE_PATTERN_0 <= self.last_read_addr <= IO_Registers.WAVE_PATTERN_F and (self.cgb_mode or self.ticks_since_read < 2):
                self.wave_ram[self.last_read_addr - IO_Registers.WAVE_PATTERN_0] = value
                return
        super().write_byte(address, value)

    def start(self):
        self.i = 0
        self.buffer = 0
        if self.cgb_mode:
            self.length.reset()
        self.length.start()

    def trigger(self):
        self.i = 0
        self.freq_divider = 6
        self.triggered = not self.cgb_mode
        if self.cgb_mode:
            self.get_wave_entry()

    def step(self, ticks):
        self.ticks_since_read += ticks
        if not self.update_length(ticks):
            return 0
        if not self.dac_enabled:
            return 0
        if (self.get_nr0() & (1 << 7)) == 0:
            return 0
        self.freq_divider -= ticks
        if self.freq_divider <= 0:
            self.reset_freq_divider()
            if self.triggered:
                self.last_output = (self.buffer >> 4) & 0x0f
                self.triggered = False
            else:
                self.last_output = self.get_wave_entry()
            self.i = (self.i + (ticks)) % 32
        return self.last_output

    def get_volume(self):
        return (self.get_nr2() >> 5) & 0b00000011

    def get_wave_entry(self):
        self.ticks_since_read = 0
        self.last_read_addr = IO_Registers.WAVE_PATTERN_0 + self.i // 2
        self.buffer = self.wave_ram[self.last_read_addr - IO_Registers.WAVE_PATTERN_0]
        b = self.buffer
        if self.i % 2 == 0:
            b = (b >> 4) & 0x0f
        else:
            b = b & 0x0f
        return {
            0: 0,
            1: b,
            2: (b >> 1),
            3: (b >> 2)
        }.get(self.get_volume())

    def set_nr0(self, value):
        super().set_nr0(value)
        self.dac_enabled  = (value & (1 << 7)) != 0
        self.channel_enabled = self.channel_enabled and self.dac_enabled

    def set_nr1(self, value):
        super().set_nr1(value)
        self.length.set_length(256 - value)

    def set_nr3(self, value):
        super().set_nr3(value)

    def set_nr4(self, value):
        if not self.cgb_mode and (value & (1 << 7)) != 0:
            if self.is_enabled() and self.freq_divider == 2:
                pos = self.i // 2
                if pos < 4:
                    self.wave_ram[0] = self.wave_ram[pos]
                else:
                    pos = pos & 0b11111100
                    for i in range(4):
                        self.wave_ram[i] = self.wave_ram[((pos + i) % 0x10)]
        super().set_nr4(value)

    def reset_freq_divider(self):
        self.freq_divider = self.get_frequency() * 4
