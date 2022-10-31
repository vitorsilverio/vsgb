from vsgb.hardware import Component 
from vsgb.descriptors import Register

class Input(Component):

    P1 = Register(address=0xff00, mask=0b0011_1111)