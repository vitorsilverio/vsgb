from typing import Callable

from vsgb.hardware.cpu import Cpu


class NoOperation:
    def __call__(self) -> int:
        return 4

class LoadRegister:
    def __init__(self, *, cpu: Cpu, dest: str, source: str) -> None:
        self.cpu = cpu
        self.dest = dest
        self.source = source
        
    def __call__(self) -> int:
        self.cpu[self.dest] = self.cpu[self.source]
        return 4

class IncrementWord:
    def __init__(self, *, cpu: Cpu, register: str) -> None:
        self.cpu = cpu
        self.register = register

    def __call__(self) -> int:
        self.cpu[self.register] += 1 
        return 4

class DecrementWord:
    def __init__(self, *, cpu: Cpu, register: str) -> None:
        self.cpu = cpu
        self.register = register

    def __call__(self) -> int:
        self.cpu[self.register] -= 1 

class IncrementByte:
    def __init__(self, *, cpu: Cpu, register: str) -> None:
        self.cpu = cpu
        self.register = register

    def __call__(self) -> int:
        self.cpu[self.register] += 1 
        return 4

class DecrementByte:
    def __init__(self, *, cpu: Cpu, register: str) -> None:
        self.cpu = cpu
        self.register = register

    def __call__(self) -> int:
        self.cpu[self.register] -= 1 

class Jump:
    def __init__(self, *, cpu: Cpu, condition: str) -> None:
        self.cpu = cpu
        self.condition = condition

    def __call__(self) -> int:
        ...

class JumpRelative:
    def __init__(self, *, cpu: Cpu, condition: str) -> None:
        self.cpu = cpu
        self.condition = condition

    def __call__(self) -> int:
        ...

class Call:
    def __init__(self, *, cpu: Cpu, condition: str) -> None:
        self.cpu = cpu
        self.condition = condition

    def __call__(self) -> int:
        ...

class Reset:
    def __init__(self, *, cpu: Cpu) -> None:
        self.cpu = cpu

    def __call__(self) -> int:
        ...

class Return:
    def __init__(self, *, cpu: Cpu) -> None:
        self.cpu = cpu

    def __call__(self) -> int:
        ...

class Add:
    def __init__(self, *, cpu: Cpu) -> None:
        self.cpu = cpu

    def __call__(self) -> int:
        ...

class Sub:
    def __init__(self, *, cpu: Cpu) -> None:
        self.cpu = cpu

    def __call__(self) -> int:
        ...

class And:
    def __init__(self, *, cpu: Cpu) -> None:
        self.cpu = cpu

    def __call__(self) -> int:
        ...

class Or:
    def __init__(self, *, cpu: Cpu) -> None:
        self.cpu = cpu

    def __call__(self) -> int:
        ...

class Xor:
    def __init__(self, *, cpu: Cpu) -> None:
        self.cpu = cpu

    def __call__(self) -> int:
        ...

class Push:
    def __init__(self, *, cpu: Cpu) -> None:
        self.cpu = cpu

    def __call__(self) -> int:
        ...

class Pop:
    def __init__(self, *, cpu: Cpu) -> None:
        self.cpu = cpu

    def __call__(self) -> int:
        ...


def inicialize_instructions(cpu: Cpu) -> list[Callable]:
    instructions = [
        NoOperation(), 
    ]

    return instructions