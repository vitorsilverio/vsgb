#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum
from vsgb.address_space import AddressSpace
from vsgb.io_registers import IO_Registers

class InterruptManager:

    ie_register: int = 0xff
    if_register: int = 0xff

    @classmethod
    def accept(cls, address: int) -> bool:
        return address in [
            IO_Registers.IE,
            IO_Registers.IF
        ]

    @classmethod
    def read(cls, address: int) -> int:
        if address == IO_Registers.IE:
            return cls.ie_register
        if address == IO_Registers.IF:
            return cls.if_register


    @classmethod
    def write(cls, address: int, value: int):
        if address == IO_Registers.IE:
            cls.ie_register = value
        elif address == IO_Registers.IF:
            cls.if_register = value


    @classmethod
    def request_interrupt(cls, interrupt : int):
        cls.if_register |= interrupt

    @classmethod
    def pending_interrupt(cls) -> int:
        pending_interrupt = cls.ie_register & cls.if_register
        if 0 == pending_interrupt & 0b00011111:
            return Interrupt.INTERRUPT_NONE # There are not pending interrupts skip test just leave
        if Interrupt.INTERRUPT_VBLANK & pending_interrupt:
            return Interrupt.INTERRUPT_VBLANK
        if Interrupt.INTERRUPT_LCDSTAT & pending_interrupt:
            return Interrupt.INTERRUPT_LCDSTAT 
        if Interrupt.INTERRUPT_TIMER & pending_interrupt:
            return Interrupt.INTERRUPT_TIMER
        if Interrupt.INTERRUPT_SERIAL & pending_interrupt:
            return Interrupt.INTERRUPT_SERIAL
        if Interrupt.INTERRUPT_JOYPAD & pending_interrupt:
            return Interrupt.INTERRUPT_JOYPAD
        return Interrupt.INTERRUPT_NONE

class Interrupt(IntEnum):
    
    INTERRUPT_NONE    = 0x00
    INTERRUPT_VBLANK  = 0x01
    INTERRUPT_LCDSTAT = 0x02
    INTERRUPT_TIMER   = 0x04
    INTERRUPT_SERIAL  = 0x08
    INTERRUPT_JOYPAD  = 0x10
