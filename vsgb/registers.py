#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Registers:

    Z_FLAG: int = 0x80
    N_FLAG: int = 0x40
    H_FLAG: int = 0x20
    C_FLAG: int = 0x10

    a: int = 0x00
    b: int = 0x00
    c: int = 0x00
    d: int = 0x00
    e: int = 0x00
    f: int = 0x00
    h: int = 0x00
    l: int = 0x00
    pc: int = 0x0000
    sp: int = 0x0000

    @classmethod    
    def set_af(cls, word : int):
        cls.a = ( word >> 8 ) & 0xff
        cls.f = word & 0xf0

    @classmethod
    def set_bc(cls, word : int):
        cls.b = ( word >> 8 ) & 0xff
        cls.c = word & 0xff

    @classmethod
    def set_de(cls, word : int):
        cls.d = ( word >> 8 ) & 0xff
        cls.e = word & 0xff

    @classmethod
    def set_hl(cls, word : int):
        cls.h = ( word >> 8 ) & 0xff
        cls.l = word & 0xff

    @classmethod
    def get_af(cls) -> int:
        return ((cls.a << 8) + cls.f) & 0xfff0

    @classmethod
    def get_bc(cls) -> int:
        return (cls.b << 8) + cls.c

    @classmethod
    def get_de(cls) -> int:
        return (cls.d << 8) + cls.e

    @classmethod
    def get_hl(cls) -> int:
        return (cls.h << 8) + cls.l

    @classmethod
    def set_z_flag(cls):
        cls.f |= cls.Z_FLAG

    @classmethod
    def reset_z_flag(cls):
        cls.f &= cls.Z_FLAG ^ 0xff

    @classmethod
    def set_n_flag(cls):
        cls.f |= cls.N_FLAG

    @classmethod
    def reset_n_flag(cls):
        cls.f &= cls.N_FLAG ^ 0xff

    @classmethod
    def set_c_flag(cls):
        cls.f |= cls.C_FLAG

    @classmethod
    def reset_c_flag(cls):
        cls.f &= cls.C_FLAG ^ 0xff

    @classmethod
    def set_h_flag(cls):
        cls.f |= cls.H_FLAG

    @classmethod
    def reset_h_flag(cls):
        cls.f &= cls.H_FLAG ^ 0xff

    @classmethod
    def is_z_flag(cls) -> bool:
        return cls.f & cls.Z_FLAG == cls.Z_FLAG

    @classmethod
    def is_n_flag(cls) -> bool:
        return cls.f & cls.N_FLAG == cls.N_FLAG

    @classmethod
    def is_c_flag(cls) -> bool:
        return cls.f & cls.C_FLAG == cls.C_FLAG

    @classmethod
    def is_h_flag(cls) -> bool:
        return cls.f & cls.H_FLAG == cls.H_FLAG

