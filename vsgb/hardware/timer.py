from vsgb.hardware import Component 
from vsgb.descriptors import Register


class Timer(Component):

    KEY1 = Register(address=0xff4d)
    TIMA = Register(address=0xff04)
    TMA = Register(address=0xff05)
    DIV = Register(address=0xff06)
    TAC = Register(address=0xff07)