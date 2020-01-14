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
from vsgb.save_state_manager import SaveStateManager


class Emulator:

    def __init__(self, file : str, cgb_mode: bool, log_level: int):
        self.cgb_mode = cgb_mode
        self.cartridge = Cartridge(file)
        self.apu = APU(cgb_mode)
        self.apu.start()
        self.input = Input()
        self.mmu = MMU(self.cartridge.rom(), self.apu, self.input, cgb_mode) 
        self.interruptManager = InterruptManager(self.mmu)
        self.cpu = CPU(self.mmu, self.interruptManager)
        self.ppu = PPU(self.mmu, self.cpu.interruptManager, cgb_mode)
        self.timer = Timer(self.mmu, self.interruptManager)
        self.dma = DMA(self.mmu)
        self.hdma = HDMA(self.mmu)
        self.window = Window(self)
        self.window.start()
        self.debug = (log_level == logging.DEBUG)
        self.changing_state = False
        self.serialize_ok = False
        self.save_state_manager = SaveStateManager()

    def run(self):
        try:
            can_exec_hdma = False
            last_ppu_mode = None
            refresh = False
            while True:
                while self.changing_state:
                    self.serialize_ok = True
                if last_ppu_mode != self.ppu.mode:
                    last_ppu_mode = self.ppu.mode
                    ly = self.mmu.read_byte(IO_Registers.LY)
                    can_exec_hdma = PPU.H_BLANK_STATE == last_ppu_mode and ly < 143
                    refresh = PPU.V_BLANK_STATE == last_ppu_mode
                ticks = 0
                if self.cgb_mode: 
                    if self.hdma.in_progress:
                        if ( self.hdma.type == HDMA.TYPE_GDMA ):
                            self.hdma.step()
                            ticks = self.hdma.ticks
                        if  (self.hdma.type == HDMA.TYPE_HDMA ) :
                                if ( can_exec_hdma ):
                                    self.hdma.step()
                                    ticks = self.hdma.ticks
                                    can_exec_hdma = False
                if self.dma.in_progress:
                    self.dma.step()
                    ticks += self.dma.ticks
                if ticks == 0:
                    self.cpu.step()
                    ticks = self.cpu.ticks
                    if self.debug:
                        logging.debug('{}\t\t\t{}'.format(self.get_last_instruction(), self.cpu.registers))
                self.timer.tick(ticks)
                self.apu.step(ticks)
                self.ppu.step(ticks)
                
                if refresh:
                    self.window.render(self.ppu.window_framebuffer)
                    refresh = False
        except Exception as e:
            print('An error occurred:')
            print(self.cpu.registers)
            print(self.get_last_instruction())
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
            self.cpu.registers.set_af(0x1180)
            self.cpu.registers.set_bc(0x0000)
            self.cpu.registers.set_de(0xff56)
            self.cpu.registers.set_hl(0x000d)
            self.cpu.registers.sp = 0xfffe
            self.mmu.write_byte(IO_Registers.KEY1, 0x81)            
        else:
            self.cpu.registers.set_af(0x01b0)
            self.cpu.registers.set_bc(0x0013)
            self.cpu.registers.set_de(0x00d8)
            self.cpu.registers.set_hl(0x014d)
            self.cpu.registers.sp = 0xfffe
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

    def save_state(self):
        self.changing_state = True
        while not self.serialize_ok:
            self.serialize_ok = False
        self.save_state_manager.create(self)
        self.changing_state = False

    def load_state(self):
        self.changing_state = True
        while not self.serialize_ok:
            self.serialize_ok = False
        self.save_state_manager.restore(self)
        self.changing_state = False
