#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygb.byte_operations import signed_value
from pygb.interrupt_manager import Interrupt, InterruptManager
from pygb.io_registers import IO_Registers
from pygb.mmu import MMU
from pygb.screen import Screen

class PPU:

    FRAMEBUFFER_SIZE = Screen.SCREEN_WIDTH * Screen.SCREEN_HEIGHT

    H_BLANK_STATE     = 0
    V_BLANK_STATE     = 1
    OAM_READ_STATE    = 2
    VMRAM_READ_STATE  = 3

    OAM_SCANLINE_TIME   = 80
    VRAM_SCANLINE_TIME  = 172
    H_BLANK_TIME        = 204
    V_BLANK_TIME        = 4560

    def __init__(self, mmu : MMU, interruptManager : InterruptManager):
        self.mmu = mmu
        self.interruptManager = interruptManager
        self.lcdController = LCDController(self.mmu)
        self.framebuffer = [0xffffffff]*PPU.FRAMEBUFFER_SIZE
        self.mode = PPU.V_BLANK_STATE
        self.modeclock = 0
        self.vblank_line = 0
        self.auxillary_modeclock = 0
        self.screen_enabled = True
        self.window_line = 0   

    def step(self, cycles : int = 1):
        self.vblank = False
        self.modeclock += cycles
        self.auxillary_modeclock += cycles
        if self.lcdController.is_screen_enabled():
            if self.screen_enabled:
                if self.mode == PPU.H_BLANK_STATE:
                    if self.modeclock >= PPU.H_BLANK_TIME:
                        self.exec_hblank()
                elif self.mode == PPU.V_BLANK_STATE:
                    self.exec_vblank()
                elif self.mode == PPU.OAM_READ_STATE:
                    if self.modeclock >= PPU.OAM_SCANLINE_TIME:
                        self.exec_oam()
                elif self.mode == PPU.VMRAM_READ_STATE:
                    if self.modeclock >= PPU.VRAM_SCANLINE_TIME:
                        self.exec_vram()
            else:
                self.screen_enabled = True
                self.modeclock = 0
                self.mode = 0
                self.auxillary_modeclock = 0
                self.window_line = 0
                self.reset_current_line()
                self.update_stat_mode()
                self.compare_lylc()
        else:
            self.screen_enabled = False
    
    def exec_vram(self):
        self.modeclock -= PPU.VRAM_SCANLINE_TIME
        self.mode = PPU.H_BLANK_STATE
        self.scanline()
        self.update_stat_mode()

    def exec_oam(self):
        self.modeclock -= PPU.OAM_SCANLINE_TIME
        self.scanline_transfered = False
        self.mode = PPU.VMRAM_READ_STATE
        self.update_stat_mode()

    def exec_hblank(self):
        self.modeclock -= PPU.H_BLANK_TIME
        self.mode = PPU.OAM_READ_STATE
        self.next_line()
        self.compare_lylc()

        if self.current_line() == 144:
            self.mode = PPU.V_BLANK_STATE
            self.auxillary_modeclock = self.modeclock
            self.vblank = True
            self.window_line = 0
            self.interruptManager.request_interrupt(Interrupt.INTERRUPT_VBLANK)

        self.update_stat_mode()

    def exec_vblank(self):
        if self.auxillary_modeclock >= 456:
            self.auxillary_modeclock -= 456
            self.vblank_line += 1

            if self.vblank_line <= 9:
            #    self.next_line() #This next line causes slow
                self.compare_lylc()

        if self.modeclock >= PPU.V_BLANK_TIME:
            self.modeclock -= PPU.V_BLANK_TIME
            self.mode = PPU.OAM_READ_STATE    
            self.update_stat_mode()
            self.reset_current_line()
            self.vblank_line = 0

    def scanline(self):
        line = self.current_line()
        if line <= 144:
            self.render_background(line)
            self.render_window(line)
            self.render_sprite(line)

    def update_stat_mode(self):
        stat = self.mmu.read_byte(IO_Registers.STAT)
        new_stat = (stat & 0xfc) | (self.mode & 0x3)
        self.mmu.write_byte(IO_Registers.STAT, new_stat)

    def current_line(self):
        return self.mmu.read_byte(IO_Registers.LY)

    def reset_current_line(self):
        self.mmu.write_byte(IO_Registers.LY, 0)

    def next_line(self):
        self.mmu.write_byte(IO_Registers.LY, self.current_line() + 1)

    def rgb(self, color_code : int) -> int:
        return {
            0: 0xffffffff,
            1: 0xffa8a8a8,
            2: 0xff555555,
            3: 0x00000000
        }.get(color_code)

    def compare_lylc(self):
      if self.lcdController.is_screen_enabled():
            lyc = self.mmu.read_byte(IO_Registers.LYC)
            stat = self.mmu.read_byte(IO_Registers.STAT)

            if lyc == self.current_line():
                stat = stat | 0x4
            else:
                stat = stat & 0xfb
            self.mmu.write_byte(IO_Registers.STAT, stat)

    def render_background(self, line : int):
        line_width = (Screen.SCREEN_HEIGHT - line -1) * Screen.SCREEN_WIDTH

        if self.lcdController.is_background_enabled:
            # tile and map select
            tiles_select = self.lcdController.select_background_window_map_tile_data()
            map_select = self.lcdController.select_background_map_tile_data()
            # x pixel offset
            scx = self.mmu.read_byte(IO_Registers.SCX)
            # y pixel offset
            scy = self.mmu.read_byte(IO_Registers.SCY)
            # line with y offset
            line_adjusted = (line + scy) & 0xff
            # get position of tile row to read
            y_offset = int(line_adjusted / 8) * 32
            # relative line number in tile
            tile_line = line_adjusted % 8
            # relative line number offset
            tile_line_offset = tile_line * 2
            palette = self.mmu.read_byte(IO_Registers.BGP)
            x = 0
            while x < 32:
                tile = 0
                if tiles_select == 0x8800:
                    tile = signed_value(self.mmu.read_byte(map_select + y_offset + x))
                    tile += 128
                else:
                    tile = self.mmu.read_byte(map_select + y_offset + x)
                line_pixel_offset = x * 8
                tile_select_offset = tile * 16
                tile_address = tiles_select + tile_select_offset + tile_line_offset
                byte_1 = self.mmu.read_byte(tile_address)
                byte_2 = self.mmu.read_byte(tile_address + 1)
                pixelx = 0
                buffer_addr = line_pixel_offset - scx
                while pixelx < 8 and buffer_addr < Screen.SCREEN_WIDTH:
                    shift = 0x1 << (7 - pixelx)
                    pixel = 1 if (byte_1 & shift > 0) else 0
                    pixel |= 2 if (byte_2 & shift > 0) else 0
                    position = line_width + buffer_addr
                    color = (palette >> (pixel * 2)) & 0x3
                    self.framebuffer[position] = self.rgb(color)
                    pixelx += 1
                    buffer_addr = line_pixel_offset + pixelx - scx
                x += 1
        else:
            for i in range(0, Screen.SCREEN_WIDTH):
                self.framebuffer[line_width + i] = 0


    def render_window(self, line : int):
        line_width = (Screen.SCREEN_HEIGHT - line -1) * Screen.SCREEN_WIDTH
        # dont render if the window is outside the bounds of the screen or
        # if the LCDC window enable bit flag is not set
        if self.window_line > 143 or not self.lcdController.is_window_enabled():
            return
        window_pos_x = self.mmu.read_byte(IO_Registers.WX) - 7
        window_pos_y = self.mmu.read_byte(IO_Registers.WY)

        # don't render if the window is outside the bounds of the screen
        if window_pos_x > 159 or window_pos_y > 143 or window_pos_y > line:
            return 

        tiles_select = self.lcdController.select_background_window_map_tile_data()
        map_select = self.lcdController.select_background_map_tile_data()

        line_adjusted = self.window_line
        y_offset = int(line_adjusted / 8) * 32
        tile_line = line_adjusted % 8
        tile_line_offset = tile_line * 2

        for x in range(0,32):
            tile = 0
            if tiles_select == 0x8800:
                tile = signed_value(self.mmu.read_byte(map_select + y_offset + x))
                tile += 128
            else:
                tile = self.mmu.read_byte(map_select + y_offset + x)
            line_pixel_offset = x * 8
            tile_select_offset = tile * 16
            tile_address = tiles_select + tile_select_offset + tile_line_offset

            byte_1 = self.mmu.read_byte(tile_address)
            byte_2 = self.mmu.read_byte(tile_address + 1)

            for pixelx in range(0,8):
                buffer_addr = line_pixel_offset + pixelx + window_pos_x

                if buffer_addr < 0 or buffer_addr >= Screen.SCREEN_WIDTH:
                    continue

                shift = 0x1 << (7 - pixelx)

                pixel = 0
                if (byte_1 & shift == shift) and (byte_2 & shift == shift):
                    pixel = 3
                elif (byte_1 & shift == 0x0) and (byte_2 & shift == shift):
                    pixel = 1
                elif (byte_1 & shift == shift) and (byte_2 & shift == 0x0):
                    pixel = 2
                elif (byte_1 & shift == 0x0) and (byte_2 & shift == 0x00):
                    pixel = 0
                position = line_width + buffer_addr
                self.framebuffer[position] = self.rgb(pixel)

        self.window_line += 1

    def render_sprite(self, line : int):
        line_width = (Screen.SCREEN_HEIGHT - line -1) * Screen.SCREEN_WIDTH
        if not self.lcdController.is_sprite_enabled():
            return

        sprite_size = self.lcdController.sprite_size()

        for sprite in range(39,-1,-1):
            sprite_offset = sprite * 4

            sprite_y = self.mmu.read_byte(0xFE00 + sprite_offset) - 16
            if sprite_y > line or (sprite_y + sprite_size) <= line:
                continue

            sprite_x = self.mmu.read_byte(0xfe00 + sprite_offset + 1) - 8
            if sprite_x < -7 or sprite_x >= Screen.SCREEN_WIDTH:
                continue

            sprite_tile_offset = (self.mmu.read_byte(0xfe00 + sprite_offset + 2) & (0xfe if sprite_size == 16 else 0xff)) * 16
            sprite_flags = self.mmu.read_byte(0xfe00 + sprite_offset + 3)
            x_flip = sprite_flags & 0x20 == 0x20
            y_flip = sprite_flags & 0x40 == 0x40
        

            tiles = 0x8000
            pixel_y = (15 if sprite_size == 16 else 7) - (line - sprite_y) if y_flip else line - sprite_y

            pixel_y_2 = 0
            offset = 0

            if sprite_size == 16 and (pixel_y >= 8):
                pixel_y_2 = (pixel_y - 8) * 2
                offset = 16
            else:
                pixel_y_2 = pixel_y * 2

            tile_address = tiles + sprite_tile_offset + pixel_y_2 + offset

            byte_1 = self.mmu.read_byte(tile_address)
            byte_2 = self.mmu.read_byte(tile_address + 1)

            for pixelx in range(0,8):
                shift = 0x1 << (pixelx if x_flip else 7 - pixelx)
                pixel = 0

                if (byte_1 & shift == shift) and (byte_2 & shift == shift):
                    pixel = 3
                elif (byte_1 & shift == 0x0) and (byte_2 & shift == shift):
                    pixel = 1
                elif (byte_1 & shift == shift) and (byte_2 & shift == 0x0):
                    pixel = 2
                elif (byte_1 & shift == 0x0) and (byte_2 & shift == 0x00):
                    continue

                buffer_x = sprite_x + pixelx
                if buffer_x < 0 or buffer_x >= Screen.SCREEN_WIDTH:
                    continue

                position = line_width + buffer_x

                self.framebuffer[position] = self.rgb(pixel)


class LCDController:

    def __init__(self, mmu : MMU):
        self.mmu = mmu

    def lcdc_status(self) -> int:
        return self.mmu.read_byte(IO_Registers.LCDC)

    def is_screen_enabled(self) -> bool:
        return self.lcdc_status() & 0x80 == 0x80

    def select_window_map(self) -> int:
        return 1 if self.lcdc_status() & 0x40 == 0x40 else 0

    def is_window_enabled(self) -> bool:
        return self.lcdc_status() & 0x20 == 0x20

    def select_background_window_map_tile_data(self) -> int:
        return 0x8000 if self.lcdc_status() & 0x10 == 0x10 else 0x8800

    def select_background_map_tile_data(self) -> int:
        return 0x9c00 if self.lcdc_status() & 0x8 == 0x8 else 0x9800

    def sprite_size(self) -> int:
        return 16 if self.lcdc_status() & 0x4 == 0x4 else 8

    def is_sprite_enabled(self) -> bool:
        return self.lcdc_status() & 0x2 == 0x2 

    def is_background_enabled(self) -> bool:
        return self.lcdc_status() & 0x1 == 0x1
    
