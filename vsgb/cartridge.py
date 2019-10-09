#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Implemented following https://gbdev.gg8.se/wiki/articles/Memory_Bank_Controllers instructions

import logging
import os
import struct

class Cartridge:

    def __init__(self, file : str):
        self.data = []
        size = os.stat(file).st_size
        with open(file,'rb') as f:
            for i in range(size):
                self.data.append(struct.unpack('<B', f.read(1))[0])

    def rom(self):
        rom_type = self.data[0x147]
        if rom_type == 0x00:
            return ROM(self.data, False, False)
        if rom_type == 0x01:
            return MBC1(self.data, False, False)
        if rom_type == 0x02:
            return MBC1(self.data, True, False)
        if rom_type == 0x03:
            return MBC1(self.data, True, True)
        if rom_type == 0x05:
            return MBC2(self.data, False)
        if rom_type == 0x06:
            return MBC2(self.data, True)
        if rom_type == 0x08:
            return ROM(self.data, True, False)
        if rom_type == 0x09:
            return ROM(self.data, True, True)
        if rom_type == 0x0f:
            return MBC3(self.data, False, True, True)
        if rom_type == 0x10:
            return MBC3(self.data, True, True, True)
        if rom_type == 0x11:
            return MBC3(self.data, False, False, False)
        if rom_type == 0x12:
            return MBC3(self.data, True, False, False)
        if rom_type == 0x13:
            return MBC3(self.data, True, True, False)
        if rom_type == 0x19:
            return MBC5(self.data, False, False)
        if rom_type == 0x1a:
            return MBC5(self.data, True, False)
        if rom_type == 0x1b:
            return MBC5(self.data, True, True)
        return None

class Battery:

    def __init__(self, save_file: str):
        self.save_file = save_file

    def load_ram(self, ram: list):
        try:
            size = os.stat(self.save_file).st_size
            with open(self.save_file,'rb') as f:
                for i in range(size):
                    ram[i] = struct.unpack('<B', f.read(1))[0]
            return ram
        except FileNotFoundError:
            # File will be generated when saving
            pass


    def save_ram(self, ram: list):
        with open(self.save_file,'wb') as f:
            f.write(bytes(ram))

class CartridgeType:

    def __init__(self, data : list, hasRam: bool, hasBattery: bool):
        self.data = data
        self.hasRam = hasRam
        self.hasBattery = hasBattery

        rom_banks_reg = self.data[0x0148]
        self.rom_banks = {
            0x00: 2,
            0x01: 4,
            0x02: 8,
            0x03: 16,
            0x04: 32,
            0x05: 64,
            0x06: 128,
            0x07: 256,
            0x52: 72,
            0x53: 80,
            0x54: 96
        }.get(rom_banks_reg, 0)

        ram_banks_reg = self.data[0x0149]
        self.ram_banks = {
            0x00: 0,
            0x01: 1,
            0x02: 1,
            0x03: 4,
            0x04: 16
        }.get(ram_banks_reg, 0)

        self.ram = [0xff] * (0x2000 * self.ram_banks)

        if self.hasBattery:
            save_file_name = bytes(self.data[0x0134:0x0143]).decode().rstrip('\x00')+".sav"
            self.battery = Battery(save_file_name)
            self.ram = self.battery.load_ram(self.ram)


    def read_rom_byte(self, address : int) -> int:
        return self.data[address]

    def write_rom_byte(self, address : int, value : int):
        pass

    def read_external_ram_byte(self, address : int) -> int:
        return 0x00

    def write_external_ram_byte(self, address : int, value : int):
        pass

class ROM(CartridgeType):

    def __init__(self, data: list, hasRam: bool, hasBattery: bool):
        super().__init__(data, hasRam, hasBattery)


