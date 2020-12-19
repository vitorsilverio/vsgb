#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vsgb.interrupt_manager import Interrupt, InterruptManager

class Timer:

    DIV_INC_TIME: int = 256 # cycles
    KEY1: int = 0
    TIMA: int = 0
    TMA: int = 0
    DIV: int = 0
    div_cycles: int = 0
    tima_cycles: int = 0

    @classmethod
    def tick(cls, cycles : int = 0):
        multiplier = 1
        cls.div_cycles += cycles

        # increment again if DOUBLE SPEED MODE
        if cls.KEY1 & 0b10000000:
            cls.div_cycles += cycles
            multiplier = 2

        if cls.KEY1 & 1: #Prepare enable/disable double speed
            cls.KEY1  &= 0b10000000
            cls.div_cycles += 128 * 1024 - 76

        # incremnt DIV register if its time to
        if cls.div_cycles >= cls.DIV_INC_TIME :
            cls.inc_div_register()
        # dont bother if TIMA is not running
        if Tima.running():
            # increment TIMA and DIV register
            cls.tima_cycles += cycles
            frequency = Tima.frequency()
            if cls.tima_cycles >= frequency:
                cls.inc_tima_register()
                cls.tima_cycles -= frequency

    @classmethod
    def inc_tima_register(cls):
        if 0xff == cls.TIMA:
            cls.TIMA = cls.TMA
            InterruptManager.request_interrupt(Interrupt.INTERRUPT_TIMER)
        else:
            cls.TIMA += 1
            cls.TIMA &= 0xff
        
    @classmethod
    def inc_div_register(cls):
        cls.DIV = ( cls.DIV + 1 ) & 0xff
        cls.div_cycles -= Timer.DIV_INC_TIME

        

class Tima:

    @staticmethod
    def running() -> bool:
        return Timer.TIMA & 0x4

    @staticmethod
    def frequency() -> int:
        return {
            0x0 : 1024,
            0x1 : 16,
            0x2 : 64,
            0x3 : 256
        }.get(Timer.TIMA & 0x3)
