#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

import simpleaudio as sa
from vsgb.io_registers import IO_Registers
from vsgb.mmu import MMU

# Sound Overview
# There are two sound channels connected to the output terminals SO1 and SO2. There is also a input terminal 
# Vin connected to the cartridge. It can be routed to either of both output terminals. GameBoy circuitry allows producing sound in four different ways: 
#   Quadrangular wave patterns with sweep and envelope functions.
#   Quadrangular wave patterns with envelope functions.
#   Voluntary wave patterns from wave RAM.
#   White noise with an envelope function.
# These four sounds can be controlled independantly and then mixed separately for each of the output terminals.
# Sound registers may be set at all times while producing sound. 
class APU:

    def __init__(self, mmu : MMU):
        self.mmu = mmu
        self.sound_channel1 = SoundChannel1(self.mmu)
        self.sound_channel2 = SoundChannel2(self.mmu)
        self.wave_channel = WaveChannel(self.mmu)
        self.noise_channel = NoiseChannel(self.mmu)
  

    def step(self):
        # NR52 - Sound on/off
        # Bit 7 - All sound on/off  (0: stop all sound circuits) (Read/Write)
        # Bit 3 - Sound 4 ON flag (Read Only)
        # Bit 2 - Sound 3 ON flag (Read Only)
        # Bit 1 - Sound 2 ON flag (Read Only)
        # Bit 0 - Sound 1 ON flag (Read Only)
        nr52 = self.mmu.read_byte(IO_Registers.NR_52)
        if nr52 & 0b10000000 == 0b10000000:
            if nr52 & 0b00000001 == 0b00000001:
                self.sound_channel1.step()
            if nr52 & 0b00000010 == 0b00000010:
                self.sound_channel2.step()
            if nr52 & 0b00000100 == 0b00000100:
                self.wave_channel.step()
            if nr52 & 0b00001000 == 0b00001000:
                self.noise_channel.step()


# Sound Channel 1 - Tone & Sweep

# FF10 - NR10 - Channel 1 Sweep register (R/W)
# Bit 6-4 - Sweep Time
# Bit 3   - Sweep Increase/Decrease
#            0: Addition    (frequency increases)
#            1: Subtraction (frequency decreases)
# Bit 2-0 - Number of sweep shift (n: 0-7)
# Sweep Time: 
# 000: sweep off - no freq change
# 001: 7.8 ms  (1/128Hz)
# 010: 15.6 ms (2/128Hz)
# 011: 23.4 ms (3/128Hz)
# 100: 31.3 ms (4/128Hz)
# 101: 39.1 ms (5/128Hz)
# 110: 46.9 ms (6/128Hz)
# 111: 54.7 ms (7/128Hz)
# The change of frequency (NR13,NR14) at each shift is calculated by the following formula where X(0) is initial freq & X(t-1) is last freq: 
#    X(t) = X(t-1) +/- X(t-1)/2^n

# FF11 - NR11 - Channel 1 Sound length/Wave pattern duty (R/W)
# Bit 7-6 - Wave Pattern Duty (Read/Write)
# Bit 5-0 - Sound length data (Write Only) (t1: 0-63)
# Wave Duty: 
# 00: 12.5% ( _-------_-------_------- )
# 01: 25%   ( __------__------__------ )
# 10: 50%   ( ____----____----____---- ) (normal)
# 11: 75%   ( ______--______--______-- )
# Sound Length = (64-t1)*(1/256) seconds The Length value is used only if Bit 6 in NR14 is set. 

# FF12 - NR12 - Channel 1 Volume Envelope (R/W)
# Bit 7-4 - Initial Volume of envelope (0-0Fh) (0=No Sound)
# Bit 3   - Envelope Direction (0=Decrease, 1=Increase)
# Bit 2-0 - Number of envelope sweep (n: 0-7)
#           (If zero, stop envelope operation.)
# Length of 1 step = n*(1/64) seconds 

# FF13 - NR13 - Channel 1 Frequency lo (Write Only)
# Lower 8 bits of 11 bit frequency (x). Next 3 bit are in NR14 ($FF14) 

# FF14 - NR14 - Channel 1 Frequency hi (R/W)
# Bit 7   - Initial (1=Restart Sound)     (Write Only)
# Bit 6   - Counter/consecutive selection (Read/Write)
#           (1=Stop output when length in NR11 expires)
# Bit 2-0 - Frequency's higher 3 bits (x) (Write Only)
# Frequency = 131072/(2048-x) Hz 
class SoundChannel1:

    def __init__(self, mmu : MMU):
        self.mmu = mmu

    def step(self):
        pass

class SoundChannel2:

    def __init__(self, mmu : MMU):
        self.mmu = mmu

    def step(self):
        print('Called S Channel 2')
        pass

class WaveChannel:

    def __init__(self, mmu : MMU):
        self.mmu = mmu

    def step(self):
        print('Called Wave')
        wave = []
        address = IO_Registers.WAVE_PATTERN_START
        while address <= IO_Registers.WAVE_PATTERN_END:
            wave.append(self.mmu.read_byte(address))
            address += 1
        wave_obj = sa.WaveObject(bytes(wave), 2, 2, 44100)
        wave_obj.play()


class NoiseChannel:

    def __init__(self, mmu : MMU):
        self.mmu = mmu

    def step(self):
        print('Called Noise')
        pass