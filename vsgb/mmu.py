#!/usr/bin/env python
# -*- coding: utf-8 -*-

import array

from vsgb.apu import APU
from vsgb.boot_rom import boot_rom, cgb_boot_rom
from vsgb.cgb_palette import CGB_Palette
from vsgb.input import Input
from vsgb.io_registers import IO_Registers
from vsgb.cartridge import CartridgeType
from vsgb.game_shark import GameShark
from vsgb.interrupt_manager import InterruptManager
from vsgb.timer import Timer
from vsgb.ppu import PPU
from vsgb.memory.wram import WorkRam
from vsgb.memory.unused_memory_area import UnusedMemoryArea

from vsgb.address_space import AddressSpace

# General Memory Map
# Start End     Description                      Notes
# 0000  3FFF    16KB ROM bank 00                 From cartridge, usually a fixed bank
# 4000  7FFF    16KB ROM Bank 01~NN              From cartridge, switchable bank via MBC (if any)
# 8000  9FFF    8KB Video RAM (VRAM)             Only bank 0 in Non-CGB mode
#                                                Switchable bank 0/1 in CGB mode
# A000  BFFF    8KB External RAM                 In cartridge, switchable bank if any
# C000  CFFF    4KB Work RAM (WRAM) bank 0
# D000  DFFF    4KB Work RAM (WRAM) bank 1~N     Only bank 1 in Non-CGB mode
#                                                Switchable bank 1~7 in CGB mode
# E000  FDFF    Mirror of C000~DDFF (ECHO RAM) 	 Typically not used
# FE00  FE9F    Sprite attribute table (OAM)
# FEA0  FEFF    Not Usable
# FF00  FF7F    I/O Registers
# FF80  FFFE    High RAM (HRAM)
# FFFF  FFFF    Interrupts Enable Register (IE) 	
class MMU:

    spaces: list = [
        InterruptManager,
        Timer,
        Input,
        WorkRam,
        PPU
    ]

    def __init__(self, rom : CartridgeType, apu: APU, cgb_mode: bool):
        self.rom = rom
        self.apu = apu
        self.zero_page = array.array('B', [0x00]*0x80)
        self.hram = array.array('B', [0x00]*0x80)
        self.bootstrap_enabled = True
        self.unusable_memory_area = UnusedMemoryArea(cgb_mode)
        self.cgb_mode = cgb_mode
        self.cgb_palette = CGB_Palette()
        if self.cgb_mode:
            self.boot_rom  = cgb_boot_rom
        else:
            self.boot_rom  = boot_rom
        self.game_shark = GameShark()

    def set_dma(self, dma):
        self.dma = dma

    def set_hdma(self, hdma):
        self.hdma = hdma
        
    def read_byte(self, address: int) -> int:
        for space in MMU.spaces:
            if space.accept(address):
                return space.read(address)

        if self.game_shark.cheats_enabled and (address in self.game_shark.cheats):
            return self.game_shark.cheats[address]

        if 0 <= address < 0x8000:
            if self.bootstrap_enabled and ((0 <= address <= 0xff) or (0x0200 <= address <= 0x08ff)):
                return self.boot_rom[address] & 0xff
            return self.rom.read_rom_byte(address)
        if 0xa000 <= address < 0xc000:
            return self.rom.read_external_ram_byte(address) & 0xff
        if 0xfea0 <= address < 0xff00:
            return self.unusable_memory_area.read_value(address) & 0xff
        if 0xff00 <= address < 0xff80:
            if address in self.apu.registers:
                return self.apu.read_register(address) & 0xff
            return IO_Registers.read_value(address) & 0xff
            
        if 0xff80 <= address < 0x10000:
            return self.hram[address - 0xff80] & 0xff
        return 0xff

    def write_byte(self, address : int, value : int, hardware_operation : bool = False):
        value = value & 0xff
        for space in MMU.spaces:
            if space.accept(address):
                space.write(address, value)
                break

        if 0 <= address < 0x8000:
            self.rom.write_rom_byte(address, value)
        elif 0xa000 <= address < 0xc000:
            self.rom.write_external_ram_byte(address, value)
        elif 0xff00 <= address < 0xff80:
            if not hardware_operation:
                if address == IO_Registers.P1:
                    IO_Registers.write_value(address,value & 0b00110000)
                elif address == IO_Registers.DIV: # Reset div register
                    IO_Registers.write_value(address,0)
                elif address == IO_Registers.DMA: # Start dma transfer
                    self.dma.request_dma_transfer(value)
                elif address == IO_Registers.HDMA5: # Start hdma transfer
                    self.hdma.request_hdma_transfer(value)
                elif address == 0xff50:
                    self.bootstrap_enabled = False
                    print('Boot rom disabled. Starting rom...')
                elif address in self.apu.registers:
                    self.apu.write_register(address, value)
                else:
                    IO_Registers.write_value(address,value)
            else:     
                IO_Registers.write_value(address,value)
        elif 0xff80 <= address < 0x10000:
            self.hram[address - 0xff80] = value

    def read_word(self, address: int) -> int:
        return (self.read_byte(address) | (self.read_byte(address + 1) << 8)) & 0xffff

    def write_word(self, address : int, value : int):
        value = (value & 0xffff)
        self.write_byte(address, (value & 0xff))
        self.write_byte((address + 1), (value >> 8) & 0xff)
