#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Sound_Controller

class Lfsr:

    def __init__(self):
        self.lfsr = 0

    def start(self):
        self.reset()

    def reset(self):
        self.lfsr = 0x7fff

    def next_bit(self, with_mode7):
        x = ((self.lfsr & 1) ^ ((self.lfsr & 2) >> 1)) != 0
        self.lfsr = self.lfsr >> 1
        self.lfsr = self.lfsr | ((1 << 14) if x else 0)
        if with_mode7:
            self.lfsr = self.lfsr | ((1 << 6) if x else 0)
        return 1 & ~self.lfsr

    def get_value(self):
        return self.lfsr