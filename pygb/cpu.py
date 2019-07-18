#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygb.interrupt_manager import InterruptManager
from pygb.registers import Registers
from pygb.timer import Timer

class CPU:

    def __init__(self,mmu):
        self.mmu = mmu
        self.registers = Registers()
        self.interruptManager = InterruptManager(mmu)
        self.timer = Timer(mmu, self.interruptManager)
        self.ticks = 0
        self.ime = False
        

    def step(self):
        print('cpu step')