#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Input:

    def __init__(self):
        self.buttons = {
            'A': False,
            'B': False,
            'START': False,
            'SELECT': False,
            'UP': False,
            'DOWN': False,
            'LEFT': False,
            'RIGHT': False
        }

    def read_input(self, joyp):
        inputs = 0xf
        if joyp & 0x20 == 0x00:
            if self.buttons['START']:
                inputs ^= 0x8
            elif self.buttons['SELECT']:
                inputs ^= 0x4
            elif self.buttons['A']:
                inputs ^= 0x1
            elif self.buttons['B']:
                inputs ^= 0x2
        elif joyp & 0x10 == 0x0:
            if self.buttons['UP'] == 1:
                inputs ^= 0x4
            elif self.buttons['DOWN']:
                inputs ^= 0x8
            elif self.buttons['LEFT']:
                inputs ^= 0x2
            elif self.buttons['RIGHT']:
                inputs ^= 0x1

        return (0xf0 & joyp) | inputs