from vsgb.interrupt_manager import Interrupt

class VideoStatInterrupt:

    def __init__(self, interrupt_manager):
        self.interrupManager = interrupt_manager

    def check_stat(self, old, new):

        if (new & 0b01000100) & ((~old) & 0b01000100):
            self.interrupManager.request_interrupt(Interrupt.INTERRUPT_LCDSTAT)
            return

        for i in range(3):
            if (new & (1 << (3+i))) & ((~old) & (1 << (3+i))) and i == (new & 0b11):
                self.interrupManager.request_interrupt(Interrupt.INTERRUPT_LCDSTAT)
                return

