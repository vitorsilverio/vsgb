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
        self.BUTTON_A = False
        self.BUTTON_B = False
        self.BUTTON_START = False
        self.BUTTON_SELECT = False
        self.BUTTON_UP = False
        self.BUTTON_DOWN = False
        self.BUTTON_LEFT = False
        self.BUTTON_RIGHT = False

    def read_input(self, joyp : int) -> int:
        _input = 0x0f
        if joyp & 0b00100000 == 0b0:
            if self.BUTTON_START:
                _input ^= 0b1000
            if self.BUTTON_SELECT:
                _input ^= 0b0100
            if self.BUTTON_B:
                _input ^= 0b0010
            if self.BUTTON_A:
                _input ^= 0b0001
        elif joyp & 0b00010000 == 0b0:
            if self.BUTTON_DOWN:
                _input ^= 0b1000
            if self.BUTTON_UP:
                _input ^= 0b0100
            if self.BUTTON_LEFT:
                _input ^= 0b0010
            if self.BUTTON_RIGHT:
                _input ^= 0b0001

        return ((0b00110000 & joyp) | _input)
