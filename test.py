#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from pygb.cartridge import ROM
from pygb.cpu import CPU
from pygb.input import Input
from pygb.instruction_performer import InstructionPerformer
from pygb.mmu import MMU
from pygb.registers import Registers
from pygb.stack_manager import StackManager


def main():
    logging.basicConfig(level=logging.DEBUG)
    run_tests()
    
def run_tests():
    test_instructions_types()

def test_instructions_types():
    _input = Input()
    rom = ROM([0]*0x8000)
    ip = InstructionPerformer(CPU(None))
    for i in range(0,0x100):
        if i not in [0xcb, 0xd3, 0xdb, 0xdd, 0xe3, 0xe4, 0xeb, 0xec, 0xed, 0xf4, 0xfc, 0xfd]:
            ip.registers = Registers()
            ip.mmu = MMU(rom, _input)
            ip.stackManager = StackManager(ip.registers, ip.mmu)
            ip.perform_instruction(i)
            if not isinstance(ip.registers.a, int):
                raise TypeError()
            if not isinstance(ip.registers.b, int):
                raise TypeError()
            if not isinstance(ip.registers.c, int):
                raise TypeError()
            if not isinstance(ip.registers.d, int):
                raise TypeError()
            if not isinstance(ip.registers.e, int):
                raise TypeError()
            if not isinstance(ip.registers.h, int):
                raise TypeError()
            if not isinstance(ip.registers.l, int):
                raise TypeError()
            if not isinstance(ip.registers.sp, int):
                raise TypeError()
            if not isinstance(ip.registers.pc, int):
                raise TypeError()
            for j in range(0,0x10000):
                if not isinstance(ip.mmu.read_byte(j), int):
                    raise TypeError()
    for i in range(0,0x100):
        ip.registers = Registers()
        ip.mmu = MMU(rom, _input)
        ip.stackManager = StackManager(ip.registers, ip.mmu)
        ip.perform_instruction(0xcb00 + i)
        if not isinstance(ip.registers.a, int):
            raise TypeError()
        if not isinstance(ip.registers.b, int):
            raise TypeError()
        if not isinstance(ip.registers.c, int):
            raise TypeError()
        if not isinstance(ip.registers.d, int):
            raise TypeError()
        if not isinstance(ip.registers.e, int):
            raise TypeError()
        if not isinstance(ip.registers.h, int):
            raise TypeError()
        if not isinstance(ip.registers.l, int):
            raise TypeError()
        if not isinstance(ip.registers.sp, int):
            raise TypeError()
        if not isinstance(ip.registers.pc, int):
            raise TypeError()
        for j in range(0,0x10000):
            if not isinstance(ip.mmu.read_byte(j), int):
                raise TypeError()


if __name__ == '__main__':
    main()