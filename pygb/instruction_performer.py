#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygb.byte_operations import signed_value

class InstructionPerformer:

    def __init__(self, cpu):
        self.cpu = cpu
        self.mmu = cpu.mmu
        self.registers = cpu.registers


    def perform_instruction(self, opcode):
        try:
            instruction = getattr(self, 'instruction_' + hex(opcode))
            return instruction()
        except:
            return self.unimplemented(opcode)

    
    def instruction_0x00(self):
        print('{}: NOP'.format(hex(self.registers.pc -1)))
        return 4
    
    def instruction_0x01(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.set_bc(word) 
        print('{}: LD BC, {}'.format(hex(self.registers.pc-3), hex(word)))
        return 12
    
    def instruction_0x02(self):
        self.mmu.write_byte(self.registers.get_bc, self.registers.a)
        print('{}: LD (BC), A'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x06(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.b = byte 
        print('{}: LD B, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8
    
    def instruction_0x08(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.mmu.write_word(word, self.registers.sp)
        print('{}: LD ({}), SP'.format(hex(self.registers.pc-2), hex(word)))
        return 20
    
    def instruction_0x0a(self):
        self.registers.a = self.mmu.read_byte(self.registers.get_bc())
        print('{}: LD A, (BC)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x0e(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.c = byte 
        print('{}: LD C, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8
    
    def instruction_0x11(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.set_de(word) 
        print('{}: LD DE, {}'.format(hex(self.registers.pc-3), hex(word)))
        return 12
    
    def instruction_0x12(self):
        self.mmu.write_byte(self.registers.get_de, self.registers.a)
        print('{}: LD (DE), A'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x16(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.d = byte 
        print('{}: LD D, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8
    
    def instruction_0x1a(self):
        self.registers.a = self.mmu.read_byte(self.registers.get_de())
        print('{}: LD A, (DE)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x1e(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.e = byte 
        print('{}: LD E, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8
    
    def instruction_0x21(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.set_hl(word) 
        print('{}: LD HL, {}'.format(hex(self.registers.pc-3), hex(word)))
        return 12
    
    def instruction_0x22(self):
        self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
        self.registers.set_hl(self.registers.get_hl()+1)
        print('{}: LD (HL+), A'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x26(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.h = byte 
        print('{}: LD H, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8
    
    def instruction_0x2a(self):
        self.registers.a = self.mmu.read_byte(self.registers.get_hl())
        self.registers.set_hl(self.registers.get_hl()+1)
        print('{}: LD A, (HL+)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x2e(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.l = byte 
        print('{}: LD L, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8
    
    def instruction_0x31(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.sp = word
        print('{}: LD SP, {}'.format(hex(self.registers.pc-3), hex(word)))
        return 12
    
    def instruction_0x32(self):
        self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
        self.registers.set_hl(self.registers.get_hl()-1)
        print('{}: LD (HL-), A'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x36(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.mmu.write_byte(self.registers.get_hl(),byte)
        print('{}: LD (HL), {}'.format(hex(self.registers.pc-2),hex(byte)))
        return 12
    
    def instruction_0x3a(self):
        self.registers.a = self.mmu.read_byte(self.registers.get_hl())
        self.registers.set_hl(self.registers.get_hl()-1)
        print('{}: LD A, (HL-)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x3e(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.a = byte
        print('{}: LD A, {}'.format(hex(self.registers.pc-2),hex(byte)))
        return 8
    
    def instruction_0x40(self):
        print('{}: LD B, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x41(self):
        self.registers.b = self.registers.c
        print('{}: LD B, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x42(self):
        self.registers.b = self.registers.d
        print('{}: LD B, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x43(self):
        self.registers.b = self.registers.e
        print('{}: LD B, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x44(self):
        self.registers.b = self.registers.h
        print('{}: LD B, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x45(self):
        self.registers.b = self.registers.l
        print('{}: LD B, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x46(self):
        self.registers.b = self.mmu.read_byte(self.registers.get_hl())
        print('{}: LD B, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x47(self):
        self.registers.b = self.registers.a
        print('{}: LD B, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x48(self):
        self.registers.c = self.registers.b
        print('{}: LD C, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x49(self):
        print('{}: LD C, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x4a(self):
        self.registers.c = self.registers.d
        print('{}: LD C, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x4b(self):
        self.registers.c = self.registers.e
        print('{}: LD C, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x4c(self):
        self.registers.c = self.registers.h
        print('{}: LD C, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x4d(self):
        self.registers.c = self.registers.l
        print('{}: LD C, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x4e(self):
        self.registers.c = self.mmu.read_byte(self.registers.get_hl())
        print('{}: LD C, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x4f(self):
        self.registers.c = self.registers.a
        print('{}: LD C, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x50(self):
        self.registers.d = self.registers.b
        print('{}: LD D, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x51(self):
        self.registers.d = self.registers.c
        print('{}: LD D, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x52(self):
        print('{}: LD D, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x53(self):
        self.registers.d = self.registers.e
        print('{}: LD D, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x54(self):
        self.registers.d = self.registers.h
        print('{}: LD D, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x55(self):
        self.registers.d = self.registers.l
        print('{}: LD D, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x56(self):
        self.registers.d = self.mmu.read_byte(self.registers.get_hl())
        print('{}: LD D, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x57(self):
        self.registers.d = self.registers.a
        print('{}: LD D, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x58(self):
        self.registers.e = self.registers.b
        print('{}: LD E, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x59(self):
        self.registers.e = self.registers.c
        print('{}: LD E, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x5a(self):
        self.registers.e = self.registers.d
        print('{}: LD E, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x5b(self):
        print('{}: LD E, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x5c(self):
        self.registers.e = self.registers.h
        print('{}: LD E, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x5d(self):
        self.registers.e = self.registers.l
        print('{}: LD E, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x5e(self):
        self.registers.e = self.mmu.read_byte(self.registers.get_hl())
        print('{}: LD E, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x5f(self):
        self.registers.e = self.registers.a
        print('{}: LD E, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x60(self):
        self.registers.h = self.registers.b
        print('{}: LD H, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x61(self):
        self.registers.h = self.registers.c
        print('{}: LD H, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x62(self):
        self.registers.h = self.registers.d
        print('{}: LD H, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x63(self):
        self.registers.h = self.registers.e
        print('{}: LD H, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x64(self):
        print('{}: LD H, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x65(self):
        self.registers.h = self.registers.l
        print('{}: LD H, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x66(self):
        self.registers.h = self.mmu.read_byte(self.registers.get_hl())
        print('{}: LD H, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x67(self):
        self.registers.h = self.registers.a
        print('{}: LD H, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x68(self):
        self.registers.l = self.registers.b
        print('{}: LD L, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x69(self):
        self.registers.l = self.registers.c
        print('{}: LD L, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x6a(self):
        self.registers.l = self.registers.d
        print('{}: LD L, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x6b(self):
        self.registers.l = self.registers.e
        print('{}: LD L, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x6c(self):
        self.registers.l = self.registers.h
        print('{}: LD L, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x6d(self):
        print('{}: LD L, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x6e(self):
        self.registers.l = self.mmu.read_byte(self.registers.get_hl())
        print('{}: LD L, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x6f(self):
        self.registers.l = self.registers.a
        print('{}: LD L, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x70(self):
        self.mmu.write_byte(self.registers.get_hl(),self.registers.b)
        print('{}: LD (HL), B'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x71(self):
        self.mmu.write_byte(self.registers.get_hl(),self.registers.c)
        print('{}: LD (HL), C'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x72(self):
        self.mmu.write_byte(self.registers.get_hl(),self.registers.d)
        print('{}: LD (HL), D'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x73(self):
        self.mmu.write_byte(self.registers.get_hl(),self.registers.e)
        print('{}: LD (HL), E'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x74(self):
        self.mmu.write_byte(self.registers.get_hl(),self.registers.h)
        print('{}: LD (HL), H'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x75(self):
        self.mmu.write_byte(self.registers.get_hl(),self.registers.l)
        print('{}: LD (HL), L'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x77(self):
        self.mmu.write_byte(self.registers.get_hl(), self.registers.a)
        print('{}: LD (HL), A'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x78(self):
        self.registers.a = self.registers.b
        print('{}: LD A, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x79(self):
        self.registers.a = self.registers.c
        print('{}: LD A, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x7a(self):
        self.registers.a = self.registers.d
        print('{}: LD A, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x7b(self):
        self.registers.a = self.registers.e
        print('{}: LD A, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x7c(self):
        self.registers.a = self.registers.h
        print('{}: LD A, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x7d(self):
        self.registers.a = self.registers.l
        print('{}: LD A, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x7e(self):
        self.registers.a = self.mmu.read_byte(self.registers.get_hl())
        print('{}: LD A, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x7f(self):
        print('{}: LD A, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x80(self):
        self.add(self.registers.b)
        print('{}: ADD A, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x81(self):
        self.add(self.registers.c)
        print('{}: ADD A, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x82(self):
        self.add(self.registers.d)
        print('{}: ADD A, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x83(self):
        self.add(self.registers.e)
        print('{}: ADD A, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x84(self):
        self.add(self.registers.h)
        print('{}: ADD A, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x85(self):
        self.add(self.registers.l)
        print('{}: ADD A, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x86(self):
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.add(byte)
        print('{}: ADD A, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x87(self):
        self.add(self.registers.a)
        print('{}: ADD A, A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x88(self):
        self.adc(self.registers.b)
        print('{}: ADC A, B'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x89(self):
        self.adc(self.registers.c)
        print('{}: ADC A, C'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x8a(self):
        self.adc(self.registers.d)
        print('{}: ADC A, D'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x8b(self):
        self.adc(self.registers.e)
        print('{}: ADC A, E'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x8c(self):
        self.adc(self.registers.h)
        print('{}: ADC A, H'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x8d(self):
        self.adc(self.registers.l)
        print('{}: ADC A, L'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0x8e(self):
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.adc(byte)
        print('{}: ADC A, (HL)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0x8f(self):
        self.adc(self.registers.a)
        print('{}: ADC A, A'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x90(self):
        self.sub(self.registers.b)
        print('{}: SUB A, B'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x91(self):
        self.sub(self.registers.c)
        print('{}: SUB A, C'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x92(self):
        self.sub(self.registers.d)
        print('{}: SUB A, D'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x93(self):
        self.sub(self.registers.e)
        print('{}: SUB A, E'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x94(self):
        self.sub(self.registers.h)
        print('{}: SUB A, H'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x95(self):
        self.sub(self.registers.l)
        print('{}: SUB A, L'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x96(self):
        self.sub(self.mmu.read_byte(self.registers.get_hl))
        print('{}: SUB A, (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x97(self):
        self.sub(self.registers.a)
        print('{}: SUB A, A'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x98(self):
        self.sbc(self.registers.b)
        print('{}: SBC A, B'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x99(self):
        self.sbc(self.registers.c)
        print('{}: SBC A, C'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x9a(self):
        self.sbc(self.registers.d)
        print('{}: SBC A, D'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x9b(self):
        self.sbc(self.registers.e)
        print('{}: SBC A, E'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x9c(self):
        self.sbc(self.registers.h)
        print('{}: SBC A, H'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x9d(self):
        self.sbc(self.registers.l)
        print('{}: SBC A, L'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0x9e(self):
        byte = self.mmu.read_byte(self.registers.get_hl())
        self.sbc(byte)
        print('{}: SBC A, (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0x9f(self):
        self.sbc(self.registers.a)
        print('{}: SBC A, A'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa0(self):
        self._and(self.registers.b)
        print('{}: AND B'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa1(self):
        self._and(self.registers.c)
        print('{}: AND C'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa2(self):
        self._and(self.registers.d)
        print('{}: AND D'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa3(self):
        self._and(self.registers.e)
        print('{}: AND E'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa4(self):
        self._and(self.registers.h)
        print('{}: AND H'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa5(self):
        self._and(self.registers.l)
        print('{}: AND L'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xa6(self):
        byte = self.mmu.read_byte(self.registers.get_hl())
        self._and(byte)
        print('{}: AND A'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0xa7(self):
        self._and(self.registers.a)
        print('{}: AND A'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb0(self):
        self._or(self.registers.b)
        print('{}: OR B'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb1(self):
        self._or(self.registers.c)
        print('{}: OR C'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb2(self):
        self._or(self.registers.d)
        print('{}: OR D'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb3(self):
        self._or(self.registers.e)
        print('{}: OR E'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb4(self):
        self._or(self.registers.h)
        print('{}: OR H'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb5(self):
        self._or(self.registers.l)
        print('{}: OR L'.format(hex(self.registers.pc-1)))
        return 4

    def instruction_0xb6(self):
        byte = self.mmu.read_byte(self.registers.get_hl())
        self._or(self.byte)
        print('{}: OR (HL)'.format(hex(self.registers.pc-1)))
        return 8

    def instruction_0xb7(self):
        self._or(self.registers.a)
        print('{}: OR A'.format(hex(self.registers.pc-1)))
        return 4
    
    def instruction_0xc1(self):
        self.registers.set_bc(self.cpu.stackManager.pop_word())
        print('{}: POP BC'.format(hex(self.registers.pc-1)))
        return 12
    
    def instruction_0xc5(self):
        self.cpu.stackManager.push_word(self.registers.get_bc())
        print('{}: PUSH BC'.format(hex(self.registers.pc-1)))
        return 16
    
    def instruction_0xc6(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.add(byte)
        print('{}: ADD A, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8
    
    def instruction_0xce(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.adc(byte)
        print('{}: ADC A, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8
    
    def instruction_0xd1(self):
        self.registers.set_de(self.cpu.stackManager.pop_word())
        print('{}: POP DE'.format(hex(self.registers.pc-1)))
        return 12
    
    def instruction_0xd5(self):
        self.cpu.stackManager.push_word(self.registers.get_de())
        print('{}: PUSH DE'.format(hex(self.registers.pc-1)))
        return 16

    def instruction_0xd6(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.sub(byte)
        print('{}: SUB A, {}'.format(hex(self.registers.pc-2),hex(byte)))
        return 8

    def instruction_0xe0(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.mmu.write_byte((byte + 0xff00), self.registers.a)
        print('{}: LDH ({}), A'.format(hex(self.registers.pc-2),hex(byte)))
        return 12
    
    def instruction_0xe1(self):
        self.registers.set_hl(self.cpu.stackManager.pop_word())
        print('{}: POP HL'.format(hex(self.registers.pc-1)))
        return 12

    def instruction_0xe2(self):
        self.mmu.write_byte((self.registers.c + 0xff00), self.registers.a)
        print('{}: LD (0xff00+C), A'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0xe5(self):
        self.cpu.stackManager.push_word(self.registers.get_hl())
        print('{}: PUSH HL'.format(hex(self.registers.pc-1)))
        return 16

    def instruction_0xe6(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self._and(byte)
        print('{}: AND {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8
    
    def instruction_0xea(self):
        word = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.mmu.write_byte(word, self.registers.a)
        print('{}: LD ({}), A'.format(hex(self.registers.pc-3),hex(word)))
        return 8
    
    def instruction_0xf0(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.a = self.mmu.read_byte((byte + 0xff00))
        print('{}: LDH A, ({})'.format(hex(self.registers.pc-2),hex(byte)))
        return 12
    
    def instruction_0xf1(self):
        self.registers.set_af(self.cpu.stackManager.pop_word())
        print('{}: POP AF'.format(hex(self.registers.pc-1)))
        return 12
    
    def instruction_0xf2(self):
        self.registers.a = self.mmu.read_byte(self.registers.c + 0xff00)
        print('{}: LD A, (0xff00+C)'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0xf5(self):
        self.cpu.stackManager.push_word(self.registers.get_af())
        print('{}: PUSH AF'.format(hex(self.registers.pc-1)))
        return 16

    def instruction_0xf6(self):
        byte = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self._or(self.byte)
        print('{}: OR {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 8
    
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
        print('{}: LDHL SP, {}'.format(hex(self.registers.pc-2), hex(byte)))
        return 12
    
    def instruction_0xf9(self):
        self.registers.sp = self.registers.get_hl()
        print('{}: LD SP, HL'.format(hex(self.registers.pc-1)))
        return 8
    
    def instruction_0xfa(self):
        byte = self.mmu.read_byte(self.mmu.read_word(self.registers.pc))
        self.registers.pc += 2
        self.registers.a = byte
        print('{}: LD A, ({})'.format(hex(self.registers.pc-3),hex(byte)))
        return 16
    
    def unimplemented(self, opcode):
        print('{}: Unknow Opcode {}'.format(hex(self.registers.pc-1), hex(opcode)))
        return 0

    def add(self, value):
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
        if (self.registersa & 0xF) - (value & 0xF) - carry < 0: 
            self.registers.set_h_flag() 
        else: 
            self.registers.reset_h_flag()
        self.registers.set_n_flag()
        self.registersa = result & 0xff

    def _and(self, value):
        result = self.registers.a & value
        if result & 0xff == 0x0:
            self.registers.set_z_flag 
        else: 
            self.registers.reset_z_flag
        self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.set_h_flag()
        self.registers.a = result & 0xff

    def _or(self, value):
        result = self.registers.a | value
        if result & 0xff == 0x0:
            self.registers.set_z_flag 
        else: 
            self.registers.reset_z_flag
        self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.registers.a = result & 0xff

    def xor(self, value):
        result = self.registers.a ^ value
        if result & 0xff == 0x0:
            self.registers.set_z_flag 
        else: 
            self.registers.reset_z_flag
        self.registers.reset_c_flag()
        self.registers.reset_n_flag()
        self.registers.reset_h_flag()
        self.registers.a = result & 0xff
