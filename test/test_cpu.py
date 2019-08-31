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
        cpu.set_reg_8(_8regs[0], 0x55)
        cpu.set_reg_8(_8regs[1], 0xAA)
        assert cpu.get_reg_16(_16reg) == 0x55AA

        cpu.set_reg_16(_16reg, 0xAA55)
        assert cpu.get_reg_8(_8regs[0]) == 0xAA
        assert cpu.get_reg_8(_8regs[1]) == 0x55

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
        assert cpu.get_reg_8(reg) == 0xAA

def test_LD_r1_r2():
    ops = {
        0x7F: ['A', 'A'],
        0x78: ['A', 'B'],
        0x79: ['A', 'C'],
        0x7A: ['A', 'D'],
        0x7B: ['A', 'E'],
        0x7C: ['A', 'H'],
        0x7D: ['A', 'L'],
        0x40: ['B', 'B'],
        0x41: ['B', 'C'],
        0x42: ['B', 'D'],
        0x43: ['B', 'E'],
        0x44: ['B', 'H'],
        0x45: ['B', 'L'],
        0x48: ['C', 'B'],
        0x49: ['C', 'C'],
        0x4A: ['C', 'D'],
        0x4B: ['C', 'E'],
        0x4C: ['C', 'H'],
        0x4D: ['C', 'L'],
        0x50: ['D', 'B'],
        0x51: ['D', 'C'],
        0x52: ['D', 'D'],
        0x53: ['D', 'E'],
        0x54: ['D', 'H'],
        0x55: ['D', 'L'],
        0x58: ['E', 'B'],
        0x59: ['E', 'C'],
        0x5A: ['E', 'D'],
        0x5B: ['E', 'E'],
        0x5C: ['E', 'H'],
        0x5D: ['E', 'L'],
        0x60: ['H', 'B'],
        0x61: ['H', 'C'],
        0x62: ['H', 'D'],
        0x63: ['H', 'E'],
        0x64: ['H', 'H'],
        0x65: ['H', 'L'],
        0x68: ['L', 'B'],
        0x69: ['L', 'C'],
        0x6A: ['L', 'D'],
        0x6B: ['L', 'E'],
        0x6C: ['L', 'H'],
        0x6D: ['L', 'L']
    }

    for op, regs in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0000] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(regs[1], 0xAA)
        cpu.tick()
        assert cpu.get_reg_8(regs[0]) == 0xAA

def test_LD_r_HL():
    ops = {
        0x7E: 'A',
        0x46: 'B',
        0x4E: 'C',
        0x56: 'D',
        0x5E: 'E',
        0x66: 'H',
        0x6E: 'L'
    }

    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0000] = op
        rom_file[0x0100] = 0xAA
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_16('HL', 0x0100)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0xAA

def test_LD_HL_r():
    ops = {
        0x70: 'B',
        0x71: 'C',
        0x72: 'D',
        0x73: 'E',
        0x74: 'H',
        0x75: 'L'
    }

    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0000] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0xAA)
        cpu.set_reg_16('HL', 0xC002)
        cpu.tick()
        assert cpu.mmu.get(0xC002) == cpu.get_reg_8(reg)

def test_LD_A_r():
    ops = {
        0x7F: 'A',
        0x78: 'B',
        0x79: 'C',
        0x7A: 'D',
        0x7B: 'E',
        0x7C: 'H',
        0x7D: 'L'
    }

    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0000] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0xAA)
        cpu.tick()
        assert cpu.get_reg_8('A') == 0xAA

def test_LD_A_rr():
    ops = {
        0x0A: 'BC',
        0x1A: 'DE',
        0x77: 'HL',
    }

    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0000] = op
        cpu = CPU(MMU(rom_file))
        cpu.mmu.set(0xC002, 0xAA)
        cpu.set_reg_16(reg, 0xC002)
        cpu.tick()
        assert cpu.get_reg_8('A') == 0xAA

def test_LD_A_nn():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0000] = 0xFA
    rom_file[0x0001] = 0x02
    rom_file[0x0002] = 0xC0
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC002, 0xAA)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xAA

def test_LD_A_n():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0000] = 0x3E
    rom_file[0x0001] = 0xAA
    cpu = CPU(MMU(rom_file))
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xAA