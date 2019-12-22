#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - http://bgb.bircd.org/pandocs.htm#lcdcolorpalettescgbonly
# - https://www.chibiakumas.com/z80/platform2.php#LessonP17

class CGB_Palette:

    def __init__(self):

        # FF68 - BCPS/BGPI - CGB Mode Only - Background Palette Index
        self.bg_palettes = [
            Color(),Color(),Color(),Color(), #BGP0
            Color(),Color(),Color(),Color(), #BGP1
            Color(),Color(),Color(),Color(), #BGP2
            Color(),Color(),Color(),Color(), #BGP3
            Color(),Color(),Color(),Color(), #BGP4
            Color(),Color(),Color(),Color(), #BGP5
            Color(),Color(),Color(),Color(), #BGP6
            Color(),Color(),Color(),Color()  #BGP7
        ]
        self.bgpi = PaletteIndex()

        # FF68 - BCPS/BGPI - CGB Mode Only - Background Palette Index
        self.ob_palettes = [
            Color(),Color(),Color(),Color(), #OBP0
            Color(),Color(),Color(),Color(), #OBP1
            Color(),Color(),Color(),Color(), #OBP2
            Color(),Color(),Color(),Color(), #OBP3
            Color(),Color(),Color(),Color(), #OBP4
            Color(),Color(),Color(),Color(), #OBP5
            Color(),Color(),Color(),Color(), #OBP6
            Color(),Color(),Color(),Color()  #OBP7
        ]
        self.obpi = PaletteIndex()


    def set_bgpi(self, value):
        self.bgpi.set_value(value)

    def get_bgpi(self):
        return self.bgpi.get_value()

    def set_bgpd(self, value):
        address = (self.bgpi.get_palette() * 4) + self.bgpi.get_color()
        if self.bgpi.get_byte_selector() == 0: # Set low byte
            self.bg_palettes[address].set_low_byte(value)
        else: # Set high byte
            self.bg_palettes[address].set_high_byte(value)
        if self.bgpi.is_autoincrement():
            self.set_bgpi(self.bgpi.get_value() + 1)

    def get_bgpd(self):
        address = (self.bgpi.get_palette() * 4) + self.bgpi.get_color()
        if self.bgpi.get_byte_selector() == 0: # Get low byte
            return self.bg_palettes[address].get_low_byte()
        else: # Get high byte
            return self.bg_palettes[address].get_high_byte()
        if self.bgpi.is_autoincrement():
            self.set_bgpi(self.bgpi.get_value() + 1)

    def set_obpi(self, value):
        self.obpi.set_value(value)

    def get_obpi(self):
        return self.obpi.get_value()

    def set_obpd(self, value):
        address = (self.obpi.get_palette() * 4) + self.obpi.get_color()
        if self.obpi.get_byte_selector() == 0: # Set low byte
            self.ob_palettes[address].set_low_byte(value)
        else: # Set high byte
            self.ob_palettes[address].set_high_byte(value)
        if self.obpi.is_autoincrement():
            self.set_obpi(self.obpi.get_value() + 1)

    def get_obpd(self):
        address = (self.obpi.get_palette() * 4) + self.obpi.get_color()
        if self.obpi.get_byte_selector() == 0: # Get low byte
            return self.ob_palettes[address].get_low_byte()
        else: # Get high byte
            return self.ob_palettes[address].get_high_byte()
        if self.obpi.is_autoincrement():
            self.set_obpi(self.obpi.get_value() + 1)

            
    def get_bg_rgba_palette_color(self, palette, color):
        address = (palette * 4) + color
        return self.bg_palettes[address].get_rgba()

    def get_ob_rgba_palette_color(self, palette, color):
        address = (palette * 4) + color
        return self.ob_palettes[address].get_rgba()

class PaletteIndex:

    """
        Bit Desc
        7   Autoincrement
        6   -
        3-5 palette
        1-2 color
        0   byte selector (0 = Low, 1 = High)
    """

    def __init__(self):
        self._value = 0
        self._autoincrement = False
        self._horizontal_flip = False
        self._vertical_flip = False
        self._palette = 0
        self._color = 0
        self._byte_selector = 0

    def set_value(self, value):
        self._value = value & 0b10111111
        self._autoincrement = self._value & 0b10000000 == 0b10000000
        self._palette = ((self._value & 0b00111000) >> 3)
        self._color = ((self._value & 0b00000110) >> 1)
        self._byte_selector = self._value & 0b00000001

    def get_value(self):
        return self._value

    def is_autoincrement(self):
        return self._autoincrement

    def get_palette(self):
        return self._palette

    def get_color(self):
        return self._color

    def get_byte_selector(self):
        return self._byte_selector


class Color:

    def __init__(self):
        self._value = 0
        self._rgba = 0

    def set_low_byte(self, value):
        self._value = ((self._value & 0xff00) | value)
        self._rgba = self.color_5_5_5_to_rgba(self._value)


    def set_high_byte(self, value):
        self._value = ((self._value & 0x00ff) | (value << 8))
        self._rgba = self.color_5_5_5_to_rgba(self._value)

    def get_low_byte(self):
        return self._value & 0xff

    def get_high_byte(self):
        return self.value >> 8
    
    def get_rgba(self):
        return self._rgba


    def color_5_5_5_to_rgba(self, color):
        blue = (color & 0b0111110000000000) >> 10
        green = (color & 0b0000001111100000) >> 5
        red = (color & 0b0000000000011111)

        # 0b11111 = 0x1F
        red = int((red / 0x1f) * 0xff)
        blue = int((blue / 0x1f) * 0xff)
        green = int((green / 0x1f) * 0xff)
        alpha = 0xff

        rgba = 0
        rgba |= (red << 24)
        rgba |= (green << 16)
        rgba |= (blue << 8)
        rgba |= alpha

        return rgba