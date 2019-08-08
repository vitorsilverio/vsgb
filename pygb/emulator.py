#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygb.cartridge import Cartridge
from pygb.cpu import CPU
from pygb.input import Input
from pygb.io_registers import IO_Registers
from pygb.mmu import MMU
from pygb.ppu import PPU
from pygb.sound import Sound
from pygb.window import Window

class Emulator:

    def __init__(self, file : str):
        self.cartridge = Cartridge(file)
        self.input = Input()
        self.mmu = MMU(self.cartridge.rom(), self.input) 
        self.cpu = CPU(self.mmu)
        self.ppu = PPU(self.mmu, self.cpu.interruptManager)
        self.sound = Sound(self.mmu, self.cpu.interruptManager)
        self.window = Window(self.input, self.cpu.interruptManager)
        self.window.start()

    def run(self):
        while True:
            self.cpu.step()
            self.ppu.step(self.cpu.ticks)
            if self.ppu.vblank:
                self.window.render(self.ppu.framebuffer)
            self.sound.step()

    def skip_boot_rom(self):
        self.cpu.registers.pc = 0x0100
        self.cpu.registers.set_af(0x01b0)
        self.cpu.registers.set_bc(0x0013)
        self.cpu.registers.set_de(0x00d8)
        self.cpu.registers.set_hl(0x014d)
        self.cpu.registers.sp = 0xffff
        self.mmu.write_byte(IO_Registers.NR_10, 0x80)
        self.mmu.write_byte(IO_Registers.NR_11, 0xbf)
        self.mmu.write_byte(IO_Registers.NR_12, 0xf3)
        self.mmu.write_byte(IO_Registers.NR_14, 0xbf)
        self.mmu.write_byte(IO_Registers.NR_21, 0x3f)
        self.mmu.write_byte(IO_Registers.NR_24, 0xbf)
        self.mmu.write_byte(IO_Registers.NR_30, 0x7f)
        self.mmu.write_byte(IO_Registers.NR_31, 0xff)
        self.mmu.write_byte(IO_Registers.NR_32, 0x9f)
        self.mmu.write_byte(IO_Registers.NR_33, 0xbf)
        self.mmu.write_byte(IO_Registers.NR_41, 0xff)
        self.mmu.write_byte(IO_Registers.NR_44, 0xbf)
        self.mmu.write_byte(IO_Registers.NR_50, 0x77)
        self.mmu.write_byte(IO_Registers.NR_51, 0xf3)
        self.mmu.write_byte(IO_Registers.NR_52, 0xf1)
        self.mmu.write_byte(IO_Registers.LCDC, 0x91)
        self.mmu.write_byte(IO_Registers.STAT, 0x05)
        self.mmu.write_byte(IO_Registers.BGP, 0xfc)
        self.mmu.write_byte(IO_Registers.OBP0, 0xff)
        self.mmu.write_byte(IO_Registers.OBP1, 0xff)
        # unmap the boot rom
        self.mmu.write_byte(0xFF50, 0x01)

