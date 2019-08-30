import numpy as np
from src.mmu import MMU
from src.cpu import CPU

def test_registers():
    cpu = CPU(MMU(np.zeros(0x8000, dtype=np.uint8)))

    regmap = {
        'AF': ['A', 'F'],
        'BC': ['B', 'C'],
        'DE': ['D', 'E'],
        'HL': ['H', 'L']
    }

    for _16reg, _8regs in regmap.items():
        cpu.regs[_8regs[0]] = 0x55
        cpu.regs[_8regs[1]] = 0xAA
        assert cpu.get_reg_16(_16reg) == 0x55AA

        cpu.set_reg_16(_16reg, 0xAA55)
        assert cpu.regs[_8regs[0]] == 0xAA
        assert cpu.regs[_8regs[1]] == 0x55

    assert cpu.sp == 0x0000
    assert cpu.pc == 0x0000

### Test opcodes

# 8-bit loads

def test_LD_nn_n():
    # Map each register's opcode
    ops = {
        0x06: 'B',
        0x0E: 'C',
        0X16: 'D',
        0X1E: 'E',
        0X26: 'H',
        0X2E: 'L'
    }

    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0000] = op
        rom_file[0x0001] = 0xAA
        cpu = CPU(MMU(rom_file))
        cpu.tick()
        assert cpu.regs[reg] == 0xAA