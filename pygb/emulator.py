#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygb.cpu import CPU
from pygb.mmu import MMU
from pygb.ppu import PPU

class Emulator:

    def __init__(self, file):
        self.mmu = MMU() 
        self.cpu = CPU(self.mmu)
        self.ppu = PPU(self.mmu)

    def run(self):
        while True:
            self.cpu.step()
            self.ppu.step()
            if self.ppu.is_vblank():
                print('Must render')

