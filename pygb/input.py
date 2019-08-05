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
        input = 0x0f
        if joyp & 0x20 == 0x00:
            if self.buttons['START']:
                input ^= 0x08
            elif self.buttons['SELECT']:
                input ^= 0x04
            elif self.buttons['A']:
                input ^= 0x01
            elif self.buttons['B']:
                input ^= 0x02
        elif joyp & 0x10 == 0x00:
            if self.buttons['UP']:
                input ^= 0x04
            elif self.buttons['DOWN']:
                input ^= 0x08
            elif self.buttons['LEFT']:
                input ^= 0x02
            elif self.buttons['RIGHT']:
                input ^= 0x01

        return (0xf0 & joyp) | input
