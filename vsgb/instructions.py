#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vsgb.registers import Registers
from vsgb.byte_operations import signed_value, set_bit

nop = lambda: 4

def invalid():
    raise RuntimeError()

def inc_byte(operand: int) -> int:
    result = getattr(Registers, operand) + 1
    if result & 0xff == 0x0:
        Registers.set_z_flag()
    else:
        Registers.reset_z_flag()
    if result & 0xf == 0x0:
        Registers.set_h_flag()
    else:
        Registers.reset_h_flag()
    Registers.reset_n_flag()
    setattr(Registers, operand, result & 0xff)
    return 4

def dec_byte(operand: int) -> int:
    result = getattr(Registers, operand) - 1
    if result & 0xff == 0x0:
        Registers.set_z_flag()
    else:
        Registers.reset_z_flag()
    if result & 0xf == 0xf:
        Registers.set_h_flag()
    else:
        Registers.reset_h_flag()
    Registers.set_n_flag()
    setattr(Registers, operand, result & 0xff)
    return 4

def bit(pos: int, operand: int) -> int:
    bit = 1 if getattr(Registers, operand) & (1 << pos) else 0
    if bit & 0xff == 0x0:
        Registers.set_z_flag()
    else:
        Registers.reset_z_flag()
    Registers.reset_n_flag()
    Registers.set_h_flag()
    return 8

def res(pos : int, operand : int) -> int:
    setattr(Registers, operand, getattr(Registers, operand) & ((1 << pos) ^ 0xff))
    return 8

def set_(pos : int, operand : int) -> int:
    setattr(Registers, operand, set_bit(pos, getattr(Registers, operand)))
    return 8

def ccf() -> int:
    if Registers.is_c_flag():
        Registers.reset_c_flag()
    else:
        Registers.set_c_flag()
    Registers.reset_n_flag()
    Registers.reset_h_flag()
    return 4

def cp(operand: int):
    result = Registers.a - getattr(Registers, operand)
    if result & 0xff == 0x0:
        Registers.set_z_flag()
    else: 
        Registers.reset_z_flag()
    if Registers.a < getattr(Registers, operand):
        Registers.set_c_flag()
    else: 
        Registers.reset_c_flag()
    if (result & 0xf) > (Registers.a & 0xf):
        Registers.set_h_flag()
    else: 
        Registers.reset_h_flag()
    Registers.set_n_flag()

def ld_op_op(op1: int, op2: int) -> int:
    setattr(Registers, int, getattr(Registers, op2))
    return 4

def _and(operand: int) -> int:
    result = Registers.a & getattr(Registers, operand)
    if result & 0xff == 0x0:
        Registers.set_z_flag()
    else: 
        Registers.reset_z_flag()
    Registers.reset_c_flag()
    Registers.reset_n_flag()
    Registers.set_h_flag()
    Registers.a = result & 0xff
    return 4

def _or(operand : int) -> int:
    result = Registers.a | getattr(Registers, operand)
    if result & 0xff == 0x0:
        Registers.set_z_flag()
    else: 
        Registers.reset_z_flag()
    Registers.reset_c_flag()
    Registers.reset_n_flag()
    Registers.reset_h_flag()
    Registers.a = result & 0xff
    return 4

def xor(operand: int) -> int:
    result = Registers.a ^ getattr(Registers, operand)
    if result & 0xff == 0x0:
        Registers.set_z_flag()
    else: 
        Registers.reset_z_flag()
    Registers.reset_c_flag()
    Registers.reset_n_flag()
    Registers.reset_h_flag()
    Registers.a = result & 0xff
    return 4

def adc(operand : int) -> int:
    carry = 1 if Registers.is_c_flag() else 0
    result = Registers.a + getattr(Registers, operand) + carry
    if result & 0xff == 0x0: 
        Registers.set_z_flag()
    else: 
        Registers.reset_z_flag()
    if result > 0xff: 
        Registers.set_c_flag()
    else: 
        Registers.reset_c_flag()
    if (Registers.a & 0xf) + (getattr(Registers, operand) & 0xf) + carry > 0xf: 
        Registers.set_h_flag()
    else: 
        Registers.reset_h_flag()
    Registers.reset_n_flag()
    Registers.a = result & 0xff
    return 4


