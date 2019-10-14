#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/The_Cartridge_Header
# - https://gbdev.gg8.se/wiki/articles/Memory_Bank_Controllers

import datetime
import logging
import os
import struct

class CartridgeHeader:
    # 0100-0103 - Entry Point
    # After displaying the Nintendo Logo, the built-in boot procedure jumps to this address (100h), 
    # which should then jump to the actual main program in the cartridge. Usually this 4 byte area 
    # contains a NOP instruction, followed by a JP 0150h instruction. But not always. 
    ENTRY_POINT = 0x0100

    # 0104-0133 - Nintendo Logo
    # These bytes define the bitmap of the Nintendo logo that is displayed when the gameboy gets 
    # turned on. The hexdump of this bitmap is:
    #     CE ED 66 66 CC 0D 00 0B 03 73 00 83 00 0C 00 0D
    #     00 08 11 1F 88 89 00 0E DC CC 6E E6 DD DD D9 99
    #     BB BB 67 63 6E 0E EC CC DD DC 99 9F BB B9 33 3E
    # The Game Boy's boot procedure verifies the content of this bitmap (after it has displayed it),
    # and LOCKS ITSELF UP if these bytes are incorrect. A CGB verifies only the first 18h bytes of 
    # the bitmap, but others (for example a pocket gameboy) verify all 30h bytes. 
    NINTENDO_LOGO = 0x0104
    
    # 0134-0143 - Title
    # Title of the game in UPPER CASE ASCII. If it is less than 16 characters then the remaining bytes 
    # are filled with 00's. When inventing the CGB, Nintendo has reduced the length of this area to 
    # 15 characters, and some months later they had the fantastic idea to reduce it to 11 characters 
    # only. The new meaning of the ex-title bytes is described below. 
    TITLE = 0x0134

    # 013F-0142 - Manufacturer Code
    # In older cartridges this area has been part of the Title (see above), in newer cartridges this 
    # area contains an 4 character uppercase manufacturer code. Purpose and Deeper Meaning unknown. 
    MANUFACTURER_CODE = 0x013f

    # 0143 - CGB Flag
    # In older cartridges this byte has been part of the Title (see above). In CGB cartridges the 
    # upper bit is used to enable CGB functions. This is required, otherwise the CGB switches itself 
    # into Non-CGB-Mode. Typical values are:
    #   80h - Game supports CGB functions, but works on old gameboys also.
    #   C0h - Game works on CGB only (physically the same as 80h).
    # Values with Bit 7 set, and either Bit 2 or 3 set, will switch the gameboy into a special 
    # non-CGB-mode with uninitialized palettes. Purpose unknown, eventually this has been supposed 
    # to be used to colorize monochrome games that include fixed palette data at a special location 
    # in ROM. 
    CGB_FLAG = 0x0143

    # 0144-0145 - New Licensee Code
    # Specifies a two character ASCII licensee code, indicating the company or publisher of the game. 
    # These two bytes are used in newer games only (games that have been released after the SGB has 
    # been invented). Older games are using the header entry at 014B instead. 
    NEW_LICENSE_CODE = 0x0144

    # 0146 - SGB Flag
    # Specifies whether the game supports SGB functions, common values are: 
    #   00h = No SGB functions (Normal Gameboy or CGB only game)
    #   03h = Game supports SGB functions
    # The SGB disables its SGB functions if this byte is set to another value than 03h. 
    SGB_FLAG = 0x0146

    # 0147 - Cartridge Type
    # Specifies which Memory Bank Controller (if any) is used in the cartridge, and if further external 
    # hardware exists in the cartridge. 
    # 00h  ROM ONLY                 19h  MBC5
    # 01h  MBC1                     1Ah  MBC5+RAM
    # 02h  MBC1+RAM                 1Bh  MBC5+RAM+BATTERY
    # 03h  MBC1+RAM+BATTERY         1Ch  MBC5+RUMBLE
    # 05h  MBC2                     1Dh  MBC5+RUMBLE+RAM
    # 06h  MBC2+BATTERY             1Eh  MBC5+RUMBLE+RAM+BATTERY
    # 08h  ROM+RAM                  20h  MBC6
    # 09h  ROM+RAM+BATTERY          22h  MBC7+SENSOR+RUMBLE+RAM+BATTERY
    # 0Bh  MMM01
    # 0Ch  MMM01+RAM
    # 0Dh  MMM01+RAM+BATTERY
    # 0Fh  MBC3+TIMER+BATTERY
    # 10h  MBC3+TIMER+RAM+BATTERY   FCh  POCKET CAMERA
    # 11h  MBC3                     FDh  BANDAI TAMA5
    # 12h  MBC3+RAM                 FEh  HuC3
    # 13h  MBC3+RAM+BATTERY         FFh  HuC1+RAM+BATTERY
    CARTRIDGE_TYPE = 0x0147

    # 0148 - ROM Size
    # Specifies the ROM Size of the cartridge. Typically calculated as "32KB shl N". 
    # 00h -  32KByte (no ROM banking)
    # 01h -  64KByte (4 banks)
    # 02h - 128KByte (8 banks)
    # 03h - 256KByte (16 banks)
    # 04h - 512KByte (32 banks)
    # 05h -   1MByte (64 banks)  - only 63 banks used by MBC1
    # 06h -   2MByte (128 banks) - only 125 banks used by MBC1
    # 07h -   4MByte (256 banks)
    # 08h -   8MByte (512 banks)
    # 52h - 1.1MByte (72 banks)
    # 53h - 1.2MByte (80 banks)
    # 54h - 1.5MByte (96 banks)
    ROM_SIZE = 0x0148

    # 0149 - RAM Size
    # Specifies the size of the external RAM in the cartridge (if any). 
    # 00h - None
    # 01h - 2 KBytes
    # 02h - 8 Kbytes
    # 03h - 32 KBytes (4 banks of 8KBytes each)
    # 04h - 128 KBytes (16 banks of 8KBytes each)
    # 05h - 64 KBytes (8 banks of 8KBytes each)
    # When using a MBC2 chip 00h must be specified in this entry, even though the MBC2 includes a 
    # built-in RAM of 512 x 4 bits.
    RAM_SIZE = 0x0149

    # 014A - Destination Code
    # Specifies if this version of the game is supposed to be sold in Japan, or anywhere else. 
    # Only two values are defined. 
    # 00h - Japanese
    # 01h - Non-Japanese
    DESTINATION_CODE = 0x014a

    # 014B - Old Licensee Code
    # Specifies the games company/publisher code in range 00-FFh. A value of 33h signalizes 
    # that the New License Code in header bytes 0144-0145 is used instead. (Super GameBoy 
    # functions won't work if <> $33.) 
    OLD_LICENSE_CODE = 0x014b
    
    # 014C - Mask ROM Version number
    # Specifies the version number of the game. That is usually 00h. 
    MASK_ROM_VERSION = 0x014c

    # 014D - Header Checksum
    # Contains an 8 bit checksum across the cartridge header bytes 0134-014C. The checksum is 
    # calculated as follows:
    #     x=0:FOR i=0134h TO 014Ch:x=x-MEM[i]-1:NEXT
    # The lower 8 bits of the result must be the same than the value in this entry. The GAME 
    # WON'T WORK if this checksum is incorrect. 
    HEADER_CHECKSUM = 0x014d

    # 014E-014F - Global Checksum
    # Contains a 16 bit checksum (upper byte first) across the whole cartridge ROM. Produced 
    # by adding all bytes of the cartridge (except for the two checksum bytes). The Gameboy 
    # doesn't verify this checksum. 
    GLOBAL_CHECKSUM = 0x014e


