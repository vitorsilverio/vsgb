from vsgb.hardware import Component

class Register:

    def __init__(self, *, address=None, initial_value=0, mask=0xff):
        self.address = address
        self.initial_value = initial_value
        self.mask = mask

    def __set_name__(self, owner, name):
        self.name = name
        if self.address and issubclass(owner, Component):
            owner.addresses[self.address] = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value & self.mask

    def __get__(self, instance, owner=None):
        if not instance or self.name not in instance.__dict__:
            instance.__dict__[self.name] = self.initial_value
        return instance.__dict__[self.name]

class FlagRegister(Register):

    def __init__(self, mapping: dict[str, int], *args, **kwargs):
        super(FlagRegister, self).__init__(*args, **kwargs)
        self.mapping = mapping

    def __set__(self, instance, value):
        super(FlagRegister, self).__set__(instance, value)
        for field, mask in self.mapping.items():
            instance.__dict__[field] = bool(value & mask)

class FlagBit(Register):

    def __init__(self, register: str, bit: int, *args, **kwargs):
        super(FlagBit, self).__init__(*args, **kwargs)
        self.register = register
        self.bit = bit

    def __set__(self, instance, value):
        super(FlagBit, self).__set__(instance, value)
        mask = 1 << self.bit
        register_value = instance.__getattribute__(self.register) 
        # Clear bit
        register_value &= ~mask
        if value:
            register_value|= mask
        instance.__dict__[self.register] = register_value
        
