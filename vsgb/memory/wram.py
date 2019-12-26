
class WorkRam:

    def __init__(self):
        self.ram = [[0x00]*0x1000, [0x00]*0x1000, [0x00]*0x1000, [0x00]*0x1000, [0x00]*0x1000, [0x00]*0x1000, [0x00]*0x1000, [0x00]*0x1000 ] 

    def write_value(self, address, bank, value):
        if address < 0xd000:
            self.ram[0][address - 0xc000] = value
        else:
            if bank == 0:
                bank = 1
            self.ram[bank][address - 0xd000] = value

    def read_value(self, address, bank):
        if address < 0xd000:
            return self.ram[0][address - 0xc000]
        if bank == 0:
            bank = 1
        return self.ram[bank][address - 0xd000]