# 1 - mnemonic
# 2 - extra bytes
# 3 - function
# 4 - tuple of params
instructions = (
    ('NOP', 0, nop, tuple()),
    ('LD BC, {:04x}', 2, nop, tuple()),
    ('LD (BC), A', 0, nop, tuple()),
    ('INC BC', 0, nop, tuple()),
    ('INC B', 0, inc_byte, ('b',)),
    ('DEC B', 0, dec_byte, ('b',)),
    ('LD B, {:02x}', 1, nop, tuple()),
    ('RLCA', 0, nop, tuple()),
    ('LD ({:04x}), SP', 2, nop, tuple()),
    ('ADD HL, BC', 0, nop, tuple()),
    ('LD A, (BC)', 0, nop, tuple()),
    ('DEC BC', 0, nop, tuple()),
    ('INC C', 0, inc_byte, ('c',)),
    ('DEC C', 0, dec_byte, ('c',)),
    ('LD C, {:02x}', 1, nop, tuple()),
    ('RRCA', 0, nop, tuple()),
    ('STOP', 0, nop, tuple()),
    ('LD DE, {:04x}', 2, nop, tuple()),
    ('LD (DE), A', 0, nop, tuple()),
    ('INC DE', 0, nop, tuple()),
    ('INC D', 0, inc_byte, ('d',)),
    ('DEC D', 0, dec_byte, ('d',)),
    ('LD D, {:02x}', 1, nop, tuple()),
    ('RLA', 0, nop, tuple()),
    ('JR {:02x}', 1, nop, tuple()),
    ('ADD HL, DE', 0, nop, tuple()),
    ('LD A, (DE)', 0, nop, tuple()),
    ('DEC DE', 0, nop, tuple()),
    ('INC E', 0, inc_byte, ('e',)),
    ('DEC E', 0, dec_byte, ('e',)),
    ('LD E, {:02x}', 1, nop, tuple()),
    ('RRA', 0, nop, tuple()),
    ('JR NZ, {:02x}', 1, nop, tuple()),
    ('LD HL, {:04x}', 2, nop, tuple()),
    ('LD (HL+), A', 0, nop, tuple()),
    ('INC HL', 0, nop, tuple()),
    ('INC H', 0, inc_byte, ('h',)),
    ('DEC H', 0, dec_byte, ('h',)),
    ('LD H, {:02x}', 1, nop, tuple()),
    ('DAA', 0, nop, tuple()),
    ('JR Z, {:02x}', 1, nop, tuple()),
    ('ADD HL, HL', 0, nop, tuple()),
    ('LD A, (HL+)', 0, nop, tuple()),
    ('DEC HL', 0, nop, tuple()),
    ('INC L', 0, inc_byte, ('l',)),
    ('DEC L', 0, dec_byte, ('l',)),
    ('LD L, {:02x}', 1, nop, tuple()),
    ('CPL', 0, nop, tuple()),
    ('JR NC, {:02x}', 1, nop, tuple()),
    ('LD SP, {:04x}', 2, nop, tuple()),
    ('LD (HL-), A', 0, nop, tuple()),
    ('INC SP', 0, nop, tuple()),
    ('INC (HL)', 0, nop, tuple()),
    ('DEC (HL)', 0, nop, tuple()),
    ('LD (HL), {:02x}', 1, nop, tuple()),
    ('SCF', 0, nop, tuple()),
    ('JR C, {:02x}', 1, nop, tuple()),
    ('ADD HL, SP', 0, nop, tuple()),
    ('LD A, (HL-)', 0, nop, tuple()),
    ('DEC SP', 0, nop, tuple()),
    ('INC A', 0, inc_byte, ('a',)),
    ('DEC A', 0, dec_byte, ('a',)),
    ('LD A, {:02x}', 1, nop, tuple()),
    ('CCF', 0, ccf, tuple()),
    ('LD B, B', 0, nop, tuple()),
    ('LD B, C', 0, ld_op_op, ('b', 'c')),
    ('LD B, D', 0, ld_op_op, ('b', 'd')),
    ('LD B, E', 0, ld_op_op, ('b', 'e')),
    ('LD B, H', 0, ld_op_op, ('b', 'h')),
    ('LD B, L', 0, ld_op_op, ('b', 'l')),
    ('LD B, (HL)', 0, nop, tuple()),
    ('LD B, A', 0, ld_op_op, ('b', 'a')),
    ('LD C, B', 0, ld_op_op, ('c', 'b')),
    ('LD C, C', 0, nop, tuple()),
    ('LD C, D', 0, ld_op_op, ('c', 'd')),
    ('LD C, E', 0, ld_op_op, ('c', 'e')),
    ('LD C, H', 0, ld_op_op, ('c', 'h')),
    ('LD C, L', 0, ld_op_op, ('c', 'l')),
    ('LD C, (HL)', 0, nop, tuple()),
    ('LD C, A', 0, ld_op_op, ('c', 'a')),
    ('LD D, B', 0, ld_op_op, ('d', 'b')),
    ('LD D, C', 0, ld_op_op, ('d', 'c')),
    ('LD D, D', 0, nop, tuple()),
    ('LD D, E', 0, ld_op_op, ('d', 'e')),
    ('LD D, H', 0, ld_op_op, ('d', 'h')),
    ('LD D, L', 0, ld_op_op, ('d', 'l')),
    ('LD D, (HL)', 0, nop, tuple()),
    ('LD D, A', 0, ld_op_op, ('d', 'a')),
    ('LD E, B', 0, ld_op_op, ('e', 'b')),
    ('LD E, C', 0, ld_op_op, ('e', 'c')),
    ('LD E, D', 0, ld_op_op, ('e', 'd')),
    ('LD E, E', 0, nop, tuple()),
    ('LD E, H', 0, ld_op_op, ('e', 'h')),
    ('LD E, L', 0, ld_op_op, ('e', 'l')),
    ('LD E, (HL)', 0, nop, tuple()),
    ('LD E, A', 0, ld_op_op, ('e', 'a')),
    ('LD H, B', 0, ld_op_op, ('h', 'b')),
    ('LD H, C', 0, ld_op_op, ('h', 'c')),
    ('LD H, D', 0, ld_op_op, ('h', 'd')),
    ('LD H, E', 0, ld_op_op, ('h', 'e')),
    ('LD H, H', 0, nop, tuple()),
    ('LD H, L', 0, ld_op_op, ('h', 'l')),
    ('LD H, (HL)', 0, nop, tuple()),
    ('LD H, A', 0, ld_op_op, ('h', 'a')),
    ('LD L, B', 0, ld_op_op, ('l', 'b')),
    ('LD L, C', 0, ld_op_op, ('l', 'c')),
    ('LD L, D', 0, ld_op_op, ('l', 'd')),
    ('LD L, E', 0, ld_op_op, ('l', 'e')),
    ('LD L, H', 0, ld_op_op, ('l', 'h')),
    ('LD L, L', 0, nop, tuple()),
    ('LD L, (HL)', 0, nop, tuple()),
    ('LD L, A', 0, ld_op_op, ('l', 'a')),
    ('LD (HL), B', 0, nop, tuple()),
    ('LD (HL), C', 0, nop, tuple()),
    ('LD (HL), D', 0, nop, tuple()),
    ('LD (HL), E', 0, nop, tuple()),
    ('LD (HL), H', 0, nop, tuple()),
    ('LD (HL), L', 0, nop, tuple()),
    ('HALT', 0, nop, tuple()),
    ('LD (HL), A', 0, nop, tuple()),
    ('LD A, B', 0, ld_op_op, ('a', 'b')),
    ('LD A, C', 0, ld_op_op, ('a', 'c')),
    ('LD A, D', 0, ld_op_op, ('a', 'd')),
    ('LD A, E', 0, ld_op_op, ('a', 'e')),
    ('LD A, H', 0, ld_op_op, ('a', 'h')),
    ('LD A, L', 0, ld_op_op, ('a', 'l')),
    ('LD A, (HL)', 0, nop, tuple()),
    ('LD A, A', 0, nop, tuple()),
    ('ADD A, B', 0, nop, tuple()),
    ('ADD A, C', 0, nop, tuple()),
    ('ADD A, D', 0, nop, tuple()),
    ('ADD A, E', 0, nop, tuple()),
    ('ADD A, H', 0, nop, tuple()),
    ('ADD A, L', 0, nop, tuple()),
    ('ADD A, (HL)', 0, nop, tuple()),
    ('ADD A, A', 0, nop, tuple()),
    ('ADC A, B', 0, adc, ('b',)),
    ('ADC A, C', 0, adc, ('c',)),
    ('ADC A, D', 0, adc, ('d',)),
    ('ADC A, E', 0, adc, ('e',)),
    ('ADC A, H', 0, adc, ('h',)),
    ('ADC A, L', 0, adc, ('l',)),
    ('ADC A, (HL)', 0, nop, tuple()),
    ('ADC A, A', 0, adc, ('a',)),
    ('SUB A, B', 0, nop, tuple()),
    ('SUB A, C', 0, nop, tuple()),
    ('SUB A, D', 0, nop, tuple()),
    ('SUB A, E', 0, nop, tuple()),
    ('SUB A, H', 0, nop, tuple()),
    ('SUB A, L', 0, nop, tuple()),
    ('SUB A, (HL)', 0, nop, tuple()),
    ('SUB A, A', 0, nop, tuple()),
    ('SBC A, B', 0, nop, tuple()),
    ('SBC A, C', 0, nop, tuple()),
    ('SBC A, D', 0, nop, tuple()),
    ('SBC A, E', 0, nop, tuple()),
    ('SBC A, H', 0, nop, tuple()),
    ('SBC A, L', 0, nop, tuple()),
    ('SBC A, (HL)', 0, nop, tuple()),
    ('SBC A, A', 0, nop, tuple()),
    ('AND B', 0, _and, ('b',)),
    ('AND C', 0, _and, ('c',)),
    ('AND D', 0, _and, ('d',)),
    ('AND E', 0, _and, ('e',)),
    ('AND H', 0, _and, ('h',)),
    ('AND L', 0, _and, ('l',)),
    ('AND (HL)', 0, nop, tuple()),
    ('AND A', 0, _and, ('a',)),
    ('XOR B', 0, xor, ('b',)),
    ('XOR C', 0, xor, ('c',)),
    ('XOR D', 0, xor, ('d',)),
    ('XOR E', 0, xor, ('e',)),
    ('XOR H', 0, xor, ('h',)),
    ('XOR L', 0, xor, ('l',)),
    ('XOR (HL)', 0, nop, tuple()),
    ('XOR A', 0, xor, ('a',)),
    ('OR B', 0, _or, ('b',)),
    ('OR C', 0, _or, ('c',)),
    ('OR D', 0, _or, ('d',)),
    ('OR E', 0, _or, ('e',)),
    ('OR H', 0, _or, ('h',)),
    ('OR L', 0, _or, ('l',)),
    ('OR (HL)', 0, nop, tuple()),
    ('OR A', 0, _or, ('a',)),
    ('CP B', 0, cp, ('b')),
    ('CP C', 0, cp, ('c')),
    ('CP D', 0, cp, ('d')),
    ('CP E', 0, cp, ('e')),
    ('CP H', 0, cp, ('h')),
    ('CP L', 0, cp, ('l')),
    ('CP (HL)', 0, nop, tuple()),
    ('CP A', 0, cp, ('a')),
    ('RET NZ', 0, nop, tuple()),
    ('POP BC', 0, nop, tuple()),
    ('JP NZ, {:04x}', 2, nop, tuple()),
    ('JP {:04x}', 2, nop, tuple()),
    ('CALL NZ, {:04x}', 2, nop, tuple()),
    ('PUSH BC', 0, nop, tuple()),
    ('ADD A, {:02x}', 1, nop, tuple()),
    ('RST 0x00', 0, nop, tuple()),
    ('RET Z', 0, nop, tuple()),
    ('RET', 0, nop, tuple()),
    ('JP Z, {:04x}', 2, nop, tuple()),
    ('PREFIX CB', 0, nop, tuple()),
    ('CALL Z, {:04x}', 2, nop, tuple()),
    ('CALL {:04x}', 2, nop, tuple()),
    ('ADC A, {:02x}', 1, nop, tuple()),
    ('RST 0x08', 0, nop, tuple()),
    ('RET NC', 0, nop, tuple()),
    ('POP DE', 0, nop, tuple()),
    ('JP NC, {:04x}', 2, nop, tuple()),
    ('INVALID INSTRUCTION (D3)', 0, invalid, tuple()),
    ('CALL NC, {:04x}', 2, nop, tuple()),
    ('PUSH DE', 0, nop, tuple()),
    ('SUB A, {:02x}', 1, nop, tuple()),
    ('RST 0x10', 0, nop, tuple()),
    ('RET C', 0, nop, tuple()),
    ('RETI', 0, nop, tuple()),
    ('JP C, {:04x}', 2, nop, tuple()),
    ('INVALID INSTRUCTION (DB)', 0, invalid, tuple()),
    ('CALL C, {:04x}', 2, nop, tuple()),
    ('INVALID INSTRUCTION (DD)', 0, invalid, tuple()),
    ('SBC A, {:02x}', 1, nop, tuple()),
    ('RST 0x18', 0, nop, tuple()),
    ('LDH ({:02x}), A', 1, nop, tuple()),
    ('POP HL', 0, nop, tuple()),
    ('LD (0xff00+C), A', 0, nop, tuple()),
    ('INVALID INSTRUCTION (E3)', 0, invalid, tuple()),
    ('INVALID INSTRUCTION (E4)', 0, invalid, tuple()),
    ('PUSH HL', 0, nop, tuple()),
    ('AND {:02x}', 1, nop, tuple()),
    ('RST 0x20', 0, nop, tuple()),
    ('ADD SP, {:02x}', 1, nop, tuple()),
    ('JP HL', 0, nop, tuple()),
    ('LD ({:04x}), A', 2, nop, tuple()),
    ('INVALID INSTRUCTION (EB)', 0, invalid, tuple()),
    ('INVALID INSTRUCTION (EC)', 0, invalid, tuple()),
    ('INVALID INSTRUCTION (ED)', 0, invalid, tuple()),
    ('XOR {:02x}', 1, nop, tuple()),
    ('RST 0x28', 0, nop, tuple()),
    ('LDH A, ({:02x})', 1, nop, tuple()),
    ('POP AF', 0, nop, tuple()),
    ('LD A, (0xff00+C)', 0, nop, tuple()),
    ('DI', 0, nop, tuple()),
    ('INVALID INSTRUCTION (F4)', 0, invalid, tuple()),
    ('PUSH AF', 0, nop, tuple()),
    ('OR {:02x}', 1, nop, tuple()),
    ('RST 0x30', 0, nop, tuple()),
    ('LDHL SP, {:02x}', 1, nop, tuple()),
    ('LD SP, HL', 0, nop, tuple()),
    ('LD A, ({:04x})', 2, nop, tuple()),
    ('EI', 0, nop, tuple()),
    ('INVALID INSTRUCTION (FC)', 0, invalid, tuple()),
    ('INVALID INSTRUCTION (FD)', 0, invalid, tuple()),
    ('CP {:02x}', 1, nop, tuple()),
    ('RST 0x38', 0, nop, tuple()),
    ('RLC B', 0, nop, tuple()),
    ('RLC C', 0, nop, tuple()),
    ('RLC D', 0, nop, tuple()),
    ('RLC E', 0, nop, tuple()),
    ('RLC H', 0, nop, tuple()),
    ('RLC L', 0, nop, tuple()),
    ('RLC (HL)', 0, nop, tuple()),
    ('RLC A', 0, nop, tuple()),
    ('RRC B', 0, nop, tuple()),
    ('RRC C', 0, nop, tuple()),
    ('RRC D', 0, nop, tuple()),
    ('RRC E', 0, nop, tuple()),
    ('RRC H', 0, nop, tuple()),
    ('RRC L', 0, nop, tuple()),
    ('RRC (HL)', 0, nop, tuple()),
    ('RRC A', 0, nop, tuple()),
    ('RL B', 0, nop, tuple()),
    ('RL C', 0, nop, tuple()),
    ('RL D', 0, nop, tuple()),
    ('RL E', 0, nop, tuple()),
    ('RL H', 0, nop, tuple()),
    ('RL L', 0, nop, tuple()),
    ('RL (HL)', 0, nop, tuple()),
    ('RL A', 0, nop, tuple()),
    ('RR B', 0, nop, tuple()),
    ('RR C', 0, nop, tuple()),
    ('RR D', 0, nop, tuple()),
    ('RR E', 0, nop, tuple()),
    ('RR H', 0, nop, tuple()),
    ('RR L', 0, nop, tuple()),
    ('RR (HL)', 0, nop, tuple()),
    ('RR A', 0, nop, tuple()),
    ('SLA B', 0, nop, tuple()),
    ('SLA C', 0, nop, tuple()),
    ('SLA D', 0, nop, tuple()),
    ('SLA E', 0, nop, tuple()),
    ('SLA H', 0, nop, tuple()),
    ('SLA L', 0, nop, tuple()),
    ('SLA (HL)', 0, nop, tuple()),
    ('SLA A', 0, nop, tuple()),
    ('SRA B', 0, nop, tuple()),
    ('SRA C', 0, nop, tuple()),
    ('SRA D', 0, nop, tuple()),
    ('SRA E', 0, nop, tuple()),
    ('SRA H', 0, nop, tuple()),
    ('SRA L', 0, nop, tuple()),
    ('SRA (HL)', 0, nop, tuple()),
    ('SRA A', 0, nop, tuple()),
    ('SWAP B', 0, nop, tuple()),
    ('SWAP C', 0, nop, tuple()),
    ('SWAP D', 0, nop, tuple()),
    ('SWAP E', 0, nop, tuple()),
    ('SWAP H', 0, nop, tuple()),
    ('SWAP L', 0, nop, tuple()),
    ('SWAP (HL)', 0, nop, tuple()),
    ('SWAP A', 0, nop, tuple()),
    ('SRL B', 0, nop, tuple()),
    ('SRL C', 0, nop, tuple()),
    ('SRL D', 0, nop, tuple()),
    ('SRL E', 0, nop, tuple()),
    ('SRL H', 0, nop, tuple()),
    ('SRL L', 0, nop, tuple()),
    ('SRL (HL)', 0, nop, tuple()),
    ('SRL A', 0, nop, tuple()),
    ('BIT 0, B', 0, bit, (0, 'b')),
    ('BIT 0, C', 0, bit, (0, 'c')),
    ('BIT 0, D', 0, bit, (0, 'd')),
    ('BIT 0, E', 0, bit, (0, 'e')),
    ('BIT 0, H', 0, bit, (0, 'h')),
    ('BIT 0, L', 0, bit, (0, 'l')),
    ('BIT 0, (HL)', 0, nop, tuple()),
    ('BIT 0, A', 0, bit, (0, 'a')),
    ('BIT 1, B', 0, bit, (1, 'b')),
    ('BIT 1, C', 0, bit, (1, 'c')),
    ('BIT 1, D', 0, bit, (1, 'd')),
    ('BIT 1, E', 0, bit, (1, 'e')),
    ('BIT 1, H', 0, bit, (1, 'h')),
    ('BIT 1, L', 0, bit, (1, 'l')),
    ('BIT 1, (HL)', 0, nop, tuple()),
    ('BIT 1, A', 0, bit, (1, 'a')),
    ('BIT 2, B', 0, bit, (2, 'b')),
    ('BIT 2, C', 0, bit, (2, 'c')),
    ('BIT 2, D', 0, bit, (2, 'd')),
    ('BIT 2, E', 0, bit, (2, 'e')),
    ('BIT 2, H', 0, bit, (2, 'h')),
    ('BIT 2, L', 0, bit, (2, 'l')),
    ('BIT 2, (HL)', 0, nop, tuple()),
    ('BIT 2, A', 0, bit, (2, 'a')),
    ('BIT 3, B', 0, bit, (3, 'b')),
    ('BIT 3, C', 0, bit, (3, 'c')),
    ('BIT 3, D', 0, bit, (3, 'd')),
    ('BIT 3, E', 0, bit, (3, 'e')),
    ('BIT 3, H', 0, bit, (3, 'h')),
    ('BIT 3, L', 0, bit, (3, 'l')),
    ('BIT 3, (HL)', 0, nop, tuple()),
    ('BIT 3, A', 0, bit, (3, 'a')),
    ('BIT 4, B', 0, bit, (4, 'b')),
    ('BIT 4, C', 0, bit, (4, 'c')),
    ('BIT 4, D', 0, bit, (4, 'd')),
    ('BIT 4, E', 0, bit, (4, 'e')),
    ('BIT 4, H', 0, bit, (4, 'h')),
    ('BIT 4, L', 0, bit, (4, 'l')),
    ('BIT 4, (HL)', 0, nop, tuple()),
    ('BIT 4, A', 0, bit, (4, 'a')),
    ('BIT 5, B', 0, bit, (5, 'b')),
    ('BIT 5, C', 0, bit, (5, 'c')),
    ('BIT 5, D', 0, bit, (5, 'd')),
    ('BIT 5, E', 0, bit, (5, 'e')),
    ('BIT 5, H', 0, bit, (5, 'h')),
    ('BIT 5, L', 0, bit, (5, 'l')),
    ('BIT 5, (HL)', 0, nop, tuple()),
    ('BIT 5, A', 0, bit, (5, 'a')),
    ('BIT 6, B', 0, bit, (6, 'b')),
    ('BIT 6, C', 0, bit, (6, 'c')),
    ('BIT 6, D', 0, bit, (6, 'd')),
    ('BIT 6, E', 0, bit, (6, 'e')),
    ('BIT 6, H', 0, bit, (6, 'h')),
    ('BIT 6, L', 0, bit, (6, 'l')),
    ('BIT 6, (HL)', 0, nop, tuple()),
    ('BIT 6, A', 0, bit, (6, 'a')),
    ('BIT 7, B', 0, bit, (7, 'b')),
    ('BIT 7, C', 0, bit, (7, 'c')),
    ('BIT 7, D', 0, bit, (7, 'd')),
    ('BIT 7, E', 0, bit, (7, 'e')),
    ('BIT 7, H', 0, bit, (7, 'h')),
    ('BIT 7, L', 0, bit, (7, 'l')),
    ('BIT 7, (HL)', 0, nop, tuple()),
    ('BIT 7, A', 0, bit, (7, 'a')),
    ('RES 0, B', 0, res, (0, 'b')),
    ('RES 0, C', 0, res, (0, 'c')),
    ('RES 0, D', 0, res, (0, 'd')),
    ('RES 0, E', 0, res, (0, 'e')),
    ('RES 0, H', 0, res, (0, 'h')),
    ('RES 0, L', 0, res, (0, 'l')),
    ('RES 0, (HL)', 0, nop, tuple()),
    ('RES 0, A', 0, res, (0, 'a')),
    ('RES 1, B', 0, res, (1, 'b')),
    ('RES 1, C', 0, res, (1, 'c')),
    ('RES 1, D', 0, res, (1, 'd')),
    ('RES 1, E', 0, res, (1, 'e')),
    ('RES 1, H', 0, res, (1, 'h')),
    ('RES 1, L', 0, res, (1, 'l')),
    ('RES 1, (HL)', 0, nop, tuple()),
    ('RES 1, A', 0, res, (1, 'a')),
    ('RES 2, B', 0, res, (2, 'b')),
    ('RES 2, C', 0, res, (2, 'c')),
    ('RES 2, D', 0, res, (2, 'd')),
    ('RES 2, E', 0, res, (2, 'e')),
    ('RES 2, H', 0, res, (2, 'h')),
    ('RES 2, L', 0, res, (2, 'l')),
    ('RES 2, (HL)', 0, nop, tuple()),
    ('RES 2, A', 0, res, (2, 'a')),
    ('RES 3, B', 0, res, (3, 'b')),
    ('RES 3, C', 0, res, (3, 'c')),
    ('RES 3, D', 0, res, (3, 'd')),
    ('RES 3, E', 0, res, (3, 'e')),
    ('RES 3, H', 0, res, (3, 'h')),
    ('RES 3, L', 0, res, (3, 'l')),
    ('RES 3, (HL)', 0, nop, tuple()),
    ('RES 3, A', 0, res, (3, 'a')),
    ('RES 4, B', 0, res, (4, 'b')),
    ('RES 4, C', 0, res, (4, 'c')),
    ('RES 4, D', 0, res, (4, 'd')),
    ('RES 4, E', 0, res, (4, 'e')),
    ('RES 4, H', 0, res, (4, 'h')),
    ('RES 4, L', 0, res, (4, 'l')),
    ('RES 4, (HL)', 0, nop, tuple()),
    ('RES 4, A', 0, res, (4, 'a')),
    ('RES 5, B', 0, res, (5, 'b')),
    ('RES 5, C', 0, res, (5, 'c')),
    ('RES 5, D', 0, res, (5, 'd')),
    ('RES 5, E', 0, res, (5, 'e')),
    ('RES 5, H', 0, res, (5, 'h')),
    ('RES 5, L', 0, res, (5, 'l')),
    ('RES 5, (HL)', 0, nop, tuple()),
    ('RES 5, A', 0, res, (5, 'a')),
    ('RES 6, B', 0, res, (6, 'b')),
    ('RES 6, C', 0, res, (6, 'c')),
    ('RES 6, D', 0, res, (6, 'd')),
    ('RES 6, E', 0, res, (6, 'e')),
    ('RES 6, H', 0, res, (6, 'h')),
    ('RES 6, L', 0, res, (6, 'l')),
    ('RES 6, (HL)', 0, nop, tuple()),
    ('RES 6, A', 0, res, (6, 'a')),
    ('RES 7, B', 0, res, (7, 'b')),
    ('RES 7, C', 0, res, (7, 'c')),
    ('RES 7, D', 0, res, (7, 'd')),
    ('RES 7, E', 0, res, (7, 'e')),
    ('RES 7, H', 0, res, (7, 'h')),
    ('RES 7, L', 0, res, (7, 'l')),
    ('RES 7, (HL)', 0, nop, tuple()),
    ('RES 7, A', 0, res, (7, 'a')),
    ('SET 0, B', 0, set_, (0, 'b')),
    ('SET 0, C', 0, set_, (0, 'c')),
    ('SET 0, D', 0, set_, (0, 'd')),
    ('SET 0, E', 0, set_, (0, 'e')),
    ('SET 0, H', 0, set_, (0, 'h')),
    ('SET 0, L', 0, set_, (0, 'l')),
    ('SET 0, (HL)', 0, nop, tuple()),
    ('SET 0, A', 0, set_, (0, 'a')),
    ('SET 1, B', 0, set_, (1, 'b')),
    ('SET 1, C', 0, set_, (1, 'c')),
    ('SET 1, D', 0, set_, (1, 'd')),
    ('SET 1, E', 0, set_, (1, 'e')),
    ('SET 1, H', 0, set_, (1, 'h')),
    ('SET 1, L', 0, set_, (1, 'l')),
    ('SET 1, (HL)', 0, nop, tuple()),
    ('SET 1, A', 0, set_, (1, 'a')),
    ('SET 2, B', 0, set_, (2, 'b')),
    ('SET 2, C', 0, set_, (2, 'c')),
    ('SET 2, D', 0, set_, (2, 'd')),
    ('SET 2, E', 0, set_, (2, 'e')),
    ('SET 2, H', 0, set_, (2, 'h')),
    ('SET 2, L', 0, set_, (2, 'l')),
    ('SET 2, (HL)', 0, nop, tuple()),
    ('SET 2, A', 0, set_, (2, 'a')),
    ('SET 3, B', 0, set_, (3, 'b')),
    ('SET 3, C', 0, set_, (3, 'c')),
    ('SET 3, D', 0, set_, (3, 'd')),
    ('SET 3, E', 0, set_, (3, 'e')),
    ('SET 3, H', 0, set_, (3, 'h')),
    ('SET 3, L', 0, set_, (3, 'l')),
    ('SET 3, (HL)', 0, nop, tuple()),
    ('SET 3, A', 0, set_, (3, 'a')),
    ('SET 4, B', 0, set_, (4, 'b')),
    ('SET 4, C', 0, set_, (4, 'c')),
    ('SET 4, D', 0, set_, (4, 'd')),
    ('SET 4, E', 0, set_, (4, 'e')),
    ('SET 4, H', 0, set_, (4, 'h')),
    ('SET 4, L', 0, set_, (4, 'l')),
    ('SET 4, (HL)', 0, nop, tuple()),
    ('SET 4, A', 0, set_, (4, 'a')),
    ('SET 5, B', 0, set_, (5, 'b')),
    ('SET 5, C', 0, set_, (5, 'c')),
    ('SET 5, D', 0, set_, (5, 'd')),
    ('SET 5, E', 0, set_, (5, 'e')),
    ('SET 5, H', 0, set_, (5, 'h')),
    ('SET 5, L', 0, set_, (5, 'l')),
    ('SET 5, (HL)', 0, nop, tuple()),
    ('SET 5, A', 0, set_, (5, 'a')),
    ('SET 6, B', 0, set_, (6, 'b')),
    ('SET 6, C', 0, set_, (6, 'c')),
    ('SET 6, D', 0, set_, (6, 'd')),
    ('SET 6, E', 0, set_, (6, 'e')),
    ('SET 6, H', 0, set_, (6, 'h')),
    ('SET 6, L', 0, set_, (6, 'l')),
    ('SET 6, (HL)', 0, nop, tuple()),
    ('SET 6, A', 0, set_, (6, 'a')),
    ('SET 7, B', 0, set_, (7, 'b')),
    ('SET 7, C', 0, set_, (7, 'c')),
    ('SET 7, D', 0, set_, (7, 'd')),
    ('SET 7, E', 0, set_, (7, 'e')),
    ('SET 7, H', 0, set_, (7, 'h')),
    ('SET 7, L', 0, set_, (7, 'l')),
    ('SET 7, (HL)', 0, nop, tuple()),
    ('SET 7, A', 0, set_, (7, 'a'))
)
