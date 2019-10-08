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
        self.ram = []
        self.save_file = save_file

    def load_ram(self, ram: list):
        try:
            size = os.stat(self.save_file).st_size
            with open(self.save_file,'rb') as f:
                for i in range(size):
                    ram[i] = struct.unpack('<B', f.read(1))[0]
        except Exception:
            pass

    def save_ram(self, ram: list):
        with open(self.save_file,'wb') as f:
            for i in range(len(ram)):
                f.write(struct.pack('<B',ram[i]))

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

        self.ram = [0x00] * (0x2000 * self.ram_banks)

        if self.hasBattery:
            self.battery = Battery('rom.sav')
            self.battery.load_ram(self.ram)


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

class MBC1(CartridgeType):

    def __init__(self, data: list, hasRam: bool, hasBattery: bool):
        super().__init__(data, hasRam, hasBattery)
        self.selected_ram_bank = 0
        self.selected_rom_bank = 1
        self.memory_model = 0
        self.cached_rom_bank_for_0x0000 = -1
        self.cached_ram_bank_for_0x4000 = -1
        self.ram_write_enabled = False

    def get_rom_bank_for_0x0000(self):
        if self.cached_rom_bank_for_0x0000 == -1:
            if self.memory_model == 0:
                self.cached_rom_bank_for_0x0000 = 0
            else:
                bank = self.selected_ram_bank << 5
                bank %= self.rom_banks
                self.cached_rom_bank_for_0x0000 = bank
        return self.cached_rom_bank_for_0x0000

    def get_rom_bank_for_0x4000(self):
        if self.cached_ram_bank_for_0x4000 == -1:
            bank = self.selected_rom_bank
            if bank % 0x20 == 0:
                bank += 1
            if self.memory_model == 1:
                bank &= 0b00011111
                bank |= (self.selected_ram_bank << 5)
            bank %= self.rom_banks
            self.cached_ram_bank_for_0x4000 = bank
        return self.cached_ram_bank_for_0x4000

    def get_rom_byte(self, bank, address):
        cartOffset = bank * 0x4000 + address
        if cartOffset < len(self.data):
            return self.data[cartOffset]
        else:
            return 0xff

    def get_ram_address(self, address):
        if self.memory_model == 0:
            return address - 0xa000
        else:
            return (self.selected_ram_bank % self.ram_banks) * 0x2000 + (address - 0xa000)
        
    def read_rom_byte(self, address : int) -> int:
        if address < 0x4000:
            return self.get_rom_byte(self.get_rom_bank_for_0x0000(), address)
        else:
            return self.get_rom_byte(self.get_rom_bank_for_0x4000(), address - 0x4000)

    def write_rom_byte(self, address : int, value : int):
        if address < 0x2000:
            self.ram_write_enabled = (value & 0b1111) == 0b1010
            if not self.ram_write_enabled:
                self.battery.save_ram(self.ram)
        elif 0x2000 <= address < 0x4000:
            bank = self.selected_rom_bank & 0b01100000
            bank = bank | (value & 0b00011111)
            self.selected_rom_bank  = bank
            self.cached_rom_bank_for_0x0000 = -1
            self.cached_ram_bank_for_0x4000 = -1
        elif 0x4000 <= address < 0x6000 and self.memory_model == 0:
            bank = self.selected_rom_bank & 0b00011111
            bank = bank | ((value & 0b11) << 5)
            self.selected_rom_bank  = bank
            self.cached_rom_bank_for_0x0000 = -1
            self.cached_ram_bank_for_0x4000 = -1
        elif 0x4000 <= address < 0x6000 and self.memory_model == 1:
            bank = value & 0b11
            self.selected_ram_bank = bank
            self.cached_rom_bank_for_0x0000 = -1
            self.cached_ram_bank_for_0x4000 = -1
        elif 0x6000 <= address < 0x8000:
            self.memory_model = value & 1
            self.cached_rom_bank_for_0x0000 = -1
            self.cached_ram_bank_for_0x4000 = -1
        
    def read_external_ram_byte(self, address : int) -> int:
        if self.ram_write_enabled:
            ram_address = self.get_ram_address(address)
            if ram_address < len(self.ram):
                return self.ram[ram_address]
            else:
                return 0xff
        else:
            return 0xff

    def write_external_ram_byte(self, address : int, value : int):
        if self.ram_write_enabled:
            ram_address = self.get_ram_address(address)
            if ram_address < len(self.ram):
                self.ram[ram_address] = value
        

