#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygb.cpu import CPU
from pygb.mmu import MMU
from pygb.ppu import PPU
from pygb.screen import Screen

class Emulator:

    def __init__(self, file):
        self.mmu = MMU() 
        self.cpu = CPU(self.mmu)
        self.ppu = PPU(self.mmu, self.cpu.interruptManager)
        self.screen = Screen()

    def run(self):
        while True:
            self.cpu.step()
            self.ppu.step()
            if self.ppu.vblank:
                self.screen.render(self.ppu.framebuffer)

