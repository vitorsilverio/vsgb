#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

from vsgb.audio.sound_channel1 import SoundChannel1
from vsgb.audio.sound_channel2 import SoundChannel2
from vsgb.audio.sound_channel3 import SoundChannel3
from vsgb.audio.sound_channel4 import SoundChannel4
from vsgb.audio.sound_driver import SoundDriver
from vsgb.io_registers import IO_Registers
import time

class APU:

    def __init__(self, cgb_mode):
        self.registers = {
            IO_Registers.NR_10: 0,
            IO_Registers.NR_11: 0,
            IO_Registers.NR_12: 0,
            IO_Registers.NR_13: 0,
            IO_Registers.NR_14: 0,
            IO_Registers.NR_21: 0,
            IO_Registers.NR_22: 0,
            IO_Registers.NR_23: 0,
            IO_Registers.NR_24: 0,
            IO_Registers.NR_30: 0,
            IO_Registers.NR_31: 0,
            IO_Registers.NR_32: 0,
            IO_Registers.NR_33: 0,
            IO_Registers.NR_34: 0,
            IO_Registers.NR_41: 0,
            IO_Registers.NR_42: 0,
            IO_Registers.NR_43: 0,
            IO_Registers.NR_44: 0,
            IO_Registers.NR_50: 0,
            IO_Registers.NR_51: 0,
            IO_Registers.NR_52: 0b10001111,
            IO_Registers.WAVE_PATTERN_0: 0x00,
            IO_Registers.WAVE_PATTERN_1: 0xff,
            IO_Registers.WAVE_PATTERN_2: 0x00,
            IO_Registers.WAVE_PATTERN_3: 0xff,
            IO_Registers.WAVE_PATTERN_4: 0x00,
            IO_Registers.WAVE_PATTERN_5: 0xff,
            IO_Registers.WAVE_PATTERN_6: 0x00,
            IO_Registers.WAVE_PATTERN_7: 0xff,
            IO_Registers.WAVE_PATTERN_8: 0x00,
            IO_Registers.WAVE_PATTERN_9: 0xff,
            IO_Registers.WAVE_PATTERN_A: 0x00,
            IO_Registers.WAVE_PATTERN_B: 0xff,
            IO_Registers.WAVE_PATTERN_C: 0x00,
            IO_Registers.WAVE_PATTERN_D: 0xff,
            IO_Registers.WAVE_PATTERN_E: 0x00,
            IO_Registers.WAVE_PATTERN_F: 0xff
        }
        self.sound_driver = SoundDriver()
        self.sound_channels = [SoundChannel1(cgb_mode), SoundChannel2(cgb_mode), SoundChannel3(cgb_mode), SoundChannel4(cgb_mode)]
        self.channels_enabled = [True]*len(self.sound_channels)

    def read_register(self, register):
        for sound_channel in self.sound_channels:
            if sound_channel.accepts(register):
                return sound_channel.read_byte(register)
        return self.registers.get(register, 0xff)

    def write_register(self, register, value):
        for sound_channel in self.sound_channels:
            if sound_channel.accepts(register):
                return sound_channel.write_byte(register, value)
                return
        self.registers[register] = value

    def start(self):
        for i in range(IO_Registers.NR_10, IO_Registers.NR_51 + 1):
            v = 0
            if i in [IO_Registers.NR_11, IO_Registers.NR_21, IO_Registers.NR_41]:
                v = self.read_register(i) & 0b00111111
            elif i == IO_Registers.NR_31:
                v = self.read_register(i)

            self.write_register(i, v)
        
        for sound_channel in self.sound_channels:
            sound_channel.start()

    def step(self, ticks):

        selection = self.read_register(IO_Registers.NR_51)
        left = 0
        right = 0
        i = 0
        while i < 4:
            channels_data =  self.sound_channels[i].step(ticks)  

            if not self.channels_enabled[i]:
                i += 1
                continue

            if (selection & (1 << i + 4)) != 0:
                left += channels_data

            if (selection & (1 << i)) != 0:
                right += channels_data

            i += 1

        left = left // 4
        right = right // 4

        volumes = self.read_register(IO_Registers.NR_50)
        left *= ((volumes >> 4) & 0b111)
        right *= (volumes & 0b111)
        
        self.sound_driver.play(left & 0xff, right & 0xff, ticks)
