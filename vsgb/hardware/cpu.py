
from vsgb.hardware import Component 
from vsgb.descriptors import FlagBit, FlagRegister, Register


class Cpu(Component):

    #Internal Registers
    IE = FlagRegister(address=0xffff, mask=0x1f, mapping={"if_joypad":0x10, "if_serial":0x8, "if_timer":0x4, "if_stat":0x2, "if_vblank":0x1})
    IF = FlagRegister(address=0xff0f, mask=0x1f, mapping={"ie_joypad":0x10, "ie_serial":0x8, "ie_timer":0x4, "ie_stat":0x2, "ie_vblank":0x1})
    
    A = Register()
    B = Register()
    C = Register()
    D = Register()
    E = Register()
    F = Register()
    H = Register()
    L = Register()
    SP = Register(mask=0xffff)
    PC = Register(mask=0xffff)

    F = FlagRegister(mask=0xf0, mapping={"zero":0x80, "negative":0x40, "half":0x20, "carry":0x10})

    zero = FlagBit(register="F",bit=7)
    negative = FlagBit(register="F",bit=6)
    half = FlagBit(register="F",bit=5)
    carry = FlagBit(register="F",bit=4)

    if_joypad = FlagBit(register="IF", bit=4)
    if_serial = FlagBit(register="IF", bit=3)
    if_timer = FlagBit(register="IF", bit=2)
    if_stat = FlagBit(register="IF", bit=1) 
    if_vblank = FlagBit(register="IF", bit=0)

    ie_joypad = FlagBit(register="IE", bit=4)
    ie_serial = FlagBit(register="IE", bit=3)
    ie_timer = FlagBit(register="IE", bit=2)
    ie_stat = FlagBit(register="IE", bit=1) 
    ie_vblank = FlagBit(register="IE", bit=0)

    @property
    def AF(self) -> int:
        return (self.A << 8) | self.F

    @property
    def BC(self) -> int:
        return (self.B << 8) | self.C

    @property
    def DE(self) -> int:
        return (self.D << 8) | self.E

    @property
    def HL(self) -> int:
        return (self.H << 8) | self.L

    @AF.setter
    def AF(self, value) -> None:
        self.A = value >> 8
        self.F = value & 0xff

    @BC.setter
    def BC(self, value) -> None:
        self.B = value >> 8
        self.C = value & 0xff
    
    @DE.setter
    def DE(self, value) -> None:
        self.D = value >> 8
        self.E = value & 0xff

    @HL.setter
    def HL(self, value) -> None:
        self.H = value >> 8
        self.L = value & 0xff