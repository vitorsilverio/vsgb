#!/usr/bin/env python
# -*- coding: utf-8 -*-

bit_mask = {
    0: 0x01,
    1: 0x02,
    2: 0x04,
    3: 0x08,
    4: 0x10,
    5: 0x20,
    6: 0x40,
    7: 0x80
}

def signed_value(byte : int) -> int:
    return (byte & 0x7F) - 0x80 if byte > 127 else byte

def set_bit(bit : int, value : int) -> int:
    return value | bit_mask[bit]

def flip_byte(byte: int) -> int:
    result = 0
    for i in range(0,8):
        result = result | ( ( ( byte & ( 1 << i ) ) << ( 7 - i ) ) >> i )
    return result