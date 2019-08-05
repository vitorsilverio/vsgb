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
        input = 0xF
        if joyp & 0x20 == 0x00:
            if self.buttons['START']:
                input ^= 0x8
            elif self.buttons['SELECT']:
                input ^= 0x4
            elif self.buttons['A']:
                input ^= 0x1
            elif self.buttons['B']:
                input ^= 0x2
        elif joyp & 0x10 == 0x0:
            if self.buttons['UP']:
                input ^= 0x4
            elif self.buttons['DOWN']:
                input ^= 0x8
            elif self.buttons['LEFT']:
                input ^= 0x2
            elif self.buttons['RIGHT']:
                input ^= 0x1

        return (0xF0 & joyp) | input
