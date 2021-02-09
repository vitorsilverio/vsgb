from vsgb.address_space import AddressSpace
from vsgb.io_registers import IO_Registers

class WorkRam(AddressSpace):

    ram = [[0x00]*0x1000, [0x00]*0x1000, [0x00]*0x1000, [0x00]*0x1000, [0x00]*0x1000, [0x00]*0x1000, [0x00]*0x1000, [0x00]*0x1000 ]
    SVBK = 1

    @classmethod
    def accept(cls, address: int) -> bool:
        return (0xc000 <= address < 0xfe00) or (address == IO_Registers.SVBK)

    @classmethod
    def read(cls, address: int) -> int:
        if address == IO_Registers.SVBK:
            return cls.SVBK
        if address >= 0xe000:
            address -= 0x2000
        if address < 0xd000:
            return cls.ram[0][address - 0xc000]
        if cls.SVBK == 0:
            cls.SVBK = 1
        return cls.ram[cls.SVBK][address - 0xd000]


    @classmethod
    def write(cls, address: int, value: int):
        if address == IO_Registers.SVBK:
            cls.SVBK = value & 0b111
            return
        if address >= 0xe000:
            address -= 0x2000
        if address < 0xd000:
            cls.ram[0][address - 0xc000] = value
        else:
            if cls.SVBK == 0:
                cls.SVBK = 1
            cls.ram[cls.SVBK][address - 0xd000] = value

