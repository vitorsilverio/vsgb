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
        self.stackManager = cpu.stackManager
        self.instrs = [
            self.NOP, self.LD_BC_d16, self.LD_REF_BC_A, self.INC_BC, self.INC_B, self.DEC_B, self.LD_B_d8, self.RLCA, self.LD_REF_a16_SP, self.ADD_HL_BC, self.LD_A_REF_BC, self.DEC_BC, self.INC_C, self.DEC_C, self.LD_C_d8, self.RRCA, 
            self.STOP, self.LD_DE_d16, self.LD_REF_DE_A, self.INC_DE, self.INC_D, self.DEC_D, self.LD_D_d8, self.RLA, self.JR_r8, self.ADD_HL_DE, self.LD_A_REF_DE, self.DEC_DE, self.INC_E, self.DEC_E, self.LD_E_d8, self.RRA, 
            self.JR_NZ_r8, self.LD_HL_d16, self.LDI_HL_A, self.INC_HL, self.INC_H, self.DEC_H, self.LD_H_d8, self.DAA, self.JR_Z_r8, self.ADD_HL_HL, self.LDI_A_HL, self.DEC_HL, self.INC_L, self.DEC_L, self.LD_L_d8, self.CPL, 
            self.JR_NC_r8, self.LD_SP_d16, self.LDD_HL_A, self.INC_SP, self.INC_REF_HL, self.DEC_REF_HL, self.LD_REF_HL_d8, self.SCF, self.JR_C_r8, self.ADD_HL_SP, self.LDD_A_HL, self.DEC_SP, self.INC_A, self.DEC_A, self.LD_A_d8, self.CCF, 
            self.LD_B_B, self.LD_B_C, self.LD_B_D, self.LD_B_E, self.LD_B_H, self.LD_B_L, self.LD_B_REF_HL, self.LD_B_A, self.LD_C_B, self.LD_C_C, self.LD_C_D, self.LD_C_E, self.LD_C_H, self.LD_C_L, self.LD_C_REF_HL, self.LD_C_A, 
            self.LD_D_B, self.LD_D_C, self.LD_D_D, self.LD_D_E, self.LD_D_H, self.LD_D_L, self.LD_D_REF_HL, self.LD_D_A, self.LD_E_B, self.LD_E_C, self.LD_E_D, self.LD_E_E, self.LD_E_H, self.LD_E_L, self.LD_E_REF_HL, self.LD_E_A, 
            self.LD_H_B, self.LD_H_C, self.LD_H_D, self.LD_H_E, self.LD_H_H, self.LD_H_L, self.LD_H_REF_HL, self.LD_H_A, self.LD_L_B, self.LD_L_C, self.LD_L_D, self.LD_L_E, self.LD_L_H, self.LD_L_L, self.LD_L_REF_HL, self.LD_L_A, 
            self.LD_REF_HL_B, self.LD_REF_HL_C, self.LD_REF_HL_D, self.LD_REF_HL_E, self.LD_REF_HL_H, self.LD_REF_HL_L, self.HALT, self.LD_REF_HL_A, self.LD_A_B, self.LD_A_C, self.LD_A_D, self.LD_A_E, self.LD_A_H, self.LD_A_L, self.LD_A_REF_HL, self.LD_A_A, 
            self.ADD_B, self.ADD_C, self.ADD_D, self.ADD_E, self.ADD_H, self.ADD_L, self.ADD_REF_HL, self.ADD_A, self.ADC_B, self.ADC_C, self.ADC_D, self.ADC_E, self.ADC_H, self.ADC_L, self.ADC_REF_HL, self.ADC_A, 
            self.SUB_B, self.SUB_C, self.SUB_D, self.SUB_E, self.SUB_H, self.SUB_L, self.SUB_REF_HL, self.SUB_A, self.SBC_B, self.SBC_C, self.SBC_D, self.SBC_E, self.SBC_H, self.SBC_L, self.SBC_REF_HL, self.SBC_A, 
            self.AND_B, self.AND_C, self.AND_D, self.AND_E, self.AND_H, self.AND_L, self.AND_REF_HL, self.AND_A, self.XOR_B, self.XOR_C, self.XOR_D, self.XOR_E, self.XOR_H, self.XOR_L, self.XOR_REF_HL, self.XOR_A, 
            self.OR_B, self.OR_C, self.OR_D, self.OR_E, self.OR_H, self.OR_L, self.OR_REF_HL, self.OR_A, self.CP_B, self.CP_C, self.CP_D, self.CP_E, self.CP_H, self.CP_L, self.CP_REF_HL, self.CP_A, 
            self.RET_NZ, self.POP_BC, self.JP_NZ_a16, self.JP_a16, self.CALL_NZ_a16, self.PUSH_BC, self.ADD_d8, self.RST_00H, self.RET_Z, self.RET, self.JP_Z_a16, None, self.CALL_Z_a16, self.CALL_a16, self.ADC_d8, self.RST_08H, 
            self.RET_NC, self.POP_DE, self.JP_NC_a16, None, self.CALL_NC_a16, self.PUSH_DE, self.SUB_d8, self.RST_10H, self.RET_C, self.RETI, self.JP_C_a16, None, self.CALL_C_a16, None, self.SBC_d8, self.RST_18H, 
            self.LDH_REF_a8_A, self.POP_HL, self.LD_REF_C_A, None, None, self.PUSH_HL, self.AND_d8, self.RST_20H, self.ADD_SP_r8, self.JP_HL, self.LD_REF_a16_A, None, None, None, self.XOR_d8, self.RST_28H, 
            self.LDH_A_REF_a8, self.POP_AF, self.LD_A_REF_C, self.DI, None, self.PUSH_AF, self.OR_d8, self.RST_30H, self.LD_HL_SP_r8, self.LD_SP_HL, self.LD_A_a16, self.EI, None, None, self.CP_d8, self.RST_38H, 
            self.RLC_B, self.RLC_C, self.RLC_D, self.RLC_E, self.RLC_H, self.RLC_L, self.RLC_REF_HL, self.RLC_A, self.RRC_B, self.RRC_C, self.RRC_D, self.RRC_E, self.RRC_H, self.RRC_L, self.RRC_REF_HL, self.RRC_A, 
            self.RL_B, self.RL_C, self.RL_D, self.RL_E, self.RL_H, self.RL_L, self.RL_REF_HL, self.RL_A, self.RR_B, self.RR_C, self.RR_D, self.RR_E, self.RR_H, self.RR_L, self.RR_REF_HL, self.RR_A, 
            self.SLA_B, self.SLA_C, self.SLA_D, self.SLA_E, self.SLA_H, self.SLA_L, self.SLA_REF_HL, self.SLA_A, self.SRA_B, self.SRA_C, self.SRA_D, self.SRA_E, self.SRA_H, self.SRA_L, self.SRA_REF_HL, self.SRA_A, 
            self.SWAP_B, self.SWAP_C, self.SWAP_D, self.SWAP_E, self.SWAP_H, self.SWAP_L, self.SWAP_REF_HL, self.SWAP_A, self.SRL_B, self.SRL_C, self.SRL_D, self.SRL_E, self.SRL_H, self.SRL_L, self.SRL_REF_HL, self.SRL_A, 
            self.BIT_0_B, self.BIT_0_C, self.BIT_0_D, self.BIT_0_E, self.BIT_0_H, self.BIT_0_L, self.BIT_0_REF_HL, self.BIT_0_A, self.BIT_1_B, self.BIT_1_C, self.BIT_1_D, self.BIT_1_E, self.BIT_1_H, self.BIT_1_L, self.BIT_1_REF_HL, self.BIT_1_A, 
            self.BIT_2_B, self.BIT_2_C, self.BIT_2_D, self.BIT_2_E, self.BIT_2_H, self.BIT_2_L, self.BIT_2_REF_HL, self.BIT_2_A, self.BIT_3_B, self.BIT_3_C, self.BIT_3_D, self.BIT_3_E, self.BIT_3_H, self.BIT_3_L, self.BIT_3_REF_HL, self.BIT_3_A, 
            self.BIT_4_B, self.BIT_4_C, self.BIT_4_D, self.BIT_4_E, self.BIT_4_H, self.BIT_4_L, self.BIT_4_REF_HL, self.BIT_4_A, self.BIT_5_B, self.BIT_5_C, self.BIT_5_D, self.BIT_5_E, self.BIT_5_H, self.BIT_5_L, self.BIT_5_REF_HL, self.BIT_5_A, 
            self.BIT_6_B, self.BIT_6_C, self.BIT_6_D, self.BIT_6_E, self.BIT_6_H, self.BIT_6_L, self.BIT_6_REF_HL, self.BIT_6_A, self.BIT_7_B, self.BIT_7_C, self.BIT_7_D, self.BIT_7_E, self.BIT_7_H, self.BIT_7_L, self.BIT_7_REF_HL, self.BIT_7_A, 
            self.RES_0_B, self.RES_0_C, self.RES_0_D, self.RES_0_E, self.RES_0_H, self.RES_0_L, self.RES_0_REF_HL, self.RES_0_A, self.RES_1_B, self.RES_1_C, self.RES_1_D, self.RES_1_E, self.RES_1_H, self.RES_1_L, self.RES_1_REF_HL, self.RES_1_A, 
            self.RES_2_B, self.RES_2_C, self.RES_2_D, self.RES_2_E, self.RES_2_H, self.RES_2_L, self.RES_2_REF_HL, self.RES_2_A, self.RES_3_B, self.RES_3_C, self.RES_3_D, self.RES_3_E, self.RES_3_H, self.RES_3_L, self.RES_3_REF_HL, self.RES_3_A, 
            self.RES_4_B, self.RES_4_C, self.RES_4_D, self.RES_4_E, self.RES_4_H, self.RES_4_L, self.RES_4_REF_HL, self.RES_4_A, self.RES_5_B, self.RES_5_C, self.RES_5_D, self.RES_5_E, self.RES_5_H, self.RES_5_L, self.RES_5_REF_HL, self.RES_5_A, 
            self.RES_6_B, self.RES_6_C, self.RES_6_D, self.RES_6_E, self.RES_6_H, self.RES_6_L, self.RES_6_REF_HL, self.RES_6_A, self.RES_7_B, self.RES_7_C, self.RES_7_D, self.RES_7_E, self.RES_7_H, self.RES_7_L, self.RES_7_REF_HL, self.RES_7_A, 
            self.SET_0_B, self.SET_0_C, self.SET_0_D, self.SET_0_E, self.SET_0_H, self.SET_0_L, self.SET_0_REF_HL, self.SET_0_A, self.SET_1_B, self.SET_1_C, self.SET_1_D, self.SET_1_E, self.SET_1_H, self.SET_1_L, self.SET_1_REF_HL, self.SET_1_A, 
            self.SET_2_B, self.SET_2_C, self.SET_2_D, self.SET_2_E, self.SET_2_H, self.SET_2_L, self.SET_2_REF_HL, self.SET_2_A, self.SET_3_B, self.SET_3_C, self.SET_3_D, self.SET_3_E, self.SET_3_H, self.SET_3_L, self.SET_3_REF_HL, self.SET_3_A, 
            self.SET_4_B, self.SET_4_C, self.SET_4_D, self.SET_4_E, self.SET_4_H, self.SET_4_L, self.SET_4_REF_HL, self.SET_4_A, self.SET_5_B, self.SET_5_C, self.SET_5_D, self.SET_5_E, self.SET_5_H, self.SET_5_L, self.SET_5_REF_HL, self.SET_5_A, 
            self.SET_6_B, self.SET_6_C, self.SET_6_D, self.SET_6_E, self.SET_6_H, self.SET_6_L, self.SET_6_REF_HL, self.SET_6_A, self.SET_7_B, self.SET_7_C, self.SET_7_D, self.SET_7_E, self.SET_7_H, self.SET_7_L, self.SET_7_REF_HL, self.SET_7_A 
        ]

    def perform_instruction(self, opcode: int) -> int:
        if 0xcb00 <= opcode :
            return self.instrs[opcode - 0xca00]()
        return self.instrs[opcode]()
    
    def NOP(self) -> int:
        return 4
    
    def LD_BC_d16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        Registers.set_bc(word) 
        return 12
    
    def LD_REF_BC_A(self) -> int:
        self.mmu.write_byte(Registers.get_bc(), Registers.a)
        return 8

    def INC_BC(self) -> int:
        Registers.set_bc((Registers.get_bc() + 1) & 0xffff )
        return 8

    def INC_B(self) -> int:
        Registers.b = self.inc_byte(Registers.b)
        return 4

    def DEC_B(self) -> int:
        Registers.b = self.dec_byte(Registers.b)
        return 4
    
    def LD_B_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        Registers.b = byte 
        return 8

    def RLCA(self) -> int:
        Registers.a = self.rlc(Registers.a)
        Registers.reset_z_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        return 4
    
    def LD_REF_a16_SP(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        self.mmu.write_word(word, Registers.sp)
        return 20

    def ADD_HL_BC(self) -> int:
        Registers.set_hl(self.add_word(Registers.get_hl(), Registers.get_bc()))
        return 8
    
    def LD_A_REF_BC(self) -> int:
        Registers.a = self.mmu.read_byte(Registers.get_bc())
        return 8

    def DEC_BC(self) -> int:
        Registers.set_bc((Registers.get_bc() - 1) & 0xffff )
        return 8

    def INC_C(self) -> int:
        Registers.c = self.inc_byte(Registers.c)
        return 4

    def DEC_C(self) -> int:
        Registers.c = self.dec_byte(Registers.c)
        return 4
    
    def LD_C_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        Registers.c = byte 
        return 8

    def RRCA(self) -> int:
        Registers.a = self.rrc(Registers.a)
        Registers.reset_h_flag()
        Registers.reset_n_flag()
        Registers.reset_z_flag()
        return 4  

    def STOP(self) -> int:
        self.cpu.stop = True
        return 4       
    
    def LD_DE_d16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        Registers.set_de(word) 
        return 12
    
    def LD_REF_DE_A(self) -> int:
        self.mmu.write_byte(Registers.get_de(), Registers.a)
        return 8

    def INC_DE(self) -> int:
        Registers.set_de((Registers.get_de() + 1) & 0xffff )
        return 8

    def INC_D(self) -> int:
        Registers.d = self.inc_byte(Registers.d)
        return 4

    def DEC_D(self) -> int:
        Registers.d = self.dec_byte(Registers.d)
        return 4
    
    def LD_D_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        Registers.d = byte 
        return 8

    def RLA(self) -> int:
        Registers.a = self.rl(Registers.a)
        Registers.reset_z_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        return 4

    def JR_r8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        Registers.pc += signed_value(byte)
        return 12

    def ADD_HL_DE(self) -> int:
        Registers.set_hl(self.add_word(Registers.get_hl(), Registers.get_de()))
        return 8
    
    def LD_A_REF_DE(self) -> int:
        Registers.a = self.mmu.read_byte(Registers.get_de())
        return 8

    def DEC_DE(self) -> int:
        Registers.set_de((Registers.get_de() - 1) & 0xffff )
        return 8

    def INC_E(self) -> int:
        Registers.e = self.inc_byte(Registers.e)
        return 4

    def DEC_E(self) -> int:
        Registers.e = self.dec_byte(Registers.e)
        return 4
    
    def LD_E_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        Registers.e = byte 
        return 8

    def RRA(self) -> int:
        Registers.a = self.rr(Registers.a)
        Registers.reset_h_flag()
        Registers.reset_n_flag()
        Registers.reset_z_flag()
        return 4  

    def JR_NZ_r8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        if not Registers.is_z_flag():
            Registers.pc += signed_value(byte)
            return 12
        return 8
    
    def LD_HL_d16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        Registers.set_hl(word) 
        return 12
    
    def LDI_HL_A(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), Registers.a)
        Registers.set_hl(Registers.get_hl()+1)
        return 8

    def INC_HL(self) -> int:
        Registers.set_hl((Registers.get_hl() + 1) & 0xffff )
        return 8

    def INC_H(self) -> int:
        Registers.h = self.inc_byte(Registers.h)
        return 4

    def DEC_H(self) -> int:
        Registers.h = self.dec_byte(Registers.h)
        return 4
    
    def LD_H_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        Registers.h = byte 
        return 8

    def DAA(self) -> int:
        temp = Registers.a 
        if Registers.is_n_flag():
            if Registers.is_h_flag():
                temp = (temp - 0x06) & 0xff
            if Registers.is_c_flag():
                temp = (temp - 0x60) & 0xff
        else:
            if Registers.is_h_flag() or (temp & 0x0f) > 0x09:
                temp += 0x06
            if Registers.is_c_flag() or temp > 0x9f:
                temp += 0x60
        Registers.reset_h_flag()
        if temp > 0xff:
            Registers.set_c_flag()
        temp &= 0xff
        if temp == 0:
            Registers.set_z_flag()
        else:
            Registers.reset_z_flag()
        Registers.a = temp
        return 4

    def JR_Z_r8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        if Registers.is_z_flag():
            Registers.pc += signed_value(byte)
            return 12
        return 8

    def ADD_HL_HL(self) -> int:
        Registers.set_hl(self.add_word(Registers.get_hl(), Registers.get_hl()))
        return 8
    
    def LDI_A_HL(self) -> int:
        Registers.a = self.mmu.read_byte(Registers.get_hl())
        Registers.set_hl(Registers.get_hl()+1)
        return 8

    def DEC_HL(self) -> int:
        Registers.set_hl((Registers.get_hl() - 1) & 0xffff )
        return 8

    def INC_L(self) -> int:
        Registers.l = self.inc_byte(Registers.l)
        return 4

    def DEC_L(self) -> int:
        Registers.l = self.dec_byte(Registers.l)
        return 4
    
    def LD_L_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        Registers.l = byte 
        return 8

    def CPL(self) -> int:
        Registers.a = Registers.a ^ 0xff
        Registers.set_n_flag()
        Registers.set_h_flag()
        return 4

    def JR_NC_r8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        if not Registers.is_c_flag():
            Registers.pc += signed_value(byte)
            return 12
        return 8
    
    def LD_SP_d16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        Registers.sp = word
        return 12
    
    def LDD_HL_A(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), Registers.a)
        Registers.set_hl(Registers.get_hl()-1)
        return 8

    def INC_SP(self) -> int:
        Registers.sp = ((Registers.sp + 1) & 0xffff )
        return 8

    def INC_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(),self.inc_byte(self.mmu.read_byte(Registers.get_hl())))
        return 12

    def DEC_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.dec_byte(self.mmu.read_byte(Registers.get_hl())))
        return 12
    
    def LD_REF_HL_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        self.mmu.write_byte(Registers.get_hl(),byte)
        return 12

    def SCF(self) -> int:
        Registers.set_c_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        return 4

    def JR_C_r8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        if Registers.is_c_flag():
            Registers.pc += signed_value(byte)
            return 12
        return 8

    def ADD_HL_SP(self) -> int:
        Registers.set_hl(self.add_word(Registers.get_hl(), Registers.sp))
        return 8
    
    def LDD_A_HL(self) -> int:
        Registers.a = self.mmu.read_byte(Registers.get_hl())
        Registers.set_hl(Registers.get_hl()-1)
        return 8

    def DEC_SP(self) -> int:
        Registers.sp = ((Registers.sp - 1) & 0xffff )
        return 8

    def INC_A(self) -> int:
        Registers.a = self.inc_byte(Registers.a)
        return 4

    def DEC_A(self) -> int:
        Registers.a = self.dec_byte(Registers.a)
        return 4
    
    def LD_A_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        Registers.a = byte
        return 8

    def CCF(self) -> int:
        if Registers.is_c_flag():
            Registers.reset_c_flag()
        else:
            Registers.set_c_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        return 4
    
    def LD_B_B(self) -> int:
        return 4
    
    def LD_B_C(self) -> int:
        Registers.b = Registers.c
        return 4
    
    def LD_B_D(self) -> int:
        Registers.b = Registers.d
        return 4
    
    def LD_B_E(self) -> int:
        Registers.b = Registers.e
        return 4
    
    def LD_B_H(self) -> int:
        Registers.b = Registers.h
        return 4
    
    def LD_B_L(self) -> int:
        Registers.b = Registers.l
        return 4
    
    def LD_B_REF_HL(self) -> int:
        Registers.b = self.mmu.read_byte(Registers.get_hl())
        return 8
    
    def LD_B_A(self) -> int:
        Registers.b = Registers.a
        return 4
    
    def LD_C_B(self) -> int:
        Registers.c = Registers.b
        return 4
    
    def LD_C_C(self) -> int:
        return 4
    
    def LD_C_D(self) -> int:
        Registers.c = Registers.d
        return 4
    
    def LD_C_E(self) -> int:
        Registers.c = Registers.e
        return 4
    
    def LD_C_H(self) -> int:
        Registers.c = Registers.h
        return 4
    
    def LD_C_L(self) -> int:
        Registers.c = Registers.l
        return 4
    
    def LD_C_REF_HL(self) -> int:
        Registers.c = self.mmu.read_byte(Registers.get_hl())
        return 8
    
    def LD_C_A(self) -> int:
        Registers.c = Registers.a
        return 4
    
    def LD_D_B(self) -> int:
        Registers.d = Registers.b
        return 4
    
    def LD_D_C(self) -> int:
        Registers.d = Registers.c
        return 4
    
    def LD_D_D(self) -> int:
        return 4
    
    def LD_D_E(self) -> int:
        Registers.d = Registers.e
        return 4
    
    def LD_D_H(self) -> int:
        Registers.d = Registers.h
        return 4
    
    def LD_D_L(self) -> int:
        Registers.d = Registers.l
        return 4
    
    def LD_D_REF_HL(self) -> int:
        Registers.d = self.mmu.read_byte(Registers.get_hl())
        return 8
    
    def LD_D_A(self) -> int:
        Registers.d = Registers.a
        return 4
    
    def LD_E_B(self) -> int:
        Registers.e = Registers.b
        return 4
    
    def LD_E_C(self) -> int:
        Registers.e = Registers.c
        return 4
    
    def LD_E_D(self) -> int:
        Registers.e = Registers.d
        return 4
    
    def LD_E_E(self) -> int:
        return 4
    
    def LD_E_H(self) -> int:
        Registers.e = Registers.h
        return 4
    
    def LD_E_L(self) -> int:
        Registers.e = Registers.l
        return 4
    
    def LD_E_REF_HL(self) -> int:
        Registers.e = self.mmu.read_byte(Registers.get_hl())
        return 8
    
    def LD_E_A(self) -> int:
        Registers.e = Registers.a
        return 4
    
    def LD_H_B(self) -> int:
        Registers.h = Registers.b
        return 4
    
    def LD_H_C(self) -> int:
        Registers.h = Registers.c
        return 4
    
    def LD_H_D(self) -> int:
        Registers.h = Registers.d
        return 4
    
    def LD_H_E(self) -> int:
        Registers.h = Registers.e
        return 4
    
    def LD_H_H(self) -> int:
        return 4
    
    def LD_H_L(self) -> int:
        Registers.h = Registers.l
        return 4
    
    def LD_H_REF_HL(self) -> int:
        Registers.h = self.mmu.read_byte(Registers.get_hl())
        return 8
    
    def LD_H_A(self) -> int:
        Registers.h = Registers.a
        return 4
    
    def LD_L_B(self) -> int:
        Registers.l = Registers.b
        return 4
    
    def LD_L_C(self) -> int:
        Registers.l = Registers.c
        return 4
    
    def LD_L_D(self) -> int:
        Registers.l = Registers.d
        return 4
    
    def LD_L_E(self) -> int:
        Registers.l = Registers.e
        return 4
    
    def LD_L_H(self) -> int:
        Registers.l = Registers.h
        return 4
    
    def LD_L_L(self) -> int:
        return 4
    
    def LD_L_REF_HL(self) -> int:
        Registers.l = self.mmu.read_byte(Registers.get_hl())
        return 8
    
    def LD_L_A(self) -> int:
        Registers.l = Registers.a
        return 4
    
    def LD_REF_HL_B(self) -> int:
        self.mmu.write_byte(Registers.get_hl(),Registers.b)
        return 8
    
    def LD_REF_HL_C(self) -> int:
        self.mmu.write_byte(Registers.get_hl(),Registers.c)
        return 8
    
    def LD_REF_HL_D(self) -> int:
        self.mmu.write_byte(Registers.get_hl(),Registers.d)
        return 8
    
    def LD_REF_HL_E(self) -> int:
        self.mmu.write_byte(Registers.get_hl(),Registers.e)
        return 8
    
    def LD_REF_HL_H(self) -> int:
        self.mmu.write_byte(Registers.get_hl(),Registers.h)
        return 8
    
    def LD_REF_HL_L(self) -> int:
        self.mmu.write_byte(Registers.get_hl(),Registers.l)
        return 8

    def HALT(self) -> int:
        self.cpu.halted = True
        self.cpu.pending_interrupts_before_halt = self.mmu.read_byte(IO_Registers.IF)
        return 4
    
    def LD_REF_HL_A(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), Registers.a)
        return 8
    
    def LD_A_B(self) -> int:
        Registers.a = Registers.b
        return 4
    
    def LD_A_C(self) -> int:
        Registers.a = Registers.c
        return 4
    
    def LD_A_D(self) -> int:
        Registers.a = Registers.d
        return 4
    
    def LD_A_E(self) -> int:
        Registers.a = Registers.e
        return 4
    
    def LD_A_H(self) -> int:
        Registers.a = Registers.h
        return 4
    
    def LD_A_L(self) -> int:
        Registers.a = Registers.l
        return 4
    
    def LD_A_REF_HL(self) -> int:
        Registers.a = self.mmu.read_byte(Registers.get_hl())
        return 8
    
    def LD_A_A(self) -> int:
        return 4
    
    def ADD_B(self) -> int:
        self.add_byte(Registers.b)
        return 4
    
    def ADD_C(self) -> int:
        self.add_byte(Registers.c)
        return 4
    
    def ADD_D(self) -> int:
        self.add_byte(Registers.d)
        return 4
    
    def ADD_E(self) -> int:
        self.add_byte(Registers.e)
        return 4
    
    def ADD_H(self) -> int:
        self.add_byte(Registers.h)
        return 4
    
    def ADD_L(self) -> int:
        self.add_byte(Registers.l)
        return 4
    
    def ADD_REF_HL(self) -> int:
        byte = self.mmu.read_byte(Registers.get_hl())
        self.add_byte(byte)
        return 8
    
    def ADD_A(self) -> int:
        self.add_byte(Registers.a)
        return 4
    
    def ADC_B(self) -> int:
        self.adc(Registers.b)
        return 4
    
    def ADC_C(self) -> int:
        self.adc(Registers.c)
        return 4
    
    def ADC_D(self) -> int:
        self.adc(Registers.d)
        return 4
    
    def ADC_E(self) -> int:
        self.adc(Registers.e)
        return 4
    
    def ADC_H(self) -> int:
        self.adc(Registers.h)
        return 4
    
    def ADC_L(self) -> int:
        self.adc(Registers.l)
        return 4
    
    def ADC_REF_HL(self) -> int:
        byte = self.mmu.read_byte(Registers.get_hl())
        self.adc(byte)
        return 8
    
    def ADC_A(self) -> int:
        self.adc(Registers.a)
        return 4

    def SUB_B(self) -> int:
        self.sub(Registers.b)
        return 4

    def SUB_C(self) -> int:
        self.sub(Registers.c)
        return 4

    def SUB_D(self) -> int:
        self.sub(Registers.d)
        return 4

    def SUB_E(self) -> int:
        self.sub(Registers.e)
        return 4

    def SUB_H(self) -> int:
        self.sub(Registers.h)
        return 4

    def SUB_L(self) -> int:
        self.sub(Registers.l)
        return 4

    def SUB_REF_HL(self) -> int:
        self.sub(self.mmu.read_byte(Registers.get_hl()))
        return 8

    def SUB_A(self) -> int:
        self.sub(Registers.a)
        return 4

    def SBC_B(self) -> int:
        self.sbc(Registers.b)
        return 4

    def SBC_C(self) -> int:
        self.sbc(Registers.c)
        return 4

    def SBC_D(self) -> int:
        self.sbc(Registers.d)
        return 4

    def SBC_E(self) -> int:
        self.sbc(Registers.e)
        return 4

    def SBC_H(self) -> int:
        self.sbc(Registers.h)
        return 4

    def SBC_L(self) -> int:
        self.sbc(Registers.l)
        return 4

    def SBC_REF_HL(self) -> int:
        byte = self.mmu.read_byte(Registers.get_hl())
        self.sbc(byte)
        return 8

    def SBC_A(self) -> int:
        self.sbc(Registers.a)
        return 4

    def AND_B(self) -> int:
        self._and(Registers.b)
        return 4

    def AND_C(self) -> int:
        self._and(Registers.c)
        return 4

    def AND_D(self) -> int:
        self._and(Registers.d)
        return 4

    def AND_E(self) -> int:
        self._and(Registers.e)
        return 4

    def AND_H(self) -> int:
        self._and(Registers.h)
        return 4

    def AND_L(self) -> int:
        self._and(Registers.l)
        return 4

    def AND_REF_HL(self) -> int:
        byte = self.mmu.read_byte(Registers.get_hl())
        self._and(byte)
        return 8

    def AND_A(self) -> int:
        self._and(Registers.a)
        return 4

    def XOR_B(self) -> int:
        self.xor(Registers.b)
        return 4

    def XOR_C(self) -> int:
        self.xor(Registers.c)
        return 4

    def XOR_D(self) -> int:
        self.xor(Registers.d)
        return 4

    def XOR_E(self) -> int:
        self.xor(Registers.e)
        return 4

    def XOR_H(self) -> int:
        self.xor(Registers.h)
        return 4

    def XOR_L(self) -> int:
        self.xor(Registers.l)
        return 4

    def XOR_REF_HL(self) -> int:
        byte = self.mmu.read_byte(Registers.get_hl())
        self.xor(byte)
        return 8

    def XOR_A(self) -> int:
        self.xor(Registers.a)
        return 4

    def OR_B(self) -> int:
        self._or(Registers.b)
        return 4

    def OR_C(self) -> int:
        self._or(Registers.c)
        return 4

    def OR_D(self) -> int:
        self._or(Registers.d)
        return 4

    def OR_E(self) -> int:
        self._or(Registers.e)
        return 4

    def OR_H(self) -> int:
        self._or(Registers.h)
        return 4

    def OR_L(self) -> int:
        self._or(Registers.l)
        return 4

    def OR_REF_HL(self) -> int:
        byte = self.mmu.read_byte(Registers.get_hl())
        self._or(byte)
        return 8

    def OR_A(self) -> int:
        self._or(Registers.a)
        return 4

    def CP_B(self) -> int:
        self.cp(Registers.b)
        return 4

    def CP_C(self) -> int:
        self.cp(Registers.c)
        return 4

    def CP_D(self) -> int:
        self.cp(Registers.d)
        return 4

    def CP_E(self) -> int:
        self.cp(Registers.e)
        return 4

    def CP_H(self) -> int:
        self.cp(Registers.h)
        return 4

    def CP_L(self) -> int:
        self.cp(Registers.l)
        return 4

    def CP_REF_HL(self) -> int:
        byte = self.mmu.read_byte(Registers.get_hl())
        self.cp(byte)
        return 8

    def CP_A(self) -> int:
        self.cp(Registers.a)
        return 4

    def RET_NZ(self) -> int:
        if not Registers.is_z_flag():
            Registers.pc = self.stackManager.pop_word()
            return 20
        return 8
    
    def POP_BC(self) -> int:
        Registers.set_bc(self.stackManager.pop_word())
        return 12

    def JP_NZ_a16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        if not Registers.is_z_flag():
            Registers.pc = word
            return 16
        return 12

    def JP_a16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc = word
        return 16

    def CALL_NZ_a16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        if not Registers.is_z_flag():
            self.stackManager.push_word(Registers.pc)
            Registers.pc = word
            return 24
        return 12
    
    def PUSH_BC(self) -> int:
        self.stackManager.push_word(Registers.get_bc())
        return 16
    
    def ADD_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        self.add_byte(byte)
        return 8

    def RST_00H(self) -> int:
        self.stackManager.push_word(Registers.pc)
        Registers.pc = 0x00
        return 16

    def RET_Z(self) -> int:
        if Registers.is_z_flag():
            Registers.pc = self.stackManager.pop_word()
            return 20
        return 8

    def RET(self) -> int:
        Registers.pc = self.stackManager.pop_word()
        return 16

    def JP_Z_a16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        if Registers.is_z_flag():
            Registers.pc = word
            return 16
        return 12

    def CALL_Z_a16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        if Registers.is_z_flag():
            self.stackManager.push_word(Registers.pc)
            Registers.pc = word
            return 24
        return 12

    def CALL_a16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        self.stackManager.push_word(Registers.pc)
        Registers.pc = word
        return 24
    
    def ADC_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        self.adc(byte)
        return 8

    def RST_08H(self) -> int:
        self.stackManager.push_word(Registers.pc)
        Registers.pc = 0x08
        return 16

    def RET_NC(self) -> int:
        if not Registers.is_c_flag():
            Registers.pc = self.stackManager.pop_word()
            return 20
        return 8
    
    def POP_DE(self) -> int:
        Registers.set_de(self.stackManager.pop_word())
        return 12

    def JP_NC_a16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        if not Registers.is_c_flag():
            Registers.pc = word
            return 16
        return 12

    def CALL_NC_a16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        if not Registers.is_c_flag():
            self.stackManager.push_word(Registers.pc)
            Registers.pc = word
            return 24
        return 12
    
    def PUSH_DE(self) -> int:
        self.stackManager.push_word(Registers.get_de())
        return 16

    def SUB_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        self.sub(byte)
        return 8

    def RST_10H(self) -> int:
        self.stackManager.push_word(Registers.pc)
        Registers.pc = 0x10
        return 16

    def RET_C(self) -> int:
        if Registers.is_c_flag():
            Registers.pc = self.stackManager.pop_word()
            return 20
        return 8

    def RETI(self) -> int:
        Registers.pc = self.stackManager.pop_word()
        self.cpu.ime = True
        return 16

    def JP_C_a16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        if Registers.is_c_flag():
            Registers.pc = word
            return 16
        return 12

    def CALL_C_a16(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        if Registers.is_c_flag():
            self.stackManager.push_word(Registers.pc)
            Registers.pc = word
            return 24
        return 12

    def SBC_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        self.sbc(byte)
        return 8

    def RST_18H(self) -> int:
        self.stackManager.push_word(Registers.pc)
        Registers.pc = 0x18
        return 16

    def LDH_REF_a8_A(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        self.mmu.write_byte((byte + 0xff00), Registers.a)
        return 12
    
    def POP_HL(self) -> int:
        Registers.set_hl(self.stackManager.pop_word())
        return 12

    def LD_REF_C_A(self) -> int:
        self.mmu.write_byte((Registers.c + 0xff00), Registers.a)
        return 8
    
    def PUSH_HL(self) -> int:
        self.stackManager.push_word(Registers.get_hl())
        return 16

    def AND_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        self._and(byte)
        return 8

    def RST_20H(self) -> int:
        self.stackManager.push_word(Registers.pc)
        Registers.pc = 0x20
        return 16

    def ADD_SP_r8(self) -> int:
        byte = signed_value(self.mmu.read_byte(Registers.pc))
        temp = Registers.sp + byte
        Registers.pc += 1
        Registers.reset_z_flag()
        Registers.reset_n_flag()
        if ( Registers.sp ^ byte ^ temp ) & 0x100 == 0x100:
            Registers.set_c_flag()
        else:
            Registers.reset_c_flag()
        if ( Registers.sp ^ byte ^ temp ) & 0x10 == 0x10:
            Registers.set_h_flag()
        else:
            Registers.reset_h_flag()
        Registers.sp = temp
        return 16

    def JP_HL(self) -> int:
        word = Registers.get_hl()
        Registers.pc = word
        return 4
    
    def LD_REF_a16_A(self) -> int:
        word = self.mmu.read_word(Registers.pc)
        Registers.pc += 2
        self.mmu.write_byte(word, Registers.a)
        return 16

    def XOR_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        self.xor(byte)
        return 8

    def RST_28H(self) -> int:
        self.stackManager.push_word(Registers.pc)
        Registers.pc = 0x28
        return 16
    
    def LDH_A_REF_a8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        Registers.a = self.mmu.read_byte((byte + 0xff00))
        return 12
    
    def POP_AF(self) -> int:
        Registers.set_af(self.stackManager.pop_word())
        return 12
    
    def LD_A_REF_C(self) -> int:
        Registers.a = self.mmu.read_byte(Registers.c + 0xff00)
        return 8

    def DI(self) -> int:
        self.cpu.ime = False
        return 4
    
    def PUSH_AF(self) -> int:
        self.stackManager.push_word(Registers.get_af())
        return 16

    def OR_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        self._or(byte)
        return 8

    def RST_30H(self) -> int:
        self.stackManager.push_word(Registers.pc)
        Registers.pc = 0x30
        return 16
    
    def LD_HL_SP_r8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        hl = Registers.sp + signed_value(byte)
        Registers.reset_z_flag()
        Registers.reset_n_flag()
        if (Registers.sp ^ signed_value(byte) ^ hl) & 0x100 == 0x100:
            Registers.set_c_flag()
        else: 
            Registers.reset_c_flag()
        if (Registers.sp ^ signed_value(byte) ^ hl) & 0x10 == 0x10:
            Registers.set_h_flag()
        else: 
            Registers.reset_h_flag()
        Registers.set_hl(hl)
        return 12
    
    def LD_SP_HL(self) -> int:
        Registers.sp = Registers.get_hl()
        return 8
    
    def LD_A_a16(self) -> int:
        byte = self.mmu.read_byte(self.mmu.read_word(Registers.pc))
        Registers.pc += 2
        Registers.a = byte
        return 16

    def EI(self) -> int:
        self.cpu.ime = True
        return 4

    def CP_d8(self) -> int:
        byte = self.mmu.read_byte(Registers.pc)
        Registers.pc += 1
        self.cp(byte)
        return 8

    def RST_38H(self) -> int:
        self.stackManager.push_word(Registers.pc)
        Registers.pc = 0x38
        return 16

    def RLC_B(self) -> int:
        Registers.b = self.rlc(Registers.b)
        return 8

    def RLC_C(self) -> int:
        Registers.c = self.rlc(Registers.c)
        return 8

    def RLC_D(self) -> int:
        Registers.d = self.rlc(Registers.d)
        return 8

    def RLC_E(self) -> int:
        Registers.e = self.rlc(Registers.e)
        return 8

    def RLC_H(self) -> int:
        Registers.h = self.rlc(Registers.h)
        return 8

    def RLC_L(self) -> int:
        Registers.l = self.rlc(Registers.l)
        return 8

    def RLC_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.rlc(self.mmu.read_byte(Registers.get_hl())))
        return 16

    def RLC_A(self) -> int:
        Registers.a = self.rlc(Registers.a)
        return 8

    def RRC_B(self) -> int:
        Registers.b = self.rrc(Registers.b)
        return 8

    def RRC_C(self) -> int:
        Registers.c = self.rrc(Registers.c)
        return 8

    def RRC_D(self) -> int:
        Registers.d = self.rrc(Registers.d)
        return 8

    def RRC_E(self) -> int:
        Registers.e = self.rrc(Registers.e)
        return 8

    def RRC_H(self) -> int:
        Registers.h = self.rrc(Registers.h)
        return 8

    def RRC_L(self) -> int:
        Registers.l = self.rrc(Registers.l)
        return 8

    def RRC_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.rrc(self.mmu.read_byte(Registers.get_hl())))
        return 16

    def RRC_A(self) -> int:
        Registers.a = self.rrc(Registers.a)
        return 8

    def RL_B(self) -> int:
        Registers.b = self.rl(Registers.b)
        return 8

    def RL_C(self) -> int:
        Registers.c = self.rl(Registers.c)
        return 8

    def RL_D(self) -> int:
        Registers.d = self.rl(Registers.d)
        return 8

    def RL_E(self) -> int:
        Registers.e = self.rl(Registers.e)
        return 8

    def RL_H(self) -> int:
        Registers.h = self.rl(Registers.h)
        return 8

    def RL_L(self) -> int:
        Registers.l = self.rl(Registers.l)
        return 8

    def RL_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.rl(self.mmu.read_byte(Registers.get_hl())))
        return 16

    def RL_A(self) -> int:
        Registers.a = self.rl(Registers.a)
        return 8

    def RR_B(self) -> int:
        Registers.b = self.rr(Registers.b)
        return 8

    def RR_C(self) -> int:
        Registers.c = self.rr(Registers.c)
        return 8

    def RR_D(self) -> int:
        Registers.d = self.rr(Registers.d)
        return 8

    def RR_E(self) -> int:
        Registers.e = self.rr(Registers.e)
        return 8

    def RR_H(self) -> int:
        Registers.h = self.rr(Registers.h)
        return 8

    def RR_L(self) -> int:
        Registers.l = self.rr(Registers.l)
        return 8

    def RR_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.rr(self.mmu.read_byte(Registers.get_hl())))
        return 16

    def RR_A(self) -> int:
        Registers.a = self.rr(Registers.a)
        return 8

    def SLA_B(self) -> int:
        Registers.b = self.sla(Registers.b)
        return 8

    def SLA_C(self) -> int:
        Registers.c = self.sla(Registers.c)
        return 8

    def SLA_D(self) -> int:
        Registers.d = self.sla(Registers.d)
        return 8

    def SLA_E(self) -> int:
        Registers.e = self.sla(Registers.e)
        return 8

    def SLA_H(self) -> int:
        Registers.h = self.sla(Registers.h)
        return 8

    def SLA_L(self) -> int:
        Registers.l = self.sla(Registers.l)
        return 8

    def SLA_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.sla(self.mmu.read_byte(Registers.get_hl())))
        return 16

    def SLA_A(self) -> int:
        Registers.a = self.sla(Registers.a)
        return 8

    def SRA_B(self) -> int:
        Registers.b = self.sra(Registers.b)
        return 8

    def SRA_C(self) -> int:
        Registers.c = self.sra(Registers.c)
        return 8

    def SRA_D(self) -> int:
        Registers.d = self.sra(Registers.d)
        return 8

    def SRA_E(self) -> int:
        Registers.e = self.sra(Registers.e)
        return 8

    def SRA_H(self) -> int:
        Registers.h = self.sra(Registers.h)
        return 8

    def SRA_L(self) -> int:
        Registers.l = self.sra(Registers.l)
        return 8

    def SRA_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.sra(self.mmu.read_byte(Registers.get_hl())))
        return 16

    def SRA_A(self) -> int:
        Registers.a = self.sra(Registers.a)
        return 8

    def SWAP_B(self) -> int:
        Registers.b = self.swap(Registers.b)
        return 8

    def SWAP_C(self) -> int:
        Registers.c = self.swap(Registers.c)
        return 8

    def SWAP_D(self) -> int:
        Registers.d = self.swap(Registers.d)
        return 8

    def SWAP_E(self) -> int:
        Registers.e = self.swap(Registers.e)
        return 8

    def SWAP_H(self) -> int:
        Registers.h = self.swap(Registers.h)
        return 8

    def SWAP_L(self) -> int:
        Registers.l = self.swap(Registers.l)
        return 8

    def SWAP_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.swap(self.mmu.read_byte(Registers.get_hl())))
        return 16

    def SWAP_A(self) -> int:
        Registers.a = self.swap(Registers.a)
        return 8

    def SRL_B(self) -> int:
        Registers.b = self.srl(Registers.b)
        return 8

    def SRL_C(self) -> int:
        Registers.c = self.srl(Registers.c)
        return 8

    def SRL_D(self) -> int:
        Registers.d = self.srl(Registers.d)
        return 8

    def SRL_E(self) -> int:
        Registers.e = self.srl(Registers.e)
        return 8

    def SRL_H(self) -> int:
        Registers.h = self.srl(Registers.h)
        return 8

    def SRL_L(self) -> int:
        Registers.l = self.srl(Registers.l)
        return 8

    def SRL_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.srl(self.mmu.read_byte(Registers.get_hl())))
        return 16

    def SRL_A(self) -> int:
        Registers.a = self.srl(Registers.a)
        return 8

    def BIT_0_B(self) -> int:
        self.bit(0, Registers.b)
        return 8

    def BIT_0_C(self) -> int:
        self.bit(0, Registers.c)
        return 8

    def BIT_0_D(self) -> int:
        self.bit(0, Registers.d)
        return 8

    def BIT_0_E(self) -> int:
        self.bit(0, Registers.e)
        return 8

    def BIT_0_H(self) -> int:
        self.bit(0, Registers.h)
        return 8

    def BIT_0_L(self) -> int:
        self.bit(0, Registers.l)
        return 8

    def BIT_0_REF_HL(self) -> int:
        self.bit(0, self.mmu.read_byte(Registers.get_hl()))
        return 12

    def BIT_0_A(self) -> int:
        self.bit(0, Registers.a)
        return 8

    def BIT_1_B(self) -> int:
        self.bit(1, Registers.b)
        return 8

    def BIT_1_C(self) -> int:
        self.bit(1, Registers.c)
        return 8

    def BIT_1_D(self) -> int:
        self.bit(1, Registers.d)
        return 8

    def BIT_1_E(self) -> int:
        self.bit(1, Registers.e)
        return 8

    def BIT_1_H(self) -> int:
        self.bit(1, Registers.h)
        return 8

    def BIT_1_L(self) -> int:
        self.bit(1, Registers.l)
        return 8

    def BIT_1_REF_HL(self) -> int:
        self.bit(1, self.mmu.read_byte(Registers.get_hl()))
        return 12

    def BIT_1_A(self) -> int:
        self.bit(1, Registers.a)
        return 8

    def BIT_2_B(self) -> int:
        self.bit(2, Registers.b)
        return 8

    def BIT_2_C(self) -> int:
        self.bit(2, Registers.c)
        return 8

    def BIT_2_D(self) -> int:
        self.bit(2, Registers.d)
        return 8

    def BIT_2_E(self) -> int:
        self.bit(2, Registers.e)
        return 8

    def BIT_2_H(self) -> int:
        self.bit(2, Registers.h)
        return 8

    def BIT_2_L(self) -> int:
        self.bit(2, Registers.l)
        return 8

    def BIT_2_REF_HL(self) -> int:
        self.bit(2, self.mmu.read_byte(Registers.get_hl()))
        return 12

    def BIT_2_A(self) -> int:
        self.bit(2, Registers.a)
        return 8

    def BIT_3_B(self) -> int:
        self.bit(3, Registers.b)
        return 8

    def BIT_3_C(self) -> int:
        self.bit(3, Registers.c)
        return 8

    def BIT_3_D(self) -> int:
        self.bit(3, Registers.d)
        return 8

    def BIT_3_E(self) -> int:
        self.bit(3, Registers.e)
        return 8

    def BIT_3_H(self) -> int:
        self.bit(3, Registers.h)
        return 8

    def BIT_3_L(self) -> int:
        self.bit(3, Registers.l)
        return 8

    def BIT_3_REF_HL(self) -> int:
        self.bit(3, self.mmu.read_byte(Registers.get_hl()))
        return 12

    def BIT_3_A(self) -> int:
        self.bit(3, Registers.a)
        return 8

    def BIT_4_B(self) -> int:
        self.bit(4, Registers.b)
        return 8

    def BIT_4_C(self) -> int:
        self.bit(4, Registers.c)
        return 8

    def BIT_4_D(self) -> int:
        self.bit(4, Registers.d)
        return 8

    def BIT_4_E(self) -> int:
        self.bit(4, Registers.e)
        return 8

    def BIT_4_H(self) -> int:
        self.bit(4, Registers.h)
        return 8

    def BIT_4_L(self) -> int:
        self.bit(4, Registers.l)
        return 8

    def BIT_4_REF_HL(self) -> int:
        self.bit(4, self.mmu.read_byte(Registers.get_hl()))
        return 12

    def BIT_4_A(self) -> int:
        self.bit(4, Registers.a)
        return 8

    def BIT_5_B(self) -> int:
        self.bit(5, Registers.b)
        return 8

    def BIT_5_C(self) -> int:
        self.bit(5, Registers.c)
        return 8

    def BIT_5_D(self) -> int:
        self.bit(5, Registers.d)
        return 8

    def BIT_5_E(self) -> int:
        self.bit(5, Registers.e)
        return 8

    def BIT_5_H(self) -> int:
        self.bit(5, Registers.h)
        return 8

    def BIT_5_L(self) -> int:
        self.bit(5, Registers.l)
        return 8

    def BIT_5_REF_HL(self) -> int:
        self.bit(5, self.mmu.read_byte(Registers.get_hl()))
        return 12

    def BIT_5_A(self) -> int:
        self.bit(5, Registers.a)
        return 8

    def BIT_6_B(self) -> int:
        self.bit(6, Registers.b)
        return 8

    def BIT_6_C(self) -> int:
        self.bit(6, Registers.c)
        return 8

    def BIT_6_D(self) -> int:
        self.bit(6, Registers.d)
        return 8

    def BIT_6_E(self) -> int:
        self.bit(6, Registers.e)
        return 8

    def BIT_6_H(self) -> int:
        self.bit(6, Registers.h)
        return 8

    def BIT_6_L(self) -> int:
        self.bit(6, Registers.l)
        return 8

    def BIT_6_REF_HL(self) -> int:
        self.bit(6, self.mmu.read_byte(Registers.get_hl()))
        return 12

    def BIT_6_A(self) -> int:
        self.bit(6, Registers.a)
        return 8

    def BIT_7_B(self) -> int:
        self.bit(7, Registers.b)
        return 8

    def BIT_7_C(self) -> int:
        self.bit(7, Registers.c)
        return 8

    def BIT_7_D(self) -> int:
        self.bit(7, Registers.d)
        return 8

    def BIT_7_E(self) -> int:
        self.bit(7, Registers.e)
        return 8

    def BIT_7_H(self) -> int:
        self.bit(7, Registers.h)
        return 8

    def BIT_7_L(self) -> int:
        self.bit(7, Registers.l)
        return 8

    def BIT_7_REF_HL(self) -> int:
        self.bit(7, self.mmu.read_byte(Registers.get_hl()))
        return 12

    def BIT_7_A(self) -> int:
        self.bit(7, Registers.a)
        return 8

    def RES_0_B(self) -> int:
        Registers.b = self.res(0, Registers.b)
        return 8

    def RES_0_C(self) -> int:
        Registers.c = self.res(0, Registers.c)
        return 8

    def RES_0_D(self) -> int:
        Registers.d = self.res(0, Registers.d)
        return 8

    def RES_0_E(self) -> int:
        Registers.e = self.res(0, Registers.e)
        return 8

    def RES_0_H(self) -> int:
        Registers.h = self.res(0, Registers.h)
        return 8

    def RES_0_L(self) -> int:
        Registers.l = self.res(0, Registers.l)
        return 8

    def RES_0_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.res(0, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def RES_0_A(self) -> int:
        Registers.a = self.res(0, Registers.a)
        return 8

    def RES_1_B(self) -> int:
        Registers.b = self.res(1, Registers.b)
        return 8

    def RES_1_C(self) -> int:
        Registers.c = self.res(1, Registers.c)
        return 8

    def RES_1_D(self) -> int:
        Registers.d = self.res(1, Registers.d)
        return 8

    def RES_1_E(self) -> int:
        Registers.e = self.res(1, Registers.e)
        return 8

    def RES_1_H(self) -> int:
        Registers.h = self.res(1, Registers.h)
        return 8

    def RES_1_L(self) -> int:
        Registers.l = self.res(1, Registers.l)
        return 8

    def RES_1_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.res(1, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def RES_1_A(self) -> int:
        Registers.a = self.res(1, Registers.a)
        return 8

    def RES_2_B(self) -> int:
        Registers.b = self.res(2, Registers.b)
        return 8

    def RES_2_C(self) -> int:
        Registers.c = self.res(2, Registers.c)
        return 8

    def RES_2_D(self) -> int:
        Registers.d = self.res(2, Registers.d)
        return 8

    def RES_2_E(self) -> int:
        Registers.e = self.res(2, Registers.e)
        return 8

    def RES_2_H(self) -> int:
        Registers.h = self.res(2, Registers.h)
        return 8

    def RES_2_L(self) -> int:
        Registers.l = self.res(2, Registers.l)
        return 8

    def RES_2_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.res(2, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def RES_2_A(self) -> int:
        Registers.a = self.res(2, Registers.a)
        return 8

    def RES_3_B(self) -> int:
        Registers.b = self.res(3, Registers.b)
        return 8

    def RES_3_C(self) -> int:
        Registers.c = self.res(3, Registers.c)
        return 8

    def RES_3_D(self) -> int:
        Registers.d = self.res(3, Registers.d)
        return 8

    def RES_3_E(self) -> int:
        Registers.e = self.res(3, Registers.e)
        return 8

    def RES_3_H(self) -> int:
        Registers.h = self.res(3, Registers.h)
        return 8

    def RES_3_L(self) -> int:
        Registers.l = self.res(3, Registers.l)
        return 8

    def RES_3_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.res(3, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def RES_3_A(self) -> int:
        Registers.a = self.res(3, Registers.a)
        return 8

    def RES_4_B(self) -> int:
        Registers.b = self.res(4, Registers.b)
        return 8

    def RES_4_C(self) -> int:
        Registers.c = self.res(4, Registers.c)
        return 8

    def RES_4_D(self) -> int:
        Registers.d = self.res(4, Registers.d)
        return 8

    def RES_4_E(self) -> int:
        Registers.e = self.res(4, Registers.e)
        return 8

    def RES_4_H(self) -> int:
        Registers.h = self.res(4, Registers.h)
        return 8

    def RES_4_L(self) -> int:
        Registers.l = self.res(4, Registers.l)
        return 8

    def RES_4_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.res(4, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def RES_4_A(self) -> int:
        Registers.a = self.res(4, Registers.a)
        return 8

    def RES_5_B(self) -> int:
        Registers.b = self.res(5, Registers.b)
        return 8

    def RES_5_C(self) -> int:
        Registers.c = self.res(5, Registers.c)
        return 8

    def RES_5_D(self) -> int:
        Registers.d = self.res(5, Registers.d)
        return 8

    def RES_5_E(self) -> int:
        Registers.e = self.res(5, Registers.e)
        return 8

    def RES_5_H(self) -> int:
        Registers.h = self.res(5, Registers.h)
        return 8

    def RES_5_L(self) -> int:
        Registers.l = self.res(5, Registers.l)
        return 8

    def RES_5_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.res(5, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def RES_5_A(self) -> int:
        Registers.a = self.res(5, Registers.a)
        return 8

    def RES_6_B(self) -> int:
        Registers.b = self.res(6, Registers.b)
        return 8

    def RES_6_C(self) -> int:
        Registers.c = self.res(6, Registers.c)
        return 8

    def RES_6_D(self) -> int:
        Registers.d = self.res(6, Registers.d)
        return 8

    def RES_6_E(self) -> int:
        Registers.e = self.res(6, Registers.e)
        return 8

    def RES_6_H(self) -> int:
        Registers.h = self.res(6, Registers.h)
        return 8

    def RES_6_L(self) -> int:
        Registers.l = self.res(6, Registers.l)
        return 8

    def RES_6_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.res(6, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def RES_6_A(self) -> int:
        Registers.a = self.res(6, Registers.a)
        return 8

    def RES_7_B(self) -> int:
        Registers.b = self.res(7, Registers.b)
        return 8

    def RES_7_C(self) -> int:
        Registers.c = self.res(7, Registers.c)
        return 8

    def RES_7_D(self) -> int:
        Registers.d = self.res(7, Registers.d)
        return 8

    def RES_7_E(self) -> int:
        Registers.e = self.res(7, Registers.e)
        return 8

    def RES_7_H(self) -> int:
        Registers.h = self.res(7, Registers.h)
        return 8

    def RES_7_L(self) -> int:
        Registers.l = self.res(7, Registers.l)
        return 8

    def RES_7_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), self.res(7, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def RES_7_A(self) -> int:
        Registers.a = self.res(7, Registers.a)
        return 8

    def SET_0_B(self) -> int:
        Registers.b = set_bit(0, Registers.b)
        return 8

    def SET_0_C(self) -> int:
        Registers.c = set_bit(0, Registers.c)
        return 8

    def SET_0_D(self) -> int:
        Registers.d = set_bit(0, Registers.d)
        return 8

    def SET_0_E(self) -> int:
        Registers.e = set_bit(0, Registers.e)
        return 8

    def SET_0_H(self) -> int:
        Registers.h = set_bit(0, Registers.h)
        return 8

    def SET_0_L(self) -> int:
        Registers.l = set_bit(0, Registers.l)
        return 8

    def SET_0_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), set_bit(0, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def SET_0_A(self) -> int:
        Registers.a = set_bit(0, Registers.a)
        return 8

    def SET_1_B(self) -> int:
        Registers.b = set_bit(1, Registers.b)
        return 8

    def SET_1_C(self) -> int:
        Registers.c = set_bit(1, Registers.c)
        return 8

    def SET_1_D(self) -> int:
        Registers.d = set_bit(1, Registers.d)
        return 8

    def SET_1_E(self) -> int:
        Registers.e = set_bit(1, Registers.e)
        return 8

    def SET_1_H(self) -> int:
        Registers.h = set_bit(1, Registers.h)
        return 8

    def SET_1_L(self) -> int:
        Registers.l = set_bit(1, Registers.l)
        return 8

    def SET_1_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), set_bit(1, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def SET_1_A(self) -> int:
        Registers.a = set_bit(1, Registers.a)
        return 8

    def SET_2_B(self) -> int:
        Registers.b = set_bit(2, Registers.b)
        return 8

    def SET_2_C(self) -> int:
        Registers.c = set_bit(2, Registers.c)
        return 8

    def SET_2_D(self) -> int:
        Registers.d = set_bit(2, Registers.d)
        return 8

    def SET_2_E(self) -> int:
        Registers.e = set_bit(2, Registers.e)
        return 8

    def SET_2_H(self) -> int:
        Registers.h = set_bit(2, Registers.h)
        return 8

    def SET_2_L(self) -> int:
        Registers.l = set_bit(2, Registers.l)
        return 8

    def SET_2_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), set_bit(2, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def SET_2_A(self) -> int:
        Registers.a = set_bit(2, Registers.a)
        return 8

    def SET_3_B(self) -> int:
        Registers.b = set_bit(3, Registers.b)
        return 8

    def SET_3_C(self) -> int:
        Registers.c = set_bit(3, Registers.c)
        return 8

    def SET_3_D(self) -> int:
        Registers.d = set_bit(3, Registers.d)
        return 8

    def SET_3_E(self) -> int:
        Registers.e = set_bit(3, Registers.e)
        return 8

    def SET_3_H(self) -> int:
        Registers.h = set_bit(3, Registers.h)
        return 8

    def SET_3_L(self) -> int:
        Registers.l = set_bit(3, Registers.l)
        return 8

    def SET_3_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), set_bit(3, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def SET_3_A(self) -> int:
        Registers.a = set_bit(3, Registers.a)
        return 8

    def SET_4_B(self) -> int:
        Registers.b = set_bit(4, Registers.b)
        return 8

    def SET_4_C(self) -> int:
        Registers.c = set_bit(4, Registers.c)
        return 8

    def SET_4_D(self) -> int:
        Registers.d = set_bit(4, Registers.d)
        return 8

    def SET_4_E(self) -> int:
        Registers.e = set_bit(4, Registers.e)
        return 8

    def SET_4_H(self) -> int:
        Registers.h = set_bit(4, Registers.h)
        return 8

    def SET_4_L(self) -> int:
        Registers.l = set_bit(4, Registers.l)
        return 8

    def SET_4_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), set_bit(4, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def SET_4_A(self) -> int:
        Registers.a = set_bit(4, Registers.a)
        return 8

    def SET_5_B(self) -> int:
        Registers.b = set_bit(5, Registers.b)
        return 8

    def SET_5_C(self) -> int:
        Registers.c = set_bit(5, Registers.c)
        return 8

    def SET_5_D(self) -> int:
        Registers.d = set_bit(5, Registers.d)
        return 8

    def SET_5_E(self) -> int:
        Registers.e = set_bit(5, Registers.e)
        return 8

    def SET_5_H(self) -> int:
        Registers.h = set_bit(5, Registers.h)
        return 8

    def SET_5_L(self) -> int:
        Registers.l = set_bit(5, Registers.l)
        return 8

    def SET_5_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), set_bit(5, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def SET_5_A(self) -> int:
        Registers.a = set_bit(5, Registers.a)
        return 8

    def SET_6_B(self) -> int:
        Registers.b = set_bit(6, Registers.b)
        return 8

    def SET_6_C(self) -> int:
        Registers.c = set_bit(6, Registers.c)
        return 8

    def SET_6_D(self) -> int:
        Registers.d = set_bit(6, Registers.d)
        return 8

    def SET_6_E(self) -> int:
        Registers.e = set_bit(6, Registers.e)
        return 8

    def SET_6_H(self) -> int:
        Registers.h = set_bit(6, Registers.h)
        return 8

    def SET_6_L(self) -> int:
        Registers.l = set_bit(6, Registers.l)
        return 8

    def SET_6_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), set_bit(6, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def SET_6_A(self) -> int:
        Registers.a = set_bit(6, Registers.a)
        return 8

    def SET_7_B(self) -> int:
        Registers.b = set_bit(7, Registers.b)
        return 8

    def SET_7_C(self) -> int:
        Registers.c = set_bit(7, Registers.c)
        return 8

    def SET_7_D(self) -> int:
        Registers.d = set_bit(7, Registers.d)
        return 8

    def SET_7_E(self) -> int:
        Registers.e = set_bit(7, Registers.e)
        return 8

    def SET_7_H(self) -> int:
        Registers.h = set_bit(7, Registers.h)
        return 8

    def SET_7_L(self) -> int:
        Registers.l = set_bit(7, Registers.l)
        return 8

    def SET_7_REF_HL(self) -> int:
        self.mmu.write_byte(Registers.get_hl(), set_bit(7, self.mmu.read_byte(Registers.get_hl())))
        return 16

    def SET_7_A(self) -> int:
        Registers.a = set_bit(7, Registers.a)
        return 8
    
    def add_byte(self, value : int) -> int:
        byte = Registers.a + value
        if (byte & 0xff) == 0x00:
            Registers.set_z_flag()
        else:
                Registers.reset_z_flag()
        if (Registers.a ^ value ^ byte) & 0x100 == 0x100:
            Registers.set_c_flag()
        else: 
            Registers.reset_c_flag()
        if (Registers.a ^ value ^ byte) & 0x10 == 0x10: 
            Registers.set_h_flag() 
        else: 
            Registers.reset_h_flag()
        Registers.reset_n_flag()
        Registers.a = byte & 0xff

    def add_word(self, value1 : int, value2 : int) -> int:
        result = value1 + value2

        Registers.reset_n_flag()
        if result & 0x10000 == 0x10000: 
            Registers.set_c_flag() 
        else: 
            Registers.reset_c_flag()
        if (value1 ^ value2 ^ (result & 0xFFFF)) & 0x1000 == 0x1000: 
            Registers.set_h_flag() 
        else: 
            Registers.reset_h_flag()

        return result & 0xFFFF

    def adc(self, value : int) -> int:
        carry = 1 if Registers.is_c_flag() else 0
        result = Registers.a + value + carry
        if result & 0xff == 0x0: 
            Registers.set_z_flag()
        else: 
            Registers.reset_z_flag()
        if result > 0xff: 
            Registers.set_c_flag()
        else: 
            Registers.reset_c_flag()
        if (Registers.a & 0xf) + (value & 0xf) + carry > 0xf: 
            Registers.set_h_flag()
        else: 
            Registers.reset_h_flag()
        Registers.reset_n_flag()
        Registers.a = result & 0xff
        
    def sub(self, value : int) -> int:
        result = Registers.a - value
        if result & 0xff == 0x0:
            Registers.set_z_flag()
        else: 
            Registers.reset_z_flag()
        if (Registers.a ^ value ^ result) & 0x100 == 0x100:
            Registers.set_c_flag() 
        else: 
            Registers.reset_c_flag()
        if (Registers.a ^ value ^ result) & 0x10 == 0x10:
            Registers.set_h_flag() 
        else: 
            Registers.reset_h_flag()
        Registers.set_n_flag()
        Registers.a = result & 0xff

    def sbc(self, value : int) -> int:
        carry = 1 if Registers.is_c_flag() else 0
        result = Registers.a - value - carry
        if result & 0xff == 0x0:
            Registers.set_z_flag() 
        else: 
            Registers.reset_z_flag()
        if result < 0x0:
            Registers.set_c_flag() 
        else: 
            Registers.reset_c_flag()
        if (Registers.a & 0xF) - (value & 0xF) - carry < 0: 
            Registers.set_h_flag() 
        else: 
            Registers.reset_h_flag()
        Registers.set_n_flag()
        Registers.a = result & 0xff

    def _and(self, value: int) -> int:
        result = Registers.a & value
        if result & 0xff == 0x0:
            Registers.set_z_flag()
        else: 
            Registers.reset_z_flag()
        Registers.reset_c_flag()
        Registers.reset_n_flag()
        Registers.set_h_flag()
        Registers.a = result & 0xff

    def _or(self, value : int) -> int:
        result = Registers.a | value
        if result & 0xff == 0x0:
            Registers.set_z_flag()
        else: 
            Registers.reset_z_flag()
        Registers.reset_c_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        Registers.a = result & 0xff

    def xor(self, value: int) -> int:
        result = Registers.a ^ value
        if result & 0xff == 0x0:
            Registers.set_z_flag()
        else: 
            Registers.reset_z_flag()
        Registers.reset_c_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        Registers.a = result & 0xff

    def cp(self, value: int):
        result = Registers.a - value
        if result & 0xff == 0x0:
            Registers.set_z_flag()
        else: 
            Registers.reset_z_flag()
        if Registers.a < value:
            Registers.set_c_flag()
        else: 
            Registers.reset_c_flag()
        if (result & 0xf) > (Registers.a & 0xf):
            Registers.set_h_flag()
        else: 
            Registers.reset_h_flag()
        Registers.set_n_flag()

    def bit(self, pos : int, value : int) -> int:
        bit = 1 if value & bit_mask[pos] == bit_mask[pos] else 0
        if bit & 0xff == 0x0:
            Registers.set_z_flag() 
        else: 
            Registers.reset_z_flag()
        Registers.reset_n_flag()
        Registers.set_h_flag()

    def res(self, pos : int, value : int) -> int:
        return value & (bit_mask[pos] ^ 0xff)

    def swap(self, value : int) -> int:
        value = ((value << 4) & 0xff) | (value >> 4)
        if value & 0xff == 0x00:
            Registers.set_z_flag() 
        else: 
            Registers.reset_z_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        Registers.reset_c_flag()
        return value


    def inc_byte(self, value : int) -> int:
        result = value + 1
        if result & 0xff == 0x0:
            Registers.set_z_flag() 
        else: 
            Registers.reset_z_flag()
        if result & 0xf == 0x0:
            Registers.set_h_flag() 
        else: 
            Registers.reset_h_flag()
        Registers.reset_n_flag()
        return result & 0xff

    def dec_byte(self, value : int) -> int:
        result = value - 1
        if result & 0xff == 0x0:
            Registers.set_z_flag() 
        else: 
            Registers.reset_z_flag()
        if result & 0xf == 0xf:
            Registers.set_h_flag() 
        else: 
            Registers.reset_h_flag()
        Registers.set_n_flag()
        return result & 0xff

    def rl(self, value : int) -> int:
        carry = 1 if Registers.is_c_flag() else 0
        if value & 0x80 == 0x80:
            Registers.set_c_flag() 
        else: 
            Registers.reset_c_flag()
        result = ((value << 1) & 0xff) + carry
        if result & 0xFF == 0x0:
            Registers.set_z_flag() 
        else: 
            Registers.reset_z_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        return result

    def rlc(self, value : int) -> int:
        bit_out = 0x1 if value & 0x80 == 0x80 else 0x0
        if bit_out == 0x1:
            Registers.set_c_flag() 
        else: 
            Registers.reset_c_flag()
        if ((value << 1) & 0xff) + bit_out == 0x00:
            Registers.set_z_flag()
        else:
            Registers.reset_z_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        return ((value << 1) & 0xff) + bit_out

    def rr(self, value : int) -> int:
        carry = 0x80 if Registers.is_c_flag() else 0x0
        if value & 0x1 == 0x1:
            Registers.set_c_flag() 
        else: 
            Registers.reset_c_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        if (value >> 1) + carry == 0:
            Registers.set_z_flag()
        else:
            Registers.reset_z_flag()
        return (value >> 1) + carry

    def rrc(self, value : int) -> int:
        bit_out = 0x80 if value & 0x1 == 0x1 else 0x0
        if bit_out == 0x80:
            Registers.set_c_flag() 
        else: 
            Registers.reset_c_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        if (value >> 1) + bit_out == 0:
            Registers.set_z_flag()
        else:
            Registers.reset_z_flag()
        return (value >> 1) + bit_out

    def srl(self, value: int) -> int:
        if value & 0x01 == 0x01:
            Registers.set_c_flag()
        else:
            Registers.reset_c_flag()
        temp = value >> 1
        if temp == 0:
            Registers.set_z_flag()
        else:
            Registers.reset_z_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        return temp & 0xff

    def sra(self, value: int) -> int:
        if value & 0x01 == 0x01:
            Registers.set_c_flag()
        else:
            Registers.reset_c_flag()
        temp = ( value >> 1 ) | ( value & 0x80 )
        if temp == 0:
            Registers.set_z_flag()
        else:
            Registers.reset_z_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        return temp & 0xff

    def sla(self, value: int) -> int:
        if value & 0x80 == 0x80:
            Registers.set_c_flag()
        else:
            Registers.reset_c_flag()
        temp = value << 1
        if temp & 0xff == 0:
            Registers.set_z_flag()
        else:
            Registers.reset_z_flag()
        Registers.reset_n_flag()
        Registers.reset_h_flag()
        return temp & 0xff
