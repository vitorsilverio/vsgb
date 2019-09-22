#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygb.interrupt_manager import Interrupt, InterruptManager
from pygb.io_registers import IO_Registers
from pygb.mmu import MMU

class Timer:

    DIV_INC_TIME = 256 # cycles

    def __init__(self, mmu : MMU, interruptManager : InterruptManager):
        self.mmu = mmu
        self.interruptManager = interruptManager
        self.div_cycles = 0
        self.tima_cycles = 0
        self.tima = Tima(mmu)

    def tick(self, cycles : int = 0):
        self.div_cycles += cycles
        # incremnt DIV register if its time to
        if self.div_cycles >= Timer.DIV_INC_TIME :
            self.inc_div_register()
        # update TIMA register
        self.tima.update()
        # dont bother if TIMA is not running
        if self.tima.running():
            # increment TIMA and DIV register
            self.tima_cycles += cycles
            frequency = self.tima.frequency()
            if self.tima_cycles >= frequency:
                self.inc_tima_register()
                self.tima_cycles -= frequency

    def inc_tima_register(self):
        tima = self.mmu.read_byte(IO_Registers.TIMA)
        if tima == 0xff:
            tima = self.mmu.read_byte(IO_Registers.TMA)
            self.interruptManager.request_interrupt(Interrupt.INTERRUPT_TIMER)
        else:
            tima += 1
        self.mmu.write_byte(IO_Registers.TIMA, tima, True)

    def inc_div_register(self):
        div = self.mmu.read_byte(IO_Registers.DIV)
        div = ( div + 1 ) & 0xff
        self.mmu.write_byte(IO_Registers.DIV, div, True)
        self.div_cycles -= Timer.DIV_INC_TIME

class Tima:

    def __init__(self, mmu : MMU):
        self.mmu = mmu
        self.register = 0

    def update(self):
        self.register = self.mmu.read_byte(IO_Registers.TAC)

    def running(self) -> bool:
        return self.register & 0x4 == 0x4

    def frequency(self) -> int:
        return {
            0x0 : 1024,
            0x1 : 16,
            0x2 : 64,
            0x3 : 256
        }.get(self.register & 0x3)