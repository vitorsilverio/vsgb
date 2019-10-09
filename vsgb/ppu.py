#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vsgb.byte_operations import signed_value
from vsgb.interrupt_manager import Interrupt, InterruptManager
from vsgb.io_registers import IO_Registers
from vsgb.mmu import MMU
from vsgb.window import Window

class PPU:

    FRAMEBUFFER_SIZE = Window.SCREEN_WIDTH * Window.SCREEN_HEIGHT

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
                self.next_line()
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
             0: 0xfcf6dfff,
             1: 0xb3ac9aff,
             2: 0x605f49ff,
             3: 0x343329ff
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
        line_width = (Window.SCREEN_HEIGHT - line -1) * Window.SCREEN_WIDTH

        if self.lcdController.is_background_enabled():
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
                buffer_addr = (line_pixel_offset - scx)
                while pixelx < 8:
                    buffer_addr = buffer_addr & 0xff
                    shift = 0x1 << (7 - pixelx)
                    pixel = 1 if (byte_1 & shift > 0) else 0
                    pixel |= 2 if (byte_2 & shift > 0) else 0
                    color = (palette >> (pixel * 2)) & 0x3
                    pixelx += 1
                    if 0 <= buffer_addr < Window.SCREEN_WIDTH:
                        position = line_width + buffer_addr
                        self.framebuffer[position] = self.rgb(color)
                        buffer_addr = ( line_pixel_offset + pixelx - scx )  
                x += 1
        else:
            for i in range(0, Window.SCREEN_WIDTH):
                self.framebuffer[line_width + i] = self.rgb(0)


    def render_window(self, line : int):
        line_width = (Window.SCREEN_HEIGHT - line -1) * Window.SCREEN_WIDTH
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
        map_select = self.lcdController.select_window_map()

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

                if buffer_addr < 0 or buffer_addr >= Window.SCREEN_WIDTH:
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
        line_width = (Window.SCREEN_HEIGHT - line -1) * Window.SCREEN_WIDTH
        if not self.lcdController.is_sprite_enabled():
            return

        sprite_size = self.lcdController.sprite_size()

        for sprite in range(39,-1,-1):
            sprite_offset = sprite * 4

            sprite_y = self.mmu.read_byte(0xfe00 + sprite_offset) - 16
            if sprite_y > line or (sprite_y + sprite_size) <= line:
                continue

            sprite_x = self.mmu.read_byte(0xfe00 + sprite_offset + 1) - 8
            if sprite_x < -7 or sprite_x >= Window.SCREEN_WIDTH:
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
                if buffer_x < 0 or buffer_x >= Window.SCREEN_WIDTH:
                    continue

                position = line_width + buffer_x

                self.framebuffer[position] = self.rgb(pixel)


class LCDController:

    # LCD Control Register
    # Bit 7 - LCD Display Enable             (0=Off, 1=On)
    # Bit 6 - Window Tile Map Display Select (0=9800-9BFF, 1=9C00-9FFF)
    # Bit 5 - Window Display Enable          (0=Off, 1=On)
    # Bit 4 - BG & Window Tile Data Select   (0=8800-97FF, 1=8000-8FFF)
    # Bit 3 - BG Tile Map Display Select     (0=9800-9BFF, 1=9C00-9FFF)
    # Bit 2 - OBJ (Sprite) Size              (0=8x8, 1=8x16)
    # Bit 1 - OBJ (Sprite) Display Enable    (0=Off, 1=On)
    # Bit 0 - BG/Window Display/Priority     (0=Off, 1=On)

    def __init__(self, mmu : MMU):
        self.mmu = mmu

    def lcdc_status(self) -> int:
        return self.mmu.read_byte(IO_Registers.LCDC)

    def is_screen_enabled(self) -> bool:
        return self.lcdc_status() & 0b10000000 == 0b10000000

    def select_window_map(self) -> int:
        return 0x9c00 if self.lcdc_status() & 0b01000000 == 0b01000000 else 0x9800

    def is_window_enabled(self) -> bool:
        return self.lcdc_status() & 0b00100000 == 0b00100000

    def select_background_window_map_tile_data(self) -> int:
        return 0x8000 if self.lcdc_status() & 0b00010000 == 0b00010000 else 0x8800

    def select_background_map_tile_data(self) -> int:
        return 0x9c00 if self.lcdc_status() & 0b00001000 == 0b00001000 else 0x9800

    def sprite_size(self) -> int:
        return 16 if self.lcdc_status() & 0b00000100 == 0b00000100 else 8

    def is_sprite_enabled(self) -> bool:
        return self.lcdc_status() & 0b00000010 == 0b00000010 

    def is_background_enabled(self) -> bool:
        return self.lcdc_status() & 0b00000001 == 0b00000001
    
