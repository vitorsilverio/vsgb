from vsgb.hardware.cpu import Cpu

cpu = Cpu()
cpu.IE = 0xffff
assert cpu.IE == 0x1f
assert 0xff0f in cpu
cpu[0xff0f] = 256
assert cpu.IF == 0
cpu.F = 0b0111_1111
assert cpu.F == 0x70
cpu.zero = True
assert cpu.F == 0xf0
print("x")