class MBC2(CartridgeType):

    def __init__(self, data: list, hasBattery: bool):
        super().__init__(data, False, hasBattery)
        logging.warning('MBC2 is not implemented')

class MBC3(CartridgeType):

    def __init__(self, data: list, hasRam: bool, hasBattery: bool, hasTimer: bool):
        super().__init__(data, hasRam, hasBattery)
        self.selected_ram_bank = 0
        self.selected_rom_bank = 1
        self.memory_model = 0
        self.cached_rom_bank_for_0x0000 = -1
        self.cached_ram_bank_for_0x4000 = -1
        self.ram_write_enabled = False

    def get_rom_bank_for_0x0000(self):
        if self.cached_rom_bank_for_0x0000 == -1:
            if self.memory_model == 0:
                self.cached_rom_bank_for_0x0000 = 0
            else:
                bank = self.selected_ram_bank << 5
                bank %= self.rom_banks
                self.cached_rom_bank_for_0x0000 = bank
        return self.cached_rom_bank_for_0x0000

    def get_rom_bank_for_0x4000(self):
        if self.cached_ram_bank_for_0x4000 == -1:
            bank = self.selected_rom_bank
            if bank % 0x20 == 0:
                bank += 1
            if self.memory_model == 1:
                bank &= 0b00011111
                bank |= (self.selected_ram_bank << 5)
            bank %= self.rom_banks
            self.cached_ram_bank_for_0x4000 = bank
        return self.cached_ram_bank_for_0x4000

    def get_rom_byte(self, bank, address):
        cartOffset = bank * 0x4000 + address
        if cartOffset < len(self.data):
            return self.data[cartOffset]
        else:
            return 0xff

    def get_ram_address(self, address):
        if self.memory_model == 0:
            return address - 0xa000
        else:
            return (self.selected_ram_bank % self.ram_banks) * 0x2000 + (address - 0xa000)
        
    def read_rom_byte(self, address : int) -> int:
        if address < 0x4000:
            return self.get_rom_byte(self.get_rom_bank_for_0x0000(), address)
        else:
            return self.get_rom_byte(self.get_rom_bank_for_0x4000(), address - 0x4000)

    def write_rom_byte(self, address : int, value : int):
        if address < 0x2000:
            self.ram_write_enabled = (value & 0b1111) == 0b1010
            if not self.ram_write_enabled:
                self.battery.save_ram(self.ram)
        elif 0x2000 <= address < 0x4000:
            bank = self.selected_rom_bank & 0b01100000
            bank = bank | (value & 0b00011111)
            self.selected_rom_bank  = bank
            self.cached_rom_bank_for_0x0000 = -1
            self.cached_ram_bank_for_0x4000 = -1
        elif 0x4000 <= address < 0x6000 and self.memory_model == 0:
            bank = self.selected_rom_bank & 0b00011111
            bank = bank | ((value & 0b11) << 5)
            self.selected_rom_bank  = bank
            self.cached_rom_bank_for_0x0000 = -1
            self.cached_ram_bank_for_0x4000 = -1
        elif 0x4000 <= address < 0x6000 and self.memory_model == 1:
            bank = value & 0b11
            self.selected_ram_bank = bank
            self.cached_rom_bank_for_0x0000 = -1
            self.cached_ram_bank_for_0x4000 = -1
        elif 0x6000 <= address < 0x8000:
            self.memory_model = value & 1
            self.cached_rom_bank_for_0x0000 = -1
            self.cached_ram_bank_for_0x4000 = -1
        
    def read_external_ram_byte(self, address : int) -> int:
        if self.ram_write_enabled:
            ram_address = self.get_ram_address(address)
            if ram_address < len(self.ram):
                return self.ram[ram_address]
            else:
                return 0xff
        else:
            return 0xff

    def write_external_ram_byte(self, address : int, value : int):
        if self.ram_write_enabled:
            ram_address = self.get_ram_address(address)
            if ram_address < len(self.ram):
                self.ram[ram_address] = value