class Cartridge:

    def __init__(self, file : str):
        self.data = []
        size = os.stat(file).st_size
        with open(file,'rb') as f:
            for i in range(size):
                self.data.append(struct.unpack('<B', f.read(1))[0])

    def rom(self):
        rom_type = self.data[CartridgeHeader.CARTRIDGE_TYPE]
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
            return ram


    def save_ram(self, ram: list):
        with open(self.save_file,'wb') as f:
            f.write(bytes(ram))

class CartridgeType:

    def __init__(self, data : list, hasRam: bool, hasBattery: bool):
        self.data = data
        self.hasRam = hasRam
        self.hasBattery = hasBattery

        rom_banks_reg = self.data[CartridgeHeader.ROM_SIZE]
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

        ram_banks_reg = self.data[CartridgeHeader.RAM_SIZE]
        self.ram_banks = {
            0x00: 0,
            0x01: 1,
            0x02: 1,
            0x03: 4,
            0x04: 16
        }.get(ram_banks_reg, 0)

        self.ram = [0xff]*(0x2000 * self.ram_banks)

        if self.hasBattery:
            save_file_name = bytes(self.data[CartridgeHeader.TITLE:(CartridgeHeader.TITLE + 15)]).decode().rstrip('\x00')+".sav"
            self.battery = Battery(save_file_name)
            self.ram = self.battery.load_ram(self.ram)


    def read_rom_byte(self, address : int) -> int:
        return self.data[address]

    def write_rom_byte(self, address : int, value : int):
        pass

    def read_external_ram_byte(self, address : int) -> int:
        if self.hasRam and self.ram is not None:
            return self.ram[address - 0xa000] & 0xff
        return 0xff

    def write_external_ram_byte(self, address : int, value : int):
        if self.hasRam:
            self.ram[address - 0xa000] = value & 0xff

