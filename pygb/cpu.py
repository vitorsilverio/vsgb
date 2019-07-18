#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygb.interrupt_manager import InterruptManager, Interrupt
from pygb.instruction_performer import InstructionPerformer
from pygb.io_registers import IO_Registers
from pygb.registers import Registers
from pygb.stack_manager import StackManager
from pygb.timer import Timer

class CPU:

    def __init__(self,mmu):
        self.mmu = mmu
        self.registers = Registers()
        self.interruptManager = InterruptManager(mmu)
        self.timer = Timer(mmu, self.interruptManager)
        self.stackManager = StackManager(self.registers, self.mmu)
        self.instructionPerformer = InstructionPerformer(self)
        self.ticks = 0
        self.ime = False
        self.halted = False
        self.pre_halt_interrupt = 0x00
        
    def step(self):
        self.ticks = 0
        if self.halted:
            if self.pre_halt_interrupt != self.mmu.read_byte(IO_Registers.IF):
                self.halted = False
        if self.ime:
            self.serve_interrupt()
        if self.halted:
            self.ticks = 4
        else:
            instruction = self.fetch_instruction()
            self.perform_instruction(instruction)
        self.timer.tick(self.ticks)
        
    def serve_interrupt(self):
        interrupt = self.interruptManager.pending_interrupt()
        if (interrupt == Interrupt.INTERRUPT_NONE):
            return False
        self.ime = False
        self.stackManager.push_word(self.registers.pc)
        if_register = self.mmu.read_byte(IO_Registers.IF)
        if interrupt == Interrupt.INTERRUPT_VBLANK:
            self.registers.pc = 0x40
            self.mmu.write_byte(IO_Registers.IF, if_register & 0xFE)
        if interrupt == Interrupt.INTERRUPT_LCDSTAT:
            self.registers.pc = 0x48
            self.mmu.write_byte(IO_Registers.IF, if_register & 0xFD)
        if interrupt == Interrupt.INTERRUPT_TIMER:
            self.registers.pc = 0x50
            self.mmu.write_byte(IO_Registers.IF, if_register & 0xFB)
        if interrupt == Interrupt.INTERRUPT_SERIAL:
            self.registers.pc = 0x58
            self.mmu.write_byte(IO_Registers.IF, if_register & 0xF7)
        if interrupt == Interrupt.INTERRUPT_JOYPAD:
            self.registers.pc = 0x60
            self.mmu.write_byte(IO_Registers.IF, if_register & 0xEF)
        self.ticks = 20

    def fetch_instruction(self):
        instruction = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        if instruction == 0xcb:
            return 0xcb00 + self.fetch_instruction()
        return instruction

    def perform_instruction(self, instruction):
        self.ticks = self.instructionPerformer.perform_instruction(instruction)



