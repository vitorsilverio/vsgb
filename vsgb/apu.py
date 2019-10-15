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

    TICKS_PER_SEC = 4194304

    def __init__(self, mmu : MMU):
        self.mmu = mmu
        self.pulse_channel1 = PulseChannel1(self.mmu)
        self.pulse_channel2 = PulseChannel2(self.mmu)
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
                self.pulse_channel1.step()
            if nr52 & 0b00000010 == 0b00000010:
                self.pulse_channel2.step()
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
class PulseChannel1(SoundChannel):

    def __init__(self, mmu : MMU):
        self.mmu = mmu

    def step(self):
        pass

class PulseChannel2(SoundChannel):

    def __init__(self, mmu : MMU):
        self.mmu = mmu

    def step(self):
        print('Called S Channel 2')
        pass

class WaveChannel(SoundChannel):

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


class NoiseChannel(SoundChannel):

    def __init__(self, mmu : MMU):
        self.mmu = mmu

    def step(self):
        print('Called Noise')
        pass

class SoundChannel:

    def __init__(self):
        self.offset = 0
        self.channel_enabled = False
        self.dac_enabled = False
        self.nr0 = 0
        self.nr1 = 0
        self.nr2 = 0
        self.nr3 = 0
        self.nr4 = 0

    
    def step(self):
        pass


class VolumeEnvelope:

    def __init__(self):
        self.initial_volume = 0
        self.envelope_direction = 0
        self.sweep = 0
        self.volume = 0
        self.i = 0
        self.finished = False

    def set_nr2(self, register):
        self.initial_volume = register >> 4
        self.envelope_direction = -1 if (register & (1 << 3)) == 0 else 1
        self.sweep = register & 0b00000111

    def is_enabled(self):
        return self.sweep > 0

    def start(self):
        self.finished = True
        self.i = 8192

    def trigger(self):
        self.volume = self.initial_volume
        self.i = 0
        self.finished = False

    def step(self):
        if self.finished: 
            return
        if (self.volume == 0 and self.envelope_direction == -1) or (self.volume == 15 and self.envelope_direction == 1):
            self.finished = True
            return
        self.i += 1
        if self.i == int(sweep * APU.TICKS_PER_SEC / 64):
            self.i = 0
            self.volume += self.envelope_direction
        return

    def get_volume(self):
        if self.is_enabled():
            return self.volume
        return self.initial_volume

class FrequencySweep:

    DIVIDER = int(APU.TICKS_PER_SEC / 128)

    def __init__(self):
        self.period = 0
        self.negate = False
        self.shift = 0
        self.timer = 0
        self.shadow_freq = 0
        self.nr13 = 0
        self.nr14 = 0
        self.i = 0
        self.overflow = False
        self.count_enabled = False
        self.negging = False

    def start(self):
        self.count_enabled = False
        self.i = 8192

    def trigger(self):
        self.negging = False
        self.overflow = False
        self.shadow_freq = self.nr13 | ((self.nr14 & 0b00000111) << 8)
        self.timer = 8 if self.period == 0 else period
        self.count_enabled = self.period != 0 or self.shift != 0
        if self.shift > 0:
            self.calculate()

    def set_nr10(self, value):
        self.period = (value >> 4) & 0b00000111
        self.negate = (value & (1 << 3)) != 0
        self.shift = value & 0b00000111
        if self.negging and not self.negate: 
            self.overflow = True

    def set_nr14(self, value):
        self.nr14 =  value
        if (value & (1 << 7)) != 0:
            self.trigger()

    def step(self):
        self.i += 1
        if self.i == FrequencySweep.DIVIDER:
            self.i = 0
            if not self.count_enabled:
                return
            self.timer -= 1
            if self.timer == 0:
                self.timer = 8 if self.period == 0 else self.period
                if self.period != 0:
                    new_freq = self.calculate()
                    if not self.overflow and self.shift != 0:
                        self.shadow_freq = new_freq
                        self.nr13 = self.shadow_freq & 0xff
                        self.nr14 = (self.shadow_freq & 0x700) >> 8
                        self.calculate()
        return

    def calculate(self):
        freq = self.shadow_freq >> self.shift
        if self.negate:
            freq = self.shadow_freq - freq
            self.negging = True
        else:
            freq = self.shadow_freq = freq

        if freq > 2047:
            self.overflow = True
        return freq

    def is_enabled(self):
        return not self.overflow

class LengthCounter:

    DIVIDER = int(APU.TICKS_PER_SEC / 128)
    
    def __init__(self, full_length):
        self.full_length = full_length
        self.length = 0
        self.i = 0
        self.enabled = False

    def start(self):
        self.i = 8192

    def step(self):
        self.i += 1
        if self.i == LengthCounter.DIVIDER:
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
                if enable != 0 and self.i < LengthCounter.DIVIDER / 2:
                    self.set_length(self.full_length - 1)
                else:
                    self.set_length(self.full_length)
        elif enable:
            if (self.length > 0 and self.i < LengthCounter.DIVIDER / 2):
                self.length -= 1
            if (self.length == 0 and trigger and self.i < LengthCounter.DIVIDER / 2):
                self.set_length(self.full_length - 1)
        else:
            if (self.length == 0 and trigger):
                self.set_length(self.full_length)
        this.enabled = enable

    def get_value(self):
        return self.length

    def is_enabled(self):
        return self.enabled

    def reset(self):
        self.enabled = True
        self.i = 0
        self.length = 0

