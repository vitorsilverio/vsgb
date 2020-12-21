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

from vsgb.address_space import AddressSpace
from vsgb.io_registers import IO_Registers

class Input(AddressSpace):

    
    BUTTON_A: bool = False
    BUTTON_B: bool = False
    BUTTON_START: bool = False
    BUTTON_SELECT: bool = False
    BUTTON_UP: bool = False
    BUTTON_DOWN: bool = False
    BUTTON_LEFT: bool = False
    BUTTON_RIGHT: bool = False
    P1: int = 0

    @classmethod
    def accept(cls, address: int) -> bool:
        return address == IO_Registers.P1

    @classmethod
    def write(cls, address: int, value: int):
        if address == IO_Registers.P1:
            cls.P1 = value

    @classmethod
    def read(cls, address : int) -> int:
        _input = 0x0f
        if 0 == cls.P1 & 0b00100000:
            if cls.BUTTON_START:
                _input ^= 0b1000
            if cls.BUTTON_SELECT:
                _input ^= 0b0100
            if cls.BUTTON_B:
                _input ^= 0b0010
            if cls.BUTTON_A:
                _input ^= 0b0001
        elif 0 == cls.P1 & 0b00010000:
            if cls.BUTTON_DOWN:
                _input ^= 0b1000
            if cls.BUTTON_UP:
                _input ^= 0b0100
            if cls.BUTTON_LEFT:
                _input ^= 0b0010
            if cls.BUTTON_RIGHT:
                _input ^= 0b0001

        return ((0b00110000 & cls.P1) | _input)
