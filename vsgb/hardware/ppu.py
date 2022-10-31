from vsgb.hardware import MemoryComponent, AddressSpace
from vsgb.descriptors import Register

class Ppu(MemoryComponent):

    LY = Register(address=0xff44)
    STAT = Register(address=0xff41)
    LYC = Register(address=0xff45)
    SCX = Register(address=0xff43)
    SCY = Register(address=0xff42)
    BGP = Register(address=0xff47)
    WX = Register(address=0xff4b)
    WY = Register(address=0xff4a)
    LCDC = Register(address=0xff40)
    OBP0 = Register(address=0xff48)
    OBP1 = Register(address=0xff49)
    VBK = Register(address=0xff4f)
    BGPI = Register(address=0xff68)
    BGPD = Register(address=0xff69)
    OBPI = Register(address=0xff6b)
    OBPD = Register(address=0xff70)

    def __init__(self) -> None:
        super().__init__()
        self.vram = []
        self.oam = []
        self.spaces.append(AddressSpace(start_address=0x0000, size=0, bind_field="vram"))
        self.spaces.append(AddressSpace(start_address=0x0000, size=0, bind_field="oam"))