#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygb.mmu import MMU
from pygb.registers import Registers

class StackManager:

    def __init__(self, registers : Registers, mmu : MMU):
        self.registers = registers
        self.mmu = mmu

    def push_byte(self, byte : int):
        byte = byte & 0xff
        self.registers.sp -= 1
        self.mmu.write_byte(self.registers.sp, byte)

    def push_word(self, word : int):
        self.push_byte((word >> 8))
        self.push_byte(word)

    def pop_byte(self) -> int:
        byte = self.mmu.read_byte(self.registers.sp)
        self.registers.sp += 1
        return byte

    def pop_word(self) -> int:
        return self.pop_byte() | ( self.pop_byte() << 8 )