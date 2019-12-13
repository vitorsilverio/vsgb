#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - http://problemkaputt.de/pandocs.htm

class CGB_Palette:

    def __init__(self):

        # FF68 - BCPS/BGPI - CGB Mode Only - Background Palette Index
        self.bg_palettes = [
            0,0,0,0, #BGP0
            0,0,0,0, #BGP1
            0,0,0,0, #BGP2
            0,0,0,0, #BGP3
            0,0,0,0, #BGP4
            0,0,0,0, #BGP5
            0,0,0,0, #BGP6
            0,0,0,0  #BGP7
        ]
        self.bgpi = 0
        self.bg_autoincrement = False
        self.bg_palette_index = 0
        self.bg_palette_color = 0
        self.bg_palette_byte_selector = 0

        # FF68 - BCPS/BGPI - CGB Mode Only - Background Palette Index
        self.ob_palettes = [
            0,0,0,0, #OBP0
            0,0,0,0, #OBP1
            0,0,0,0, #OBP2
            0,0,0,0, #OBP3
            0,0,0,0, #OBP4
            0,0,0,0, #OBP5
            0,0,0,0, #OBP6
            0,0,0,0  #OBP7
        ]
        self.obpi = 0
        self.ob_autoincrement = False
        self.ob_palette_index = 0
        self.ob_palette_color = 0
        self.ob_palette_byte_selector = 0

    def set_bgpi(self, value):
        """
            Bit Desc
            7   Autoincrement
            6   -
            3-5 palette
            1-2 color
            0   byte selector (0 = Low, 1 = High)
        """
        self.bgpi = value
        self.bg_autoincrement = value & 0b10000000 == 0b10000000
        self.bg_palette_index = ((value & 0b00111000) >> 3)
        self.bg_palette_color = ((value & 0b00000110) >> 1)
        self.bg_palette_byte_selector = value & 0b00000001

    def set_bgpd(self, value):
        address = (self.bg_palette_index * 4) + self.bg_palette_color
        if self.bg_palette_byte_selector == 0: # Set low byte
            self.bg_palettes[address] = ((self.bg_palettes[address] & 0xff00) | value)
        else: # Set high byte
            self.bg_palettes[address] = ((self.bg_palettes[address] & 0x00ff) | (value << 8))
        if self.bg_autoincrement:
            self.set_bgpi(self.bgpi + 1)

    def get_bgpd(self):
        address = (self.bg_palette_index * 4) + self.bg_palette_color
        if self.bg_palette_byte_selector == 0: # Get low byte
            return self.bg_palettes[address] & 0xff
        else: # Get high byte
            return self.bg_palettes[address] >> 8
        if self.bg_autoincrement:
            self.set_bgpi(self.bgpi + 1)

     def set_obpi(self, value):
        """
            Bit Desc
            7   Autoincrement
            6   -
            3-5 palette
            1-2 color
            0   byte selector (0 = Low, 1 = High)
        """
        self.obpi = value
        self.ob_autoincrement = value & 0b10000000 == 0b10000000
        self.ob_palette_index = ((value & 0b00111000) >> 3)
        self.ob_palette_color = ((value & 0b00000110) >> 1)
        self.ob_palette_byte_selector = value & 0b00000001

    def set_obpd(self, value):
        address = (self.ob_palette_index * 4) + self.ob_palette_color
        if self.ob_palette_byte_selector == 0: # Set low byte
            self.ob_palettes[address] = ((self.ob_palettes[address] & 0xff00) | value)
        else: # Set high byte
            self.ob_palettes[address] = ((self.ob_palettes[address] & 0x00ff) | (value << 8))
        if self.ob_autoincrement:
            self.set_obpi(self.obpi + 1)

    def get_obpd(self):
        address = (self.ob_palette_index * 4) + self.ob_palette_color
        if self.ob_palette_byte_selector == 0: # Get low byte
            return self.ob_palettes[address] & 0xff
        else: # Get high byte
            return self.ob_palettes[address] >> 8
        if self.ob_autoincrement:
            self.set_obpi(self.obpi + 1)
            
    def get_bg_rgba_palette_color(self, palette, color):
        address = (palette * 4) + color
        return self.color_5_5_5_to_rgba(self.bg_palettes[address])

    def get_ob_rgba_palette_color(self, palette, color):
        address = (palette * 4) + color
        return self.color_5_5_5_to_rgba(self.ob_palettes[address])

    def color_5_5_5_to_rgba(self, color):
        red = (color & 0b0111110000000000) >> 10
        blue = (color & 0b0000001111100000) >> 5
        green = (color & 0b0000000000011111)

        # 0b11111 = 0x1F
        red = (red / 0x1f) * 0xff
        blue = (blue / 0x1f) * 0xff
        green = (green / 0x1f) * 0xff 
        alpha = 0xff

        rgba = 0
        rgba |= (red << 24)
        rgba |= (green << 16)
        rgba |= (blue << 8)
        rgba |= alpha

        return rgba


       