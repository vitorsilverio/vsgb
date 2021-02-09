from vsgb.address_space import AddressSpace

class HighRam(AddressSpace):

    ram = [0]*0x80

    @classmethod
    def accept(cls, address: int) -> bool:
        return (0xff80 <= address < 0xffff)

    @classmethod
    def read(cls, address: int) -> int:
        return cls.ram[address - 0xff80]


    @classmethod
    def write(cls, address: int, value: int):
        cls.ram[address - 0xff80] = value