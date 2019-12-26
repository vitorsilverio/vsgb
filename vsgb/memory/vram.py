
class VideoRam:

    def __init__(self):
        self.ram = [[0x00]*0x2000, [0x00]*0x2000] 

    def write_value(self, address, bank, value):
        self.ram[bank][address - 0x8000] = value

    def read_value(self, address, bank):
        return self.ram[bank][address - 0x8000]
