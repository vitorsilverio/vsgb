#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vsgb.registers import Registers
from vsgb.mmu import MMU

class StackManager:

    @staticmethod
    def push_byte(byte : int):
        byte = byte & 0xff
        Registers.sp -= 1
        MMU.write(Registers.sp, byte)

    @classmethod
    def push_word(cls, word : int):
        cls.push_byte((word >> 8))
        cls.push_byte(word)

    @staticmethod
    def pop_byte() -> int:
        byte = MMU.read(Registers.sp)
        Registers.sp += 1
        return byte

    @classmethod
    def pop_word(cls) -> int:
        return cls.pop_byte() | ( cls.pop_byte() << 8 )

