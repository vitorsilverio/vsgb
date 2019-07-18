#!/usr/bin/env python
# -*- coding: utf-8 -*-

class InstructionPerformer:

    def __init__(self, cpu):
        self.cpu = cpu

    def perform_instruction(self, instruction):
        if instruction == 0x00:
            print('{}: NOP'.format(hex(self.cpu.registers.pc)))
            return 4
        if instruction == 0x01:
            word = self.cpu.mmu.read_word(self.cpu.registers.pc)
            self.cpu.registers.pc += 2
            self.cpu.registers.set_bc(word) 
            print('{}: LD BC, {}'.format(hex(self.cpu.registers.pc), hex(word)))
            return 4
        if instruction == 0x06:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            self.cpu.registers.b = byte 
            print('{}: LD B, {}'.format(hex(self.cpu.registers.pc), hex(byte)))
            return 4
        if instruction == 0x0e:
            byte = self.cpu.mmu.read_byte(self.cpu.registers.pc)
            self.cpu.registers.pc += 1
            self.cpu.registers.c = byte 
            print('{}: LD C, {}'.format(hex(self.cpu.registers.pc), hex(byte)))
            return 4
        if instruction == 0x11:
            word = self.cpu.mmu.read_word(self.cpu.registers.pc)
            self.cpu.registers.pc += 2
            self.cpu.registers.set_de(word) 
            print('{}: LD DE, {}'.format(hex(self.cpu.registers.pc), hex(word)))
            return 4 
        if instruction == 0x21:
            word = self.cpu.mmu.read_word(self.cpu.registers.pc)
            self.cpu.registers.pc += 2
            self.cpu.registers.set_hl(word) 
            print('{}: LD HL, {}'.format(hex(self.cpu.registers.pc), hex(word)))
            return 4   
        if instruction == 0x31:
            word = self.cpu.mmu.read_word(self.cpu.registers.pc)
            self.cpu.registers.pc += 2
            self.cpu.registers.sp = word
            print('{}: LD SP, {}'.format(hex(self.cpu.registers.pc), hex(word)))
            return 4 
        print('{}: Unknow Opcode {}'.format(hex(self.cpu.registers.pc), hex(instruction)))
        return 0
        


