#!/usr/bin/env python
# -*- coding: utf-8 -*-

def signed_value(byte : int) -> int:
    return (byte & 0x7F) - 0x80 if byte > 127 else byte

def set_bit(bit : int, value : int) -> int:
    return value | (1 << bit)

def check_bit(bit : int, value : int) -> int:
    return (value >> bit) & 1

def flip_byte(byte: int) -> int:
    result = 0
    for i in range(0,8):
        result = result | ( ( ( byte & ( 1 << i ) ) << ( 7 - i ) ) >> i )
    return result