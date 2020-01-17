#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

class PolynomialCounter:

    def __init__(self):
        self.i = 0
        self.shifted_divisor = 0

    def set_nr43(self,value):
        clock_shifted = value >> 4
        divisor = 0
        divisor = {
            0: 8,
            1: 16,
            2: 32,
            3: 48,
            4: 64,
            5: 80,
            6: 96,
            7: 112
        }.get(value & 0b00000111)
        self.shifted_divisor = divisor << clock_shifted
        self.i = 1

    def step(self, ticks):
        self.i -= ticks
        if self.i <= 0:
            self.i = self.shifted_divisor
            return True
        else:
            return False