# None (32KByte ROM only)
# Small games of not more than 32KBytes ROM do not require a MBC chip 
# for ROM banking. The ROM is directly mapped to memory at 0000-7FFFh. 
# Optionally up to 8KByte of RAM could be connected at A000-BFFF, even 
# though that could require a tiny MBC-like circuit, but no real MBC 
# chip. 
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
        return self.data[(0x4000 * (self.rom_bank % self.rom_banks)) + (address - 0x4000)]

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
            if self.hasBattery and not self.ram_enabled:
                self.battery.save_ram(self.ram)

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
            prev_mode = self.memory_mode
            self.memory_mode = value & 0b00000001
            if prev_mode != self.memory_mode:
                if self.memory_mode == MBC1.RAM_BANKING_MODE:
                    self.ram_bank = ( self.rom_bank >> 5 ) & 0b00000011
                    self.rom_bank = self.rom_bank & 0b00011111
                else:
                    self.rom_bank = self.rom_bank | ((self.ram_bank & 0b00000011) << 5)
                    self.ram_bank = 0
        
    def read_external_ram_byte(self, address : int) -> int:
        # A000-BFFF - RAM Bank 00-03, if any (Read/Write)
        # This area is used to address external RAM in the cartridge (if any). External RAM is often battery 
        # buffered, allowing to store game positions or high score tables, even if the gameboy is turned off, 
        # or if the cartridge is removed from the gameboy. Available RAM sizes are: 2KByte (at A000-A7FF), 
        # 8KByte (at A000-BFFF), and 32KByte (in form of four 8K banks at A000-BFFF). 
        if self.ram_enabled:
            return self.ram[((self.ram_bank % self.ram_banks) * 0x2000) + (address - 0xa000)]
        return 0xff

    def write_external_ram_byte(self, address : int, value : int):
        # A000-BFFF - RAM Bank 00-03, if any (Read/Write)
        # This area is used to address external RAM in the cartridge (if any). External RAM is often battery 
        # buffered, allowing to store game positions or high score tables, even if the gameboy is turned off, 
        # or if the cartridge is removed from the gameboy. Available RAM sizes are: 2KByte (at A000-A7FF), 
        # 8KByte (at A000-BFFF), and 32KByte (in form of four 8K banks at A000-BFFF). 
        if self.ram_enabled:
            self.ram[((self.ram_bank % self.ram_banks) * 0x2000) + (address - 0xa000)] = value
        
# MBC2 (max 256KByte ROM and 512x4 bits RAM)
class MBC2(CartridgeType):

    def __init__(self, data: list, hasBattery: bool):
        super().__init__(data, False, hasBattery)
        logging.warning('MBC2 is not implemented')

