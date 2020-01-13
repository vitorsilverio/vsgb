#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

import math
#import numpy
import simpleaudio as sa
from vsgb.io_registers import IO_Registers



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
        self.sound_channels = [SoundChannel1(cgb_mode),SoundChannel2(cgb_mode),SoundChannel3(cgb_mode), SoundChannel4(cgb_mode)]
        self.channels_data = [0]*len(self.sound_channels)
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

    def step(self):
        
        for i in range(len(self.sound_channels)):
            self.channels_data[i] =  self.sound_channels[i].step()         

        selection = self.read_register(IO_Registers.NR_51)
        left = 0
        right = 0

        for i in range(len(self.sound_channels)):
            if not self.channels_enabled[i]:
                continue

            if (selection & (1 << i + 4)) != 0:
                left += self.channels_data[i]

            if (selection & (1 << i)) != 0:
                right += self.channels_data[i]

        left = int(left / 4)
        right = int(right / 4)

        volumes = self.read_register(IO_Registers.NR_50)
        left *= ((volumes >> 4) & 0b111)
        right *= (volumes & 0b111)

        self.sound_driver.play(left & 0xff, right & 0xff)

class SoundDriver():

    TICKS_PER_SEC = 4194304
    BUFFER_SIZE = 3000

    def __init__(self):
        self.sample_rate = 22050
        self.buffer = [0]*SoundDriver.BUFFER_SIZE
        self.ticks = 0
        self.div = int(SoundDriver.TICKS_PER_SEC / self.sample_rate)
        self.i = 0
        self.play_obj = None

    
    def play(self, left, right):
        if self.ticks != 0:
            self.ticks += 1
            self.ticks %= self.div
            return
        self.ticks += 1

        self.buffer[self.i] = left
        self.buffer[self.i+1] = right
        self.i += 2

        if self.i >= SoundDriver.BUFFER_SIZE / 2:
            wave = bytes(self.buffer)
            wave_obj = sa.WaveObject(wave,2,1,self.sample_rate)
            try:
                self.play_obj.stop()
            except:
                pass
            self.play_obj = wave_obj.play()
            #self.play_obj.wait_done()
            self.i = 0

    def stop(self):
        self.buffer = [0]*SoundDriver.BUFFER_SIZE
        if self.play_obj is not None:
            self.play_obj.stop()


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

    def step(self):
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

    def update_length(self):
        self.length.step()
        if not self.length.enabled:
            return self.channel_enabled
        if self.channel_enabled and self.length.length == 0:
            self.channel_enabled = False
        return self.channel_enabled
    

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

    def step(self):
        self.volume_envelope.step()
        e = self.update_length() and self.update_sweep() and self.dac_enabled
        if not e:
            return 0
        self.freq_divider -= 1
        if self.freq_divider == 0:
            self.reset_freq_divider()
            self.last_output = (self.get_duty() & (1 >> self.i)) >> self.i
            self.i = (self.i + 1) % 8
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

    def update_sweep(self):
        self.frequency_sweep.step()
        if self.channel_enabled and not self.frequency_sweep.is_enabled():
            self.channel_enabled = False
        return self.channel_enabled

