#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - http://bgb.bircd.org/pandocs.htm

# FF00 - P1/JOYP - Joypad (R/W)
# The eight gameboy buttons/direction keys are arranged in form of a 2x4 matrix. 
# Select either button or direction keys by writing to this register, then read-out bit 0-3.
#  Bit 7 - Not used
#  Bit 6 - Not used
#  Bit 5 - P15 Select Button Keys      (0=Select)
#  Bit 4 - P14 Select Direction Keys   (0=Select)
#  Bit 3 - P13 Input Down  or Start    (0=Pressed) (Read Only)
#  Bit 2 - P12 Input Up    or Select   (0=Pressed) (Read Only)
#  Bit 1 - P11 Input Left  or Button B (0=Pressed) (Read Only)
#  Bit 0 - P10 Input Right or Button A (0=Pressed) (Read Only)
# Note: Most programs are repeatedly reading from this port several times 
# (the first reads used as short delay, allowing the inputs to stabilize, 
# and only the value from the last read actually used).

class Input:

    def __init__(self):
        self.buttons = {
            'A': False,
            'B': False,
            'START': False,
            'SELECT': False,
            'UP': False,
            'DOWN': False,
            'LEFT': False,
            'RIGHT': False
        }
        self._interrupt = False

    def must_interrupt(self):
        must_interrupt = self._interrupt 
        self._interrupt = False
        return must_interrupt

    def request_interrupt(self):
        self._interrupt = True

    def read_input(self, joyp : int) -> int:
        _input = 0x0f
        if joyp & 0x20 == 0x00:
            if self.buttons['START']:
                _input ^= 0x08
            if self.buttons['SELECT']:
                _input ^= 0x04
            if self.buttons['A']:
                _input ^= 0x01
            if self.buttons['B']:
                _input ^= 0x02
        elif joyp & 0x10 == 0x00:
            if self.buttons['UP']:
                _input ^= 0x04
            if self.buttons['DOWN']:
                _input ^= 0x08
            if self.buttons['LEFT']:
                _input ^= 0x02
            if self.buttons['RIGHT']:
                _input ^= 0x01

        return ((0xf0 & joyp) | _input) & 0b00111111