# MBC3 (max 2MByte ROM and/or 64KByte RAM and Timer)
# Beside for the ability to access up to 2MB ROM (128 banks), and 64KB RAM (8 banks), the MBC3 also includes 
# a built-in Real Time Clock (RTC). The RTC requires an external 32.768 kHz Quartz Oscillator, and an external 
# battery (if it should continue to tick when the gameboy is turned off).
class MBC3(CartridgeType):

    def __init__(self, data: list, hasRam: bool, hasBattery: bool, hasTimer: bool):
        super().__init__(data, hasRam, hasBattery)
        self.ram_bank = 0
        self.rom_bank = 1
        self.ram_enabled = False
        self.has_timer = hasTimer
        self.rtc_register_mode = False
        self.rtc_register_selected = 0
      
    def read_rom_byte(self, address : int) -> int:
        # 0000-3FFF - ROM Bank 00 (Read Only)
        # Same as for MBC1. 
        if address < 0x4000:
            return self.data[address]
        # 4000-7FFF - ROM Bank 01-7F (Read Only)
        # Same as for MBC1, except that accessing banks 20h, 40h, and 60h is supported now
        if self.rom_bank == 0:
            self.rom_bank += 1
        return self.data[(0x4000 * (self.rom_bank % self.rom_banks)) + (address - 0x4000)]

    def write_rom_byte(self, address : int, value : int):
        # 0000-1FFF - RAM and Timer Enable (Write Only)
        # Mostly the same as for MBC1, a value of 0Ah will enable reading and writing to external RAM - and to 
        # the RTC Registers! A value of 00h will disable either. 
        if 0x0000 <= address <= 0x1fff:
            self.ram_enabled = (value & 0x0f == 0x0a)
            if self.hasBattery and not self.ram_enabled:
                self.battery.save_ram(self.ram)

        # 2000-3FFF - ROM Bank Number (Write Only)
        # Same as for MBC1, except that the whole 7 bits of the ROM Bank Number are written directly to this address. 
        # As for the MBC1, writing a value of 00h, will select Bank 01h instead. All other values 01-7Fh select the 
        # corresponding ROM Banks. 
        if 0x2000 <= address <= 0x3fff:
            self.rom_bank = value & 0b01111111
            if self.rom_bank == 0:
                self.rom_bank += 1

        # 4000-5FFF - RAM Bank Number - or - RTC Register Select (Write Only)
        # As for the MBC1s RAM Banking Mode, writing a value in range for 00h-07h maps the corresponding external 
        # RAM Bank (if any) into memory at A000-BFFF. When writing a value of 08h-0Ch, this will map the corresponding 
        # RTC register into memory at A000-BFFF. That register could then be read/written by accessing any address in 
        # that area, typically that is done by using address A000. 
        if 0x4000 <= address <= 0x5fff:
            if 0x08 <= value <= 0x0c:
                self.rtc_register_mode = True
                self.rtc_register_selected = value
            elif 0x00 <= value <= 0x07:
                self.rtc_register_mode = False
                self.ram_bank = value

        
        # 6000-7FFF - Latch Clock Data (Write Only)
        # When writing 00h, and then 01h to this register, the current time becomes latched into the RTC registers. 
        # The latched data will not change until it becomes latched again, by repeating the write 00h->01h procedure. 
        # This is supposed for <reading> from the RTC registers. This can be proven by reading the latched (frozen) time 
        # from the RTC registers, and then unlatch the registers to show the clock itself continues to tick in background. 
        if 0x6000 <= address <= 0x7fff:
            pass #unimplemented latch clock
        
    def read_external_ram_byte(self, address : int) -> int:
        # A000-BFFF - RAM Bank 00-07, if any (Read/Write)
        # A000-BFFF - RTC Register 08-0C (Read/Write)
        # Depending on the current Bank Number/RTC Register selection (see below), this memory space is used to access 
        # an 8KByte external RAM Bank, or a single RTC Register.
        if self.has_timer and self.rtc_register_mode:
            now = datetime.datetime.now()
            # The Clock Counter Registers
            # 08h  RTC S   Seconds   0-59 (0-3Bh)
            # 09h  RTC M   Minutes   0-59 (0-3Bh)
            # 0Ah  RTC H   Hours     0-23 (0-17h)
            # 0Bh  RTC DL  Lower 8 bits of Day Counter (0-FFh)
            # 0Ch  RTC DH  Upper 1 bit of Day Counter, Carry Bit, Halt Flag
            #       Bit 0  Most significant bit of Day Counter (Bit 8)
            #       Bit 6  Halt (0=Active, 1=Stop Timer)
            #       Bit 7  Day Counter Carry Bit (1=Counter Overflow)
            if self.rtc_register_selected == 0x08:
                return now.second & 0xff
            if self.rtc_register_selected == 0x09:
                return now.minute & 0xff
            if self.rtc_register_selected == 0x0a:
                return now.hour & 0xff
            if self.rtc_register_selected == 0x0b:
                return now.timetuple().tm_yday & 0xff
            if self.rtc_register_selected == 0x0c:
                if now.timetuple().tm_yday > 0xff:
                    return 0x01
                return 0x00 

        if self.ram_enabled:
            return self.ram[((self.ram_bank % self.ram_banks) * 0x2000) + (address - 0xa000)]
        return 0xff

    def write_external_ram_byte(self, address : int, value : int):
        # A000-BFFF - RAM Bank 00-07, if any (Read/Write)
        # A000-BFFF - RTC Register 08-0C (Read/Write)
        # Depending on the current Bank Number/RTC Register selection (see below), this memory space is used to access 
        # an 8KByte external RAM Bank, or a single RTC Register.
        if self.has_timer and self.rtc_register_mode:
            pass #unimplemented
        elif self.ram_enabled:
            self.ram[((self.ram_bank % self.ram_banks) * 0x2000) + (address - 0xa000)] = value


# MBC5 (max 8MByte ROM and/or 128KByte RAM)
class MBC5(CartridgeType):

    def __init__(self, data: list, hasRam: bool, hasBattery: bool):
        super().__init__(data, hasRam, hasBattery)
        logging.warning('MBC5 is not implemented')
