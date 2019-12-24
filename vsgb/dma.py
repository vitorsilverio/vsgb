#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Documentation source:
# - http://problemkaputt.de/pandocs.htm

from vsgb.io_registers import IO_Registers
from vsgb.mmu import MMU

"""
FF46 - DMA - DMA Transfer and Start Address (W)
Writing to this register launches a DMA transfer from ROM or RAM to OAM memory (sprite attribute table). The written value specifies the transfer source address divided by 100h, ie. source & destination are:
  Source:      XX00-XX9F   ;XX in range from 00-F1h
  Destination: FE00-FE9F
It takes 160 microseconds until the transfer has completed (80 microseconds in CGB Double Speed Mode), during this time the CPU can access only HRAM (memory at FF80-FFFE). For this reason, the programmer must copy a short procedure into HRAM, and use this procedure to start the transfer from inside HRAM, and wait until the transfer has finished:
   ld  (0FF46h),a ;start DMA transfer, a=start address/100h
   ld  a,28h      ;delay...
  wait:           ;total 5x40 cycles, approx 200ms
   dec a          ;1 cycle
   jr  nz,wait    ;4 cycles
Most programs are executing this procedure from inside of their VBlank procedure, but it is possible to execute it during display redraw also, allowing to display more than 40 sprites on the screen (ie. for example 40 sprites in upper half, and other 40 sprites in lower half of the screen).
"""
class DMA:

    def __init__(self, mmu: MMU):
        self.mmu = mmu
        self.ticks = 0
        self.in_progress = False
        self.page = 0x0000
        self.counter = 0x00
        self.mmu.set_dma(self)
        self.wait_set_delay = False

    def request_dma_transfer(self, page: int):
        self.page = (page << 8)
        self.in_progress = True
        self.counter = 0x00
        self.ticks = 0
        self.wait_set_delay = True

    def step(self):
        if self.wait_set_delay:
            self.ticks = 8
            self.wait_set_delay = False
        else:
            source_address = self.page + self.counter
            destination_address = 0xfe00 + self.counter
            self.mmu.write_byte(destination_address, self.mmu.read_byte(source_address))
            self.counter += 1
            self.ticks = 20
            if self.counter == 0xa0:
                self.in_progress = False

"""
LCD VRAM DMA Transfers (CGB only)

FF51 - HDMA1 - CGB Mode Only - New DMA Source, High
FF52 - HDMA2 - CGB Mode Only - New DMA Source, Low
FF53 - HDMA3 - CGB Mode Only - New DMA Destination, High
FF54 - HDMA4 - CGB Mode Only - New DMA Destination, Low
FF55 - HDMA5 - CGB Mode Only - New DMA Length/Mode/Start
These registers are used to initiate a DMA transfer from ROM or RAM to VRAM. The Source Start Address may be located at 0000-7FF0 or A000-DFF0, the lower four bits of the address are ignored (treated as zero). The Destination Start Address may be located at 8000-9FF0, the lower four bits of the address are ignored (treated as zero), the upper 3 bits are ignored either (destination is always in VRAM).

Writing to FF55 starts the transfer, the lower 7 bits of FF55 specify the Transfer Length (divided by 10h, minus 1). Ie. lengths of 10h-800h bytes can be defined by the values 00h-7Fh. And the upper bit of FF55 indicates the Transfer Mode:

Bit7=0 - General Purpose DMA
When using this transfer method, all data is transferred at once. The execution of the program is halted until the transfer has completed. Note that the General Purpose DMA blindly attempts to copy the data, even if the LCD controller is currently accessing VRAM. So General Purpose DMA should be used only if the Display is disabled, or during V-Blank, or (for rather short blocks) during H-Blank.
The execution of the program continues when the transfer has been completed, and FF55 then contains a value if FFh.

Bit7=1 - H-Blank DMA
The H-Blank DMA transfers 10h bytes of data during each H-Blank, ie. at LY=0-143, no data is transferred during V-Blank (LY=144-153), but the transfer will then continue at LY=00. The execution of the program is halted during the separate transfers, but the program execution continues during the 'spaces' between each data block.
Note that the program may not change the Destination VRAM bank (FF4F), or the Source ROM/RAM bank (in case data is transferred from bankable memory) until the transfer has completed!
Reading from Register FF55 returns the remaining length (divided by 10h, minus 1), a value of 0FFh indicates that the transfer has completed. It is also possible to terminate an active H-Blank transfer by writing zero to Bit 7 of FF55. In that case reading from FF55 may return any value for the lower 7 bits, but Bit 7 will be read as "1".

Confirming if the DMA Transfer is Active
Reading Bit 7 of FF55 can be used to confirm if the DMA transfer is active (1=Not Active, 0=Active). This works under any circumstances - after completion of General Purpose, or H-Blank Transfer, and after manually terminating a H-Blank Transfer.

Transfer Timings
In both Normal Speed and Double Speed Mode it takes about 8us to transfer a block of 10h bytes. That are 8 cycles in Normal Speed Mode, and 16 'fast' cycles in Double Speed Mode.
Older MBC controllers (like MBC1-4) and slower ROMs are not guaranteed to support General Purpose or H-Blank DMA, that's because there are always 2 bytes transferred per microsecond (even if the itself program runs it Normal Speed Mode).
"""
class HDMA:

    TYPE_GDMA = 0
    TYPE_HDMA = 1

    def __init__(self, mmu: MMU):
        self.mmu = mmu
        self.mmu.set_hdma(self)
        self.ticks = 0
        self.in_progress = False
        self.type = HDMA.TYPE_GDMA

    def request_hdma_transfer(self, request: int):
        self.in_progress = True
        self.type = (request >> 7) & 0x01
        self.length = ((request & 0b01111111) + 1) * 0x10
        self.msb_source_address = self.mmu.read_byte(IO_Registers.HDMA1)
        self.lsb_source_address = self.mmu.read_byte(IO_Registers.HDMA2) & 0b1111000
        self.msb_destination_address = self.mmu.read_byte(IO_Registers.HDMA3) & 0b00011111
        self.lsb_destination_address = self.mmu.read_byte(IO_Registers.HDMA4) & 0b1111000
        self.counter = 0x00
        self.ticks = 0
        self.mmu.write_byte(IO_Registers.HDMA5, request & 0b01111111, True) #DMA in progress
        print('DMA REQUEST (type:{} from:{:02x}{:02x} to:{:02x}{:02x} len:{:04x})'.format(self.type, self.msb_source_address, 
        self.lsb_source_address, self.msb_destination_address + 0x80, self.lsb_destination_address, self.length))

    
    def step(self):
        source_address = (self.msb_source_address << 8) + self.lsb_source_address + self.counter
        destination_address = 0x8000 + (self.msb_destination_address << 8) + self.lsb_destination_address + self.counter
        for i in range(0x10):
            self.mmu.write_byte(destination_address + i, self.mmu.read_byte(source_address + i))
        self.counter += 0x10
        
        self.ticks = 32
        if self.mmu.read_byte(IO_Registers.KEY1) & 0b10000000: #double speed mode
            self.ticks = 64
        remaining = self.length - self.counter
        if remaining == 0:
            self.mmu.write_byte(IO_Registers.HDMA5, 0xff, True) # HDMA is done
            self.in_progress = False
        else:
            self.mmu.write_byte(IO_Registers.HDMA5, int(remaining / 0x10) -1 , True)
                


