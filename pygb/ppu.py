#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygb.screen import Screen

class PPU:

    FRAMEBUFFER_SIZE = Screen.SCREEN_WIDTH * Screen.SCREEN_HEIGHT

    H_BLANK_STATE     = 0
    V_BLANK_STATE     = 1
    OAM_READ_STATE    = 2
    VMRAM_READ_STATE  = 3

    OAM_SCANLINE_TIME   = 80
    VRAM_SCANLINE_TIME  = 172
    H_BLANK_TIME        = 204
    V_BLANK_TIME        = 4560

    def __init__(self, mmu):
        self.mmu = mmu
        self.framebuffer = [0]*PPU.FRAMEBUFFER_SIZE
        self.mode = PPU.V_BLANK_STATE
        self.modeclock = 0
        self.vblank_line = 0
        self.auxiliary_modeclock = 0
        self.screen_enabled = True
        self.window_line = 0

    def step(self, cycles=1):
        self.vblank = False
        self.modeclock += cycles
        self.auxillary_modeclock += cycles