class AddressSpace:

    @classmethod
    def accept(cls, address: int) -> bool:
        pass

    @classmethod
    def read(cls, address: int) -> int:
        return 0xff

    @classmethod
    def write(cls, address: int, value: int):
        pass