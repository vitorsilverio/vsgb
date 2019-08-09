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
        self._interrupt = False

    def must_interrupt(self):
        must_interrupt = self._interrupt 
        self._interrupt = False
        return must_interrupt

    def request_interrupt(self):
        self._interrupt = True

    def read_input(self, joyp : int) -> int:
        _input = 0x0f
        if joyp & 0x20 == 0x00:
            if self.buttons['START']:
                _input ^= 0x08
            elif self.buttons['SELECT']:
                _input ^= 0x04
            elif self.buttons['A']:
                _input ^= 0x01
            elif self.buttons['B']:
                _input ^= 0x02
        elif joyp & 0x10 == 0x00:
            if self.buttons['UP']:
                _input ^= 0x04
            elif self.buttons['DOWN']:
                _input ^= 0x08
            elif self.buttons['LEFT']:
                _input ^= 0x02
            elif self.buttons['RIGHT']:
                _input ^= 0x01

        return (0xf0 & joyp) | _input
