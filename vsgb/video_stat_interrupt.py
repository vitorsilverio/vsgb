from vsgb.interrupt_manager import Interrupt, InterruptManager

class VideoStatInterrupt:

    @staticmethod
    def check_stat(old, new):

        if (new & 0b01000100) & ((~old) & 0b01000100):
        #if (new & 0b01000100):
            InterruptManager.request_interrupt(Interrupt.INTERRUPT_LCDSTAT)
            return

        for i in range(3):
            #if (new & (1 << (3+i))) & ((~old) & (1 << (3+i))) and i == (new & 0b11):
            if (new & (1 << (3+i))) and i == (new & 0b11):
                InterruptManager.request_interrupt(Interrupt.INTERRUPT_LCDSTAT)
                return

