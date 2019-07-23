#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import struct

class Cartridge:

    def __init__(self, file):
        self.data = []
        size = os.stat(file).st_size
        with open(file,'rb') as f:
            for i in range(0,size):
                self.data.append(struct.unpack('<B', f.read(1))[0])

    def rom(self):
        rom_type = self.data[0x147]
        logging.info('ROM TYPE: {}'.format(rom_type))
        if rom_type in [0x00, 0x08, 0x09]:
            return ROM(self.data)
        if rom_type in [0x01, 0x02, 0x03]:
            return MB1(self.data)
        if rom_type in [0x05, 0x06]:
            return MB2(self.data)
        if rom_type in [0xF, 0x10, 0x11, 0x12, 0x13]:
            return MB3(self.data)
        if rom_type in [0x15, 0x16, 0x17]:
            return MB4(self.data)
        if rom_type in [0x19, 0x1b, 0x1c, 0x1d, 0x1e]:
            return MB5(self.data)

class CartridgeType:

    def __init__(self, data):
        self.data = data
        self.external_ram = [0]*0x2000

    def select_data(self):
        return self.data

    def select_external_ram(self):
        return self.external_ram

    def read_rom_byte(self, address):
        return self.select_data()[address]

    def write_rom_byte(self, address, value):
        pass

    def read_external_ram_byte(self, address):
        return self.select_external_ram()[address - 0xa000]

    def write_external_ram_byte(self, address, value):
        value = value & 0xff
        self.select_external_ram()[address - 0xa000] = value

class ROM(CartridgeType):

    def __init__(self, data):
        super().__init__(data)

class MB1(CartridgeType):

    def __init__(self, data):
        super().__init__(data)

class MB2(CartridgeType):

    def __init__(self, data):
        super().__init__(data)

class MB3(CartridgeType):

    def __init__(self, data):
        super().__init__(data)

class MB4(CartridgeType):

    def __init__(self, data):
        super().__init__(data)

class MB5(CartridgeType):

    def __init__(self, data):
        super().__init__(data)