class SoundChannel2(AbstractSoundChannel):

    def __init__(self, cgb_mode):
        super().__init__(IO_Registers.NR_21 - 1, 64, cgb_mode)
        self.freq_divider = 0
        self.volume_envelope = VolumeEnvelope()

    def start(self):
        self.i = 0
        if self.cgb_mode:
            self.length.reset()
        self.length.start()
        self.volume_envelope.start()

    def trigger(self):
        self.i = 0
        self.freq_divider = 1
        self.volume_envelope.trigger()

    def step(self):
        self.volume_envelope.step()
        e = self.update_length() and self.dac_enabled
        if not e:
            return 0
        self.freq_divider -= 1
        if self.freq_divider == 0:
            self.reset_freq_divider()
            self.last_output = (self.get_duty() & (1 >> self.i)) >> self.i
            self.i = (self.i + 1) % 8
        return self.last_output * self.volume_envelope.get_volume()

    def set_nr0(self, value):
        super().set_nr0(value)

    def set_nr1(self, value):
        super().set_nr1(value)
        self.length.set_length(64 - (value & 0b00111111))

    def set_nr2(self, value):
        super().set_nr2(value)
        self.volume_envelope.set_nr2(value)
        self.dac_enabled = (value & 0b11111000) != 0


    def get_duty(self):
        return {
            0: 0b00000001,
            1: 0b10000001,
            2: 0b10000111,
            3: 0b01111110
        }.get(self.get_nr1() >> 6)

    def reset_freq_divider(self):
        self.freq_divider = self.get_frequency() * 4

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
            elif IO_Registers.WAVE_PATTERN_0 <= self.last_read_addr <= IO_Registers.WAVE_PATTERN_F and (self.cgb_mode or self.ticks_since_read < 2):
                return self.wave_ram[self.last_read_addr - IO_Registers.WAVE_PATTERN_0]
        return super().read_byte(address)

    def write_byte(self, address, value):
        if IO_Registers.WAVE_PATTERN_0 <= address <= IO_Registers.WAVE_PATTERN_F:
            if not self.is_enabled():
                self.wave_ram[address - IO_Registers.WAVE_PATTERN_0] = value
                return
            elif IO_Registers.WAVE_PATTERN_0 <= self.last_read_addr <= IO_Registers.WAVE_PATTERN_F and (self.cgb_mode or self.ticks_since_read < 2):
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

    def step(self):
        self.ticks_since_read += 1
        if not self.update_length():
            return 0
        if not self.dac_enabled:
            return 0
        if (self.get_nr0() & (1 << 7)) == 0:
            return 0
        self.freq_divider -= 1
        if self.freq_divider == 0:
            self.reset_freq_divider()
            if self.triggered:
                self.last_output = (self.buffer >> 4) & 0x0f
                self.triggered = False
            else:
                self.last_output = self.get_wave_entry()
            self.i = (self.i + 1) % 32
        return self.last_output

    def get_volume(self):
        return (self.get_nr2() >> 5) & 0b00000011

    def get_wave_entry(self):
        self.ticks_since_read = 0
        self.last_read_addr = IO_Registers.WAVE_PATTERN_0 + int(self.i / 2)
        self.buffer = self.wave_ram[self.last_read_addr-IO_Registers.WAVE_PATTERN_0]
        b = self.buffer
        if self.i % 2 == 0:
            b = (b >> 4) & 0x0f
        else:
            b = b & 0x0f
        return {
            0: 0,
            1: b,
            2: b >> 1,
            3: b >> 2
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
                pos = self.i / 2
                if pos < 4:
                    self.wave_ram[0] = self.wave_ram[pos]
                else:
                    pos = pos & 0b11111100
                    for i in range(4):
                        self.wave_ram[i] = self.wave_ram[((pos + i) % 0x10)]
        super().set_nr4(value)

    def reset_freq_divider(self):
        self.freq_divider = self.get_frequency() * 4

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

    def step(self):
        self.volume_envelope.step()
        if not self.update_length():
            return 0
        if not self.dac_enabled:
            return 0
        
        if self.polynominal_counter.step():
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


class LengthCounter:

    DIVIDER = int(SoundDriver.TICKS_PER_SEC / 256)

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
            self.length == self.full_length
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

class VolumeEnvelope:

    def __init__(self):
        self.i = 0
        self.volume = 0
        self.initial_volume = 0
        self.sweep = 0
        self.envelope_direction = 0
        self.finished = False

    def set_nr2(self, value):
        self.initial_volume = value >> 4
        self.envelope_direction = -1 if (value & 0b00001000 == 0) else 1
        self.sweep = value & 0b00000111

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

        if (self.volume == 0 and self.envelope_direction == -1 ) or (self.volume == 15 and self.envelope_direction == 1):
            self.finished = True
            return
        self.i += 1
        if self.i == self.sweep * SoundDriver.TICKS_PER_SEC / 64:
            self.i = 0
            self.volume += self.envelope_direction

    def get_volume(self):
        if self.is_enabled():
            return self.volume
        else:
            return self.initial_volume

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
    
    def step(self):
        self.i += 1
        if self.i == FrequencySweep.DIVIDER:
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

class Lfsr:

    def __init__(self):
        self.lfsr = 0

    def start(self):
        self.reset()

    def reset(self):
        self.lfsr = 0x7fff

    def next_bit(self, with_mode7):
        x = ((self.lfsr & 1) ^ ((self.lfsr & 2) >> 1)) != 0
        self.lfsr = self.lfsr >> 1
        self.lfsr = self.lfsr | ((1 << 14) if x else 0)
        if with_mode7:
            self.lfsr = self.lfsr | ((1 << 6) if x else 0)
        return 1 & ~self.lfsr

    def get_value(self):
        return self.lfsr

class PolynomialCounter:

    def __init__(self):
        self.i = 0
        self.shifted_divisor = 0

    def set_nr43(self,value):
        clock_shifted = value >> 4
        divisor = 0
        divisor = {
            0: 8,
            1: 16,
            2: 32,
            3: 48,
            4: 64,
            5: 80,
            6: 96,
            7: 112
        }.get(value & 0b00000111)
        self.shifted_divisor = divisor << clock_shifted
        self.i = 1

    def step(self):
        self.i -= 1
        if self.i == 0:
            self.i = self.shifted_divisor
            return True
        else:
            return False