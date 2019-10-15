#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from vsgb.byte_operations import signed_value, set_bit, bit_mask
from vsgb.io_registers import IO_Registers
from vsgb.registers import Registers

class InstructionPerformer:

    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = cpu.mmu
        self.registers = cpu.registers
        self.stackManager = cpu.stackManager
        self.instrs = [
            self.inst0x0, self.inst0x1, self.inst0x2, self.inst0x3, self.inst0x4, self.inst0x5, self.inst0x6, self.inst0x7, self.inst0x8, self.inst0x9, self.inst0xa, self.inst0xb, self.inst0xc, self.inst0xd, self.inst0xe, self.inst0xf, 
            self.inst0x10, self.inst0x11, self.inst0x12, self.inst0x13, self.inst0x14, self.inst0x15, self.inst0x16, self.inst0x17, self.inst0x18, self.inst0x19, self.inst0x1a, self.inst0x1b, self.inst0x1c, self.inst0x1d, self.inst0x1e, self.inst0x1f, 
            self.inst0x20, self.inst0x21, self.inst0x22, self.inst0x23, self.inst0x24, self.inst0x25, self.inst0x26, self.inst0x27, self.inst0x28, self.inst0x29, self.inst0x2a, self.inst0x2b, self.inst0x2c, self.inst0x2d, self.inst0x2e, self.inst0x2f, 
            self.inst0x30, self.inst0x31, self.inst0x32, self.inst0x33, self.inst0x34, self.inst0x35, self.inst0x36, self.inst0x37, self.inst0x38, self.inst0x39, self.inst0x3a, self.inst0x3b, self.inst0x3c, self.inst0x3d, self.inst0x3e, self.inst0x3f, 
            self.inst0x40, self.inst0x41, self.inst0x42, self.inst0x43, self.inst0x44, self.inst0x45, self.inst0x46, self.inst0x47, self.inst0x48, self.inst0x49, self.inst0x4a, self.inst0x4b, self.inst0x4c, self.inst0x4d, self.inst0x4e, self.inst0x4f, 
            self.inst0x50, self.inst0x51, self.inst0x52, self.inst0x53, self.inst0x54, self.inst0x55, self.inst0x56, self.inst0x57, self.inst0x58, self.inst0x59, self.inst0x5a, self.inst0x5b, self.inst0x5c, self.inst0x5d, self.inst0x5e, self.inst0x5f, 
            self.inst0x60, self.inst0x61, self.inst0x62, self.inst0x63, self.inst0x64, self.inst0x65, self.inst0x66, self.inst0x67, self.inst0x68, self.inst0x69, self.inst0x6a, self.inst0x6b, self.inst0x6c, self.inst0x6d, self.inst0x6e, self.inst0x6f, 
            self.inst0x70, self.inst0x71, self.inst0x72, self.inst0x73, self.inst0x74, self.inst0x75, self.inst0x76, self.inst0x77, self.inst0x78, self.inst0x79, self.inst0x7a, self.inst0x7b, self.inst0x7c, self.inst0x7d, self.inst0x7e, self.inst0x7f, 
            self.inst0x80, self.inst0x81, self.inst0x82, self.inst0x83, self.inst0x84, self.inst0x85, self.inst0x86, self.inst0x87, self.inst0x88, self.inst0x89, self.inst0x8a, self.inst0x8b, self.inst0x8c, self.inst0x8d, self.inst0x8e, self.inst0x8f, 
            self.inst0x90, self.inst0x91, self.inst0x92, self.inst0x93, self.inst0x94, self.inst0x95, self.inst0x96, self.inst0x97, self.inst0x98, self.inst0x99, self.inst0x9a, self.inst0x9b, self.inst0x9c, self.inst0x9d, self.inst0x9e, self.inst0x9f, 
            self.inst0xa0, self.inst0xa1, self.inst0xa2, self.inst0xa3, self.inst0xa4, self.inst0xa5, self.inst0xa6, self.inst0xa7, self.inst0xa8, self.inst0xa9, self.inst0xaa, self.inst0xab, self.inst0xac, self.inst0xad, self.inst0xae, self.inst0xaf, 
            self.inst0xb0, self.inst0xb1, self.inst0xb2, self.inst0xb3, self.inst0xb4, self.inst0xb5, self.inst0xb6, self.inst0xb7, self.inst0xb8, self.inst0xb9, self.inst0xba, self.inst0xbb, self.inst0xbc, self.inst0xbd, self.inst0xbe, self.inst0xbf, 
            self.inst0xc0, self.inst0xc1, self.inst0xc2, self.inst0xc3, self.inst0xc4, self.inst0xc5, self.inst0xc6, self.inst0xc7, self.inst0xc8, self.inst0xc9, self.inst0xca, None, self.inst0xcc, self.inst0xcd, self.inst0xce, self.inst0xcf, 
            self.inst0xd0, self.inst0xd1, self.inst0xd2, None, self.inst0xd4, self.inst0xd5, self.inst0xd6, self.inst0xd7, self.inst0xd8, self.inst0xd9, self.inst0xda, None, self.inst0xdc, None, self.inst0xde, self.inst0xdf, 
            self.inst0xe0, self.inst0xe1, self.inst0xe2, None, None, self.inst0xe5, self.inst0xe6, self.inst0xe7, self.inst0xe8, self.inst0xe9, self.inst0xea, None, None, None, self.inst0xee, self.inst0xef, 
            self.inst0xf0, self.inst0xf1, self.inst0xf2, self.inst0xf3, None, self.inst0xf5, self.inst0xf6, self.inst0xf7, self.inst0xf8, self.inst0xf9, self.inst0xfa, self.inst0xfb, None, None, self.inst0xfe, self.inst0xff, 
            self.inst0xcb00, self.inst0xcb01, self.inst0xcb02, self.inst0xcb03, self.inst0xcb04, self.inst0xcb05, self.inst0xcb06, self.inst0xcb07, self.inst0xcb08, self.inst0xcb09, self.inst0xcb0a, self.inst0xcb0b, self.inst0xcb0c, self.inst0xcb0d, self.inst0xcb0e, self.inst0xcb0f, 
            self.inst0xcb10, self.inst0xcb11, self.inst0xcb12, self.inst0xcb13, self.inst0xcb14, self.inst0xcb15, self.inst0xcb16, self.inst0xcb17, self.inst0xcb18, self.inst0xcb19, self.inst0xcb1a, self.inst0xcb1b, self.inst0xcb1c, self.inst0xcb1d, self.inst0xcb1e, self.inst0xcb1f, 
            self.inst0xcb20, self.inst0xcb21, self.inst0xcb22, self.inst0xcb23, self.inst0xcb24, self.inst0xcb25, self.inst0xcb26, self.inst0xcb27, self.inst0xcb28, self.inst0xcb29, self.inst0xcb2a, self.inst0xcb2b, self.inst0xcb2c, self.inst0xcb2d, self.inst0xcb2e, self.inst0xcb2f, 
            self.inst0xcb30, self.inst0xcb31, self.inst0xcb32, self.inst0xcb33, self.inst0xcb34, self.inst0xcb35, self.inst0xcb36, self.inst0xcb37, self.inst0xcb38, self.inst0xcb39, self.inst0xcb3a, self.inst0xcb3b, self.inst0xcb3c, self.inst0xcb3d, self.inst0xcb3e, self.inst0xcb3f, 
            self.inst0xcb40, self.inst0xcb41, self.inst0xcb42, self.inst0xcb43, self.inst0xcb44, self.inst0xcb45, self.inst0xcb46, self.inst0xcb47, self.inst0xcb48, self.inst0xcb49, self.inst0xcb4a, self.inst0xcb4b, self.inst0xcb4c, self.inst0xcb4d, self.inst0xcb4e, self.inst0xcb4f, 
            self.inst0xcb50, self.inst0xcb51, self.inst0xcb52, self.inst0xcb53, self.inst0xcb54, self.inst0xcb55, self.inst0xcb56, self.inst0xcb57, self.inst0xcb58, self.inst0xcb59, self.inst0xcb5a, self.inst0xcb5b, self.inst0xcb5c, self.inst0xcb5d, self.inst0xcb5e, self.inst0xcb5f, 
            self.inst0xcb60, self.inst0xcb61, self.inst0xcb62, self.inst0xcb63, self.inst0xcb64, self.inst0xcb65, self.inst0xcb66, self.inst0xcb67, self.inst0xcb68, self.inst0xcb69, self.inst0xcb6a, self.inst0xcb6b, self.inst0xcb6c, self.inst0xcb6d, self.inst0xcb6e, self.inst0xcb6f, 
            self.inst0xcb70, self.inst0xcb71, self.inst0xcb72, self.inst0xcb73, self.inst0xcb74, self.inst0xcb75, self.inst0xcb76, self.inst0xcb77, self.inst0xcb78, self.inst0xcb79, self.inst0xcb7a, self.inst0xcb7b, self.inst0xcb7c, self.inst0xcb7d, self.inst0xcb7e, self.inst0xcb7f, 
            self.inst0xcb80, self.inst0xcb81, self.inst0xcb82, self.inst0xcb83, self.inst0xcb84, self.inst0xcb85, self.inst0xcb86, self.inst0xcb87, self.inst0xcb88, self.inst0xcb89, self.inst0xcb8a, self.inst0xcb8b, self.inst0xcb8c, self.inst0xcb8d, self.inst0xcb8e, self.inst0xcb8f, 
            self.inst0xcb90, self.inst0xcb91, self.inst0xcb92, self.inst0xcb93, self.inst0xcb94, self.inst0xcb95, self.inst0xcb96, self.inst0xcb97, self.inst0xcb98, self.inst0xcb99, self.inst0xcb9a, self.inst0xcb9b, self.inst0xcb9c, self.inst0xcb9d, self.inst0xcb9e, self.inst0xcb9f, 
            self.inst0xcba0, self.inst0xcba1, self.inst0xcba2, self.inst0xcba3, self.inst0xcba4, self.inst0xcba5, self.inst0xcba6, self.inst0xcba7, self.inst0xcba8, self.inst0xcba9, self.inst0xcbaa, self.inst0xcbab, self.inst0xcbac, self.inst0xcbad, self.inst0xcbae, self.inst0xcbaf, 
            self.inst0xcbb0, self.inst0xcbb1, self.inst0xcbb2, self.inst0xcbb3, self.inst0xcbb4, self.inst0xcbb5, self.inst0xcbb6, self.inst0xcbb7, self.inst0xcbb8, self.inst0xcbb9, self.inst0xcbba, self.inst0xcbbb, self.inst0xcbbc, self.inst0xcbbd, self.inst0xcbbe, self.inst0xcbbf, 
            self.inst0xcbc0, self.inst0xcbc1, self.inst0xcbc2, self.inst0xcbc3, self.inst0xcbc4, self.inst0xcbc5, self.inst0xcbc6, self.inst0xcbc7, self.inst0xcbc8, self.inst0xcbc9, self.inst0xcbca, self.inst0xcbcb, self.inst0xcbcc, self.inst0xcbcd, self.inst0xcbce, self.inst0xcbcf, 
            self.inst0xcbd0, self.inst0xcbd1, self.inst0xcbd2, self.inst0xcbd3, self.inst0xcbd4, self.inst0xcbd5, self.inst0xcbd6, self.inst0xcbd7, self.inst0xcbd8, self.inst0xcbd9, self.inst0xcbda, self.inst0xcbdb, self.inst0xcbdc, self.inst0xcbdd, self.inst0xcbde, self.inst0xcbdf, 
            self.inst0xcbe0, self.inst0xcbe1, self.inst0xcbe2, self.inst0xcbe3, self.inst0xcbe4, self.inst0xcbe5, self.inst0xcbe6, self.inst0xcbe7, self.inst0xcbe8, self.inst0xcbe9, self.inst0xcbea, self.inst0xcbeb, self.inst0xcbec, self.inst0xcbed, self.inst0xcbee, self.inst0xcbef, 
            self.inst0xcbf0, self.inst0xcbf1, self.inst0xcbf2, self.inst0xcbf3, self.inst0xcbf4, self.inst0xcbf5, self.inst0xcbf6, self.inst0xcbf7, self.inst0xcbf8, self.inst0xcbf9, self.inst0xcbfa, self.inst0xcbfb, self.inst0xcbfc, self.inst0xcbfd, self.inst0xcbfe, self.inst0xcbff 
        ]

    def perform_instruction(self, opcode: int) -> int:
        if opcode >= 0xcb00:
            return self.instrs[opcode - 0xca00]()
        return self.instrs[opcode]()
    
    def inst0x0(self) -> int:
        return 4
    
    def inst0x1(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.set_bc(word) 
        return 12
    
    def inst0x2(self) -> int:
        self.mmu.write_byte(self.registers.get_bc(), self.registers.a)
        return 8

    def inst0x3(self) -> int:
        self.registers.set_bc((self.registers.get_bc() + 1) & 0xffff )
        return 8

    def inst0x4(self) -> int:
        self.registers.b = self.inc_byte(self.registers.b)
        return 4

    def inst0x5(self) -> int:
        self.registers.b = self.dec_byte(self.registers.b)
        return 4
    
    def inst0x6(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.b = byte 
        return 8

    def inst0x7(self) -> int:
        self.registers.a = self.rlc(self.registers.a)
        self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        return 4
    
    def inst0x8(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.mmu.write_word(word, self.registers.sp)
        return 20

    def inst0x9(self) -> int:
        self.registers.set_hl(self.add_word(self.registers.get_hl(), self.registers.get_bc()))
        return 8
    
    def inst0xa(self) -> int:
        self.registers.a = self.mmu.read_byte(self.registers.get_bc())
        return 8

    def inst0xb(self) -> int:
        self.registers.set_bc((self.registers.get_bc() - 1) & 0xffff )
        return 8

    def inst0xc(self) -> int:
        self.registers.c = self.inc_byte(self.registers.c)
        return 4

    def inst0xd(self) -> int:
        self.registers.c = self.dec_byte(self.registers.c)
        return 4
    
    def inst0xe(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.c = byte 
        return 8

    def inst0xf(self) -> int:
        self.registers.a = self.rrc(self.registers.a)
        self.registers.reset_h_flag()
        self.registers.reset_n_flag()
        self.registers.reset_z_flag()
        return 4  

    def inst0x10(self) -> int:
        self.cpu.stop = True
        return 4       
    
    def inst0x11(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.set_de(word) 
        return 12
    
    def inst0x12(self) -> int:
        self.mmu.write_byte(self.registers.get_de(), self.registers.a)
        return 8

    def inst0x13(self) -> int:
        self.registers.set_de((self.registers.get_de() + 1) & 0xffff )
        return 8

    def inst0x14(self) -> int:
        self.registers.d = self.inc_byte(self.registers.d)
        return 4

    def inst0x15(self) -> int:
        self.registers.d = self.dec_byte(self.registers.d)
        return 4
    
    def inst0x16(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.d = byte 
        return 8

    def inst0x17(self) -> int:
        self.registers.a = self.rl(self.registers.a)
        self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        return 4

    def inst0x18(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.pc += signed_value(byte)
        return 12

    def inst0x19(self) -> int:
        self.registers.set_hl(self.add_word(self.registers.get_hl(), self.registers.get_de()))
        return 8
    
    def inst0x1a(self) -> int:
        self.registers.a = self.mmu.read_byte(self.registers.get_de())
        return 8

    def inst0x1b(self) -> int:
        self.registers.set_de((self.registers.get_de() - 1) & 0xffff )
        return 8

    def inst0x1c(self) -> int:
        self.registers.e = self.inc_byte(self.registers.e)
        return 4

    def inst0x1d(self) -> int:
        self.registers.e = self.dec_byte(self.registers.e)
        return 4
    
    def inst0x1e(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.e = byte 
        return 8

    def inst0x1f(self) -> int:
        self.registers.a = self.rr(self.registers.a)
        self.registers.reset_h_flag()
        self.registers.reset_n_flag()
        self.registers.reset_z_flag()
        return 4  

    def inst0x20(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        if not self.registers.is_z_flag():
            self.registers.pc += signed_value(byte)
            return 12
        return 8
    
    def inst0x21(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.set_hl(word) 
        return 12
    
    def inst0x22(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
        self.registers.set_hl(self.registers.get_hl()+1)
        return 8

    def inst0x23(self) -> int:
        self.registers.set_hl((self.registers.get_hl() + 1) & 0xffff )
        return 8

    def inst0x24(self) -> int:
        self.registers.h = self.inc_byte(self.registers.h)
        return 4

    def inst0x25(self) -> int:
        self.registers.h = self.dec_byte(self.registers.h)
        return 4
    
    def inst0x26(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.h = byte 
        return 8

    def inst0x27(self) -> int:
        temp = self.registers.a 
        if self.registers.is_n_flag():
            if self.registers.is_h_flag():
                temp = (temp - 0x06) & 0xff
            if self.registers.is_c_flag():
                temp = (temp - 0x60) & 0xff
        else:
            if self.registers.is_h_flag() or (temp & 0x0f) > 0x09:
                temp += 0x06
            if self.registers.is_c_flag() or temp > 0x9f:
                temp += 0x60
        self.registers.reset_h_flag()
        if temp > 0xff:
            self.registers.set_c_flag()
        temp &= 0xff
        if temp == 0:
            self.registers.set_z_flag()
        else:
            self.registers.reset_z_flag()
        self.registers.a = temp
        return 4

    def inst0x28(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        if self.registers.is_z_flag():
            self.registers.pc += signed_value(byte)
            return 12
        return 8

    def inst0x29(self) -> int:
        self.registers.set_hl(self.add_word(self.registers.get_hl(), self.registers.get_hl()))
        return 8
    
    def inst0x2a(self) -> int:
        self.registers.a = self.mmu.read_byte(self.registers.get_hl())
        self.registers.set_hl(self.registers.get_hl()+1)
        return 8

    def inst0x2b(self) -> int:
        self.registers.set_hl((self.registers.get_hl() - 1) & 0xffff )
        return 8

    def inst0x2c(self) -> int:
        self.registers.l = self.inc_byte(self.registers.l)
        return 4

    def inst0x2d(self) -> int:
        self.registers.l = self.dec_byte(self.registers.l)
        return 4
    
    def inst0x2e(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.l = byte 
        return 8

    def inst0x2f(self) -> int:
        self.registers.a = self.registers.a ^ 0xff
        self.registers.set_n_flag()
        self.registers.set_h_flag()
        return 4

    def inst0x30(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        if not self.registers.is_c_flag():
            self.registers.pc += signed_value(byte)
            return 12
        return 8
    
    def inst0x31(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.sp = word
        return 12
    
    def inst0x32(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
        self.registers.set_hl(self.registers.get_hl()-1)
        return 8

    def inst0x33(self) -> int:
        self.registers.sp = ((self.registers.sp + 1) & 0xffff )
        return 8

    def inst0x34(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.inc_byte(self.mmu.read_byte(self.registers.get_hl())))
        return 12

    def inst0x35(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.dec_byte(self.mmu.read_byte(self.registers.get_hl())))
        return 12
    
    def inst0x36(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.mmu.write_byte(self.registers.get_hl(),byte)
        return 12

    def inst0x37(self) -> int:
        self.registers.set_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        return 4

    def inst0x38(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        if self.registers.is_c_flag():
            self.registers.pc += signed_value(byte)
            return 12
        return 8

    def inst0x39(self) -> int:
        self.registers.set_hl(self.add_word(self.registers.get_hl(), self.registers.sp))
        return 8
    
    def inst0x3a(self) -> int:
        self.registers.a = self.mmu.read_byte(self.registers.get_hl())
        self.registers.set_hl(self.registers.get_hl()-1)
        return 8

    def inst0x3b(self) -> int:
        self.registers.sp = ((self.registers.sp - 1) & 0xffff )
        return 8

    def inst0x3c(self) -> int:
        self.registers.a = self.inc_byte(self.registers.a)
        return 4

    def inst0x3d(self) -> int:
        self.registers.a = self.dec_byte(self.registers.a)
        return 4
    
    def inst0x3e(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.a = byte
        return 8

    def inst0x3f(self) -> int:
        if self.registers.is_c_flag():
            self.registers.reset_c_flag()
        else:
            self.registers.set_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        return 4
    
    def inst0x40(self) -> int:
        return 4
    
    def inst0x41(self) -> int:
        self.registers.b = self.registers.c
        return 4
    
    def inst0x42(self) -> int:
        self.registers.b = self.registers.d
        return 4
    
    def inst0x43(self) -> int:
        self.registers.b = self.registers.e
        return 4
    
    def inst0x44(self) -> int:
        self.registers.b = self.registers.h
        return 4
    
    def inst0x45(self) -> int:
        self.registers.b = self.registers.l
        return 4
    
    def inst0x46(self) -> int:
        self.registers.b = self.mmu.read_byte(self.registers.get_hl())
        return 8
    
    def inst0x47(self) -> int:
        self.registers.b = self.registers.a
        return 4
    
    def inst0x48(self) -> int:
        self.registers.c = self.registers.b
        return 4
    
    def inst0x49(self) -> int:
        return 4
    
    def inst0x4a(self) -> int:
        self.registers.c = self.registers.d
        return 4
    
    def inst0x4b(self) -> int:
        self.registers.c = self.registers.e
        return 4
    
    def inst0x4c(self) -> int:
        self.registers.c = self.registers.h
        return 4
    
    def inst0x4d(self) -> int:
        self.registers.c = self.registers.l
        return 4
    
    def inst0x4e(self) -> int:
        self.registers.c = self.mmu.read_byte(self.registers.get_hl())
        return 8
    
    def inst0x4f(self) -> int:
        self.registers.c = self.registers.a
        return 4
    
    def inst0x50(self) -> int:
        self.registers.d = self.registers.b
        return 4
    
    def inst0x51(self) -> int:
        self.registers.d = self.registers.c
        return 4
    
    def inst0x52(self) -> int:
        return 4
    
    def inst0x53(self) -> int:
        self.registers.d = self.registers.e
        return 4
    
    def inst0x54(self) -> int:
        self.registers.d = self.registers.h
        return 4
    
    def inst0x55(self) -> int:
        self.registers.d = self.registers.l
        return 4
    
    def inst0x56(self) -> int:
        self.registers.d = self.mmu.read_byte(self.registers.get_hl())
        return 8
    
    def inst0x57(self) -> int:
        self.registers.d = self.registers.a
        return 4
    
    def inst0x58(self) -> int:
        self.registers.e = self.registers.b
        return 4
    
    def inst0x59(self) -> int:
        self.registers.e = self.registers.c
        return 4
    
    def inst0x5a(self) -> int:
        self.registers.e = self.registers.d
        return 4
    
    def inst0x5b(self) -> int:
        return 4
    
    def inst0x5c(self) -> int:
        self.registers.e = self.registers.h
        return 4
    
    def inst0x5d(self) -> int:
        self.registers.e = self.registers.l
        return 4
    
    def inst0x5e(self) -> int:
        self.registers.e = self.mmu.read_byte(self.registers.get_hl())
        return 8
    
    def inst0x5f(self) -> int:
        self.registers.e = self.registers.a
        return 4
    
    def inst0x60(self) -> int:
        self.registers.h = self.registers.b
        return 4
    
    def inst0x61(self) -> int:
        self.registers.h = self.registers.c
        return 4
    
    def inst0x62(self) -> int:
        self.registers.h = self.registers.d
        return 4
    
    def inst0x63(self) -> int:
        self.registers.h = self.registers.e
        return 4
    
    def inst0x64(self) -> int:
        return 4
    
    def inst0x65(self) -> int:
        self.registers.h = self.registers.l
        return 4
    
    def inst0x66(self) -> int:
        self.registers.h = self.mmu.read_byte(self.registers.get_hl())
        return 8
    
    def inst0x67(self) -> int:
        self.registers.h = self.registers.a
        return 4
    
    def inst0x68(self) -> int:
        self.registers.l = self.registers.b
        return 4
    
    def inst0x69(self) -> int:
        self.registers.l = self.registers.c
        return 4
    
    def inst0x6a(self) -> int:
        self.registers.l = self.registers.d
        return 4
    
    def inst0x6b(self) -> int:
        self.registers.l = self.registers.e
        return 4
    
    def inst0x6c(self) -> int:
        self.registers.l = self.registers.h
        return 4
    
    def inst0x6d(self) -> int:
        return 4
    
    def inst0x6e(self) -> int:
        self.registers.l = self.mmu.read_byte(self.registers.get_hl())
        return 8
    
    def inst0x6f(self) -> int:
        self.registers.l = self.registers.a
        return 4
    
    def inst0x70(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.registers.b)
        return 8
    
    def inst0x71(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.registers.c)
        return 8
    
    def inst0x72(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.registers.d)
        return 8
    
    def inst0x73(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.registers.e)
        return 8
    
    def inst0x74(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.registers.h)
        return 8
    
    def inst0x75(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(),self.registers.l)
        return 8

    def inst0x76(self) -> int:
        self.cpu.halted = True
        self.cpu.pending_interrupts_before_halt = self.mmu.read_byte(IO_Registers.IF)
        return 4
    
    def inst0x77(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
        return 8
    
    def inst0x78(self) -> int:
        self.registers.a = self.registers.b
        return 4
    
    def inst0x79(self) -> int:
        self.registers.a = self.registers.c
        return 4
    
    def inst0x7a(self) -> int:
        self.registers.a = self.registers.d
        return 4
    
    def inst0x7b(self) -> int:
        self.registers.a = self.registers.e
        return 4
    
    def inst0x7c(self) -> int:
        self.registers.a = self.registers.h
        return 4
    
    def inst0x7d(self) -> int:
        self.registers.a = self.registers.l
        return 4
    
    def inst0x7e(self) -> int:
        self.registers.a = self.mmu.read_byte(self.registers.get_hl())
        return 8
    
    def inst0x7f(self) -> int:
        return 4
    
    def inst0x80(self) -> int:
        self.add_byte(self.registers.b)
        return 4
    
    def inst0x81(self) -> int:
        self.add_byte(self.registers.c)
        return 4
    
    def inst0x82(self) -> int:
        self.add_byte(self.registers.d)
        return 4
    
    def inst0x83(self) -> int:
        self.add_byte(self.registers.e)
        return 4
    
    def inst0x84(self) -> int:
        self.add_byte(self.registers.h)
        return 4
    
    def inst0x85(self) -> int:
        self.add_byte(self.registers.l)
        return 4
    
    def inst0x86(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.add_byte(byte)
        return 8
    
    def inst0x87(self) -> int:
        self.add_byte(self.registers.a)
        return 4
    
    def inst0x88(self) -> int:
        self.adc(self.registers.b)
        return 4
    
    def inst0x89(self) -> int:
        self.adc(self.registers.c)
        return 4
    
    def inst0x8a(self) -> int:
        self.adc(self.registers.d)
        return 4
    
    def inst0x8b(self) -> int:
        self.adc(self.registers.e)
        return 4
    
    def inst0x8c(self) -> int:
        self.adc(self.registers.h)
        return 4
    
    def inst0x8d(self) -> int:
        self.adc(self.registers.l)
        return 4
    
    def inst0x8e(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.adc(byte)
        return 8
    
    def inst0x8f(self) -> int:
        self.adc(self.registers.a)
        return 4

    def inst0x90(self) -> int:
        self.sub(self.registers.b)
        return 4

    def inst0x91(self) -> int:
        self.sub(self.registers.c)
        return 4

    def inst0x92(self) -> int:
        self.sub(self.registers.d)
        return 4

    def inst0x93(self) -> int:
        self.sub(self.registers.e)
        return 4

    def inst0x94(self) -> int:
        self.sub(self.registers.h)
        return 4

    def inst0x95(self) -> int:
        self.sub(self.registers.l)
        return 4

    def inst0x96(self) -> int:
        self.sub(self.mmu.read_byte(self.registers.get_hl()))
        return 8

    def inst0x97(self) -> int:
        self.sub(self.registers.a)
        return 4

    def inst0x98(self) -> int:
        self.sbc(self.registers.b)
        return 4

    def inst0x99(self) -> int:
        self.sbc(self.registers.c)
        return 4

    def inst0x9a(self) -> int:
        self.sbc(self.registers.d)
        return 4

    def inst0x9b(self) -> int:
        self.sbc(self.registers.e)
        return 4

    def inst0x9c(self) -> int:
        self.sbc(self.registers.h)
        return 4

    def inst0x9d(self) -> int:
        self.sbc(self.registers.l)
        return 4

    def inst0x9e(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.sbc(byte)
        return 8

    def inst0x9f(self) -> int:
        self.sbc(self.registers.a)
        return 4

    def inst0xa0(self) -> int:
        self._and(self.registers.b)
        return 4

    def inst0xa1(self) -> int:
        self._and(self.registers.c)
        return 4

    def inst0xa2(self) -> int:
        self._and(self.registers.d)
        return 4

    def inst0xa3(self) -> int:
        self._and(self.registers.e)
        return 4

    def inst0xa4(self) -> int:
        self._and(self.registers.h)
        return 4

    def inst0xa5(self) -> int:
        self._and(self.registers.l)
        return 4

    def inst0xa6(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self._and(byte)
        return 8

    def inst0xa7(self) -> int:
        self._and(self.registers.a)
        return 4

    def inst0xa8(self) -> int:
        self.xor(self.registers.b)
        return 4

    def inst0xa9(self) -> int:
        self.xor(self.registers.c)
        return 4

    def inst0xaa(self) -> int:
        self.xor(self.registers.d)
        return 4

    def inst0xab(self) -> int:
        self.xor(self.registers.e)
        return 4

    def inst0xac(self) -> int:
        self.xor(self.registers.h)
        return 4

    def inst0xad(self) -> int:
        self.xor(self.registers.l)
        return 4

    def inst0xae(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.xor(byte)
        return 8

    def inst0xaf(self) -> int:
        self.xor(self.registers.a)
        return 4

    def inst0xb0(self) -> int:
        self._or(self.registers.b)
        return 4

    def inst0xb1(self) -> int:
        self._or(self.registers.c)
        return 4

    def inst0xb2(self) -> int:
        self._or(self.registers.d)
        return 4

    def inst0xb3(self) -> int:
        self._or(self.registers.e)
        return 4

    def inst0xb4(self) -> int:
        self._or(self.registers.h)
        return 4

    def inst0xb5(self) -> int:
        self._or(self.registers.l)
        return 4

    def inst0xb6(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self._or(byte)
        return 8

    def inst0xb7(self) -> int:
        self._or(self.registers.a)
        return 4

    def inst0xb8(self) -> int:
        self.cp(self.registers.b)
        return 4

    def inst0xb9(self) -> int:
        self.cp(self.registers.c)
        return 4

    def inst0xba(self) -> int:
        self.cp(self.registers.d)
        return 4

    def inst0xbb(self) -> int:
        self.cp(self.registers.e)
        return 4

    def inst0xbc(self) -> int:
        self.cp(self.registers.h)
        return 4

    def inst0xbd(self) -> int:
        self.cp(self.registers.l)
        return 4

    def inst0xbe(self) -> int:
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.cp(byte)
        return 8

    def inst0xbf(self) -> int:
        self.cp(self.registers.a)
        return 4

    def inst0xc0(self) -> int:
        if not self.registers.is_z_flag():
            self.registers.pc = self.stackManager.pop_word()
            return 20
        return 8
    
    def inst0xc1(self) -> int:
        self.registers.set_bc(self.stackManager.pop_word())
        return 12

    def inst0xc2(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        if not self.registers.is_z_flag():
            self.registers.pc = word
            return 16
        return 12

    def inst0xc3(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc = word
        return 16

    def inst0xc4(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        if not self.registers.is_z_flag():
            self.stackManager.push_word(self.registers.pc)
            self.registers.pc = word
            return 24
        return 12
    
    def inst0xc5(self) -> int:
        self.stackManager.push_word(self.registers.get_bc())
        return 16
    
    def inst0xc6(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.add_byte(byte)
        return 8

    def inst0xc7(self) -> int:
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x00
        return 16

    def inst0xc8(self) -> int:
        if self.registers.is_z_flag():
            self.registers.pc = self.stackManager.pop_word()
            return 20
        return 8

    def inst0xc9(self) -> int:
        self.registers.pc = self.stackManager.pop_word()
        return 16

    def inst0xca(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        if self.registers.is_z_flag():
            self.registers.pc = word
            return 16
        return 12

    def inst0xcc(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        if self.registers.is_z_flag():
            self.stackManager.push_word(self.registers.pc)
            self.registers.pc = word
            return 24
        return 12

    def inst0xcd(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = word
        return 24
    
    def inst0xce(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.adc(byte)
        return 8

    def inst0xcf(self) -> int:
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x08
        return 16

    def inst0xd0(self) -> int:
        if not self.registers.is_c_flag():
            self.registers.pc = self.stackManager.pop_word()
            return 20
        return 8
    
    def inst0xd1(self) -> int:
        self.registers.set_de(self.stackManager.pop_word())
        return 12

    def inst0xd2(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        if not self.registers.is_c_flag():
            self.registers.pc = word
            return 16
        return 12

    def inst0xd4(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        if not self.registers.is_c_flag():
            self.stackManager.push_word(self.registers.pc)
            self.registers.pc = word
            return 24
        return 12
    
    def inst0xd5(self) -> int:
        self.stackManager.push_word(self.registers.get_de())
        return 16

    def inst0xd6(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.sub(byte)
        return 8

    def inst0xd7(self) -> int:
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x10
        return 16

    def inst0xd8(self) -> int:
        if self.registers.is_c_flag():
            self.registers.pc = self.stackManager.pop_word()
            return 20
        return 8

    def inst0xd9(self) -> int:
        self.registers.pc = self.stackManager.pop_word()
        self.cpu.ime = True
        return 16

    def inst0xda(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        if self.registers.is_c_flag():
            self.registers.pc = word
            return 16
        return 12

    def inst0xdc(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        if self.registers.is_c_flag():
            self.stackManager.push_word(self.registers.pc)
            self.registers.pc = word
            return 24
        return 12

    def inst0xde(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.sbc(byte)
        return 8

    def inst0xdf(self) -> int:
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x18
        return 16

    def inst0xe0(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.mmu.write_byte((byte + 0xff00), self.registers.a)
        return 12
    
    def inst0xe1(self) -> int:
        self.registers.set_hl(self.stackManager.pop_word())
        return 12

    def inst0xe2(self) -> int:
        self.mmu.write_byte((self.registers.c + 0xff00), self.registers.a)
        return 8
    
    def inst0xe5(self) -> int:
        self.stackManager.push_word(self.registers.get_hl())
        return 16

    def inst0xe6(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self._and(byte)
        return 8

    def inst0xe7(self) -> int:
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x20
        return 16

    def inst0xe8(self) -> int:
        byte = signed_value(self.mmu.read_byte(self.registers.pc))
        temp = self.registers.sp + byte
        self.registers.pc += 1
        self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        if ( self.registers.sp ^ byte ^ temp ) & 0x100 == 0x100:
            self.registers.set_c_flag()
        else:
            self.registers.reset_c_flag()
        if ( self.registers.sp ^ byte ^ temp ) & 0x10 == 0x10:
            self.registers.set_h_flag()
        else:
            self.registers.reset_h_flag()
        self.registers.sp = temp
        return 16

    def inst0xe9(self) -> int:
        word = self.registers.get_hl()
        self.registers.pc = word
        return 4
    
    def inst0xea(self) -> int:
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.mmu.write_byte(word, self.registers.a)
        return 16

    def inst0xee(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.xor(byte)
        return 8

    def inst0xef(self) -> int:
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x28
        return 16
    
    def inst0xf0(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.a = self.mmu.read_byte((byte + 0xff00))
        return 12
    
    def inst0xf1(self) -> int:
        self.registers.set_af(self.stackManager.pop_word())
        return 12
    
    def inst0xf2(self) -> int:
        self.registers.a = self.mmu.read_byte(self.registers.c + 0xff00)
        return 8

    def inst0xf3(self) -> int:
        self.cpu.ime = False
        return 4
    
    def inst0xf5(self) -> int:
        self.stackManager.push_word(self.registers.get_af())
        return 16

    def inst0xf6(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self._or(byte)
        return 8

    def inst0xf7(self) -> int:
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x30
        return 16
    
    def inst0xf8(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        hl = self.registers.sp + signed_value(byte)
        self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        if (self.registers.sp ^ signed_value(byte) ^ hl) & 0x100 == 0x100:
            self.registers.set_c_flag()
        else: 
            self.registers.reset_c_flag()
        if (self.registers.sp ^ signed_value(byte) ^ hl) & 0x10 == 0x10:
            self.registers.set_h_flag()
        else: 
            self.registers.reset_h_flag()
        self.registers.set_hl(hl)
        return 12
    
    def inst0xf9(self) -> int:
        self.registers.sp = self.registers.get_hl()
        return 8
    
    def inst0xfa(self) -> int:
        byte = self.mmu.read_byte(self.mmu.read_word(self.registers.pc))
        self.registers.pc += 2
        self.registers.a = byte
        return 16

    def inst0xfb(self) -> int:
        self.cpu.ime = True
        return 4

    def inst0xfe(self) -> int:
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.cp(byte)
        return 8

    def inst0xff(self) -> int:
        self.stackManager.push_word(self.registers.pc)
        self.registers.pc = 0x38
        return 16

    def inst0xcb00(self) -> int:
        self.registers.b = self.rlc(self.registers.b)
        return 8

    def inst0xcb01(self) -> int:
        self.registers.c = self.rlc(self.registers.c)
        return 8

    def inst0xcb02(self) -> int:
        self.registers.d = self.rlc(self.registers.d)
        return 8

    def inst0xcb03(self) -> int:
        self.registers.e = self.rlc(self.registers.e)
        return 8

    def inst0xcb04(self) -> int:
        self.registers.h = self.rlc(self.registers.h)
        return 8

    def inst0xcb05(self) -> int:
        self.registers.l = self.rlc(self.registers.l)
        return 8

    def inst0xcb06(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.rlc(self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcb07(self) -> int:
        self.registers.a = self.rlc(self.registers.a)
        return 8

    def inst0xcb08(self) -> int:
        self.registers.b = self.rrc(self.registers.b)
        return 8

    def inst0xcb09(self) -> int:
        self.registers.c = self.rrc(self.registers.c)
        return 8

    def inst0xcb0a(self) -> int:
        self.registers.d = self.rrc(self.registers.d)
        return 8

    def inst0xcb0b(self) -> int:
        self.registers.e = self.rrc(self.registers.e)
        return 8

    def inst0xcb0c(self) -> int:
        self.registers.h = self.rrc(self.registers.h)
        return 8

    def inst0xcb0d(self) -> int:
        self.registers.l = self.rrc(self.registers.l)
        return 8

    def inst0xcb0e(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.rrc(self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcb0f(self) -> int:
        self.registers.a = self.rrc(self.registers.a)
        return 8

    def inst0xcb10(self) -> int:
        self.registers.b = self.rl(self.registers.b)
        return 8

    def inst0xcb11(self) -> int:
        self.registers.c = self.rl(self.registers.c)
        return 8

    def inst0xcb12(self) -> int:
        self.registers.d = self.rl(self.registers.d)
        return 8

    def inst0xcb13(self) -> int:
        self.registers.e = self.rl(self.registers.e)
        return 8

    def inst0xcb14(self) -> int:
        self.registers.h = self.rl(self.registers.h)
        return 8

    def inst0xcb15(self) -> int:
        self.registers.l = self.rl(self.registers.l)
        return 8

    def inst0xcb16(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.rl(self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcb17(self) -> int:
        self.registers.a = self.rl(self.registers.a)
        return 8

    def inst0xcb18(self) -> int:
        self.registers.b = self.rr(self.registers.b)
        return 8

    def inst0xcb19(self) -> int:
        self.registers.c = self.rr(self.registers.c)
        return 8

    def inst0xcb1a(self) -> int:
        self.registers.d = self.rr(self.registers.d)
        return 8

    def inst0xcb1b(self) -> int:
        self.registers.e = self.rr(self.registers.e)
        return 8

    def inst0xcb1c(self) -> int:
        self.registers.h = self.rr(self.registers.h)
        return 8

    def inst0xcb1d(self) -> int:
        self.registers.l = self.rr(self.registers.l)
        return 8

    def inst0xcb1e(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.rr(self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcb1f(self) -> int:
        self.registers.a = self.rr(self.registers.a)
        return 8

    def inst0xcb20(self) -> int:
        self.registers.b = self.sla(self.registers.b)
        return 8

    def inst0xcb21(self) -> int:
        self.registers.c = self.sla(self.registers.c)
        return 8

    def inst0xcb22(self) -> int:
        self.registers.d = self.sla(self.registers.d)
        return 8

    def inst0xcb23(self) -> int:
        self.registers.e = self.sla(self.registers.e)
        return 8

    def inst0xcb24(self) -> int:
        self.registers.h = self.sla(self.registers.h)
        return 8

    def inst0xcb25(self) -> int:
        self.registers.l = self.sla(self.registers.l)
        return 8

    def inst0xcb26(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.sla(self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcb27(self) -> int:
        self.registers.a = self.sla(self.registers.a)
        return 8

    def inst0xcb28(self) -> int:
        self.registers.b = self.sra(self.registers.b)
        return 8

    def inst0xcb29(self) -> int:
        self.registers.c = self.sra(self.registers.c)
        return 8

    def inst0xcb2a(self) -> int:
        self.registers.d = self.sra(self.registers.d)
        return 8

    def inst0xcb2b(self) -> int:
        self.registers.e = self.sra(self.registers.e)
        return 8

    def inst0xcb2c(self) -> int:
        self.registers.h = self.sra(self.registers.h)
        return 8

    def inst0xcb2d(self) -> int:
        self.registers.l = self.sra(self.registers.l)
        return 8

    def inst0xcb2e(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.sra(self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcb2f(self) -> int:
        self.registers.a = self.sra(self.registers.a)
        return 8

    def inst0xcb30(self) -> int:
        self.registers.b = self.swap(self.registers.b)
        return 8

    def inst0xcb31(self) -> int:
        self.registers.c = self.swap(self.registers.c)
        return 8

    def inst0xcb32(self) -> int:
        self.registers.d = self.swap(self.registers.d)
        return 8

    def inst0xcb33(self) -> int:
        self.registers.e = self.swap(self.registers.e)
        return 8

    def inst0xcb34(self) -> int:
        self.registers.h = self.swap(self.registers.h)
        return 8

    def inst0xcb35(self) -> int:
        self.registers.l = self.swap(self.registers.l)
        return 8

    def inst0xcb36(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.swap(self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcb37(self) -> int:
        self.registers.a = self.swap(self.registers.a)
        return 8

    def inst0xcb38(self) -> int:
        self.registers.b = self.srl(self.registers.b)
        return 8

    def inst0xcb39(self) -> int:
        self.registers.c = self.srl(self.registers.c)
        return 8

    def inst0xcb3a(self) -> int:
        self.registers.d = self.srl(self.registers.d)
        return 8

    def inst0xcb3b(self) -> int:
        self.registers.e = self.srl(self.registers.e)
        return 8

    def inst0xcb3c(self) -> int:
        self.registers.h = self.srl(self.registers.h)
        return 8

    def inst0xcb3d(self) -> int:
        self.registers.l = self.srl(self.registers.l)
        return 8

    def inst0xcb3e(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.srl(self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcb3f(self) -> int:
        self.registers.a = self.srl(self.registers.a)
        return 8

    def inst0xcb40(self) -> int:
        self.bit(0, self.registers.b)
        return 8

    def inst0xcb41(self) -> int:
        self.bit(0, self.registers.c)
        return 8

    def inst0xcb42(self) -> int:
        self.bit(0, self.registers.d)
        return 8

    def inst0xcb43(self) -> int:
        self.bit(0, self.registers.e)
        return 8

    def inst0xcb44(self) -> int:
        self.bit(0, self.registers.h)
        return 8

    def inst0xcb45(self) -> int:
        self.bit(0, self.registers.l)
        return 8

    def inst0xcb46(self) -> int:
        self.bit(0, self.mmu.read_byte(self.registers.get_hl()))
        return 12

    def inst0xcb47(self) -> int:
        self.bit(0, self.registers.a)
        return 8

    def inst0xcb48(self) -> int:
        self.bit(1, self.registers.b)
        return 8

    def inst0xcb49(self) -> int:
        self.bit(1, self.registers.c)
        return 8

    def inst0xcb4a(self) -> int:
        self.bit(1, self.registers.d)
        return 8

    def inst0xcb4b(self) -> int:
        self.bit(1, self.registers.e)
        return 8

    def inst0xcb4c(self) -> int:
        self.bit(1, self.registers.h)
        return 8

    def inst0xcb4d(self) -> int:
        self.bit(1, self.registers.l)
        return 8

    def inst0xcb4e(self) -> int:
        self.bit(1, self.mmu.read_byte(self.registers.get_hl()))
        return 12

    def inst0xcb4f(self) -> int:
        self.bit(1, self.registers.a)
        return 8

    def inst0xcb50(self) -> int:
        self.bit(2, self.registers.b)
        return 8

    def inst0xcb51(self) -> int:
        self.bit(2, self.registers.c)
        return 8

    def inst0xcb52(self) -> int:
        self.bit(2, self.registers.d)
        return 8

    def inst0xcb53(self) -> int:
        self.bit(2, self.registers.e)
        return 8

    def inst0xcb54(self) -> int:
        self.bit(2, self.registers.h)
        return 8

    def inst0xcb55(self) -> int:
        self.bit(2, self.registers.l)
        return 8

    def inst0xcb56(self) -> int:
        self.bit(2, self.mmu.read_byte(self.registers.get_hl()))
        return 12

    def inst0xcb57(self) -> int:
        self.bit(2, self.registers.a)
        return 8

    def inst0xcb58(self) -> int:
        self.bit(3, self.registers.b)
        return 8

    def inst0xcb59(self) -> int:
        self.bit(3, self.registers.c)
        return 8

    def inst0xcb5a(self) -> int:
        self.bit(3, self.registers.d)
        return 8

    def inst0xcb5b(self) -> int:
        self.bit(3, self.registers.e)
        return 8

    def inst0xcb5c(self) -> int:
        self.bit(3, self.registers.h)
        return 8

    def inst0xcb5d(self) -> int:
        self.bit(3, self.registers.l)
        return 8

    def inst0xcb5e(self) -> int:
        self.bit(3, self.mmu.read_byte(self.registers.get_hl()))
        return 12

    def inst0xcb5f(self) -> int:
        self.bit(3, self.registers.a)
        return 8

    def inst0xcb60(self) -> int:
        self.bit(4, self.registers.b)
        return 8

    def inst0xcb61(self) -> int:
        self.bit(4, self.registers.c)
        return 8

    def inst0xcb62(self) -> int:
        self.bit(4, self.registers.d)
        return 8

    def inst0xcb63(self) -> int:
        self.bit(4, self.registers.e)
        return 8

    def inst0xcb64(self) -> int:
        self.bit(4, self.registers.h)
        return 8

    def inst0xcb65(self) -> int:
        self.bit(4, self.registers.l)
        return 8

    def inst0xcb66(self) -> int:
        self.bit(4, self.mmu.read_byte(self.registers.get_hl()))
        return 12

    def inst0xcb67(self) -> int:
        self.bit(4, self.registers.a)
        return 8

    def inst0xcb68(self) -> int:
        self.bit(5, self.registers.b)
        return 8

    def inst0xcb69(self) -> int:
        self.bit(5, self.registers.c)
        return 8

    def inst0xcb6a(self) -> int:
        self.bit(5, self.registers.d)
        return 8

    def inst0xcb6b(self) -> int:
        self.bit(5, self.registers.e)
        return 8

    def inst0xcb6c(self) -> int:
        self.bit(5, self.registers.h)
        return 8

    def inst0xcb6d(self) -> int:
        self.bit(5, self.registers.l)
        return 8

    def inst0xcb6e(self) -> int:
        self.bit(5, self.mmu.read_byte(self.registers.get_hl()))
        return 12

    def inst0xcb6f(self) -> int:
        self.bit(5, self.registers.a)
        return 8

    def inst0xcb70(self) -> int:
        self.bit(6, self.registers.b)
        return 8

    def inst0xcb71(self) -> int:
        self.bit(6, self.registers.c)
        return 8

    def inst0xcb72(self) -> int:
        self.bit(6, self.registers.d)
        return 8

    def inst0xcb73(self) -> int:
        self.bit(6, self.registers.e)
        return 8

    def inst0xcb74(self) -> int:
        self.bit(6, self.registers.h)
        return 8

    def inst0xcb75(self) -> int:
        self.bit(6, self.registers.l)
        return 8

    def inst0xcb76(self) -> int:
        self.bit(6, self.mmu.read_byte(self.registers.get_hl()))
        return 12

    def inst0xcb77(self) -> int:
        self.bit(6, self.registers.a)
        return 8

    def inst0xcb78(self) -> int:
        self.bit(7, self.registers.b)
        return 8

    def inst0xcb79(self) -> int:
        self.bit(7, self.registers.c)
        return 8

    def inst0xcb7a(self) -> int:
        self.bit(7, self.registers.d)
        return 8

    def inst0xcb7b(self) -> int:
        self.bit(7, self.registers.e)
        return 8

    def inst0xcb7c(self) -> int:
        self.bit(7, self.registers.h)
        return 8

    def inst0xcb7d(self) -> int:
        self.bit(7, self.registers.l)
        return 8

    def inst0xcb7e(self) -> int:
        self.bit(7, self.mmu.read_byte(self.registers.get_hl()))
        return 12

    def inst0xcb7f(self) -> int:
        self.bit(7, self.registers.a)
        return 8

    def inst0xcb80(self) -> int:
        self.registers.b = self.res(0, self.registers.b)
        return 8

    def inst0xcb81(self) -> int:
        self.registers.c = self.res(0, self.registers.c)
        return 8

    def inst0xcb82(self) -> int:
        self.registers.d = self.res(0, self.registers.d)
        return 8

    def inst0xcb83(self) -> int:
        self.registers.e = self.res(0, self.registers.e)
        return 8

    def inst0xcb84(self) -> int:
        self.registers.h = self.res(0, self.registers.h)
        return 8

    def inst0xcb85(self) -> int:
        self.registers.l = self.res(0, self.registers.l)
        return 8

    def inst0xcb86(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(0, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcb87(self) -> int:
        self.registers.a = self.res(0, self.registers.a)
        return 8

    def inst0xcb88(self) -> int:
        self.registers.b = self.res(1, self.registers.b)
        return 8

    def inst0xcb89(self) -> int:
        self.registers.c = self.res(1, self.registers.c)
        return 8

    def inst0xcb8a(self) -> int:
        self.registers.d = self.res(1, self.registers.d)
        return 8

    def inst0xcb8b(self) -> int:
        self.registers.e = self.res(1, self.registers.e)
        return 8

    def inst0xcb8c(self) -> int:
        self.registers.h = self.res(1, self.registers.h)
        return 8

    def inst0xcb8d(self) -> int:
        self.registers.l = self.res(1, self.registers.l)
        return 8

    def inst0xcb8e(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(1, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcb8f(self) -> int:
        self.registers.a = self.res(1, self.registers.a)
        return 8

    def inst0xcb90(self) -> int:
        self.registers.b = self.res(2, self.registers.b)
        return 8

    def inst0xcb91(self) -> int:
        self.registers.c = self.res(2, self.registers.c)
        return 8

    def inst0xcb92(self) -> int:
        self.registers.d = self.res(2, self.registers.d)
        return 8

    def inst0xcb93(self) -> int:
        self.registers.e = self.res(2, self.registers.e)
        return 8

    def inst0xcb94(self) -> int:
        self.registers.h = self.res(2, self.registers.h)
        return 8

    def inst0xcb95(self) -> int:
        self.registers.l = self.res(2, self.registers.l)
        return 8

    def inst0xcb96(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(2, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcb97(self) -> int:
        self.registers.a = self.res(2, self.registers.a)
        return 8

    def inst0xcb98(self) -> int:
        self.registers.b = self.res(3, self.registers.b)
        return 8

    def inst0xcb99(self) -> int:
        self.registers.c = self.res(3, self.registers.c)
        return 8

    def inst0xcb9a(self) -> int:
        self.registers.d = self.res(3, self.registers.d)
        return 8

    def inst0xcb9b(self) -> int:
        self.registers.e = self.res(3, self.registers.e)
        return 8

    def inst0xcb9c(self) -> int:
        self.registers.h = self.res(3, self.registers.h)
        return 8

    def inst0xcb9d(self) -> int:
        self.registers.l = self.res(3, self.registers.l)
        return 8

    def inst0xcb9e(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(3, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcb9f(self) -> int:
        self.registers.a = self.res(3, self.registers.a)
        return 8

    def inst0xcba0(self) -> int:
        self.registers.b = self.res(4, self.registers.b)
        return 8

    def inst0xcba1(self) -> int:
        self.registers.c = self.res(4, self.registers.c)
        return 8

    def inst0xcba2(self) -> int:
        self.registers.d = self.res(4, self.registers.d)
        return 8

    def inst0xcba3(self) -> int:
        self.registers.e = self.res(4, self.registers.e)
        return 8

    def inst0xcba4(self) -> int:
        self.registers.h = self.res(4, self.registers.h)
        return 8

    def inst0xcba5(self) -> int:
        self.registers.l = self.res(4, self.registers.l)
        return 8

    def inst0xcba6(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(4, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcba7(self) -> int:
        self.registers.a = self.res(4, self.registers.a)
        return 8

    def inst0xcba8(self) -> int:
        self.registers.b = self.res(5, self.registers.b)
        return 8

    def inst0xcba9(self) -> int:
        self.registers.c = self.res(5, self.registers.c)
        return 8

    def inst0xcbaa(self) -> int:
        self.registers.d = self.res(5, self.registers.d)
        return 8

    def inst0xcbab(self) -> int:
        self.registers.e = self.res(5, self.registers.e)
        return 8

    def inst0xcbac(self) -> int:
        self.registers.h = self.res(5, self.registers.h)
        return 8

    def inst0xcbad(self) -> int:
        self.registers.l = self.res(5, self.registers.l)
        return 8

    def inst0xcbae(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(5, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcbaf(self) -> int:
        self.registers.a = self.res(5, self.registers.a)
        return 8

    def inst0xcbb0(self) -> int:
        self.registers.b = self.res(6, self.registers.b)
        return 8

    def inst0xcbb1(self) -> int:
        self.registers.c = self.res(6, self.registers.c)
        return 8

    def inst0xcbb2(self) -> int:
        self.registers.d = self.res(6, self.registers.d)
        return 8

    def inst0xcbb3(self) -> int:
        self.registers.e = self.res(6, self.registers.e)
        return 8

    def inst0xcbb4(self) -> int:
        self.registers.h = self.res(6, self.registers.h)
        return 8

    def inst0xcbb5(self) -> int:
        self.registers.l = self.res(6, self.registers.l)
        return 8

    def inst0xcbb6(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(6, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcbb7(self) -> int:
        self.registers.a = self.res(6, self.registers.a)
        return 8

    def inst0xcbb8(self) -> int:
        self.registers.b = self.res(7, self.registers.b)
        return 8

    def inst0xcbb9(self) -> int:
        self.registers.c = self.res(7, self.registers.c)
        return 8

    def inst0xcbba(self) -> int:
        self.registers.d = self.res(7, self.registers.d)
        return 8

    def inst0xcbbb(self) -> int:
        self.registers.e = self.res(7, self.registers.e)
        return 8

    def inst0xcbbc(self) -> int:
        self.registers.h = self.res(7, self.registers.h)
        return 8

    def inst0xcbbd(self) -> int:
        self.registers.l = self.res(7, self.registers.l)
        return 8

    def inst0xcbbe(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), self.res(7, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcbbf(self) -> int:
        self.registers.a = self.res(7, self.registers.a)
        return 8

    def inst0xcbc0(self) -> int:
        self.registers.b = set_bit(0, self.registers.b)
        return 8

    def inst0xcbc1(self) -> int:
        self.registers.c = set_bit(0, self.registers.c)
        return 8

    def inst0xcbc2(self) -> int:
        self.registers.d = set_bit(0, self.registers.d)
        return 8

    def inst0xcbc3(self) -> int:
        self.registers.e = set_bit(0, self.registers.e)
        return 8

    def inst0xcbc4(self) -> int:
        self.registers.h = set_bit(0, self.registers.h)
        return 8

    def inst0xcbc5(self) -> int:
        self.registers.l = set_bit(0, self.registers.l)
        return 8

    def inst0xcbc6(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(0, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcbc7(self) -> int:
        self.registers.a = set_bit(0, self.registers.a)
        return 8

    def inst0xcbc8(self) -> int:
        self.registers.b = set_bit(1, self.registers.b)
        return 8

    def inst0xcbc9(self) -> int:
        self.registers.c = set_bit(1, self.registers.c)
        return 8

    def inst0xcbca(self) -> int:
        self.registers.d = set_bit(1, self.registers.d)
        return 8

    def inst0xcbcb(self) -> int:
        self.registers.e = set_bit(1, self.registers.e)
        return 8

    def inst0xcbcc(self) -> int:
        self.registers.h = set_bit(1, self.registers.h)
        return 8

    def inst0xcbcd(self) -> int:
        self.registers.l = set_bit(1, self.registers.l)
        return 8

    def inst0xcbce(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(1, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcbcf(self) -> int:
        self.registers.a = set_bit(1, self.registers.a)
        return 8

    def inst0xcbd0(self) -> int:
        self.registers.b = set_bit(2, self.registers.b)
        return 8

    def inst0xcbd1(self) -> int:
        self.registers.c = set_bit(2, self.registers.c)
        return 8

    def inst0xcbd2(self) -> int:
        self.registers.d = set_bit(2, self.registers.d)
        return 8

    def inst0xcbd3(self) -> int:
        self.registers.e = set_bit(2, self.registers.e)
        return 8

    def inst0xcbd4(self) -> int:
        self.registers.h = set_bit(2, self.registers.h)
        return 8

    def inst0xcbd5(self) -> int:
        self.registers.l = set_bit(2, self.registers.l)
        return 8

    def inst0xcbd6(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(2, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcbd7(self) -> int:
        self.registers.a = set_bit(2, self.registers.a)
        return 8

    def inst0xcbd8(self) -> int:
        self.registers.b = set_bit(3, self.registers.b)
        return 8

    def inst0xcbd9(self) -> int:
        self.registers.c = set_bit(3, self.registers.c)
        return 8

    def inst0xcbda(self) -> int:
        self.registers.d = set_bit(3, self.registers.d)
        return 8

    def inst0xcbdb(self) -> int:
        self.registers.e = set_bit(3, self.registers.e)
        return 8

    def inst0xcbdc(self) -> int:
        self.registers.h = set_bit(3, self.registers.h)
        return 8

    def inst0xcbdd(self) -> int:
        self.registers.l = set_bit(3, self.registers.l)
        return 8

    def inst0xcbde(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(3, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcbdf(self) -> int:
        self.registers.a = set_bit(3, self.registers.a)
        return 8

    def inst0xcbe0(self) -> int:
        self.registers.b = set_bit(4, self.registers.b)
        return 8

    def inst0xcbe1(self) -> int:
        self.registers.c = set_bit(4, self.registers.c)
        return 8

    def inst0xcbe2(self) -> int:
        self.registers.d = set_bit(4, self.registers.d)
        return 8

    def inst0xcbe3(self) -> int:
        self.registers.e = set_bit(4, self.registers.e)
        return 8

    def inst0xcbe4(self) -> int:
        self.registers.h = set_bit(4, self.registers.h)
        return 8

    def inst0xcbe5(self) -> int:
        self.registers.l = set_bit(4, self.registers.l)
        return 8

    def inst0xcbe6(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(4, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcbe7(self) -> int:
        self.registers.a = set_bit(4, self.registers.a)
        return 8

    def inst0xcbe8(self) -> int:
        self.registers.b = set_bit(5, self.registers.b)
        return 8

    def inst0xcbe9(self) -> int:
        self.registers.c = set_bit(5, self.registers.c)
        return 8

    def inst0xcbea(self) -> int:
        self.registers.d = set_bit(5, self.registers.d)
        return 8

    def inst0xcbeb(self) -> int:
        self.registers.e = set_bit(5, self.registers.e)
        return 8

    def inst0xcbec(self) -> int:
        self.registers.h = set_bit(5, self.registers.h)
        return 8

    def inst0xcbed(self) -> int:
        self.registers.l = set_bit(5, self.registers.l)
        return 8

    def inst0xcbee(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(5, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcbef(self) -> int:
        self.registers.a = set_bit(5, self.registers.a)
        return 8

    def inst0xcbf0(self) -> int:
        self.registers.b = set_bit(6, self.registers.b)
        return 8

    def inst0xcbf1(self) -> int:
        self.registers.c = set_bit(6, self.registers.c)
        return 8

    def inst0xcbf2(self) -> int:
        self.registers.d = set_bit(6, self.registers.d)
        return 8

    def inst0xcbf3(self) -> int:
        self.registers.e = set_bit(6, self.registers.e)
        return 8

    def inst0xcbf4(self) -> int:
        self.registers.h = set_bit(6, self.registers.h)
        return 8

    def inst0xcbf5(self) -> int:
        self.registers.l = set_bit(6, self.registers.l)
        return 8

    def inst0xcbf6(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(6, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcbf7(self) -> int:
        self.registers.a = set_bit(6, self.registers.a)
        return 8

    def inst0xcbf8(self) -> int:
        self.registers.b = set_bit(7, self.registers.b)
        return 8

    def inst0xcbf9(self) -> int:
        self.registers.c = set_bit(7, self.registers.c)
        return 8

    def inst0xcbfa(self) -> int:
        self.registers.d = set_bit(7, self.registers.d)
        return 8

    def inst0xcbfb(self) -> int:
        self.registers.e = set_bit(7, self.registers.e)
        return 8

    def inst0xcbfc(self) -> int:
        self.registers.h = set_bit(7, self.registers.h)
        return 8

    def inst0xcbfd(self) -> int:
        self.registers.l = set_bit(7, self.registers.l)
        return 8

    def inst0xcbfe(self) -> int:
        self.mmu.write_byte(self.registers.get_hl(), set_bit(7, self.mmu.read_byte(self.registers.get_hl())))
        return 16

    def inst0xcbff(self) -> int:
        self.registers.a = set_bit(7, self.registers.a)
        return 8
    
    def add_byte(self, value : int) -> int:
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

    def add_word(self, value1 : int, value2 : int) -> int:
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

    def adc(self, value : int) -> int:
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
        
    def sub(self, value : int) -> int:
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

    def sbc(self, value : int) -> int:
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

    def _and(self, value: int) -> int:
        result = self.registers.a & value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.set_h_flag()
        self.registers.a = result & 0xff

    def _or(self, value : int) -> int:
        result = self.registers.a | value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.registers.a = result & 0xff

    def xor(self, value: int) -> int:
        result = self.registers.a ^ value
        if result & 0xff == 0x0:
            self.registers.set_z_flag()
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.registers.a = result & 0xff

    def cp(self, value: int):
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

    def bit(self, pos : int, value : int) -> int:
        bit = 1 if value & bit_mask[pos] == bit_mask[pos] else 0
        if bit & 0xff == 0x0:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.set_h_flag()

    def res(self, pos : int, value : int) -> int:
        return value & (bit_mask[pos] ^ 0xff)

    def swap(self, value : int) -> int:
        value = ((value << 4) & 0xff) | (value >> 4)
        if value & 0xff == 0x00:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.registers.reset_c_flag()
        return value


    def inc_byte(self, value : int) -> int:
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

    def dec_byte(self, value : int) -> int:
        result = value - 1
        if result & 0xff == 0x0:
            self.registers.set_z_flag() 
        else: 
            self.registers.reset_z_flag()
        if result & 0xf == 0xf:
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()
        self.registers.set_n_flag()
        return result & 0xff

    def rl(self, value : int) -> int:
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

    def rlc(self, value : int) -> int:
        bit_out = 0x1 if value & 0x80 == 0x80 else 0x0
        if bit_out == 0x1:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        if ((value << 1) & 0xff) + bit_out == 0x00:
            self.registers.set_z_flag()
        else:
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        return ((value << 1) & 0xff) + bit_out

    def rr(self, value : int) -> int:
        carry = 0x80 if self.registers.is_c_flag() else 0x0
        if value & 0x1 == 0x1:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        if (value >> 1) + carry == 0:
            self.registers.set_z_flag()
        else:
            self.registers.reset_z_flag()
        return (value >> 1) + carry

    def rrc(self, value : int) -> int:
        bit_out = 0x80 if value & 0x1 == 0x1 else 0x0
        if bit_out == 0x80:
            self.registers.set_c_flag() 
        else: 
            self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        if (value >> 1) + bit_out == 0:
            self.registers.set_z_flag()
        else:
            self.registers.reset_z_flag()
        return (value >> 1) + bit_out

    def srl(self, value: int) -> int:
        if value & 0x01 == 0x01:
            self.registers.set_c_flag()
        else:
            self.registers.reset_c_flag()
        temp = value >> 1
        if temp == 0:
            self.registers.set_z_flag()
        else:
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        return temp & 0xff

    def sra(self, value: int) -> int:
        if value & 0x01 == 0x01:
            self.registers.set_c_flag()
        else:
            self.registers.reset_c_flag()
        temp = ( value >> 1 ) | ( value & 0x80 )
        if temp == 0:
            self.registers.set_z_flag()
        else:
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        return temp & 0xff

    def sla(self, value: int) -> int:
        if value & 0x80 == 0x80:
            self.registers.set_c_flag()
        else:
            self.registers.reset_c_flag()
        temp = value << 1
        if temp & 0xff == 0:
            self.registers.set_z_flag()
        else:
            self.registers.reset_z_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        return temp & 0xff
