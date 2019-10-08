#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum

from vsgb.io_registers import IO_Registers
from vsgb.mmu import MMU

class InterruptManager:

    def __init__(self, mmu : MMU):
        self.mmu = mmu

    def request_interrupt(self, interrupt : int):
        if_register = self.mmu.read_byte(IO_Registers.IF)
        self.mmu.write_byte(IO_Registers.IF, (if_register | interrupt))

    def pending_interrupt(self) -> int:
        ie_register = self.mmu.read_byte(IO_Registers.IE)
        if_register = self.mmu.read_byte(IO_Registers.IF)
        pending_interrupt = ie_register & if_register
        if pending_interrupt & Interrupt.INTERRUPT_VBLANK == Interrupt.INTERRUPT_VBLANK:
            return Interrupt.INTERRUPT_VBLANK
        if pending_interrupt & Interrupt.INTERRUPT_LCDSTAT == Interrupt.INTERRUPT_LCDSTAT:
            return Interrupt.INTERRUPT_LCDSTAT 
        if pending_interrupt & Interrupt.INTERRUPT_TIMER == Interrupt.INTERRUPT_TIMER:
            return Interrupt.INTERRUPT_TIMER
        if pending_interrupt & Interrupt.INTERRUPT_SERIAL == Interrupt.INTERRUPT_SERIAL:
            return Interrupt.INTERRUPT_SERIAL
        if pending_interrupt & Interrupt.INTERRUPT_JOYPAD == Interrupt.INTERRUPT_JOYPAD:
            return Interrupt.INTERRUPT_JOYPAD
        return Interrupt.INTERRUPT_NONE

class Interrupt(IntEnum):
    
    INTERRUPT_NONE    = 0x00
    INTERRUPT_VBLANK  = 0x01
    INTERRUPT_LCDSTAT = 0x02
    INTERRUPT_TIMER   = 0x04
    INTERRUPT_SERIAL  = 0x08
    INTERRUPT_JOYPAD  = 0x10