class MBC5(CartridgeType):

    def __init__(self, data: list, hasRam: bool, hasBattery: bool):
        super().__init__(data, hasRam, hasBattery)
        self.selected_ram_bank = 0
        self.selected_rom_bank = 1
        self.memory_model = 0
        self.cached_rom_bank_for_0x0000 = -1
        self.cached_ram_bank_for_0x4000 = -1
        self.ram_write_enabled = False

    def get_rom_bank_for_0x0000(self):
        if self.cached_rom_bank_for_0x0000 == -1:
            if self.memory_model == 0:
                self.cached_rom_bank_for_0x0000 = 0
            else:
                bank = self.selected_ram_bank << 5
                bank %= self.rom_banks
                self.cached_rom_bank_for_0x0000 = bank
        return self.cached_rom_bank_for_0x0000

    def get_rom_bank_for_0x4000(self):
        if self.cached_ram_bank_for_0x4000 == -1:
            bank = self.selected_rom_bank
            if bank % 0x20 == 0:
                bank += 1
            if self.memory_model == 1:
                bank &= 0b00011111
                bank |= (self.selected_ram_bank << 5)
            bank %= self.rom_banks
            self.cached_ram_bank_for_0x4000 = bank
        return self.cached_ram_bank_for_0x4000

    def get_rom_byte(self, bank, address):
        cartOffset = bank * 0x4000 + address
        if cartOffset < len(self.data):
            return self.data[cartOffset]
        else:
            return 0xff

    def get_ram_address(self, address):
        if self.memory_model == 0:
            return address - 0xa000
        else:
            return (self.selected_ram_bank % self.ram_banks) * 0x2000 + (address - 0xa000)
        
    def read_rom_byte(self, address : int) -> int:
        if address < 0x4000:
            return self.get_rom_byte(self.get_rom_bank_for_0x0000(), address)
        else:
            return self.get_rom_byte(self.get_rom_bank_for_0x4000(), address - 0x4000)

    def write_rom_byte(self, address : int, value : int):
        if address < 0x2000:
            self.ram_write_enabled = (value & 0b1111) == 0b1010
            if not self.ram_write_enabled:
                self.battery.save_ram(self.ram)
        elif 0x2000 <= address < 0x4000:
            bank = self.selected_rom_bank & 0b01100000
            bank = bank | (value & 0b00011111)
            self.selected_rom_bank  = bank
            self.cached_rom_bank_for_0x0000 = -1
            self.cached_ram_bank_for_0x4000 = -1
        elif 0x4000 <= address < 0x6000 and self.memory_model == 0:
            bank = self.selected_rom_bank & 0b00011111
            bank = bank | ((value & 0b11) << 5)
            self.selected_rom_bank  = bank
            self.cached_rom_bank_for_0x0000 = -1
            self.cached_ram_bank_for_0x4000 = -1
        elif 0x4000 <= address < 0x6000 and self.memory_model == 1:
            bank = value & 0b11
            self.selected_ram_bank = bank
            self.cached_rom_bank_for_0x0000 = -1
            self.cached_ram_bank_for_0x4000 = -1
        elif 0x6000 <= address < 0x8000:
            self.memory_model = value & 1
            self.cached_rom_bank_for_0x0000 = -1
            self.cached_ram_bank_for_0x4000 = -1
        
    def read_external_ram_byte(self, address : int) -> int:
        if self.ram_write_enabled:
            ram_address = self.get_ram_address(address)
            if ram_address < len(self.ram):
                return self.ram[ram_address]
            else:
                return 0xff
        else:
            return 0xff

    def write_external_ram_byte(self, address : int, value : int):
        if self.ram_write_enabled:
            ram_address = self.get_ram_address(address)
            if ram_address < len(self.ram):
                self.ram[ram_address] = value
