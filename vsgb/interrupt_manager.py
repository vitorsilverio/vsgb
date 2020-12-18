#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum

class InterruptManager:

    ie_register: int = 0xff
    if_register: int = 0xff

    @classmethod
    def request_interrupt(cls, interrupt : int):
        cls.if_register |= interrupt

    @classmethod
    def pending_interrupt(cls) -> int:
        pending_interrupt = cls.ie_register & cls.if_register
        if 0 == pending_interrupt & 0b00011111:
            return Interrupt.INTERRUPT_NONE # There are not pending interrupts skip test just leave
        if Interrupt.INTERRUPT_VBLANK == Interrupt.INTERRUPT_VBLANK & pending_interrupt:
            return Interrupt.INTERRUPT_VBLANK
        if Interrupt.INTERRUPT_LCDSTAT == Interrupt.INTERRUPT_LCDSTAT & pending_interrupt:
            return Interrupt.INTERRUPT_LCDSTAT 
        if Interrupt.INTERRUPT_TIMER == Interrupt.INTERRUPT_TIMER & pending_interrupt:
            return Interrupt.INTERRUPT_TIMER
        if Interrupt.INTERRUPT_SERIAL == Interrupt.INTERRUPT_SERIAL & pending_interrupt:
            return Interrupt.INTERRUPT_SERIAL
        if Interrupt.INTERRUPT_JOYPAD == Interrupt.INTERRUPT_JOYPAD & pending_interrupt:
            return Interrupt.INTERRUPT_JOYPAD
        return Interrupt.INTERRUPT_NONE

class Interrupt(IntEnum):
    
    INTERRUPT_NONE    = 0x00
    INTERRUPT_VBLANK  = 0x01
    INTERRUPT_LCDSTAT = 0x02
    INTERRUPT_TIMER   = 0x04
    INTERRUPT_SERIAL  = 0x08
    INTERRUPT_JOYPAD  = 0x10
