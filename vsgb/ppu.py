#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - https://gbdev.gg8.se/wiki/articles/Video_Display

from vsgb.byte_operations import signed_value, flip_byte, check_bit
from vsgb.interrupt_manager import Interrupt, InterruptManager
from vsgb.io_registers import IO_Registers
from vsgb.window import Window
from vsgb.address_space import AddressSpace


class PPU(AddressSpace):

    #Consts
    FRAMEBUFFER_SIZE: int    = Window.SCREEN_WIDTH * Window.SCREEN_HEIGHT
    H_BLANK_STATE: int       = 0
    V_BLANK_STATE: int       = 1
    OAM_READ_STATE: int      = 2
    VMRAM_READ_STATE: int    = 3
    OAM_SCANLINE_TIME: int   = 80
    VRAM_SCANLINE_TIME: int  = 172
    H_BLANK_TIME: int        = 204
    V_BLANK_TIME: int        = 4560

    #Vars
    framebuffer: list        = [0xffffffff]*FRAMEBUFFER_SIZE
    original_color: list     = [0]*FRAMEBUFFER_SIZE
    bg_priority: list        = [False]*FRAMEBUFFER_SIZE
    mode: int                = V_BLANK_STATE
    modeclock: int           = 0
    vblank_line: int         = 0
    auxillary_modeclock: int = 0
    screen_enabled: bool     = True
    window_line: int         = 0   
    cgb_mode: bool           = False 

    # Registers
    ly: int   = 0
    stat: int = 0
    lyc: int  = 0
    scx: int  = 0
    scy: int  = 0
    bgp: int  = 0
    wx: int   = 0
    wy: int   = 0
    lcdc: int = 0
    obp0: int = 0
    obp1: int = 0
    vbk: int  = 0

    # Memory
    vram: list = [[0]*0x2000,[0]*0x2000]
    oam: list = [0]*0xa0

    @classmethod
    def accept(cls, address: int) -> bool:
        return (0x8000 <= address < 0xa000) or (0xfe00 <= address < 0xfea0) or (address in [
            IO_Registers.LY,
            IO_Registers.STAT,
            IO_Registers.LYC,
            IO_Registers.SCX,
            IO_Registers.SCY,
            IO_Registers.BGP,
            IO_Registers.WX,
            IO_Registers.WY,
            IO_Registers.LCDC,
            IO_Registers.OBP0,
            IO_Registers.OBP1,
            IO_Registers.VBK
        ])

    @classmethod
    def read(cls, address: int) -> int:
        if 0x8000 <= address < 0xa000:
            return cls.vram[cls.vbk][address - 0x8000]
        if 0xfe00 <= address < 0xfea0:
            return cls.oam[address - 0xfe00]
        if address == IO_Registers.LY:
            return cls.ly
        if address == IO_Registers.STAT:
            return cls.stat
        if address == IO_Registers.LYC:
            return cls.lyc
        if address == IO_Registers.SCX:
            return cls.scx
        if address == IO_Registers.SCY:
            return cls.scy
        if address == IO_Registers.BGP:
            return cls.bgp
        if address == IO_Registers.WX:
            return cls.wx
        if address == IO_Registers.WY:
            return cls.wy
        if address == IO_Registers.LCDC:
            return cls.lcdc
        if address == IO_Registers.OBP0:
            return cls.obp0
        if address == IO_Registers.OBP1:
            return cls.obp1
        if address == IO_Registers.VBK:
            return cls.vbk


    @classmethod
    def write(cls, address: int, value: int):
        if 0x8000 <= address < 0xa000:
            cls.vram[cls.vbk][address - 0x8000] = value
        elif 0xfe00 <= address < 0xfea0:
            cls.oam[address - 0xfe00] = value
        elif address == IO_Registers.LY:
            cls.ly = value
        elif address == IO_Registers.STAT:
            cls.stat = value
        elif address == IO_Registers.LYC:
            cls.lyc = value
        elif address == IO_Registers.SCX:
            cls.scx = value
        elif address == IO_Registers.SCY:
            cls.scy = value
        elif address == IO_Registers.BGP:
            cls.bgp = value
        elif address == IO_Registers.WX:
            cls.wx = value
        elif address == IO_Registers.WY:
            cls.wy = value
        elif address == IO_Registers.LCDC:
            cls.lcdc = value
        elif address == IO_Registers.OBP0:
            cls.obp0 = value
        elif address == IO_Registers.OBP1:
            cls.obp1 = value
        elif address == IO_Registers.VBK:
            cls.vbk = value & 1

    @staticmethod
    def check_stat(old: int, new: int):

        if (new & 0b01000100) & ((~old) & 0b01000100):
        #if (new & 0b01000100):
            InterruptManager.request_interrupt(Interrupt.INTERRUPT_LCDSTAT)
            return

        for i in range(3):
            #if (new & (1 << (3+i))) & ((~old) & (1 << (3+i))) and i == (new & 0b11):
            if (new & (1 << (3+i))) and i == (new & 0b11):
                InterruptManager.request_interrupt(Interrupt.INTERRUPT_LCDSTAT)
                return     

    @classmethod
    def step(cls, cycles : int = 1):
        cls.modeclock += cycles
        cls.auxillary_modeclock += cycles
        if LCDControlRegister.lcd_display_enable(cls.lcdc):
            if cls.screen_enabled:
                if cls.mode == cls.H_BLANK_STATE:
                    if cls.modeclock >= cls.H_BLANK_TIME:
                        cls.exec_hblank()
                elif cls.mode == cls.V_BLANK_STATE:
                    cls.exec_vblank()
                elif cls.mode == cls.OAM_READ_STATE:
                    if cls.modeclock >= cls.OAM_SCANLINE_TIME:
                        cls.exec_oam()
                elif cls.mode == cls.VMRAM_READ_STATE:
                    if cls.modeclock >= cls.VRAM_SCANLINE_TIME:
                        cls.exec_vram()
                
            else:
                cls.screen_enabled = True
                cls.modeclock = 0
                cls.mode = 0
                cls.auxillary_modeclock = 0
                cls.window_line = 0
                cls.ly = 0
                cls.update_stat_mode()
                cls.compare_lylc()
        else:
            cls.screen_enabled = False
    
    @classmethod
    def exec_vram(cls):
        cls.modeclock -= cls.VRAM_SCANLINE_TIME
        cls.mode = cls.H_BLANK_STATE
        cls.scanline()
        cls.update_stat_mode()

    @classmethod
    def exec_oam(cls):
        cls.modeclock -= cls.OAM_SCANLINE_TIME
        cls.mode = cls.VMRAM_READ_STATE
        cls.update_stat_mode()

    @classmethod
    def exec_hblank(cls):
        cls.modeclock -= cls.H_BLANK_TIME
        cls.mode = cls.OAM_READ_STATE
        cls.ly += 1
        cls.compare_lylc()

        if cls.ly == 144:
            cls.mode = cls.V_BLANK_STATE
            cls.auxillary_modeclock = cls.modeclock
            cls.window_line = 0
            InterruptManager.request_interrupt(Interrupt.INTERRUPT_VBLANK)
            Window.framebuffer = cls.framebuffer

        cls.update_stat_mode()

        
    @classmethod
    def exec_vblank(cls):
        if cls.auxillary_modeclock >= 456:
            cls.auxillary_modeclock -= 456
            cls.vblank_line += 1

            if cls.vblank_line <= 9:
                cls.ly += 1
                cls.compare_lylc()

        if cls.modeclock >= cls.V_BLANK_TIME:
            cls.modeclock -= cls.V_BLANK_TIME
            cls.mode = cls.OAM_READ_STATE    
            cls.update_stat_mode()
            cls.ly = 0
            cls.vblank_line = 0

    @classmethod
    def scanline(cls):
        if cls.ly <= 144:
            cls.render_background(cls.ly)
            cls.render_window(cls.ly)
            cls.render_sprite(cls.ly)

    @classmethod
    def update_stat_mode(cls):
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

        
        new_stat = (cls.stat & 0xfc) | (cls.mode & 0x3)
        cls.check_stat(cls.stat,new_stat)
        cls.STAT = new_stat
        
    @staticmethod
    def rgb(color_code : int) -> int:
        return {
             0: 0x7fff,
             1: 0x421f,
             2: 0x1cf2,
             3: 0x0000
        }.get(color_code)

    @staticmethod
    def rgb_sprite(color_code : int) -> int:
        return {
             0: 0x7fff,
             1: 0x1bef,
             2: 0x0200,
             3: 0x0000
        }.get(color_code)

    @classmethod
    def compare_lylc(cls):
      if LCDControlRegister.lcd_display_enable(cls.lcdc):
            
            old_stat = cls.stat

            if cls.lyc == cls.ly:
                stat = cls.stat | 0x4
            else:
                stat = cls.stat & 0xfb
            cls.check_stat(old_stat, stat)
            cls.STAT =  stat

    @classmethod
    def render_background(cls, line : int):
        line_width = (Window.SCREEN_HEIGHT - line -1) * Window.SCREEN_WIDTH

        if LCDControlRegister.bg_window_display_priority(cls.lcdc):
            # tile and map select
            tiles_select = LCDControlRegister.bg_and_window_tile_data_select(cls.lcdc)
            map_select = LCDControlRegister.bg_tile_map_display_select(cls.lcdc)
            # line with y offset
            line_adjusted = (line + cls.scy) & 0xff
            # get position of tile row to read
            y_offset = (line_adjusted // 8) * 32
            # relative line number in tile
            tile_line = line_adjusted % 8
            # relative line number offset
            tile_line_offset = tile_line * 2
            x = 0
            while x < 32:
                tile = 0
                if tiles_select == 0x800:
                    tile = signed_value(cls.vram[0][map_select + y_offset + x])
                    tile += 128
                else:
                    tile = cls.vram[0][map_select + y_offset + x]
                    

                line_pixel_offset = x * 8
                tile_select_offset = tile * 16
                tile_address = tiles_select + tile_select_offset + tile_line_offset

                
                
                if not cls.cgb_mode:
                    byte_1 = cls.vram[0][tile_address]
                    byte_2 = cls.vram[0][tile_address + 1]
                else:
                    tile_attributes = TileAttributes(cls.vram[0][map_select + y_offset + x])
                    if tile_attributes.is_vertical_flip():
                        tile_address = tile_address - tile_line_offset + ( 7 - tile_line ) * 2
                    byte_1 = cls.vram[tile_attributes.get_vram_bank()][tile_address]
                    byte_2 = cls.vram[tile_attributes.get_vram_bank()][tile_address + 1]
                    if tile_attributes.is_horizontal_flip():
                        byte_1 = flip_byte(byte_1)
                        byte_2 = flip_byte(byte_2)

                pixelx = 0
                buffer_addr = (line_pixel_offset - cls.scx)
                while pixelx < 8:

                    shift = 0x1 << (7 - pixelx)
                    pixelx += 1

                    buffer_addr &= 0xff

                    if 0 <= buffer_addr < Window.SCREEN_WIDTH:

                        pixel = 1 if (byte_1 & shift > 0) else 0
                        pixel |= 2 if (byte_2 & shift > 0) else 0
                        color = (cls.bgp >> (pixel * 2)) & 0x3
                        

                        position = line_width + buffer_addr % Window.SCREEN_WIDTH
                        cls.original_color[position] = color
                        if not cls.cgb_mode:
                            cls.framebuffer[position] = cls.rgb(color)
                            
                        else:
                            """
                            if cls.mmu.bootstrap_enabled or cls.mmu.rom.is_cgb():
                                color = pixel
                            """
                            
                            #cls.framebuffer[position] = cls.mmu.cgb_palette.get_bg_rgba_palette_color(tile_attributes.get_palette(), color)
                            cls.framebuffer[position] = cls.rgb(color) #FIXME
                            
                            cls.bg_priority[position] = tile_attributes.is_bg_priority()
                            
                    buffer_addr = ( line_pixel_offset + pixelx - cls.scx )
                            
                x += 1
        else:
            for i in range(0, Window.SCREEN_WIDTH):
                cls.framebuffer[line_width + i] = cls.rgb(0)
                cls.original_color[line_width + i] = 0


    @classmethod
    def render_window(cls, line : int):
        line_width = (Window.SCREEN_HEIGHT - line -1) * Window.SCREEN_WIDTH
        # dont render if the window is outside the bounds of the screen or
        # if the LCDC window enable bit flag is not set
        if cls.window_line > 143 or not LCDControlRegister.window_display_enable(cls.lcdc):
            return

        window_pos_x = cls.wx - 7
        window_pos_y = cls.wy

        # don't render if the window is outside the bounds of the screen
        if window_pos_x > 159 or window_pos_y > 143 or window_pos_y > line:
            return 

        tiles_select = LCDControlRegister.bg_and_window_tile_data_select(cls.lcdc)
        map_select = LCDControlRegister.window_tile_map_display_select(cls.lcdc)

        line_adjusted = cls.window_line
        y_offset = (line_adjusted // 8) * 32
        tile_line = line_adjusted % 8
        tile_line_offset = tile_line * 2

        for x in range(32):
            tile = 0
            if tiles_select == 0x800:
                tile = signed_value(cls.vram[0][map_select + y_offset + x])
                tile += 128
            else:
                tile = cls.vram[0][map_select + y_offset + x]
            
            line_pixel_offset = x * 8
            tile_select_offset = tile * 16
            tile_address = tiles_select + tile_select_offset + tile_line_offset
            

            
            tile_attributes = TileAttributes(cls.vram[1][map_select + y_offset + x])
            
            if not cls.cgb_mode:
                byte_1 = cls.vram[0][tile_address]
                byte_2 = cls.vram[0][tile_address + 1]
            else:
                if tile_attributes.is_vertical_flip():
                    tile_address = tile_address - tile_line_offset + ( 7 - tile_line ) * 2
                byte_1 = cls.vram[tile_attributes.get_vram_bank()][tile_address]
                byte_2 = cls.vram[tile_attributes.get_vram_bank()][tile_address + 1]
                if tile_attributes.is_horizontal_flip():
                    byte_1 = flip_byte(byte_1)
                    byte_2 = flip_byte(byte_2)


            for pixelx in range(8):
                buffer_addr = line_pixel_offset + pixelx + window_pos_x

                if buffer_addr < 0 or buffer_addr >= Window.SCREEN_WIDTH:
                    continue

                shift = 0x1 << (7 - pixelx)

                pixel = 0
                if (byte_1 & shift == shift) and (byte_2 & shift == shift):
                    pixel = 3
                elif (byte_1 & shift == 0x0) and (byte_2 & shift == shift):
                    pixel = 2
                elif (byte_1 & shift == shift) and (byte_2 & shift == 0x0):
                    pixel = 1
                elif (byte_1 & shift == 0x0) and (byte_2 & shift == 0x00):
                    pixel = 0
                position = line_width + buffer_addr
                color = (cls.bgp >> (pixel * 2)) & 0x3
                if not cls.cgb_mode:
                    cls.framebuffer[position] = cls.rgb(color)
                    cls.original_color[position] = color
                else:
                    if cls.mmu.bootstrap_enabled or cls.mmu.rom.is_cgb():
                        color = pixel
                    cls.framebuffer[position] = cls.mmu.cgb_palette.get_bg_rgba_palette_color(tile_attributes.get_palette(), color)
                    cls.bg_priority[position] = tile_attributes.is_bg_priority()
                    cls.original_color[position] = color

        cls.window_line += 1

    @classmethod
    def render_sprite(cls, line : int):
        line_width = (Window.SCREEN_HEIGHT - line -1) * Window.SCREEN_WIDTH
        if not LCDControlRegister.sprite_display_enable(cls.lcdc):
            return

        sprite_size = LCDControlRegister.sprite_size(cls.lcdc)

        for sprite in range(39,-1,-1):
            sprite_offset = sprite * 4

            sprite_y = cls.oam[sprite_offset] - 16
            if sprite_y > line or (sprite_y + sprite_size) <= line:
                continue

            sprite_x = cls.oam[sprite_offset + 1] - 8
            if sprite_x < -7 or sprite_x >= Window.SCREEN_WIDTH:
                continue

            sprite_tile_offset = (cls.oam[sprite_offset + 2] & (0xfe if sprite_size == 16 else 0xff)) * 16
            
            sprite_attributes = SpriteAttributes(cls.oam[sprite_offset + 3])

            tiles = 0
            pixel_y = (15 if sprite_size == 16 else 7) - (line - sprite_y) if sprite_attributes.is_vertical_flip() else line - sprite_y

            pixel_y_2 = 0
            offset = 0

            if sprite_size == 16 and (pixel_y >= 8):
                pixel_y_2 = (pixel_y - 8) * 2
                offset = 16
            else:
                pixel_y_2 = pixel_y * 2

            tile_address = tiles + sprite_tile_offset + pixel_y_2 + offset
            byte_1 = cls.vram[sprite_attributes.get_vram_bank()][tile_address]
            byte_2 = cls.vram[sprite_attributes.get_vram_bank()][tile_address + 1]

            if sprite_attributes.get_palette() == 0:
                palette = cls.obp0
            else:
                palette = cls.obp1

            for pixelx in range(8):
                shift = 0x1 << (pixelx if sprite_attributes.is_horizontal_flip() else 7 - pixelx)
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

                if sprite_attributes.is_priority() or cls.original_color[position] == 0 :
                    if not cls.cgb_mode:
                        cls.framebuffer[position] = cls.rgb_sprite(color)

                    elif not cls.bg_priority[position] \
                        or cls.original_color[position] == 0:
                        if cls.mmu.bootstrap_enabled or cls.mmu.rom.is_cgb():
                            color = pixel
                        cls.framebuffer[position] = cls.mmu.cgb_palette.get_ob_rgba_palette_color(sprite_attributes.get_cgb_palette(), color)
        



class LCDControlRegister:

    """
    LCD Control Register
    Bit 7 - LCD Display Enable             (0=Off, 1=On)
    Bit 6 - Window Tile Map Display Select (0=9800-9BFF, 1=9C00-9FFF)
    Bit 5 - Window Display Enable          (0=Off, 1=On)
    Bit 4 - BG & Window Tile Data Select   (0=8800-97FF, 1=8000-8FFF)
    Bit 3 - BG Tile Map Display Select     (0=9800-9BFF, 1=9C00-9FFF)
    Bit 2 - OBJ (Sprite) Size              (0=8x8, 1=8x16)
    Bit 1 - OBJ (Sprite) Display Enable    (0=Off, 1=On)
    Bit 0 - BG/Window Display/Priority     (0=Off, 1=On)
    """

    @staticmethod
    def lcd_display_enable(lcdc: int) -> int:
        return check_bit(7,lcdc)

    @staticmethod
    def window_tile_map_display_select(lcdc: int) -> int:
        if check_bit(6,lcdc):
            return 0x1c00
        return 0x1800

    @staticmethod
    def window_display_enable(lcdc: int) -> int:
        return check_bit(5,PPU.lcdc)

    @staticmethod
    def bg_and_window_tile_data_select(lcdc: int) -> int:
        if check_bit(4,lcdc):
            return 0
        return 0x800

    @staticmethod
    def bg_tile_map_display_select(lcdc: int) -> int:
        if check_bit(3,lcdc):
            return 0x1c00
        return 0x1800

    @staticmethod
    def sprite_size(lcdc: int) -> int:
        if check_bit(2,lcdc):
            return 16
        return 8

    @staticmethod
    def sprite_display_enable(lcdc: int) -> int:
        return check_bit(1,lcdc) 

    @staticmethod
    def bg_window_display_priority(lcdc: int) -> int:
        return check_bit(0,lcdc)


class TileAttributes:

    """
    Map Attributes (CGB Mode only)
    In CGB Mode, an additional map of 32x32 bytes is stored in VRAM Bank 1 (each byte defines attributes for the corresponding tile-number map entry in VRAM Bank 0):
    Bit 0-2  Background Palette number  (BGP0-7)
    Bit 3    Tile VRAM Bank number      (0=Bank 0, 1=Bank 1)
    Bit 4    Not used
    Bit 5    Horizontal Flip            (0=Normal, 1=Mirror horizontally)
    Bit 6    Vertical Flip              (0=Normal, 1=Mirror vertically)
    Bit 7    BG-to-OAM Priority         (0=Use OAM priority bit, 1=BG Priority)
    When Bit 7 is set, the corresponding BG tile will have priority above all OBJs (regardless of the priority bits in OAM memory). There's also an Master Priority flag in LCDC register Bit 0 which overrides all other priority bits when cleared.
    """

    def __init__(self, value):
        self.value = value
        self._palette = self.value & 0b00000111
        self._vram_bank = (self.value & 0b00001000) >> 3
        self._horizontal_flip = self.value & 0b00100000 == 0b00100000
        self._vertical_flip = self.value & 0b01000000 == 0b01000000
        self._bg_priority = self.value & 0b10000000 == 0b10000000

    def get_palette(self):
        return self._palette

    def get_vram_bank(self):
        return self._vram_bank

    def is_horizontal_flip(self):
        return self._horizontal_flip

    def is_vertical_flip(self):
        return self._vertical_flip

    def is_bg_priority(self):
        return self._bg_priority
    

class SpriteAttributes:

    """
    Attributes/Flags:
    Bit7   OBJ-to-BG Priority (0=OBJ Above BG, 1=OBJ Behind BG color 1-3)
    (Used for both BG and Window. BG color 0 is always behind OBJ)
    Bit6   Y flip          (0=Normal, 1=Vertically mirrored)
    Bit5   X flip          (0=Normal, 1=Horizontally mirrored)
    Bit4   Palette number  **Non CGB Mode Only** (0=OBP0, 1=OBP1)
    Bit3   Tile VRAM-Bank  **CGB Mode Only**     (0=Bank 0, 1=Bank 1)
    Bit2-0 Palette number  **CGB Mode Only**     (OBP0-7)
    """

    def __init__(self, value):
        self.value = value
        self._ob_priority = self.value & 0x80 != 0x80
        self._horizontal_flip = self.value & 0x20 == 0x20
        self._vertical_flip = self.value & 0x40 == 0x40
        self._palette = (self.value & 0b00010000) >> 4
        self._bank = (self.value & 0b00001000) >> 3
        self._cgb_palette = self.value & 0b00000111


    def is_priority(self):
        return self._ob_priority
    
    def is_horizontal_flip(self):
        return self._horizontal_flip

    def is_vertical_flip(self):
        return self._vertical_flip

    def get_palette(self):
        return self._palette
    
    def get_cgb_palette(self):
        return self._cgb_palette

    def get_vram_bank(self):
        return self._bank
