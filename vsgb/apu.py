#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

import simpleaudio as sa
from threading import Thread
from vsgb.io_registers import IO_Registers



class APU:

    TICKS_PER_SEC = 4194304

    def __init__(self):
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
            IO_Registers.NR_52: 0,
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

    def read_register(self, register):
        return self.registers.get(register, 0xff)

    def write_register(self, register, value):
        self.registers[register] = value

class SoundDriver(Thread):

    def __init__(self, apu : APU):
        self.sample_rate = 44100
        super(SoundDriver, self). __init__()
        self.apu = apu

    
    def run(self):
        #Sound loop
        while True:
            if self.sound_on(1):
                """
                freq = self.apu.read_register(IO_Registers.NR_13) | ((self.apu.read_register(IO_Registers.NR_14) & 0b0111) << 8)
                samples = self.apu.read_register(IO_Registers.NR_11) & 0b00111111
                x = np.arange(samples)
                duty = {
                    0: 0.125,
                    1: 0.25,
                    2: 0.5,
                    3: 0.75
                }.get((self.apu.read_register(IO_Registers.NR_11) & 0b11000000) >> 6)
                y = 100 * self.square(2 * np.pi * freq * x / self.sample_rate , duty = duty)
                wave_obj = sa.WaveObject(y, 2, 1, self.sample_rate)
                play_obj = wave_obj.play()
                print('Freq: {}, Duty: {}, len: {}'.format(freq, duty, samples))
                """
                pass
                


    def sound_on(self, channel):
        """
        FF26 - NR52 - Sound on/off
        If your GB programs don't use sound then write 00h to this register to save 16% or more on GB power consumption. Disabeling the sound controller by clearing Bit 7 destroys the contents of all sound registers. Also, it is not possible to access any sound registers (execpt FF26) while the sound controller is disabled.
            Bit 7 - All sound on/off  (0: stop all sound circuits) (Read/Write)
            Bit 3 - Sound 4 ON flag (Read Only)
            Bit 2 - Sound 3 ON flag (Read Only)
            Bit 1 - Sound 2 ON flag (Read Only)
            Bit 0 - Sound 1 ON flag (Read Only)
            Bits 0-3 of this register are read only status bits, writing to these bits does NOT enable/disable sound. The flags get set when sound output is restarted by setting the Initial flag (Bit 7 in NR14-NR44), the flag remains set until the sound length has expired (if enabled). A volume envelopes which has decreased to zero volume will NOT cause the sound flag to go off.
        """
        nr52 = self.apu.read_register(IO_Registers.NR_52)
        if nr52 & 0b10000000 == 0:
            return False
        if channel == 1:
            return nr52 & 0b0001 != 0
        if channel == 1:
            return nr52 & 0b0010 != 0
        if channel == 1:
            return nr52 & 0b0100 != 0
        if channel == 1:
            return nr52 & 0b1000 != 0
        return False

    def square(self, wave, duty):

        return np.sin(wave)
