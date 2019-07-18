#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Registers:

    def __init__(self):
        self.a = 0x00
        self.b = 0x00
        self.c = 0x00
        self.d = 0x00
        self.e = 0x00
        self.f = 0x00
        self.h = 0x00
        self.l = 0x00
        self.pc = 0x0000
        self.sp = 0x0000

    def set_af(self, word):
        self.a = ( word >> 8 ) & 0xff
        self.f = word & 0xff

    def set_bc(self, word):
        self.b = ( word >> 8 ) & 0xff
        self.c = word & 0xff

    def set_de(self, word):
        self.d = ( word >> 8 ) & 0xff
        self.e = word & 0xff

    def set_hl(self, word):
        self.h = ( word >> 8 ) & 0xff
        self.l = word & 0xff

    def get_af(self):
        return (self.a << 8) + self.f

    def get_bc(self):
        return (self.b << 8) + self.c

    def get_de(self):
        return (self.d << 8) + self.e

    def get_hl(self):
        return (self.h << 8) + self.l