#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Video_Display

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
        self.lcdControlRegister = LCDControlRegister(self.mmu)
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
        if self.lcdControlRegister.lcd_display_enable():
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
        # LCD Status Register
        # FF41 - STAT - LCDC Status (R/W)
        # -------------------------------
        # Bit 6 - LYC=LY Coincidence Interrupt (1=Enable) (Read/Write)
        # Bit 5 - Mode 2 OAM Interrupt         (1=Enable) (Read/Write)
        # Bit 4 - Mode 1 V-Blank Interrupt     (1=Enable) (Read/Write)
        # Bit 3 - Mode 0 H-Blank Interrupt     (1=Enable) (Read/Write)
        # Bit 2 - Coincidence Flag  (0:LYC<>LY, 1:LYC=LY) (Read Only)
        # Bit 1-0 - Mode Flag       (Mode 0-3, see below) (Read Only)
        #   0: During H-Blank
        #   1: During V-Blank
        #   2: During Searching OAM
        #   3: During Transferring Data to LCD Driver

        # The two lower STAT bits show the current status of the LCD controller.
        # The LCD controller operates on a 222 Hz = 4.194 MHz dot clock. An entire frame is 154 scanlines, 70224 dots, or 16.74 ms. On scanlines 0 through 143, the LCD controller cycles through modes 2, 3, and 0 once every 456 dots. Scanlines 144 through 153 are mode 1.
        # The following are typical when the display is enabled: 

        # Mode 2  2_____2_____2_____2_____2_____2___________________2____
        # Mode 3  _33____33____33____33____33____33__________________3___
        # Mode 0  ___000___000___000___000___000___000________________000
        # Mode 1  ____________________________________11111111111111_____

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
             0: 0xf0f0f0ff,
             1: 0xc0d8a8ff,
             2: 0x0090a8ff,
             3: 0x000000ff
        }.get(color_code)

    def rgb_sprite(self, color_code : int) -> int:
        return {
             0: 0xf0f0f0ff,
             1: 0xe8a0a0ff,
             2: 0x806050ff,
             3: 0x000000ff
        }.get(color_code)

    def compare_lylc(self):
      if self.lcdControlRegister.lcd_display_enable():
            lyc = self.mmu.read_byte(IO_Registers.LYC)
            stat = self.mmu.read_byte(IO_Registers.STAT)

            if lyc == self.current_line():
                stat = stat | 0x4
            else:
                stat = stat & 0xfb
            self.mmu.write_byte(IO_Registers.STAT, stat)

    def render_background(self, line : int):
        line_width = (Window.SCREEN_HEIGHT - line -1) * Window.SCREEN_WIDTH

        if self.lcdControlRegister.bg_window_display_priority():
            # tile and map select
            tiles_select = self.lcdControlRegister.bg_and_window_tile_data_select()
            map_select = self.lcdControlRegister.bg_tile_map_display_select()
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
        if self.window_line > 143 or not self.lcdControlRegister.window_display_enable():
            return

        window_pos_x = self.mmu.read_byte(IO_Registers.WX) - 7
        window_pos_y = self.mmu.read_byte(IO_Registers.WY)

        # don't render if the window is outside the bounds of the screen
        if window_pos_x > 159 or window_pos_y > 143 or window_pos_y > line:
            return 

        tiles_select = self.lcdControlRegister.bg_and_window_tile_data_select()
        map_select = self.lcdControlRegister.window_tile_map_display_select()

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

            palette = self.mmu.read_byte(IO_Registers.BGP)

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
                color = (palette >> (pixel * 2)) & 0x3
                self.framebuffer[position] = self.rgb(color)

        self.window_line += 1

    def render_sprite(self, line : int):
        line_width = (Window.SCREEN_HEIGHT - line -1) * Window.SCREEN_WIDTH
        if not self.lcdControlRegister.sprite_display_enable():
            return

        sprite_size = self.lcdControlRegister.sprite_size()

        for sprite in range(39,-1,-1):
            sprite_offset = sprite * 4

            sprite_y = self.mmu.read_byte(0xfe00 + sprite_offset) - 16
            if sprite_y > line or (sprite_y + sprite_size) <= line:
                continue

            sprite_x = self.mmu.read_byte(0xfe00 + sprite_offset + 1) - 8
            if sprite_x < -7 or sprite_x >= Window.SCREEN_WIDTH:
                continue

            sprite_tile_offset = (self.mmu.read_byte(0xfe00 + sprite_offset + 2) & (0xfe if sprite_size == 16 else 0xff)) * 16
            
            #  Attributes/Flags:
            # Bit7   OBJ-to-BG Priority (0=OBJ Above BG, 1=OBJ Behind BG color 1-3)
            # (Used for both BG and Window. BG color 0 is always behind OBJ)
            # Bit6   Y flip          (0=Normal, 1=Vertically mirrored)
            # Bit5   X flip          (0=Normal, 1=Horizontally mirrored)
            # Bit4   Palette number  **Non CGB Mode Only** (0=OBP0, 1=OBP1)
            # Bit3   Tile VRAM-Bank  **CGB Mode Only**     (0=Bank 0, 1=Bank 1)
            # Bit2-0 Palette number  **CGB Mode Only**     (OBP0-7)
            sprite_flags = self.mmu.read_byte(0xfe00 + sprite_offset + 3)
            priority = sprite_flags & 0x80 != 0x80
            x_flip = sprite_flags & 0x20 == 0x20
            y_flip = sprite_flags & 0x40 == 0x40
            palette = sprite_flags & 0b00010000

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

            obp0 = self.mmu.read_byte(IO_Registers.OBP0)
            obp1 = self.mmu.read_byte(IO_Registers.OBP1)
            if palette == 0:
                palette = obp0
            else:
                palette = obp1

            for pixelx in range(0,8):
                shift = 0x1 << (pixelx if x_flip else 7 - pixelx)
                pixel = 0

                if (byte_1 & shift == shift) and (byte_2 & shift == shift):
                    pixel = 3
                elif (byte_1 & shift == 0x0) and (byte_2 & shift == shift):
                    pixel = 2
                elif (byte_1 & shift == shift) and (byte_2 & shift == 0x0):
                    pixel = 1
                elif (byte_1 & shift == 0x0) and (byte_2 & shift == 0x00):
                    continue

                buffer_x = sprite_x + pixelx
                if buffer_x < 0 or buffer_x >= Window.SCREEN_WIDTH:
                    continue

                position = line_width + buffer_x

                color = (palette >> (pixel * 2)) & 0x3

                if priority or self.framebuffer[position] == self.rgb(0):
                    self.framebuffer[position] = self.rgb_sprite(color)



class LCDControlRegister:

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

    def lcd_display_enable(self) -> bool:
        return self.lcdc_status() & 0b10000000 == 0b10000000

    def window_tile_map_display_select(self) -> int:
        return 0x9c00 if self.lcdc_status() & 0b01000000 == 0b01000000 else 0x9800

    def window_display_enable(self) -> bool:
        return self.lcdc_status() & 0b00100000 == 0b00100000

    def bg_and_window_tile_data_select(self) -> int:
        return 0x8000 if self.lcdc_status() & 0b00010000 == 0b00010000 else 0x8800

    def bg_tile_map_display_select(self) -> int:
        return 0x9c00 if self.lcdc_status() & 0b00001000 == 0b00001000 else 0x9800

    def sprite_size(self) -> int:
        return 16 if self.lcdc_status() & 0b00000100 == 0b00000100 else 8

    def sprite_display_enable(self) -> bool:
        return self.lcdc_status() & 0b00000010 == 0b00000010 

    def bg_window_display_priority(self) -> bool:
        return self.lcdc_status() & 0b00000001 == 0b00000001
    
