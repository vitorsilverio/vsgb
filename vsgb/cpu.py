#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from vsgb.interrupt_manager import InterruptManager, Interrupt
from vsgb.instruction_performer import InstructionPerformer
from vsgb.io_registers import IO_Registers
from vsgb.mmu import MMU
from vsgb.registers import Registers
from vsgb.stack_manager import StackManager


class CPU:

    def __init__(self, mmu: MMU):
        self.mmu = mmu        
        self.stackManager = StackManager(self.mmu)
        self.instructionPerformer = InstructionPerformer(self)
        self.ticks = 0
        self.ime = False
        self.halted = False
        self.stop = False
        self.pending_interrupts_before_halt = 0x00
        self.last_pc = 0
        self.last_instruction = 0

    
    def step(self):
        self.ticks = 0
        if self.stop:
            return None
        self.check_halted()
        if self.ime or 0 != self.pending_interrupts_before_halt:
            self.serve_interrupt()
        if self.halted:
            self.ticks += 4
        else:
            self.last_pc = Registers.pc
            instruction = self.fetch_instruction()
            self.last_instruction = instruction
            self.perform_instruction(instruction)
        return None
    
    def check_halted(self):
        if self.halted and self.pending_interrupts_before_halt != InterruptManager.if_register:
            self.ticks += 4
            self.halted = False

    def serve_interrupt(self):
        interrupt = InterruptManager.pending_interrupt()
        if interrupt == Interrupt.INTERRUPT_NONE:
            return None
        self.ime = False
        if self.halted:
            self.halted = False
        self.stackManager.push_word(Registers.pc)
        if interrupt == Interrupt.INTERRUPT_VBLANK:
            Registers.pc = 0x40 #RST 40H
            InterruptManager.if_register &= 0b11111110
        elif interrupt == Interrupt.INTERRUPT_LCDSTAT:
            Registers.pc = 0x48 #RST 48H
            InterruptManager.if_register &= 0b11111101
        elif interrupt == Interrupt.INTERRUPT_TIMER:
            Registers.pc = 0x50 #RST 50H
            InterruptManager.if_register &= 0b11111011
        elif interrupt == Interrupt.INTERRUPT_SERIAL:
            Registers.pc = 0x58 #RST 58H
            InterruptManager.if_register &= 0b11110111
        elif interrupt == Interrupt.INTERRUPT_JOYPAD:
            Registers.pc = 0x60 #RST 60H
            InterruptManager.if_register &= 0b11101111
        self.ticks += 20
        return None

    def fetch_instruction(self, prefix: bool = False) -> int:
        instruction = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        if 0xcb == instruction and not prefix:
            return 0xcb00 + self.fetch_instruction(True)
        return instruction

    def perform_instruction(self, instruction : int):
        self.ticks += self.instructionPerformer.perform_instruction(instruction)



