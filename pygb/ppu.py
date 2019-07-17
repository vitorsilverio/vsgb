
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PPU:

    def __init__(self, mmu):
        self.mmu = mmu
        print('PPU')

    def step(self):
        print('ppu step')

    def is_vblank(self):
        print('not vblank')
        return False