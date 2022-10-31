from dataclasses import dataclass

class Component:

    addresses = {}

    def __contains__(self, value):
        return value in Component.addresses.keys()

    def __getitem__(self, key):
        return self.__getattribute__(Component.addresses[key])

    def __setitem__(self, key, value):
        self.__setattr__(Component.addresses[key], value)

@dataclass
class AddressSpace:
    start_address: int
    size: int
    bind_field: str

    def __contains__(self, value):
        return self.start_address <= value < self.start_address + self.size

def MemoryComponent(Component):

    def __init__(self):
        super(MemoryComponent, self).__init__()
        self.spaces: list[AddressSpace] = []

    def __contains__(self, value):
        if super(MemoryComponent, self).__contains__(value):
            return True
        for space in self.spaces:
            if value in space:
                return True
        return False

    def __getitem__(self, key):
        if super(MemoryComponent, self).__contains__(key):
            return super(MemoryComponent, self).__getitem__(key)
        for space in self.spaces:
            if key in space:
                return self.__getattrib__(space.bind_field)[key-space.start_address]
        return 0

    def __setitem__(self, key, value):
        if super(MemoryComponent, self).__contains__(key):
            super(MemoryComponent, self).__setitem__(key, value)
        else:
            for space in self.spaces:
                if key in space:
                    self.__getattrib__(space.bind_field)[key-space.start_address] = value
                    break
