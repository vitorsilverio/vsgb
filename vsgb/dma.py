#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vsgb.io_registers import IO_Registers
from vsgb.mmu import MMU

"""
FF46 - DMA - DMA Transfer and Start Address (W)
Writing to this register launches a DMA transfer from ROM or RAM to OAM memory (sprite attribute table). The written value specifies the transfer source address divided by 100h, ie. source & destination are:
  Source:      XX00-XX9F   ;XX in range from 00-F1h
  Destination: FE00-FE9F
It takes 160 microseconds until the transfer has completed (80 microseconds in CGB Double Speed Mode), during this time the CPU can access only HRAM (memory at FF80-FFFE). For this reason, the programmer must copy a short procedure into HRAM, and use this procedure to start the transfer from inside HRAM, and wait until the transfer has finished:
   ld  (0FF46h),a ;start DMA transfer, a=start address/100h
   ld  a,28h      ;delay...
  wait:           ;total 5x40 cycles, approx 200ms
   dec a          ;1 cycle
   jr  nz,wait    ;4 cycles
Most programs are executing this procedure from inside of their VBlank procedure, but it is possible to execute it during display redraw also, allowing to display more than 40 sprites on the screen (ie. for example 40 sprites in upper half, and other 40 sprites in lower half of the screen).
"""
class DMA:

    def __init__(self, mmu: MMU):
        self.mmu = mmu
        self.ticks = 0
        self.in_progress = False
        self.page = 0x0000
        self.counter = 0x00
        self.mmu.set_dma(self)
        self.wait_set_delay = False

    def request_dma_transfer(self, page: int):
        self.page = (page << 8)
        self.in_progress = True
        self.counter = 0x00
        self.ticks = 0
        self.wait_set_delay = True

    def step(self):
        if self.wait_set_delay:
            self.ticks = 8
            self.wait_set_delay = False
        else:
            source_address = self.page + self.counter
            destination_address = 0xfe00 + self.counter
            self.mmu.write_byte(destination_address, self.mmu.read_byte(source_address))
            self.counter += 1
            self.ticks = 20
            if self.counter == 0xa0:
                self.in_progress = False