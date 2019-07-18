#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygb.byte_operations import signed_value

class InstructionPerformer:

    def __init__(self, cpu):
        self.cpu = cpu

    def perform_instruction(self, instruction):
        if instruction == 0x00:
            print('{}: NOP'.format(hex(self.cpu.registers.pc -1)))
            return 4
        if instruction == 0x01:
            word = self.cpu.mmu.read_word(self.cpu.registers.pc)
            self.cpu.registers.pc += 2
            self.cpu.registers.set_bc(word) 
            print('{}: LD BC, {}'.format(hex(self.cpu.registers.pc-3), hex(word)))
            return 12
        if instruction == 0x02:
            self.cpu.mmu.write_byte(self.cpu.registers.get_bc, self.cpu.registers.a)
            print('{}: LD (BC), A'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x06:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            self.cpu.registers.b = byte 
            print('{}: LD B, {}'.format(hex(self.cpu.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0x08:
            word = self.cpu.mmu.read_word(self.cpu.registers.pc)
            self.cpu.registers.pc += 2
            self.cpu.mmu.write_word(word, self.cpu.registers.sp)
            print('{}: LD ({}), SP'.format(hex(self.cpu.registers.pc-2), hex(word)))
            return 20
        if instruction == 0x0a:
            self.cpu.registers.a = self.cpu.mmu.read_byte(self.cpu.registers.get_bc())
            print('{}: LD A, (BC)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x0e:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            self.cpu.registers.c = byte 
            print('{}: LD C, {}'.format(hex(self.cpu.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0x11:
            word = self.cpu.mmu.read_word(self.cpu.registers.pc)
            self.cpu.registers.pc += 2
            self.cpu.registers.set_de(word) 
            print('{}: LD DE, {}'.format(hex(self.cpu.registers.pc-3), hex(word)))
            return 12
        if instruction == 0x12:
            self.cpu.mmu.write_byte(self.cpu.registers.get_de, self.cpu.registers.a)
            print('{}: LD (DE), A'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x16:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            self.cpu.registers.d = byte 
            print('{}: LD D, {}'.format(hex(self.cpu.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0x1a:
            self.cpu.registers.a = self.cpu.mmu.read_byte(self.cpu.registers.get_de())
            print('{}: LD A, (DE)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x1e:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            self.cpu.registers.e = byte 
            print('{}: LD E, {}'.format(hex(self.cpu.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0x21:
            word = self.cpu.mmu.read_word(self.cpu.registers.pc)
            self.cpu.registers.pc += 2
            self.cpu.registers.set_hl(word) 
            print('{}: LD HL, {}'.format(hex(self.cpu.registers.pc-3), hex(word)))
            return 12
        if instruction == 0x22:
            self.cpu.mmu.write_byte(self.cpu.registers.get_hl(), self.cpu.registers.a)
            self.cpu.registers.set_hl(self.cpu.registers.get_hl()+1)
            print('{}: LD (HL+), A'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x26:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            self.cpu.registers.h = byte 
            print('{}: LD H, {}'.format(hex(self.cpu.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0x2a:
            self.cpu.registers.a = self.cpu.mmu.read_byte(self.cpu.registers.get_hl())
            self.cpu.registers.set_hl(self.cpu.registers.get_hl()+1)
            print('{}: LD A, (HL+)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x2e:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            self.cpu.registers.l = byte 
            print('{}: LD L, {}'.format(hex(self.cpu.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0x31:
            word = self.cpu.mmu.read_word(self.cpu.registers.pc)
            self.cpu.registers.pc += 2
            self.cpu.registers.sp = word
            print('{}: LD SP, {}'.format(hex(self.cpu.registers.pc-3), hex(word)))
            return 12
        if instruction == 0x32:
            self.cpu.mmu.write_byte(self.cpu.registers.get_hl(), self.cpu.registers.a)
            self.cpu.registers.set_hl(self.cpu.registers.get_hl()-1)
            print('{}: LD (HL-), A'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x36:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            self.cpu.mmu.write_byte(self.cpu.registers.get_hl(),byte)
            print('{}: LD (HL), {}'.format(hex(self.cpu.registers.pc-2),hex(byte)))
            return 12
        if instruction == 0x3a:
            self.cpu.registers.a = self.cpu.mmu.read_byte(self.cpu.registers.get_hl())
            self.cpu.registers.set_hl(self.cpu.registers.get_hl()-1)
            print('{}: LD A, (HL-)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x3e:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            self.cpu.registers.a = byte
            print('{}: LD A, {}'.format(hex(self.cpu.registers.pc-2),hex(byte)))
            return 8
        if instruction == 0x40:
            print('{}: LD B, B'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x41:
            self.cpu.registers.b = self.cpu.registers.c
            print('{}: LD B, C'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x42:
            self.cpu.registers.b = self.cpu.registers.d
            print('{}: LD B, D'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x43:
            self.cpu.registers.b = self.cpu.registers.e
            print('{}: LD B, E'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x44:
            self.cpu.registers.b = self.cpu.registers.h
            print('{}: LD B, H'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x45:
            self.cpu.registers.b = self.cpu.registers.l
            print('{}: LD B, L'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x46:
            self.cpu.registers.b = self.cpu.mmu.read_byte(self.cpu.registers.get_hl())
            print('{}: LD B, (HL)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x47:
            self.cpu.registers.b = self.cpu.registers.a
            print('{}: LD B, A'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x48:
            self.cpu.registers.c = self.cpu.registers.b
            print('{}: LD C, B'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x49:
            print('{}: LD C, C'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x4a:
            self.cpu.registers.c = self.cpu.registers.d
            print('{}: LD C, D'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x4b:
            self.cpu.registers.c = self.cpu.registers.e
            print('{}: LD C, E'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x4c:
            self.cpu.registers.c = self.cpu.registers.h
            print('{}: LD C, H'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x4d:
            self.cpu.registers.c = self.cpu.registers.l
            print('{}: LD C, L'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x4e:
            self.cpu.registers.c = self.cpu.mmu.read_byte(self.cpu.registers.get_hl())
            print('{}: LD C, (HL)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x4f:
            self.cpu.registers.c = self.cpu.registers.a
            print('{}: LD C, A'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x50:
            self.cpu.registers.d = self.cpu.registers.b
            print('{}: LD D, B'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x51:
            self.cpu.registers.d = self.cpu.registers.c
            print('{}: LD D, C'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x52:
            print('{}: LD D, D'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x53:
            self.cpu.registers.d = self.cpu.registers.e
            print('{}: LD D, E'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x54:
            self.cpu.registers.d = self.cpu.registers.h
            print('{}: LD D, H'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x55:
            self.cpu.registers.d = self.cpu.registers.l
            print('{}: LD D, L'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x56:
            self.cpu.registers.d = self.cpu.mmu.read_byte(self.cpu.registers.get_hl())
            print('{}: LD D, (HL)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x57:
            self.cpu.registers.d = self.cpu.registers.a
            print('{}: LD D, A'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x58:
            self.cpu.registers.e = self.cpu.registers.b
            print('{}: LD E, B'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x59:
            self.cpu.registers.e = self.cpu.registers.c
            print('{}: LD E, C'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x5a:
            self.cpu.registers.e = self.cpu.registers.d
            print('{}: LD E, D'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x5b:
            print('{}: LD E, E'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x5c:
            self.cpu.registers.e = self.cpu.registers.h
            print('{}: LD E, H'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x5d:
            self.cpu.registers.e = self.cpu.registers.l
            print('{}: LD E, L'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x5e:
            self.cpu.registers.e = self.cpu.mmu.read_byte(self.cpu.registers.get_hl())
            print('{}: LD E, (HL)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x5f:
            self.cpu.registers.e = self.cpu.registers.a
            print('{}: LD E, A'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x60:
            self.cpu.registers.h = self.cpu.registers.b
            print('{}: LD H, B'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x61:
            self.cpu.registers.h = self.cpu.registers.c
            print('{}: LD H, C'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x62:
            self.cpu.registers.h = self.cpu.registers.d
            print('{}: LD H, D'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x63:
            self.cpu.registers.h = self.cpu.registers.e
            print('{}: LD H, E'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x64:
            print('{}: LD H, H'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x65:
            self.cpu.registers.h = self.cpu.registers.l
            print('{}: LD H, L'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x66:
            self.cpu.registers.h = self.cpu.mmu.read_byte(self.cpu.registers.get_hl())
            print('{}: LD H, (HL)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x67:
            self.cpu.registers.h = self.cpu.registers.a
            print('{}: LD H, A'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x68:
            self.cpu.registers.l = self.cpu.registers.b
            print('{}: LD L, B'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x69:
            self.cpu.registers.l = self.cpu.registers.c
            print('{}: LD L, C'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x6a:
            self.cpu.registers.l = self.cpu.registers.d
            print('{}: LD L, D'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x6b:
            self.cpu.registers.l = self.cpu.registers.e
            print('{}: LD L, E'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x6c:
            self.cpu.registers.l = self.cpu.registers.h
            print('{}: LD L, H'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x6d:
            print('{}: LD L, L'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x6e:
            self.cpu.registers.l = self.cpu.mmu.read_byte(self.cpu.registers.get_hl())
            print('{}: LD L, (HL)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x6f:
            self.cpu.registers.l = self.cpu.registers.a
            print('{}: LD L, A'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x70:
            self.cpu.mmu.write_byte(self.cpu.registers.get_hl(),self.cpu.registers.b)
            print('{}: LD (HL), B'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x71:
            self.cpu.mmu.write_byte(self.cpu.registers.get_hl(),self.cpu.registers.c)
            print('{}: LD (HL), C'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x72:
            self.cpu.mmu.write_byte(self.cpu.registers.get_hl(),self.cpu.registers.d)
            print('{}: LD (HL), D'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x73:
            self.cpu.mmu.write_byte(self.cpu.registers.get_hl(),self.cpu.registers.e)
            print('{}: LD (HL), E'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x74:
            self.cpu.mmu.write_byte(self.cpu.registers.get_hl(),self.cpu.registers.h)
            print('{}: LD (HL), H'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x75:
            self.cpu.mmu.write_byte(self.cpu.registers.get_hl(),self.cpu.registers.l)
            print('{}: LD (HL), L'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x77:
            self.cpu.mmu.write_byte(self.cpu.registers.get_hl(), self.cpu.registers.a)
            print('{}: LD (HL), A'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x78:
            self.cpu.registers.a = self.cpu.registers.b
            print('{}: LD A, B'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x79:
            self.cpu.registers.a = self.cpu.registers.c
            print('{}: LD A, C'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x7a:
            self.cpu.registers.a = self.cpu.registers.d
            print('{}: LD A, D'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x7b:
            self.cpu.registers.a = self.cpu.registers.e
            print('{}: LD A, E'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x7c:
            self.cpu.registers.a = self.cpu.registers.h
            print('{}: LD A, H'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x7d:
            self.cpu.registers.a = self.cpu.registers.l
            print('{}: LD A, L'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x7e:
            self.cpu.registers.a = self.cpu.mmu.read_byte(self.cpu.registers.get_hl())
            print('{}: LD A, (HL)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x7f:
            print('{}: LD A, A'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x80:
            byte = self.cpu.registers.a + self.cpu.registers.b
            if (byte & 0xff) == 0x00:
                self.cpu.registers.set_z_flag
            else:
                 self.cpu.registers.reset_z_flag
            if (self.cpu.registers.a ^ self.cpu.registers.b ^ byte) & 0x100 == 0x100:
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a ^ self.cpu.registers.b ^ byte) & 0x10 == 0x10: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = byte & 0xff
            print('{}: ADD A, B'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x81:
            byte = self.cpu.registers.a + self.cpu.registers.c
            if (byte & 0xff) == 0x00:
                self.cpu.registers.set_z_flag
            else:
                 self.cpu.registers.reset_z_flag
            if (self.cpu.registers.a ^ self.cpu.registers.c ^ byte) & 0x100 == 0x100:
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a ^ self.cpu.registers.c ^ byte) & 0x10 == 0x10: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = byte & 0xff
            print('{}: ADD A, C'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x82:
            byte = self.cpu.registers.a + self.cpu.registers.d
            if (byte & 0xff) == 0x00:
                self.cpu.registers.set_z_flag
            else:
                 self.cpu.registers.reset_z_flag
            if (self.cpu.registers.a ^ self.cpu.registers.d ^ byte) & 0x100 == 0x100:
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a ^ self.cpu.registers.d ^ byte) & 0x10 == 0x10: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = byte & 0xff
            print('{}: ADD A, D'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x83:
            byte = self.cpu.registers.a + self.cpu.registers.e
            if (byte & 0xff) == 0x00:
                self.cpu.registers.set_z_flag
            else:
                 self.cpu.registers.reset_z_flag
            if (self.cpu.registers.a ^ self.cpu.registers.e ^ byte) & 0x100 == 0x100:
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a ^ self.cpu.registers.e ^ byte) & 0x10 == 0x10: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = byte & 0xff
            print('{}: ADD A, E'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x84:
            byte = self.cpu.registers.a + self.cpu.registers.h
            if (byte & 0xff) == 0x00:
                self.cpu.registers.set_z_flag
            else:
                 self.cpu.registers.reset_z_flag
            if (self.cpu.registers.a ^ self.cpu.registers.h ^ byte) & 0x100 == 0x100:
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a ^ self.cpu.registers.h ^ byte) & 0x10 == 0x10: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = byte & 0xff
            print('{}: ADD A, H'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x85:
            byte = self.cpu.registers.a + self.cpu.registers.l
            if (byte & 0xff) == 0x00:
                self.cpu.registers.set_z_flag
            else:
                 self.cpu.registers.reset_z_flag
            if (self.cpu.registers.a ^ self.cpu.registers.l ^ byte) & 0x100 == 0x100:
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a ^ self.cpu.registers.l ^ byte) & 0x10 == 0x10: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = byte & 0xff
            print('{}: ADD A, L'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x86:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.get_hl())
            result = self.cpu.registers.a + byte
            if (byte & 0xff) == 0x00:
                self.cpu.registers.set_z_flag
            else:
                 self.cpu.registers.reset_z_flag
            if (self.cpu.registers.a ^ byte ^ result) & 0x100 == 0x100:
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a ^ byte ^ result) & 0x10 == 0x10: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = result & 0xff
            print('{}: ADD A, (HL)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x87:
            byte = self.cpu.registers.a + self.cpu.registers.a
            if (byte & 0xff) == 0x00:
                self.cpu.registers.set_z_flag
            else:
                 self.cpu.registers.reset_z_flag
            if (self.cpu.registers.a ^ self.cpu.registers.a ^ byte) & 0x100 == 0x100:
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a ^ self.cpu.registers.a ^ byte) & 0x10 == 0x10: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = byte & 0xff
            print('{}: ADD A, A'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x88:
            carry = 1 if self.cpu.registers.is_c_flag() else 0
            result = self.cpu.registers.a + self.cpu.registers.b + carry
            if result & 0xff == 0x0: 
                self.cpu.registers.set_z_flag 
            else: 
                self.cpu.registers.reset_z_flag
            if result > 0xff: 
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a & 0xf) + (self.cpu.registers.b & 0xf) + carry > 0xf: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = result & 0xFF
            print('{}: ADC A, B'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x89:
            carry = 1 if self.cpu.registers.is_c_flag() else 0
            result = self.cpu.registers.a + self.cpu.registers.c + carry
            if result & 0xff == 0x0: 
                self.cpu.registers.set_z_flag 
            else: 
                self.cpu.registers.reset_z_flag
            if result > 0xff: 
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a & 0xf) + (self.cpu.registers.c & 0xf) + carry > 0xf: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = result & 0xFF
            print('{}: ADC A, C'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x8a:
            carry = 1 if self.cpu.registers.is_c_flag() else 0
            result = self.cpu.registers.a + self.cpu.registers.d + carry
            if result & 0xff == 0x0: 
                self.cpu.registers.set_z_flag 
            else: 
                self.cpu.registers.reset_z_flag
            if result > 0xff: 
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a & 0xf) + (self.cpu.registers.d & 0xf) + carry > 0xf: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = result & 0xFF
            print('{}: ADC A, D'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x8b:
            carry = 1 if self.cpu.registers.is_c_flag() else 0
            result = self.cpu.registers.a + self.cpu.registers.e + carry
            if result & 0xff == 0x0: 
                self.cpu.registers.set_z_flag 
            else: 
                self.cpu.registers.reset_z_flag
            if result > 0xff: 
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a & 0xf) + (self.cpu.registers.e & 0xf) + carry > 0xf: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = result & 0xFF
            print('{}: ADC A, E'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x8c:
            carry = 1 if self.cpu.registers.is_c_flag() else 0
            result = self.cpu.registers.a + self.cpu.registers.h + carry
            if result & 0xff == 0x0: 
                self.cpu.registers.set_z_flag 
            else: 
                self.cpu.registers.reset_z_flag
            if result > 0xff: 
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a & 0xf) + (self.cpu.registers.h & 0xf) + carry > 0xf: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = result & 0xFF
            print('{}: ADC A, H'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x8d:
            carry = 1 if self.cpu.registers.is_c_flag() else 0
            result = self.cpu.registers.a + self.cpu.registers.l + carry
            if result & 0xff == 0x0: 
                self.cpu.registers.set_z_flag 
            else: 
                self.cpu.registers.reset_z_flag
            if result > 0xff: 
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a & 0xf) + (self.cpu.registers.l & 0xf) + carry > 0xf: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = result & 0xFF
            print('{}: ADC A, L'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0x8e:
            carry = 1 if self.cpu.registers.is_c_flag() else 0
            byte = self.cpu.mmu.read_byte(self.cpu.registers.get_hl())
            result = self.cpu.registers.a + byte + carry
            if result & 0xff == 0x0: 
                self.cpu.registers.set_z_flag 
            else: 
                self.cpu.registers.reset_z_flag
            if result > 0xff: 
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a & 0xf) + (byte & 0xf) + carry > 0xf: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = result & 0xFF
            print('{}: ADC A, (HL)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0x8f:
            carry = 1 if self.cpu.registers.is_c_flag() else 0
            result = self.cpu.registers.a + self.cpu.registers.a + carry
            if result & 0xff == 0x0: 
                self.cpu.registers.set_z_flag 
            else: 
                self.cpu.registers.reset_z_flag
            if result > 0xff: 
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a & 0xf) + (self.cpu.registers.a & 0xf) + carry > 0xf: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = result & 0xFF
            print('{}: ADC A, A'.format(hex(self.cpu.registers.pc-1)))
            return 4
        if instruction == 0xc1:
            self.cpu.registers.set_bc(self.cpu.stackManager.pop_word())
            print('{}: POP BC'.format(hex(self.cpu.registers.pc-1)))
            return 12
        if instruction == 0xc5:
            self.cpu.stackManager.push_word(self.cpu.registers.get_bc())
            print('{}: PUSH BC'.format(hex(self.cpu.registers.pc-1)))
            return 16
        if instruction == 0xc6:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            result = self.cpu.registers.a + byte
            if (byte & 0xff) == 0x00:
                self.cpu.registers.set_z_flag
            else:
                 self.cpu.registers.reset_z_flag
            if (self.cpu.registers.a ^ byte ^ result) & 0x100 == 0x100:
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a ^ byte ^ result) & 0x10 == 0x10: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = result & 0xff
            print('{}: ADD A, {}'.format(hex(self.cpu.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0xce:
            carry = 1 if self.cpu.registers.is_c_flag() else 0
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            result = self.cpu.registers.a + byte + carry
            if result & 0xff == 0x0: 
                self.cpu.registers.set_z_flag 
            else: 
                self.cpu.registers.reset_z_flag
            if result > 0xff: 
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.a & 0xf) + (byte & 0xf) + carry > 0xf: 
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.reset_n_flag
            self.cpu.registers.a = result & 0xFF
            print('{}: ADC A, {}'.format(hex(self.cpu.registers.pc-2), hex(byte)))
            return 8
        if instruction == 0xd1:
            self.cpu.registers.set_de(self.cpu.stackManager.pop_word())
            print('{}: POP DE'.format(hex(self.cpu.registers.pc-1)))
            return 12
        if instruction == 0xd5:
            self.cpu.stackManager.push_word(self.cpu.registers.get_de())
            print('{}: PUSH DE'.format(hex(self.cpu.registers.pc-1)))
            return 16
        if instruction == 0xe1:
            self.cpu.registers.set_hl(self.cpu.stackManager.pop_word())
            print('{}: POP HL'.format(hex(self.cpu.registers.pc-1)))
            return 12
        if instruction == 0xe5:
            self.cpu.stackManager.push_word(self.cpu.registers.get_hl())
            print('{}: PUSH HL'.format(hex(self.cpu.registers.pc-1)))
            return 16
        if instruction == 0xe0:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            self.cpu.mmu.write_byte((byte + 0xff00), self.cpu.registers.a)
            print('{}: LDH ({}), A'.format(hex(self.cpu.registers.pc-2),hex(byte)))
            return 12
        if instruction == 0xe2:
            self.cpu.mmu.write_byte((self.cpu.registers.c + 0xff00), self.cpu.registers.a)
            print('{}: LD (0xff00+C), A'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0xea:
            word = self.cpu.mmu.read_word(self.cpu.registers.pc)
            self.cpu.registers.pc += 2
            self.cpu.mmu.write_byte(word, self.cpu.registers.a)
            print('{}: LD ({}), A'.format(hex(self.cpu.registers.pc-3),hex(word)))
            return 8
        if instruction == 0xf0:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            self.cpu.registers.a = self.cpu.mmu.read_byte((byte + 0xff00))
            print('{}: LDH A, ({})'.format(hex(self.cpu.registers.pc-2),hex(byte)))
            return 12
        if instruction == 0xf1:
            self.cpu.registers.set_af(self.cpu.stackManager.pop_word())
            print('{}: POP AF'.format(hex(self.cpu.registers.pc-1)))
            return 12
        if instruction == 0xf2:
            self.cpu.registers.a = self.cpu.mmu.read_byte(self.cpu.registers.c + 0xff00)
            print('{}: LD A, (0xff00+C)'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0xf5:
            self.cpu.stackManager.push_word(self.cpu.registers.get_af())
            print('{}: PUSH AF'.format(hex(self.cpu.registers.pc-1)))
            return 16
        if instruction == 0xf8:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            hl = self.cpu.registers.sp + signed_value(byte)
            self.cpu.registers.reset_z_flag()
            self.cpu.registers.reset_n_flag()
            if (self.cpu.registers.sp ^ signed_value(byte) ^ hl) & 0x100 == 0x100:
                self.cpu.registers.set_c_flag 
            else: 
                self.cpu.registers.reset_c_flag
            if (self.cpu.registers.sp ^ signed_value(byte) ^ hl) & 0x10 == 0x10:
                self.cpu.registers.set_h_flag 
            else: 
                self.cpu.registers.reset_h_flag
            self.cpu.registers.set_hl(hl)
            print('{}: LDHL SP, {}'.format(hex(self.cpu.registers.pc-2), hex(byte)))
            return 12
        if instruction == 0xf9:
            self.cpu.registers.sp = self.cpu.registers.get_hl()
            print('{}: LD SP, HL'.format(hex(self.cpu.registers.pc-1)))
            return 8
        if instruction == 0xfa:
            byte = self.cpu.mmu.read_byte(self.cpu.mmu.read_word(self.cpu.registers.pc))
            self.cpu.registers.pc += 2
            self.cpu.registers.a = byte
            print('{}: LD A, ({})'.format(hex(self.cpu.registers.pc-3),hex(byte)))
            return 16
        print('{}: Unknow Opcode {}'.format(hex(self.cpu.registers.pc-1), hex(instruction)))
        return 0
        


