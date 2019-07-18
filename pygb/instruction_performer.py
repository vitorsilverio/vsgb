#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygb.byte_operations import signed_value

class InstructionPerformer:

    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = cpu.mmu
        self.registers = cpu.registers


    def perform_instruction(self, instruction):
        if instruction == 0x00:
            print('{}: NOP'.format(hex(self.registers.pc -1)))
            return 4
        if instruction == 0x01:
            word = self.mmu.read_word(self.registers.pc)
            self.registers.pc += 2
            self.registers.set_bc(word) 
            print('{}: LD BC, {}'.format(hex(self.registers.pc-3), hex(word)))
            return 12
        if instruction == 0x02:
            self.mmu.write_byte(self.registers.get_bc, self.registers.a)
            print('{}: LD (BC), A'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x06:
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            self.registers.b = byte 
            print('{}: LD B, {}'.format(hex(self.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0x08:
            word = self.mmu.read_word(self.registers.pc)
            self.registers.pc += 2
            self.mmu.write_word(word, self.registers.sp)
            print('{}: LD ({}), SP'.format(hex(self.registers.pc-2), hex(word)))
            return 20
        if instruction == 0x0a:
            self.registers.a = self.mmu.read_byte(self.registers.get_bc())
            print('{}: LD A, (BC)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x0e:
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            self.registers.c = byte 
            print('{}: LD C, {}'.format(hex(self.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0x11:
            word = self.mmu.read_word(self.registers.pc)
            self.registers.pc += 2
            self.registers.set_de(word) 
            print('{}: LD DE, {}'.format(hex(self.registers.pc-3), hex(word)))
            return 12
        if instruction == 0x12:
            self.mmu.write_byte(self.registers.get_de, self.registers.a)
            print('{}: LD (DE), A'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x16:
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            self.registers.d = byte 
            print('{}: LD D, {}'.format(hex(self.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0x1a:
            self.registers.a = self.mmu.read_byte(self.registers.get_de())
            print('{}: LD A, (DE)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x1e:
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            self.registers.e = byte 
            print('{}: LD E, {}'.format(hex(self.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0x21:
            word = self.mmu.read_word(self.registers.pc)
            self.registers.pc += 2
            self.registers.set_hl(word) 
            print('{}: LD HL, {}'.format(hex(self.registers.pc-3), hex(word)))
            return 12
        if instruction == 0x22:
            self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
            self.registers.set_hl(self.registers.get_hl()+1)
            print('{}: LD (HL+), A'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x26:
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            self.registers.h = byte 
            print('{}: LD H, {}'.format(hex(self.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0x2a:
            self.registers.a = self.mmu.read_byte(self.registers.get_hl())
            self.registers.set_hl(self.registers.get_hl()+1)
            print('{}: LD A, (HL+)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x2e:
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            self.registers.l = byte 
            print('{}: LD L, {}'.format(hex(self.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0x31:
            word = self.mmu.read_word(self.registers.pc)
            self.registers.pc += 2
            self.registers.sp = word
            print('{}: LD SP, {}'.format(hex(self.registers.pc-3), hex(word)))
            return 12
        if instruction == 0x32:
            self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
            self.registers.set_hl(self.registers.get_hl()-1)
            print('{}: LD (HL-), A'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x36:
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            self.mmu.write_byte(self.registers.get_hl(),byte)
            print('{}: LD (HL), {}'.format(hex(self.registers.pc-2),hex(byte)))
            return 12
        if instruction == 0x3a:
            self.registers.a = self.mmu.read_byte(self.registers.get_hl())
            self.registers.set_hl(self.registers.get_hl()-1)
            print('{}: LD A, (HL-)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x3e:
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            self.registers.a = byte
            print('{}: LD A, {}'.format(hex(self.registers.pc-2),hex(byte)))
            return 8
        if instruction == 0x40:
            print('{}: LD B, B'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x41:
            self.registers.b = self.registers.c
            print('{}: LD B, C'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x42:
            self.registers.b = self.registers.d
            print('{}: LD B, D'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x43:
            self.registers.b = self.registers.e
            print('{}: LD B, E'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x44:
            self.registers.b = self.registers.h
            print('{}: LD B, H'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x45:
            self.registers.b = self.registers.l
            print('{}: LD B, L'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x46:
            self.registers.b = self.mmu.read_byte(self.registers.get_hl())
            print('{}: LD B, (HL)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x47:
            self.registers.b = self.registers.a
            print('{}: LD B, A'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x48:
            self.registers.c = self.registers.b
            print('{}: LD C, B'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x49:
            print('{}: LD C, C'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x4a:
            self.registers.c = self.registers.d
            print('{}: LD C, D'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x4b:
            self.registers.c = self.registers.e
            print('{}: LD C, E'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x4c:
            self.registers.c = self.registers.h
            print('{}: LD C, H'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x4d:
            self.registers.c = self.registers.l
            print('{}: LD C, L'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x4e:
            self.registers.c = self.mmu.read_byte(self.registers.get_hl())
            print('{}: LD C, (HL)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x4f:
            self.registers.c = self.registers.a
            print('{}: LD C, A'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x50:
            self.registers.d = self.registers.b
            print('{}: LD D, B'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x51:
            self.registers.d = self.registers.c
            print('{}: LD D, C'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x52:
            print('{}: LD D, D'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x53:
            self.registers.d = self.registers.e
            print('{}: LD D, E'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x54:
            self.registers.d = self.registers.h
            print('{}: LD D, H'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x55:
            self.registers.d = self.registers.l
            print('{}: LD D, L'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x56:
            self.registers.d = self.mmu.read_byte(self.registers.get_hl())
            print('{}: LD D, (HL)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x57:
            self.registers.d = self.registers.a
            print('{}: LD D, A'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x58:
            self.registers.e = self.registers.b
            print('{}: LD E, B'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x59:
            self.registers.e = self.registers.c
            print('{}: LD E, C'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x5a:
            self.registers.e = self.registers.d
            print('{}: LD E, D'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x5b:
            print('{}: LD E, E'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x5c:
            self.registers.e = self.registers.h
            print('{}: LD E, H'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x5d:
            self.registers.e = self.registers.l
            print('{}: LD E, L'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x5e:
            self.registers.e = self.mmu.read_byte(self.registers.get_hl())
            print('{}: LD E, (HL)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x5f:
            self.registers.e = self.registers.a
            print('{}: LD E, A'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x60:
            self.registers.h = self.registers.b
            print('{}: LD H, B'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x61:
            self.registers.h = self.registers.c
            print('{}: LD H, C'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x62:
            self.registers.h = self.registers.d
            print('{}: LD H, D'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x63:
            self.registers.h = self.registers.e
            print('{}: LD H, E'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x64:
            print('{}: LD H, H'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x65:
            self.registers.h = self.registers.l
            print('{}: LD H, L'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x66:
            self.registers.h = self.mmu.read_byte(self.registers.get_hl())
            print('{}: LD H, (HL)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x67:
            self.registers.h = self.registers.a
            print('{}: LD H, A'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x68:
            self.registers.l = self.registers.b
            print('{}: LD L, B'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x69:
            self.registers.l = self.registers.c
            print('{}: LD L, C'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x6a:
            self.registers.l = self.registers.d
            print('{}: LD L, D'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x6b:
            self.registers.l = self.registers.e
            print('{}: LD L, E'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x6c:
            self.registers.l = self.registers.h
            print('{}: LD L, H'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x6d:
            print('{}: LD L, L'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x6e:
            self.registers.l = self.mmu.read_byte(self.registers.get_hl())
            print('{}: LD L, (HL)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x6f:
            self.registers.l = self.registers.a
            print('{}: LD L, A'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x70:
            self.mmu.write_byte(self.registers.get_hl(),self.registers.b)
            print('{}: LD (HL), B'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x71:
            self.mmu.write_byte(self.registers.get_hl(),self.registers.c)
            print('{}: LD (HL), C'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x72:
            self.mmu.write_byte(self.registers.get_hl(),self.registers.d)
            print('{}: LD (HL), D'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x73:
            self.mmu.write_byte(self.registers.get_hl(),self.registers.e)
            print('{}: LD (HL), E'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x74:
            self.mmu.write_byte(self.registers.get_hl(),self.registers.h)
            print('{}: LD (HL), H'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x75:
            self.mmu.write_byte(self.registers.get_hl(),self.registers.l)
            print('{}: LD (HL), L'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x77:
            self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
            print('{}: LD (HL), A'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x78:
            self.registers.a = self.registers.b
            print('{}: LD A, B'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x79:
            self.registers.a = self.registers.c
            print('{}: LD A, C'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x7a:
            self.registers.a = self.registers.d
            print('{}: LD A, D'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x7b:
            self.registers.a = self.registers.e
            print('{}: LD A, E'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x7c:
            self.registers.a = self.registers.h
            print('{}: LD A, H'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x7d:
            self.registers.a = self.registers.l
            print('{}: LD A, L'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x7e:
            self.registers.a = self.mmu.read_byte(self.registers.get_hl())
            print('{}: LD A, (HL)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x7f:
            print('{}: LD A, A'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x80:
            byte = self.registers.a + self.registers.b
            if (byte & 0xff) == 0x00:
                self.registers.set_z_flag
            else:
                 self.registers.reset_z_flag
            if (self.registers.a ^ self.registers.b ^ byte) & 0x100 == 0x100:
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a ^ self.registers.b ^ byte) & 0x10 == 0x10: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = byte & 0xff
            print('{}: ADD A, B'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x81:
            byte = self.registers.a + self.registers.c
            if (byte & 0xff) == 0x00:
                self.registers.set_z_flag
            else:
                 self.registers.reset_z_flag
            if (self.registers.a ^ self.registers.c ^ byte) & 0x100 == 0x100:
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a ^ self.registers.c ^ byte) & 0x10 == 0x10: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = byte & 0xff
            print('{}: ADD A, C'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x82:
            byte = self.registers.a + self.registers.d
            if (byte & 0xff) == 0x00:
                self.registers.set_z_flag
            else:
                 self.registers.reset_z_flag
            if (self.registers.a ^ self.registers.d ^ byte) & 0x100 == 0x100:
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a ^ self.registers.d ^ byte) & 0x10 == 0x10: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = byte & 0xff
            print('{}: ADD A, D'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x83:
            byte = self.registers.a + self.registers.e
            if (byte & 0xff) == 0x00:
                self.registers.set_z_flag
            else:
                 self.registers.reset_z_flag
            if (self.registers.a ^ self.registers.e ^ byte) & 0x100 == 0x100:
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a ^ self.registers.e ^ byte) & 0x10 == 0x10: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = byte & 0xff
            print('{}: ADD A, E'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x84:
            byte = self.registers.a + self.registers.h
            if (byte & 0xff) == 0x00:
                self.registers.set_z_flag
            else:
                 self.registers.reset_z_flag
            if (self.registers.a ^ self.registers.h ^ byte) & 0x100 == 0x100:
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a ^ self.registers.h ^ byte) & 0x10 == 0x10: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = byte & 0xff
            print('{}: ADD A, H'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x85:
            byte = self.registers.a + self.registers.l
            if (byte & 0xff) == 0x00:
                self.registers.set_z_flag
            else:
                 self.registers.reset_z_flag
            if (self.registers.a ^ self.registers.l ^ byte) & 0x100 == 0x100:
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a ^ self.registers.l ^ byte) & 0x10 == 0x10: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = byte & 0xff
            print('{}: ADD A, L'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x86:
            byte = self.mmu.read_byte(self.registers.get_hl())
            result = self.registers.a + byte
            if (byte & 0xff) == 0x00:
                self.registers.set_z_flag
            else:
                 self.registers.reset_z_flag
            if (self.registers.a ^ byte ^ result) & 0x100 == 0x100:
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a ^ byte ^ result) & 0x10 == 0x10: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = result & 0xff
            print('{}: ADD A, (HL)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x87:
            byte = self.registers.a + self.registers.a
            if (byte & 0xff) == 0x00:
                self.registers.set_z_flag
            else:
                 self.registers.reset_z_flag
            if (self.registers.a ^ self.registers.a ^ byte) & 0x100 == 0x100:
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a ^ self.registers.a ^ byte) & 0x10 == 0x10: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = byte & 0xff
            print('{}: ADD A, A'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x88:
            carry = 1 if self.registers.is_c_flag() else 0
            result = self.registers.a + self.registers.b + carry
            if result & 0xff == 0x0: 
                self.registers.set_z_flag 
            else: 
                self.registers.reset_z_flag
            if result > 0xff: 
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a & 0xf) + (self.registers.b & 0xf) + carry > 0xf: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = result & 0xFF
            print('{}: ADC A, B'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x89:
            carry = 1 if self.registers.is_c_flag() else 0
            result = self.registers.a + self.registers.c + carry
            if result & 0xff == 0x0: 
                self.registers.set_z_flag 
            else: 
                self.registers.reset_z_flag
            if result > 0xff: 
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a & 0xf) + (self.registers.c & 0xf) + carry > 0xf: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = result & 0xFF
            print('{}: ADC A, C'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x8a:
            carry = 1 if self.registers.is_c_flag() else 0
            result = self.registers.a + self.registers.d + carry
            if result & 0xff == 0x0: 
                self.registers.set_z_flag 
            else: 
                self.registers.reset_z_flag
            if result > 0xff: 
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a & 0xf) + (self.registers.d & 0xf) + carry > 0xf: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = result & 0xFF
            print('{}: ADC A, D'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x8b:
            carry = 1 if self.registers.is_c_flag() else 0
            result = self.registers.a + self.registers.e + carry
            if result & 0xff == 0x0: 
                self.registers.set_z_flag 
            else: 
                self.registers.reset_z_flag
            if result > 0xff: 
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a & 0xf) + (self.registers.e & 0xf) + carry > 0xf: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = result & 0xFF
            print('{}: ADC A, E'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x8c:
            carry = 1 if self.registers.is_c_flag() else 0
            result = self.registers.a + self.registers.h + carry
            if result & 0xff == 0x0: 
                self.registers.set_z_flag 
            else: 
                self.registers.reset_z_flag
            if result > 0xff: 
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a & 0xf) + (self.registers.h & 0xf) + carry > 0xf: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = result & 0xFF
            print('{}: ADC A, H'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x8d:
            carry = 1 if self.registers.is_c_flag() else 0
            result = self.registers.a + self.registers.l + carry
            if result & 0xff == 0x0: 
                self.registers.set_z_flag 
            else: 
                self.registers.reset_z_flag
            if result > 0xff: 
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a & 0xf) + (self.registers.l & 0xf) + carry > 0xf: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = result & 0xFF
            print('{}: ADC A, L'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0x8e:
            carry = 1 if self.registers.is_c_flag() else 0
            byte = self.mmu.read_byte(self.registers.get_hl())
            result = self.registers.a + byte + carry
            if result & 0xff == 0x0: 
                self.registers.set_z_flag 
            else: 
                self.registers.reset_z_flag
            if result > 0xff: 
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a & 0xf) + (byte & 0xf) + carry > 0xf: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = result & 0xFF
            print('{}: ADC A, (HL)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0x8f:
            carry = 1 if self.registers.is_c_flag() else 0
            result = self.registers.a + self.registers.a + carry
            if result & 0xff == 0x0: 
                self.registers.set_z_flag 
            else: 
                self.registers.reset_z_flag
            if result > 0xff: 
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a & 0xf) + (self.registers.a & 0xf) + carry > 0xf: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = result & 0xFF
            print('{}: ADC A, A'.format(hex(self.registers.pc-1)))
            return 4
        if instruction == 0xc1:
            self.registers.set_bc(self.cpu.stackManager.pop_word())
            print('{}: POP BC'.format(hex(self.registers.pc-1)))
            return 12
        if instruction == 0xc5:
            self.cpu.stackManager.push_word(self.registers.get_bc())
            print('{}: PUSH BC'.format(hex(self.registers.pc-1)))
            return 16
        if instruction == 0xc6:
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            result = self.registers.a + byte
            if (byte & 0xff) == 0x00:
                self.registers.set_z_flag
            else:
                 self.registers.reset_z_flag
            if (self.registers.a ^ byte ^ result) & 0x100 == 0x100:
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a ^ byte ^ result) & 0x10 == 0x10: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = result & 0xff
            print('{}: ADD A, {}'.format(hex(self.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0xce:
            carry = 1 if self.registers.is_c_flag() else 0
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            result = self.registers.a + byte + carry
            if result & 0xff == 0x0: 
                self.registers.set_z_flag 
            else: 
                self.registers.reset_z_flag
            if result > 0xff: 
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.a & 0xf) + (byte & 0xf) + carry > 0xf: 
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.reset_n_flag
            self.registers.a = result & 0xFF
            print('{}: ADC A, {}'.format(hex(self.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0xd1:
            self.registers.set_de(self.cpu.stackManager.pop_word())
            print('{}: POP DE'.format(hex(self.registers.pc-1)))
            return 12
        if instruction == 0xd5:
            self.cpu.stackManager.push_word(self.registers.get_de())
            print('{}: PUSH DE'.format(hex(self.registers.pc-1)))
            return 16
        if instruction == 0xe1:
            self.registers.set_hl(self.cpu.stackManager.pop_word())
            print('{}: POP HL'.format(hex(self.registers.pc-1)))
            return 12
        if instruction == 0xe5:
            self.cpu.stackManager.push_word(self.registers.get_hl())
            print('{}: PUSH HL'.format(hex(self.registers.pc-1)))
            return 16
        if instruction == 0xe0:
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            self.mmu.write_byte((byte + 0xff00), self.registers.a)
            print('{}: LDH ({}), A'.format(hex(self.registers.pc-2),hex(byte)))
            return 12
        if instruction == 0xe2:
            self.mmu.write_byte((self.registers.c + 0xff00), self.registers.a)
            print('{}: LD (0xff00+C), A'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0xea:
            word = self.mmu.read_word(self.registers.pc)
            self.registers.pc += 2
            self.mmu.write_byte(word, self.registers.a)
            print('{}: LD ({}), A'.format(hex(self.registers.pc-3),hex(word)))
            return 8
        if instruction == 0xf0:
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            self.registers.a = self.mmu.read_byte((byte + 0xff00))
            print('{}: LDH A, ({})'.format(hex(self.registers.pc-2),hex(byte)))
            return 12
        if instruction == 0xf1:
            self.registers.set_af(self.cpu.stackManager.pop_word())
            print('{}: POP AF'.format(hex(self.registers.pc-1)))
            return 12
        if instruction == 0xf2:
            self.registers.a = self.mmu.read_byte(self.registers.c + 0xff00)
            print('{}: LD A, (0xff00+C)'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0xf5:
            self.cpu.stackManager.push_word(self.registers.get_af())
            print('{}: PUSH AF'.format(hex(self.registers.pc-1)))
            return 16
        if instruction == 0xf8:
            byte = self.mmu.read_byte(self.registers.pc)
            self.registers.pc += 1
            hl = self.registers.sp + signed_value(byte)
            self.registers.reset_z_flag()
            self.registers.reset_n_flag()
            if (self.registers.sp ^ signed_value(byte) ^ hl) & 0x100 == 0x100:
                self.registers.set_c_flag 
            else: 
                self.registers.reset_c_flag
            if (self.registers.sp ^ signed_value(byte) ^ hl) & 0x10 == 0x10:
                self.registers.set_h_flag 
            else: 
                self.registers.reset_h_flag
            self.registers.set_hl(hl)
            print('{}: LDHL SP, {}'.format(hex(self.registers.pc-2), hex(byte)))
            return 12
        if instruction == 0xf9:
            self.registers.sp = self.registers.get_hl()
            print('{}: LD SP, HL'.format(hex(self.registers.pc-1)))
            return 8
        if instruction == 0xfa:
            byte = self.mmu.read_byte(self.mmu.read_word(self.registers.pc))
            self.registers.pc += 2
            self.registers.a = byte
            print('{}: LD A, ({})'.format(hex(self.registers.pc-3),hex(byte)))
            return 16
        print('{}: Unknow Opcode {}'.format(hex(self.registers.pc-1), hex(instruction)))
        return 0
        


