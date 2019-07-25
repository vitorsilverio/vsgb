#!/usr/bin/env python
# -*- coding: utf-8 -*-

class StackManager:

    def __init__(self, registers, mmu):
        self.registers = registers
        self.mmu = mmu

    def push_byte(self, byte):
        byte = byte & 0xff
        self.registers.sp -= 1
        self.mmu.write_byte(self.registers.sp, byte)

    def push_word(self, word):
        self.push_byte((word >> 8))
        self.push_byte(word)

    def pop_byte(self):
        byte = self.mmu.read_byte(self.registers.sp)
        self.registers.sp += 1
        return byte

    def pop_word(self):
        try:
            low_byte = self.pop_byte() & 0xff
        except TypeError:
            low_byte = 0
        try:
            high_byte = self.pop_byte() & 0xff
        except TypeError:
            high_byte = 0
        return low_byte | ( high_byte << 8 )