# MBC1 (max 2MByte ROM and/or 32KByte RAM)
# ----------------------------------------
# This is the first MBC chip for the gameboy. Any newer MBC chips are working similiar, 
# so that is relative easy to upgrade a program from one MBC chip to another - or even 
# to make it compatible to several different types of MBCs.
# Note that the memory in range 0000-7FFF is used for both reading from ROM, and for 
# writing to the MBCs Control Registers. 
class MBC1(CartridgeType):

    ROM_BANKING_MODE = 0x00
    RAM_BANKING_MODE = 0x01

    def __init__(self, data: list, hasRam: bool, hasBattery: bool):
        super().__init__(data, hasRam, hasBattery)
        self.ram_bank = 0
        self.rom_bank = 1
        self.memory_mode = 0
        self.ram_enabled = False

      
    def read_rom_byte(self, address : int) -> int:
        # 0000-3FFF - ROM Bank 00 (Read Only)
        # This area always contains the first 16KBytes of the cartridge ROM.
        if address < 0x4000:
            return self.data[address]
        # 4000-7FFF - ROM Bank 01-7F (Read Only)
        # This area may contain any of the further 16KByte banks of the ROM, allowing to 
        # address up to 125 ROM Banks (almost 2MByte). As described below, bank numbers 
        # 20h, 40h, and 60h cannot be used, resulting in the odd amount of 125 banks. 
        if self.rom_bank == 0:
            self.rom_bank += 1
        if self.memory_mode == MBC1.ROM_BANKING_MODE and self.rom_bank in [0x20, 0x40, 0x60]:
            self.rom_bank += 1
        return self.data[(0x4000 * self.rom_bank) + (address - 0x4000)]

    def write_rom_byte(self, address : int, value : int):
        # 0000-1FFF - RAM Enable (Write Only)
        # Before external RAM can be read or written, it must be enabled by writing to this 
        # address space. It is recommended to disable external RAM after accessing it, in 
        # order to protect its contents from damage during power down of the gameboy. Usually 
        # the following values are used:
        # - 00h  Disable RAM (default)
        # - 0Ah  Enable RAM
        # Practically any value with 0Ah in the lower 4 bits enables RAM, and any other value disables RAM.
        if 0x0000 <= address <= 0x1fff:
            self.ram_enabled = (value & 0x0f == 0x0a)

        # 2000-3FFF - ROM Bank Number (Write Only)
        # Writing to this address space selects the lower 5 bits of the ROM Bank Number (in range 01-1Fh). 
        # When 00h is written, the MBC translates that to bank 01h also. That doesn't harm so far, because 
        # ROM Bank 00h can be always directly accessed by reading from 0000-3FFF. But (when using the register 
        # below to specify the upper ROM Bank bits), the same happens for Bank 20h, 40h, and 60h. Any attempt 
        # to address these ROM Banks will select Bank 21h, 41h, and 61h instead. 
        if 0x2000 <= address <= 0x3fff:
            self.rom_bank = value & 0b00011111
            if self.rom_bank == 0:
                self.rom_bank += 1
            if self.memory_mode == MBC1.ROM_BANKING_MODE and self.rom_bank in [0x20, 0x40, 0x60]:
                self.rom_bank += 1

        # 4000-5FFF - RAM Bank Number - or - Upper Bits of ROM Bank Number (Write Only)
        # This 2bit register can be used to select a RAM Bank in range from 00-03h, or to specify the upper 
        # two bits (Bit 5-6) of the ROM Bank number, depending on the current ROM/RAM Mode. (See below.) 
        if 0x4000 <= address <= 0x5fff:
            if self.memory_mode == MBC1.RAM_BANKING_MODE:
                self.ram_bank = (value & 0b00000011)
                self.rom_bank = self.rom_bank & 0b00011111
            else:
                self.ram_bank = 0
                self.rom_bank = self.rom_bank | ((value & 0b00000011) << 5)
        
        # 6000-7FFF - ROM/RAM Mode Select (Write Only)
        # This 1bit Register selects whether the two bits of the above register should be used as upper 
        # two bits of the ROM Bank, or as RAM Bank Number. 
        # - 00h = ROM Banking Mode (up to 8KByte RAM, 2MByte ROM) (default)
        # - 01h = RAM Banking Mode (up to 32KByte RAM, 512KByte ROM)
        # The program may freely switch between both modes, the only limitiation is that only RAM Bank 00h 
        # can be used during Mode 0, and only ROM Banks 00-1Fh can be used during Mode 1.
        if 0x6000 <= address <= 0x7fff:
            self.memory_mode = value & 0b00000001
        
    def read_external_ram_byte(self, address : int) -> int:
        # A000-BFFF - RAM Bank 00-03, if any (Read/Write)
        # This area is used to address external RAM in the cartridge (if any). External RAM is often battery 
        # buffered, allowing to store game positions or high score tables, even if the gameboy is turned off, 
        # or if the cartridge is removed from the gameboy. Available RAM sizes are: 2KByte (at A000-A7FF), 
        # 8KByte (at A000-BFFF), and 32KByte (in form of four 8K banks at A000-BFFF). 
        if self.ram_enabled:
            return self.ram[(self.ram_bank * 0x2000) + (address - 0xa000)]
        else:
            0xff

    def write_external_ram_byte(self, address : int, value : int):
        # A000-BFFF - RAM Bank 00-03, if any (Read/Write)
        # This area is used to address external RAM in the cartridge (if any). External RAM is often battery 
        # buffered, allowing to store game positions or high score tables, even if the gameboy is turned off, 
        # or if the cartridge is removed from the gameboy. Available RAM sizes are: 2KByte (at A000-A7FF), 
        # 8KByte (at A000-BFFF), and 32KByte (in form of four 8K banks at A000-BFFF). 
        if self.ram_enabled:
            self.ram[(self.ram_bank * 0x2000) + (address - 0xa000)] = value
            if self.hasBattery:
                self.battery.save_ram(self.ram)
        

class MBC2(CartridgeType):

    def __init__(self, data: list, hasBattery: bool):
        super().__init__(data, False, hasBattery)
        logging.warning('MBC2 is not implemented')

class MBC3(MBC1):

    def __init__(self, data: list, hasRam: bool, hasBattery: bool, hasTimer: bool):
        super().__init__(data, hasRam, hasBattery)
        logging.warning('MBC3 is not implemented')

class MBC5(CartridgeType):

    def __init__(self, data: list, hasRam: bool, hasBattery: bool):
        super().__init__(data, hasRam, hasBattery)
        logging.warning('MBC5 is not implemented')