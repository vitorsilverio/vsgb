#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pygb.byte_operations import signed_value, set_bit, bit_mask
from pygb.io_registers import IO_Registers

class InstructionPerformer:

    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = cpu.mmu
        self.registers = cpu.registers
        self.stackManager = cpu.stackManager

    def perform_instruction(self, opcode):
        try:
            instruction = getattr(self, 'instruction_' + hex(opcode))
            return instruction()
        except:
            return self.unimplemented(opcode)

    
    def instruction_0x0(self):
        self.debug('{}: NOP'.format(hex(self.registers.pc -1)))
        return 4
    
    def instruction_0x1(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.set_bc(word) 
        self.debug('{}: LD BC, {}'.format(hex(self.registers.pc-3), hex(word)))
        return 12
    
    def instruction_0x2(self):
        self.mmu.write_byte(self.registers.get_bc(), self.registers.a)
        self.debug('{}: LD (BC), A'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x3(self):
        self.registers.set_bc((self.registers.get_bc() + 1) & 0xffff )
        self.debug('{}: INC BC'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x4(self):
        self.registers.b = self.inc_byte(self.registers.b)
        self.debug('{}: INC B'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x5(self):
        self.registers.b = self.dec_byte(self.registers.b)
        self.debug('{}: DEC B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x6(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.b = byte 
        self.debug('{}: LD B, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def instruction_0x7(self):
        self.registers.a = self.rlc(self.registers.a)
        self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.debug('{}: RLCA'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x8(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.mmu.write_word(word, self.registers.sp)
        self.debug('{}: LD ({}), SP'.format(hex(self.registers.pc-3), hex(word)))
        return 20

    def instruction_0x9(self):
        self.registers.set_hl(self.add_word(self.registers.get_hl(), self.registers.get_bc()))
        self.debug('{}: ADD HL, BC'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0xa(self):
        self.registers.a = self.mmu.read_byte(self.registers.get_bc())
        self.debug('{}: LD A, (BC)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0xb(self):
        self.registers.set_bc((self.registers.get_bc() - 1) & 0xffff )
        self.debug('{}: DEC BC'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0xc(self):
        self.registers.c = self.inc_byte(self.registers.c)
        self.debug('{}: INC C'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xd(self):
        self.registers.c = self.dec_byte(self.registers.c)
        self.debug('{}: DEC C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0xe(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.c = byte 
        self.debug('{}: LD C, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def instruction_0xf(self):
        self.registers.a = self.rrc(self.registers.a)
        self.registers.reset_h_flag()
        self.registers.reset_n_flag()
        self.registers.reset_z_flag()
        self.debug('{}: RRCA'.format(hex(self.registers.pc-1)))
        return 4  

    def instruction_0x10(self):
        self.cpu.stop = True
        self.registers.pc += 1
        self.debug('{}: STOP 0'.format(hex(self.registers.pc-2)))
        return 4       
    
    def instruction_0x11(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.set_de(word) 
        self.debug('{}: LD DE, {}'.format(hex(self.registers.pc-3), hex(word)))
        return 12
    
    def instruction_0x12(self):
        self.mmu.write_byte(self.registers.get_de(), self.registers.a)
        self.debug('{}: LD (DE), A'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x13(self):
        self.registers.set_de((self.registers.get_de() + 1) & 0xffff )
        self.debug('{}: INC DE'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x14(self):
        self.registers.d = self.inc_byte(self.registers.d)
        self.debug('{}: INC D'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x15(self):
        self.registers.d = self.dec_byte(self.registers.d)
        self.debug('{}: DEC D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x16(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.d = byte 
        self.debug('{}: LD D, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def instruction_0x17(self):
        self.registers.a = self.rl(self.registers.a)
        self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.debug('{}: RLA'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x18(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.debug('{}: JR {}'.format(hex(self.registers.pc-2), hex(byte)))
        self.registers.pc += signed_value(byte)
        return 12

    def instruction_0x19(self):
        self.registers.set_hl(self.add_word(self.registers.get_hl(), self.registers.get_de()))
        self.debug('{}: ADD HL, DE'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x1a(self):
        self.registers.a = self.mmu.read_byte(self.registers.get_de())
        self.debug('{}: LD A, (DE)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x1b(self):
        self.registers.set_de((self.registers.get_de() - 1) & 0xffff )
        self.debug('{}: DEC DE'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x1c(self):
        self.registers.e = self.inc_byte(self.registers.e)
        self.debug('{}: INC E'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x1d(self):
        self.registers.e = self.dec_byte(self.registers.e)
        self.debug('{}: DEC E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x1e(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.e = byte 
        self.debug('{}: LD E, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def instruction_0x1f(self):
        self.registers.a = self.rr(self.registers.a)
        self.registers.reset_h_flag()
        self.registers.reset_n_flag()
        self.registers.reset_z_flag()
        self.debug('{}: RRA'.format(hex(self.registers.pc-1)))
        return 4  

    def instruction_0x20(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.debug('{}: JR NZ, {}'.format(hex(self.registers.pc-2), hex(byte)))
        if not self.registers.is_z_flag():
            self.registers.pc += signed_value(byte)
            return 12
        else:
            return 8
    
    def instruction_0x21(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.set_hl(word) 
        self.debug('{}: LD HL, {}'.format(hex(self.registers.pc-3), hex(word)))
        return 12
    
    def instruction_0x22(self):
        self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
        self.registers.set_hl(self.registers.get_hl()+1)
        self.debug('{}: LD (HL+), A'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x23(self):
        self.registers.set_hl((self.registers.get_hl() + 1) & 0xffff )
        self.debug('{}: INC HL'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x24(self):
        self.registers.h = self.inc_byte(self.registers.h)
        self.debug('{}: INC H'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x25(self):
        self.registers.h = self.dec_byte(self.registers.h)
        self.debug('{}: DEC H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x26(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.h = byte 
        self.debug('{}: LD H, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def instruction_0x27(self):
        temp_a = self.registers.a
        if not self.registers.is_n_flag():
            if self.registers.is_h_flag() or (temp_a & 0xf) > 0x9:
                temp_a = temp_a + 0x06
            if self.registers.is_c_flag() or (temp_a > 0x9f):
                temp_a = temp_a + 0x60
        else:
            if self.registers.is_h_flag():
                temp_a = (temp_a - 0x06) & 0xff
            if self.registers.is_c_flag():
                temp_a = temp_a - 0x60
        self.registers.reset_h_flag()
        self.registers.reset_z_flag()

        if temp_a & 0x100 == 0x100:
            self.registers.set_c_flag()
        temp_a = temp_a & 0xff
        if temp_a == 0x0:
            self.registers.set_z_flag()
        self.registers.a = temp_a
        self.debug('{}: DAA'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x28(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.debug('{}: JR Z, {}'.format(hex(self.registers.pc-2), hex(byte)))
        if self.registers.is_z_flag():
            self.registers.pc += signed_value(byte)
            return 12
        else:
            return 8

    def instruction_0x29(self):
        self.registers.set_hl(self.add_word(self.registers.get_hl(), self.registers.get_hl()))
        self.debug('{}: ADD HL, HL'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x2a(self):
        self.registers.a = self.mmu.read_byte(self.registers.get_hl())
        self.registers.set_hl(self.registers.get_hl()+1)
        self.debug('{}: LD A, (HL+)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x2b(self):
        self.registers.set_hl((self.registers.get_hl() - 1) & 0xffff )
        self.debug('{}: DEC HL'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x2c(self):
        self.registers.l = self.inc_byte(self.registers.l)
        self.debug('{}: INC L'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x2d(self):
        self.registers.l = self.dec_byte(self.registers.l)
        self.debug('{}: DEC L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x2e(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.l = byte 
        self.debug('{}: LD L, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def instruction_0x2f(self):
        self.registers.a = self.registers.a ^ 0xff
        self.registers.set_n_flag()
        self.registers.set_h_flag()
        self.debug('{}: CPL'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x30(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.debug('{}: JR NC, {}'.format(hex(self.registers.pc-2), hex(byte)))
        if not self.registers.is_c_flag():
            self.registers.pc += signed_value(byte)
            return 12
        else:
            return 8
    
    def instruction_0x31(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.sp = word
        self.debug('{}: LD SP, {}'.format(hex(self.registers.pc-3), hex(word)))
        return 12
    
    def instruction_0x32(self):
        self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
        self.registers.set_hl(self.registers.get_hl()-1)
        self.debug('{}: LD (HL-), A'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x33(self):
        self.registers.sp = ((self.registers.sp + 1) & 0xffff )
        self.debug('{}: INC SP'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x34(self):
        self.mmu.write_byte(self.registers.get_hl(),self.inc_byte(self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: INC C'.format(hex(self.registers.pc-1)))
        return 12

    def instruction_0x35(self):
        self.mmu.write_byte(self.registers.get_hl(), self.dec_byte(self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: DEC (HL)'.format(hex(self.registers.pc-1)))
        return 12
    
    def instruction_0x36(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.mmu.write_byte(self.registers.get_hl(),byte)
        self.debug('{}: LD (HL), {}'.format(hex(self.registers.pc-2),hex(byte)))
        return 12

    def instruction_0x37(self):
        self.registers.set_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.debug('{}: SCF'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x38(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.debug('{}: JR C, {}'.format(hex(self.registers.pc-2), hex(byte)))
        if self.registers.is_c_flag():
            self.registers.pc += signed_value(byte)
            return 12
        else:
            return 8

    def instruction_0x39(self):
        self.registers.set_hl(self.add_word(self.registers.get_hl(), self.registers.sp))
        self.debug('{}: ADD HL, SP'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x3a(self):
        self.registers.a = self.mmu.read_byte(self.registers.get_hl())
        self.registers.set_hl(self.registers.get_hl()-1)
        self.debug('{}: LD A, (HL-)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x3b(self):
        self.registers.sp = ((self.registers.sp - 1) & 0xffff )
        self.debug('{}: DEC SP'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x3c(self):
        self.registers.a = self.inc_byte(self.registers.a)
        self.debug('{}: INC A'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x3d(self):
        self.registers.a = self.dec_byte(self.registers.a)
        self.debug('{}: DEC A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x3e(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.a = byte
        self.debug('{}: LD A, {}'.format(hex(self.registers.pc-2),hex(byte)))
        return 8

    def instruction_0x3f(self):
        if self.registers.is_c_flag():
            self.registers.reset_c_flag()
        else:
            self.registers.set_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.debug('{}: CCF'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x40(self):
        self.debug('{}: LD B, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x41(self):
        self.registers.b = self.registers.c
        self.debug('{}: LD B, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x42(self):
        self.registers.b = self.registers.d
        self.debug('{}: LD B, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x43(self):
        self.registers.b = self.registers.e
        self.debug('{}: LD B, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x44(self):
        self.registers.b = self.registers.h
        self.debug('{}: LD B, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x45(self):
        self.registers.b = self.registers.l
        self.debug('{}: LD B, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x46(self):
        self.registers.b = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD B, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x47(self):
        self.registers.b = self.registers.a
        self.debug('{}: LD B, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x48(self):
        self.registers.c = self.registers.b
        self.debug('{}: LD C, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x49(self):
        self.debug('{}: LD C, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x4a(self):
        self.registers.c = self.registers.d
        self.debug('{}: LD C, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x4b(self):
        self.registers.c = self.registers.e
        self.debug('{}: LD C, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x4c(self):
        self.registers.c = self.registers.h
        self.debug('{}: LD C, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x4d(self):
        self.registers.c = self.registers.l
        self.debug('{}: LD C, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x4e(self):
        self.registers.c = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD C, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x4f(self):
        self.registers.c = self.registers.a
        self.debug('{}: LD C, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x50(self):
        self.registers.d = self.registers.b
        self.debug('{}: LD D, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x51(self):
        self.registers.d = self.registers.c
        self.debug('{}: LD D, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x52(self):
        self.debug('{}: LD D, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x53(self):
        self.registers.d = self.registers.e
        self.debug('{}: LD D, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x54(self):
        self.registers.d = self.registers.h
        self.debug('{}: LD D, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x55(self):
        self.registers.d = self.registers.l
        self.debug('{}: LD D, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x56(self):
        self.registers.d = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD D, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x57(self):
        self.registers.d = self.registers.a
        self.debug('{}: LD D, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x58(self):
        self.registers.e = self.registers.b
        self.debug('{}: LD E, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x59(self):
        self.registers.e = self.registers.c
        self.debug('{}: LD E, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x5a(self):
        self.registers.e = self.registers.d
        self.debug('{}: LD E, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x5b(self):
        self.debug('{}: LD E, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x5c(self):
        self.registers.e = self.registers.h
        self.debug('{}: LD E, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x5d(self):
        self.registers.e = self.registers.l
        self.debug('{}: LD E, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x5e(self):
        self.registers.e = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD E, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x5f(self):
        self.registers.e = self.registers.a
        self.debug('{}: LD E, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x60(self):
        self.registers.h = self.registers.b
        self.debug('{}: LD H, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x61(self):
        self.registers.h = self.registers.c
        self.debug('{}: LD H, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x62(self):
        self.registers.h = self.registers.d
        self.debug('{}: LD H, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x63(self):
        self.registers.h = self.registers.e
        self.debug('{}: LD H, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x64(self):
        self.debug('{}: LD H, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x65(self):
        self.registers.h = self.registers.l
        self.debug('{}: LD H, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x66(self):
        self.registers.h = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD H, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x67(self):
        self.registers.h = self.registers.a
        self.debug('{}: LD H, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x68(self):
        self.registers.l = self.registers.b
        self.debug('{}: LD L, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x69(self):
        self.registers.l = self.registers.c
        self.debug('{}: LD L, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x6a(self):
        self.registers.l = self.registers.d
        self.debug('{}: LD L, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x6b(self):
        self.registers.l = self.registers.e
        self.debug('{}: LD L, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x6c(self):
        self.registers.l = self.registers.h
        self.debug('{}: LD L, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x6d(self):
        self.debug('{}: LD L, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x6e(self):
        self.registers.l = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD L, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x6f(self):
        self.registers.l = self.registers.a
        self.debug('{}: LD L, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x70(self):
        self.mmu.write_byte(self.registers.get_hl(),self.registers.b)
        self.debug('{}: LD (HL), B'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x71(self):
        self.mmu.write_byte(self.registers.get_hl(),self.registers.c)
        self.debug('{}: LD (HL), C'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x72(self):
        self.mmu.write_byte(self.registers.get_hl(),self.registers.d)
        self.debug('{}: LD (HL), D'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x73(self):
        self.mmu.write_byte(self.registers.get_hl(),self.registers.e)
        self.debug('{}: LD (HL), E'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x74(self):
        self.mmu.write_byte(self.registers.get_hl(),self.registers.h)
        self.debug('{}: LD (HL), H'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x75(self):
        self.mmu.write_byte(self.registers.get_hl(),self.registers.l)
        self.debug('{}: LD (HL), L'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x76(self):
        self.cpu.pre_halt_interrupt = self.mmu.read_byte(IO_Registers.IF)
        self.cpu.halted = True
        self.debug('{}: HALT'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x77(self):
        self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
        self.debug('{}: LD (HL), A'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x78(self):
        self.registers.a = self.registers.b
        self.debug('{}: LD A, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x79(self):
        self.registers.a = self.registers.c
        self.debug('{}: LD A, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x7a(self):
        self.registers.a = self.registers.d
        self.debug('{}: LD A, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x7b(self):
        self.registers.a = self.registers.e
        self.debug('{}: LD A, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x7c(self):
        self.registers.a = self.registers.h
        self.debug('{}: LD A, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x7d(self):
        self.registers.a = self.registers.l
        self.debug('{}: LD A, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x7e(self):
        self.registers.a = self.mmu.read_byte(self.registers.get_hl())
        self.debug('{}: LD A, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x7f(self):
        self.debug('{}: LD A, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x80(self):
        self.add_byte(self.registers.b)
        self.debug('{}: ADD A, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x81(self):
        self.add_byte(self.registers.c)
        self.debug('{}: ADD A, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x82(self):
        self.add_byte(self.registers.d)
        self.debug('{}: ADD A, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x83(self):
        self.add_byte(self.registers.e)
        self.debug('{}: ADD A, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x84(self):
        self.add_byte(self.registers.h)
        self.debug('{}: ADD A, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x85(self):
        self.add_byte(self.registers.l)
        self.debug('{}: ADD A, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x86(self):
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.add_byte(byte)
        self.debug('{}: ADD A, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x87(self):
        self.add_byte(self.registers.a)
        self.debug('{}: ADD A, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x88(self):
        self.adc(self.registers.b)
        self.debug('{}: ADC A, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x89(self):
        self.adc(self.registers.c)
        self.debug('{}: ADC A, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x8a(self):
        self.adc(self.registers.d)
        self.debug('{}: ADC A, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x8b(self):
        self.adc(self.registers.e)
        self.debug('{}: ADC A, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x8c(self):
        self.adc(self.registers.h)
        self.debug('{}: ADC A, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x8d(self):
        self.adc(self.registers.l)
        self.debug('{}: ADC A, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x8e(self):
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.adc(byte)
        self.debug('{}: ADC A, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x8f(self):
        self.adc(self.registers.a)
        self.debug('{}: ADC A, A'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x90(self):
        self.sub(self.registers.b)
        self.debug('{}: SUB A, B'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x91(self):
        self.sub(self.registers.c)
        self.debug('{}: SUB A, C'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x92(self):
        self.sub(self.registers.d)
        self.debug('{}: SUB A, D'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x93(self):
        self.sub(self.registers.e)
        self.debug('{}: SUB A, E'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x94(self):
        self.sub(self.registers.h)
        self.debug('{}: SUB A, H'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x95(self):
        self.sub(self.registers.l)
        self.debug('{}: SUB A, L'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x96(self):
        self.sub(self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: SUB A, (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x97(self):
        self.sub(self.registers.a)
        self.debug('{}: SUB A, A'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x98(self):
        self.sbc(self.registers.b)
        self.debug('{}: SBC A, B'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x99(self):
        self.sbc(self.registers.c)
        self.debug('{}: SBC A, C'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x9a(self):
        self.sbc(self.registers.d)
        self.debug('{}: SBC A, D'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x9b(self):
        self.sbc(self.registers.e)
        self.debug('{}: SBC A, E'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x9c(self):
        self.sbc(self.registers.h)
        self.debug('{}: SBC A, H'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x9d(self):
        self.sbc(self.registers.l)
        self.debug('{}: SBC A, L'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x9e(self):
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.sbc(byte)
        self.debug('{}: SBC A, (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x9f(self):
        self.sbc(self.registers.a)
        self.debug('{}: SBC A, A'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa0(self):
        self._and(self.registers.b)
        self.debug('{}: AND B'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa1(self):
        self._and(self.registers.c)
        self.debug('{}: AND C'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa2(self):
        self._and(self.registers.d)
        self.debug('{}: AND D'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa3(self):
        self._and(self.registers.e)
        self.debug('{}: AND E'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa4(self):
        self._and(self.registers.h)
        self.debug('{}: AND H'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa5(self):
        self._and(self.registers.l)
        self.debug('{}: AND L'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa6(self):
        byte = self.mmu.read_byte(self.registers.get_hl())
        self._and(byte)
        self.debug('{}: AND (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0xa7(self):
        self._and(self.registers.a)
        self.debug('{}: AND A'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa8(self):
        self.xor(self.registers.b)
        self.debug('{}: XOR B'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa9(self):
        self.xor(self.registers.c)
        self.debug('{}: XOR C'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xaa(self):
        self.xor(self.registers.d)
        self.debug('{}: XOR D'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xab(self):
        self.xor(self.registers.e)
        self.debug('{}: XOR E'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xac(self):
        self.xor(self.registers.h)
        self.debug('{}: XOR H'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xad(self):
        self.xor(self.registers.l)
        self.debug('{}: XOR L'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xae(self):
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.xor(byte)
        self.debug('{}: XOR (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0xaf(self):
        self.xor(self.registers.a)
        self.debug('{}: XOR A'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb0(self):
        self._or(self.registers.b)
        self.debug('{}: OR B'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb1(self):
        self._or(self.registers.c)
        self.debug('{}: OR C'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb2(self):
        self._or(self.registers.d)
        self.debug('{}: OR D'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb3(self):
        self._or(self.registers.e)
        self.debug('{}: OR E'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb4(self):
        self._or(self.registers.h)
        self.debug('{}: OR H'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb5(self):
        self._or(self.registers.l)
        self.debug('{}: OR L'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb6(self):
        byte = self.mmu.read_byte(self.registers.get_hl())
        self._or(byte)
        self.debug('{}: OR (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0xb7(self):
        self._or(self.registers.a)
        self.debug('{}: OR A'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb8(self):
        self.cp(self.registers.b)
        self.debug('{}: CP B'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb9(self):
        self.cp(self.registers.c)
        self.debug('{}: CP C'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xba(self):
        self.cp(self.registers.d)
        self.debug('{}: CP D'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xbb(self):
        self.cp(self.registers.e)
        self.debug('{}: CP E'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xbc(self):
        self.cp(self.registers.h)
        self.debug('{}: CP H'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xbd(self):
        self.cp(self.registers.l)
        self.debug('{}: CP L'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xbe(self):
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.cp(byte)
        self.debug('{}: CP (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0xbf(self):
        self.cp(self.registers.a)
        self.debug('{}: CP A'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xc0(self):
        self.debug('{}: RET NZ'.format(hex(self.registers.pc-1)))
        if not self.registers.is_z_flag():
            self.registers.pc = self.stackManager.pop_word()
            return 20
        return 8
    
    def instruction_0xc1(self):
        self.registers.set_bc(self.stackManager.pop_word())
        self.debug('{}: POP BC'.format(hex(self.registers.pc-1)))
        return 12

    def instruction_0xc2(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: JP NZ, {}'.format(hex(self.registers.pc-3), hex(word)))
        if not self.registers.is_z_flag():
            self.registers.pc = word
            return 16
        else:
            return 12

    def instruction_0xc3(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc = word
        self.debug('{}: JP {}'.format(hex(self.registers.pc-3), hex(word)))
        return 16

    def instruction_0xc4(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: CALL NZ, {}'.format(hex(self.registers.pc-3), hex(word)))
        if not self.registers.is_z_flag():
            self.stackManager.push_word(self.registers.pc)
            self.registers.pc = word
            return 24
        else:
            return 12
    
    def instruction_0xc5(self):
        self.stackManager.push_word(self.registers.get_bc())
        self.debug('{}: PUSH BC'.format(hex(self.registers.pc-1)))
        return 16
    
    def instruction_0xc6(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.add_byte(byte)
        self.debug('{}: ADD A, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def instruction_0xc7(self):
        self.debug('{}: RST 0x00'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x00
        return 16

    def instruction_0xc8(self):
        self.debug('{}: RET Z'.format(hex(self.registers.pc-1)))
        if self.registers.is_z_flag():
            self.registers.pc = self.stackManager.pop_word()
            return 20
        return 8

    def instruction_0xc9(self):
        self.registers.pc = self.stackManager.pop_word()
        self.debug('{}: RET'.format(hex(self.registers.pc-1)))
        return 16

    def instruction_0xca(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: JP Z, {}'.format(hex(self.registers.pc-3), hex(word)))
        if self.registers.is_z_flag():
            self.registers.pc = word
            return 16
        else:
            return 12

    def instruction_0xcc(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: CALL Z, {}'.format(hex(self.registers.pc-3), hex(word)))
        if self.registers.is_z_flag():
            self.stackManager.push_word(self.registers.pc)
            self.registers.pc = word
            return 24
        else:
            return 12

    def instruction_0xcd(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: CALL {}'.format(hex(self.registers.pc-3), hex(word)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = word
        return 12
    
    def instruction_0xce(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.adc(byte)
        self.debug('{}: ADC A, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def instruction_0xcf(self):
        self.debug('{}: RST 0x08'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x08
        return 16

    def instruction_0xd0(self):
        self.debug('{}: RET NC'.format(hex(self.registers.pc-1)))
        if not self.registers.is_c_flag():
            self.registers.pc = self.stackManager.pop_word()
            return 20
        return 8
    
    def instruction_0xd1(self):
        self.registers.set_de(self.stackManager.pop_word())
        self.debug('{}: POP DE'.format(hex(self.registers.pc-1)))
        return 12

    def instruction_0xd2(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: JP NC, {}'.format(hex(self.registers.pc-3), hex(word)))
        if not self.registers.is_c_flag():
            self.registers.pc = word
            return 16
        else:
            return 12

    def instruction_0xd4(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: CALL NC, {}'.format(hex(self.registers.pc-3), hex(word)))
        if not self.registers.is_c_flag():
            self.stackManager.push_word(self.registers.pc)
            self.registers.pc = word
            return 24
        else:
            return 12
    
    def instruction_0xd5(self):
        self.stackManager.push_word(self.registers.get_de())
        self.debug('{}: PUSH DE'.format(hex(self.registers.pc-1)))
        return 16

    def instruction_0xd6(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.sub(byte)
        self.debug('{}: SUB A, {}'.format(hex(self.registers.pc-2),hex(byte)))
        return 8

    def instruction_0xd7(self):
        self.debug('{}: RST 0x10'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x10
        return 16

    def instruction_0xd8(self):
        self.debug('{}: RET C'.format(hex(self.registers.pc-1)))
        if self.registers.is_c_flag():
            self.registers.pc = self.stackManager.pop_word()
            return 20
        return 8

    def instruction_0xd9(self):
        self.registers.pc = self.stackManager.pop_word()
        self.cpu.ime = True
        self.debug('{}: RETI'.format(hex(self.registers.pc-1)))
        return 16

    def instruction_0xda(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: JP C, {}'.format(hex(self.registers.pc-3), hex(word)))
        if self.registers.is_c_flag():
            self.registers.pc = word
            return 16
        else:
            return 12

    def instruction_0xdc(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.debug('{}: CALL C, {}'.format(hex(self.registers.pc-3), hex(word)))
        if self.registers.is_c_flag():
            self.stackManager.push_word(self.registers.pc)
            self.registers.pc = word
            return 24
        else:
            return 12

    def instruction_0xdf(self):
        self.debug('{}: RST 0x18'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x18
        return 16

    def instruction_0xe0(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.mmu.write_byte((byte + 0xff00), self.registers.a)
        self.debug('{}: LDH ({}), A'.format(hex(self.registers.pc-2),hex(byte)))
        return 12
    
    def instruction_0xe1(self):
        self.registers.set_hl(self.stackManager.pop_word())
        self.debug('{}: POP HL'.format(hex(self.registers.pc-1)))
        return 12

    def instruction_0xe2(self):
        self.mmu.write_byte((self.registers.c + 0xff00), self.registers.a)
        self.debug('{}: LD (0xff00+C), A'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0xe5(self):
        self.stackManager.push_word(self.registers.get_hl())
        self.debug('{}: PUSH HL'.format(hex(self.registers.pc-1)))
        return 16

    def instruction_0xe6(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self._and(byte)
        self.debug('{}: AND {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def instruction_0xe7(self):
        self.debug('{}: RST 0x20'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x20
        return 16

    def instruction_0xe9(self):
        word = self.mmu.read_word(self.registers.get_hl())
        self.registers.pc = word
        self.debug('{}: JP (HL)'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0xea(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.mmu.write_byte(word, self.registers.a)
        self.debug('{}: LD ({}), A'.format(hex(self.registers.pc-3),hex(word)))
        return 8

    def instruction_0xee(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.xor(byte)
        self.debug('{}: XOR {}'.format(hex(self.registers.pc-1), hex(byte)))
        return 8

    def instruction_0xef(self):
        self.debug('{}: RST 0x28'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x28
        return 16
    
    def instruction_0xf0(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.a = self.mmu.read_byte((byte + 0xff00))
        self.debug('{}: LDH A, ({})'.format(hex(self.registers.pc-2),hex(byte)))
        return 12
    
    def instruction_0xf1(self):
        self.registers.set_af(self.stackManager.pop_word())
        self.debug('{}: POP AF'.format(hex(self.registers.pc-1)))
        return 12
    
    def instruction_0xf2(self):
        self.registers.a = self.mmu.read_byte(self.registers.c + 0xff00)
        self.debug('{}: LD A, (0xff00+C)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0xf3(self):
        self.cpu.ime = False
        self.debug('{}: DI'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0xf5(self):
        self.stackManager.push_word(self.registers.get_af())
        self.debug('{}: PUSH AF'.format(hex(self.registers.pc-1)))
        return 16

    def instruction_0xf6(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self._or(self.byte)
        self.debug('{}: OR {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def instruction_0xf7(self):
        self.debug('{}: RST 0x30'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x30
        return 16
    
    def instruction_0xf8(self):
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
        self.debug('{}: LDHL SP, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 12
    
    def instruction_0xf9(self):
        self.registers.sp = self.registers.get_hl()
        self.debug('{}: LD SP, HL'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0xfa(self):
        byte = self.mmu.read_byte(self.mmu.read_word(self.registers.pc))
        self.registers.pc += 2
        self.registers.a = byte
        self.debug('{}: LD A, ({})'.format(hex(self.registers.pc-3),hex(byte)))
        return 16

    def instruction_0xfb(self):
        self.cpu.ime = True
        self.debug('{}: EI'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xfe(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.cp(byte)
        self.debug('{}: CP {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8

    def instruction_0xff(self):
        self.debug('{}: RST 0x38'.format(hex(self.registers.pc-1)))
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x38
        return 16

    def instruction_0xcb11(self):
        self.registers.c = self.rl(self.registers.c)
        self.debug('{}: RL C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb30(self):
        self.registers.b = self.swap(self.registers.b)
        self.debug('{}: SWAP B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb31(self):
        self.registers.c = self.swap(self.registers.c)
        self.debug('{}: SWAP C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb32(self):
        self.registers.d = self.swap(self.registers.d)
        self.debug('{}: SWAP D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb33(self):
        self.registers.e = self.swap(self.registers.e)
        self.debug('{}: SWAP E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb34(self):
        self.registers.h = self.swap(self.registers.h)
        self.debug('{}: SWAP H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb35(self):
        self.registers.l = self.swap(self.registers.l)
        self.debug('{}: SWAP L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb36(self):
        self.mmu.write_byte(self.registers.get_hl(), self.swap(self.mmu.read_byte(self.registers.get_hl())))
        self.debug('{}: SWAP (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb37(self):
        self.registers.a = self.swap(self.registers.a)
        self.debug('{}: SWAP A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb40(self):
        self.bit(0, self.registers.b)
        self.debug('{}: BIT 0, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb41(self):
        self.bit(0, self.registers.c)
        self.debug('{}: BIT 0, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb42(self):
        self.bit(0, self.registers.d)
        self.debug('{}: BIT 0, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb43(self):
        self.bit(0, self.registers.e)
        self.debug('{}: BIT 0, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb44(self):
        self.bit(0, self.registers.h)
        self.debug('{}: BIT 0, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb45(self):
        self.bit(0, self.registers.l)
        self.debug('{}: BIT 0, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb46(self):
        self.bit(0, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 0, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb47(self):
        self.bit(0, self.registers.a)
        self.debug('{}: BIT 0, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb48(self):
        self.bit(1, self.registers.b)
        self.debug('{}: BIT 1, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb49(self):
        self.bit(1, self.registers.c)
        self.debug('{}: BIT 1, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb4a(self):
        self.bit(1, self.registers.d)
        self.debug('{}: BIT 1, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb4b(self):
        self.bit(1, self.registers.e)
        self.debug('{}: BIT 1, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb4c(self):
        self.bit(1, self.registers.h)
        self.debug('{}: BIT 1, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb4d(self):
        self.bit(1, self.registers.l)
        self.debug('{}: BIT 1, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb4e(self):
        self.bit(1, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 1, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb4f(self):
        self.bit(1, self.registers.a)
        self.debug('{}: BIT 1, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb50(self):
        self.bit(2, self.registers.b)
        self.debug('{}: BIT 2, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb51(self):
        self.bit(2, self.registers.c)
        self.debug('{}: BIT 2, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb52(self):
        self.bit(2, self.registers.d)
        self.debug('{}: BIT 2, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb53(self):
        self.bit(2, self.registers.e)
        self.debug('{}: BIT 2, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb54(self):
        self.bit(2, self.registers.h)
        self.debug('{}: BIT 2, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb55(self):
        self.bit(2, self.registers.l)
        self.debug('{}: BIT 2, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb56(self):
        self.bit(2, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 2, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb57(self):
        self.bit(2, self.registers.a)
        self.debug('{}: BIT 2, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb58(self):
        self.bit(3, self.registers.b)
        self.debug('{}: BIT 3, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb59(self):
        self.bit(3, self.registers.c)
        self.debug('{}: BIT 3, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb5a(self):
        self.bit(3, self.registers.d)
        self.debug('{}: BIT 3, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb5b(self):
        self.bit(3, self.registers.e)
        self.debug('{}: BIT 3, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb5c(self):
        self.bit(3, self.registers.h)
        self.debug('{}: BIT 3, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb5d(self):
        self.bit(3, self.registers.l)
        self.debug('{}: BIT 3, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb5e(self):
        self.bit(3, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 3, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb5f(self):
        self.bit(3, self.registers.a)
        self.debug('{}: BIT 3, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb60(self):
        self.bit(4, self.registers.b)
        self.debug('{}: BIT 4, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb61(self):
        self.bit(4, self.registers.c)
        self.debug('{}: BIT 4, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb62(self):
        self.bit(4, self.registers.d)
        self.debug('{}: BIT 4, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb63(self):
        self.bit(4, self.registers.e)
        self.debug('{}: BIT 4, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb64(self):
        self.bit(4, self.registers.h)
        self.debug('{}: BIT 4, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb65(self):
        self.bit(4, self.registers.l)
        self.debug('{}: BIT 4, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb66(self):
        self.bit(4, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 4, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb67(self):
        self.bit(4, self.registers.a)
        self.debug('{}: BIT 4, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb68(self):
        self.bit(5, self.registers.b)
        self.debug('{}: BIT 5, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb69(self):
        self.bit(5, self.registers.c)
        self.debug('{}: BIT 5, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb6a(self):
        self.bit(5, self.registers.d)
        self.debug('{}: BIT 5, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb6b(self):
        self.bit(5, self.registers.e)
        self.debug('{}: BIT 5, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb6c(self):
        self.bit(5, self.registers.h)
        self.debug('{}: BIT 5, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb6d(self):
        self.bit(5, self.registers.l)
        self.debug('{}: BIT 5, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb6e(self):
        self.bit(5, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 5, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb6f(self):
        self.bit(5, self.registers.a)
        self.debug('{}: BIT 5, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb70(self):
        self.bit(6, self.registers.b)
        self.debug('{}: BIT 6, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb71(self):
        self.bit(6, self.registers.c)
        self.debug('{}: BIT 6, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb72(self):
        self.bit(6, self.registers.d)
        self.debug('{}: BIT 6, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb73(self):
        self.bit(6, self.registers.e)
        self.debug('{}: BIT 6, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb74(self):
        self.bit(6, self.registers.h)
        self.debug('{}: BIT 6, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb75(self):
        self.bit(6, self.registers.l)
        self.debug('{}: BIT 6, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb76(self):
        self.bit(6, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 6, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb77(self):
        self.bit(6, self.registers.a)
        self.debug('{}: BIT 6, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb78(self):
        self.bit(7, self.registers.b)
        self.debug('{}: BIT 7, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb79(self):
        self.bit(7, self.registers.c)
        self.debug('{}: BIT 7, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb7a(self):
        self.bit(7, self.registers.d)
        self.debug('{}: BIT 7, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb7b(self):
        self.bit(7, self.registers.e)
        self.debug('{}: BIT 7, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb7c(self):
        self.bit(7, self.registers.h)
        self.debug('{}: BIT 7, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb7d(self):
        self.bit(7, self.registers.l)
        self.debug('{}: BIT 7, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb7e(self):
        self.bit(7, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: BIT 7, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb7f(self):
        self.bit(7, self.registers.a)
        self.debug('{}: BIT 7, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb80(self):
        self.res(0, self.registers.b)
        self.debug('{}: RES 0, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb81(self):
        self.res(0, self.registers.c)
        self.debug('{}: RES 0, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb82(self):
        self.res(0, self.registers.d)
        self.debug('{}: RES 0, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb83(self):
        self.res(0, self.registers.e)
        self.debug('{}: RES 0, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb84(self):
        self.res(0, self.registers.h)
        self.debug('{}: RES 0, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb85(self):
        self.res(0, self.registers.l)
        self.debug('{}: RES 0, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb86(self):
        self.res(0, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: RES 0, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb87(self):
        self.res(0, self.registers.a)
        self.debug('{}: RES 0, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb88(self):
        self.res(1, self.registers.b)
        self.debug('{}: RES 1, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb89(self):
        self.res(1, self.registers.c)
        self.debug('{}: RES 1, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb8a(self):
        self.res(1, self.registers.d)
        self.debug('{}: RES 1, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb8b(self):
        self.res(1, self.registers.e)
        self.debug('{}: RES 1, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb8c(self):
        self.res(1, self.registers.h)
        self.debug('{}: RES 1, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb8d(self):
        self.res(1, self.registers.l)
        self.debug('{}: RES 1, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb8e(self):
        self.res(1, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: RES 1, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb8f(self):
        self.res(1, self.registers.a)
        self.debug('{}: RES 1, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb90(self):
        self.res(2, self.registers.b)
        self.debug('{}: RES 2, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb91(self):
        self.res(2, self.registers.c)
        self.debug('{}: RES 2, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb92(self):
        self.res(2, self.registers.d)
        self.debug('{}: RES 2, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb93(self):
        self.res(2, self.registers.e)
        self.debug('{}: RES 2, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb94(self):
        self.res(2, self.registers.h)
        self.debug('{}: RES 2, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb95(self):
        self.res(2, self.registers.l)
        self.debug('{}: RES 2, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb96(self):
        self.res(2, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: RES 2, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb97(self):
        self.res(2, self.registers.a)
        self.debug('{}: RES 2, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb98(self):
        self.res(3, self.registers.b)
        self.debug('{}: RES 3, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb99(self):
        self.res(3, self.registers.c)
        self.debug('{}: RES 3, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb9a(self):
        self.res(3, self.registers.d)
        self.debug('{}: RES 3, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb9b(self):
        self.res(3, self.registers.e)
        self.debug('{}: RES 3, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb9c(self):
        self.res(3, self.registers.h)
        self.debug('{}: RES 3, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb9d(self):
        self.res(3, self.registers.l)
        self.debug('{}: RES 3, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcb9e(self):
        self.res(3, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: RES 3, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcb9f(self):
        self.res(3, self.registers.a)
        self.debug('{}: RES 3, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcba0(self):
        self.res(4, self.registers.b)
        self.debug('{}: RES 4, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcba1(self):
        self.res(4, self.registers.c)
        self.debug('{}: RES 4, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcba2(self):
        self.res(4, self.registers.d)
        self.debug('{}: RES 4, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcba3(self):
        self.res(4, self.registers.e)
        self.debug('{}: RES 4, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcba4(self):
        self.res(4, self.registers.h)
        self.debug('{}: RES 4, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcba5(self):
        self.res(4, self.registers.l)
        self.debug('{}: RES 4, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcba6(self):
        self.res(4, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: RES 4, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcba7(self):
        self.res(4, self.registers.a)
        self.debug('{}: RES 4, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcba8(self):
        self.res(5, self.registers.b)
        self.debug('{}: RES 5, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcba9(self):
        self.res(5, self.registers.c)
        self.debug('{}: RES 5, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbaa(self):
        self.res(5, self.registers.d)
        self.debug('{}: RES 5, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbab(self):
        self.res(5, self.registers.e)
        self.debug('{}: RES 5, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbac(self):
        self.res(5, self.registers.h)
        self.debug('{}: RES 5, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbad(self):
        self.res(5, self.registers.l)
        self.debug('{}: RES 5, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbae(self):
        self.res(5, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: RES 5, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcbaf(self):
        self.res(5, self.registers.a)
        self.debug('{}: RES 5, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbb0(self):
        self.res(6, self.registers.b)
        self.debug('{}: RES 6, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbb1(self):
        self.res(6, self.registers.c)
        self.debug('{}: RES 6, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbb2(self):
        self.res(6, self.registers.d)
        self.debug('{}: RES 6, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbb3(self):
        self.res(6, self.registers.e)
        self.debug('{}: RES 6, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbb4(self):
        self.res(6, self.registers.h)
        self.debug('{}: RES 6, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbb5(self):
        self.res(6, self.registers.l)
        self.debug('{}: RES 6, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbb6(self):
        self.res(6, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: RES 6, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcbb7(self):
        self.res(6, self.registers.a)
        self.debug('{}: RES 6, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbb8(self):
        self.res(7, self.registers.b)
        self.debug('{}: RES 7, B'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbb9(self):
        self.res(7, self.registers.c)
        self.debug('{}: RES 7, C'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbba(self):
        self.res(7, self.registers.d)
        self.debug('{}: RES 7, D'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbbb(self):
        self.res(7, self.registers.e)
        self.debug('{}: RES 7, E'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbbc(self):
        self.res(7, self.registers.h)
        self.debug('{}: RES 7, H'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbbd(self):
        self.res(7, self.registers.l)
        self.debug('{}: RES 7, L'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbbe(self):
        self.res(7, self.mmu.read_byte(self.registers.get_hl()))
        self.debug('{}: RES 7, (HL)'.format(hex(self.registers.pc-2)))
        return 16

    def instruction_0xcbbf(self):
        self.res(7, self.registers.a)
        self.debug('{}: RES 7, A'.format(hex(self.registers.pc-2)))
        return 8

    def instruction_0xcbc7(self):
        self.registers.a = set_bit(0, self.registers.a)
        self.debug('{}: SET 0, A'.format(hex(self.registers.pc-2)))
        return 8
    
    def unimplemented(self, opcode):
        logging.error('{}: Unknow Opcode {}'.format(hex(self.registers.pc-1), hex(opcode)))
        raise NotImplementedError()

    def add_byte(self, value):
        byte = self.registers.a + value
        if (byte & 0xff) == 0x00:
            self.registers.set_z_flag()
        else:
                self.registers.reset_z_flag()
        if (self.registers.a ^ value ^ byte) & 0x100 == 0x100:
            self.registers.set_c_flag()
        else: 
            self.registers.reset_c_flag()
        if (self.registers.a ^ value ^ byte) & 0x10 == 0x10: 
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()
        self.registers.reset_n_flag()
        self.registers.a = byte & 0xff

    def add_word(self, value1, value2):
        result = value1 + value2

        self.registers.reset_n_flag()
        if result & 0x10000 == 0x10000: 
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        if (value1 ^ value2 ^ (result & 0xFFFF)) & 0x1000 == 0x1000: 
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()

        return result & 0xFFFF

    def adc(self, value):
        carry = 1 if self.registers.is_c_flag() else 0
        result = self.registers.a + value + carry
        if result & 0xff == 0x0: 
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        if result > 0xff: 
            self.registers.set_c_flag()
        else: 
            self.registers.reset_c_flag()
        if (self.registers.a & 0xf) + (value & 0xf) + carry > 0xf: 
            self.registers.set_h_flag()
        else: 
            self.registers.reset_h_flag()
        self.registers.reset_n_flag()
        self.registers.a = result & 0xff
        
    def sub(self, value):
        result = self.registers.a - value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        if (self.registers.a ^ value ^ result) & 0x100 == 0x100:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        if (self.registers.a ^ value ^ result) & 0x10 == 0x10:
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()
        self.registers.set_n_flag()
        self.registers.a = result & 0xff

    def sbc(self, value):
        carry = 1 if self.registers.is_c_flag() else 0
        result = self.registers.a - value - carry
        if result & 0xff == 0x0:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        if result < 0x0:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        if (self.registers.a & 0xF) - (value & 0xF) - carry < 0: 
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()
        self.registers.set_n_flag()
        self.registers.a = result & 0xff

    def _and(self, value):
        result = self.registers.a & value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.set_h_flag()
        self.registers.a = result & 0xff

    def _or(self, value):
        result = self.registers.a | value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.registers.a = result & 0xff

    def xor(self, value):
        result = self.registers.a ^ value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.registers.a = result & 0xff

    def cp(self, value):
        result = self.registers.a - value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        if self.registers.a < value:
            self.registers.set_c_flag()
        else: 
            self.registers.reset_c_flag()
        if (result & 0xf) > (self.registers.a & 0xf):
            self.registers.set_h_flag()
        else: 
            self.registers.reset_h_flag()
        self.registers.set_n_flag()

    def bit(self, pos, value):
        bit = 1 if value & bit_mask[pos] == bit_mask[pos] else 0
        if bit & 0xff == 0x0:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.set_h_flag()

    def res(self, pos, value):
        return value & (bit_mask[pos] ^ 0xff)

    def swap(self, value):
        value = ((value << 4) & 0xff) | (value >> 4)
        if value & 0xff == 0x00:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.registers.reset_c_flag()
        return value


    def inc_byte(self, value):
        result = value + 1
        if result & 0xff == 0x0:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        if result & 0xf == 0x0:
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()
        self.registers.reset_n_flag()
        return result & 0xff

    def dec_byte(self, value):
        result = value - 1
        if result & 0xff == 0x0:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        if result & 0xf == 0x0:
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()
        self.registers.set_n_flag()
        return result & 0xff

    def rl(self, value):
        carry = 1 if self.registers.is_c_flag() else 0
        if value & 0x80 == 0x80:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        result = ((value << 1) & 0xff) + carry
        if result & 0xFF == 0x0:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        return result

    def rlc(self, value):
        bit_out = 0x1 if value & 0x80 == 0x80 else 0x0
        if bit_out == 0x1:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        return ((value << 1) & 0xff) + bit_out

    def rr(self, value):
        carry = 0x80 if self.registers.is_c_flag() else 0x0
        if value & 0x1 == 0x1:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        return (value >> 1) + carry

    def rrc(self, value):
        bit_out = 0x80 if value & 0x1 == 0x1 else 0x0
        if bit_out == 0x80:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        return (value >> 1) + bit_out

    def debug(self, text):
        logging.debug(text)
