#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import struct

class Cartridge:

    def __init__(self, file : str):
        self.data = []
        size = os.stat(file).st_size
        with open(file,'rb') as f:
            for i in range(0,size):
                self.data.append(struct.unpack('<B', f.read(1))[0])

    def rom(self):
        rom_type = self.data[0x147]
        logging.debug('ROM TYPE: {}'.format(rom_type))
        if rom_type in [0x00, 0x08, 0x09]:
            return ROM(self.data)
        if rom_type in [0x01, 0x02, 0x03]:
            return MBC1(self.data)
        if rom_type in [0x05, 0x06]:
            return MBC2(self.data)
        if rom_type in [0xF, 0x10, 0x11, 0x12, 0x13]:
            return MBC3(self.data)
        if rom_type in [0x15, 0x16, 0x17]:
            return MBC4(self.data)
        if rom_type in [0x19, 0x1b, 0x1c, 0x1d, 0x1e]:
            return MBC5(self.data)
        return None

class CartridgeType:

    def __init__(self, data : list):
        self.data = data
        self.external_ram = [0]*0x2000

    def select_data(self) -> list:
        return self.data

    def select_external_ram(self) -> list:
        return self.external_ram

    def read_rom_byte(self, address : int) -> int:
        return self.select_data()[address]

    def write_rom_byte(self, address : int, value : int):
        value = value & 0xff
        self.select_data()[address] = value

    def read_external_ram_byte(self, address : int) -> int:
        return self.select_external_ram()[address - 0xa000]

    def write_external_ram_byte(self, address : int, value : int):
        value = value & 0xff
        self.select_external_ram()[address - 0xa000] = value

class ROM(CartridgeType):

    def __init__(self, data: list):
        super().__init__(data)

    def write_rom_byte(self, address : int, value : int):
        logging.warning('Changing ROM Bank or RAM Bank is not possible in this cartridge type')

class MBC1(CartridgeType):

    def __init__(self, data : list):
        super().__init__(data)
        self.rom_bank = 1
        self.ram_bank = 0
        self.ram_enabled = False
        self.memory_model = 0

    def read_rom_byte(self, address : int) -> int:
        if address < 0x4000:
            return super().read_rom_byte(address)
        point_address = address - 0x4000
        offset = self.rom_bank * 0x4000
        return self.data[offset + point_address]

    def write_rom_byte(self, address : int, value : int):
        if  address < 0x2000:
            self.ram_enabled = (value & 0b1111) == 0b1010
            if not self.ram_enabled:
                #Must save in battery
                pass
        elif address < 0x4000:
            bank = self.rom_bank & 0b01100000
            bank = bank | (value & 0b00011111)
            self.rom_bank = bank
        elif address < 0x6000 and self.memory_model == 0:
            bank = self.rom_bank & 0b00011111
            bank = bank | ((value & 0b11) << 5)
            self.rom_bank = bank
        elif address < 0x6000 and self.memory_model == 1:
            bank = value & 0b11
            self.ram_bank = bank
        elif  address < 0x8000:
            self.memory_model = value & 1

class MBC2(CartridgeType):

    def __init__(self, data : list):
        super().__init__(data)
        logging.warning('MBC2 is not implemented')

class MBC3(CartridgeType):

    def __init__(self, data : list):
        super().__init__(data)
        logging.warning('MBC3 is not implemented')

class MBC4(CartridgeType):

    def __init__(self, data : list):
        super().__init__(data)
        logging.warning('MBC4 is not implemented')

class MBC5(CartridgeType):

    def __init__(self, data : list):
        super().__init__(data)
        logging.warning('MBC5 is not implemented')