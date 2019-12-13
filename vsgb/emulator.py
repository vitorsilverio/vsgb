#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from vsgb.apu import APU
from vsgb.cartridge import Cartridge
from vsgb.cpu import CPU
from vsgb.dma import DMA, HDMA
from vsgb.input import Input
from vsgb.interrupt_manager import InterruptManager, Interrupt
from vsgb.io_registers import IO_Registers
from vsgb.mmu import MMU
from vsgb.ppu import PPU
from vsgb.timer import Timer
from vsgb.window import Window
from vsgb.instructions import instructions

class Emulator:

    def __init__(self, file : str, cgb_mode: bool, log_level: int):
        self.cgb_mode = cgb_mode
        self.cartridge = Cartridge(file)
        self.apu = APU()
        self.input = Input()
        self.mmu = MMU(self.cartridge.rom(), self.apu, self.input, cgb_mode) 
        self.interruptManager = InterruptManager(self.mmu)
        self.cpu = CPU(self.mmu, self.interruptManager)
        self.ppu = PPU(self.mmu, self.cpu.interruptManager, cgb_mode)
        self.timer = Timer(self.mmu, self.interruptManager)
        self.dma = DMA(self.mmu)
        self.hdma = HDMA(self.mmu)
        self.window = Window(self.input)
        self.window.start()
        self.debug = (log_level == logging.DEBUG)

    def run(self):
        try:
            while True and not self.cpu.stop:
                ticks = 0
                if self.cgb_mode and self.hdma.in_progress:
                    if self.hdma.type == HDMA.TYPE_HDMA and self.ppu.mode != PPU.H_BLANK_STATE:
                        self.hdma.stop_dma()
                    else:
                        self.hdma.step()
                        ticks = self.hdma.ticks
                elif self.dma.in_progress:
                    self.dma.step()
                    ticks = self.dma.ticks
                else:
                    self.cpu.step()
                    ticks = self.cpu.ticks
                    if self.debug:
                        logging.debug('{}\t\t\t{}'.format(self.get_last_instruction(), self.cpu.registers))
                self.timer.tick(ticks)
                self.ppu.step(ticks)
                if self.ppu.vblank:
                    self.window.render(self.ppu.framebuffer)
        except Exception as e:
            print('An error occurred:')
            print(self.cpu.registers)
            print(self.get_last_instruction)
            raise e

    def get_last_instruction(self):
        last_instruction = instructions[self.cpu.last_instruction][0]
        last_instruction_size = instructions[self.cpu.last_instruction][1]
        if last_instruction_size == 1:
            last_instruction = last_instruction.format(self.mmu.read_byte(self.cpu.last_pc+1))
        if last_instruction_size == 2:
            last_instruction = last_instruction.format(self.mmu.read_word(self.cpu.last_pc+1))
        return '{:04x}: {}'.format(self.cpu.last_pc, last_instruction)


    def skip_boot_rom(self):
        self.cpu.registers.pc = 0x0100
        if self.mmu.rom.is_cgb() and self.cgb_mode:
            self.cpu.registers.set_af(0x11b0)
        else:
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

