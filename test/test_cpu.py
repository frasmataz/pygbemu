import numpy as np
from mmu import MMU
from cpu import CPU

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

    assert cpu.sp == 0xFFFE
    assert cpu.pc == 0x0100

def test_flags():
    flags = ['Z', 'N', 'H', 'C']
    cpu = CPU(MMU(np.zeros(0x8000, dtype=np.uint8)))

    for flag in flags:
        cpu.set_flag(flag, 1)
        assert cpu.get_flag(flag) == 1
        cpu.set_flag(flag, 0)
        assert cpu.get_flag(flag) == 0

def test_add_8():
    cpu = CPU(MMU(np.zeros(0x8000, dtype=np.uint8)))
    assert cpu.add_8(0x11, 0x22) == 0x33
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0
    assert cpu.add_8(0xFF, 0x01) == 0x00
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 1
    assert cpu.add_8(0x0F, 0x01) == 0x10
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0
    assert cpu.add_8(0xF0, 0x10) == 0x00
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_add_16():
    cpu = CPU(MMU(np.zeros(0x8000, dtype=np.uint8)))
    assert cpu.add_16(0x1111, 0x2222) == 0x3333
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0
    assert cpu.add_16(0xFFFF, 0x0001) == 0x0000
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 1
    assert cpu.add_16(0x0F00, 0x0100) == 0x1000
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0
    assert cpu.add_16(0xF000, 0x1000) == 0x0000
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_sub_8():
    cpu = CPU(MMU(np.zeros(0x8000, dtype=np.uint8)))
    assert cpu.sub_8(0x33, 0x22) == 0x11
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0
    assert cpu.sub_8(0x00, 0x01) == 0xFF
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 1
    assert cpu.sub_8(0x10, 0x01) == 0x0F
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0
    assert cpu.sub_8(0x00, 0x10) == 0xF0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_sub_16():
    cpu = CPU(MMU(np.zeros(0x8000, dtype=np.uint8)))
    assert cpu.sub_16(0x3333, 0x2222) == 0x1111
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0
    assert cpu.sub_16(0x0000, 0x0001) == 0xFFFF
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 1
    assert cpu.sub_16(0x1000, 0x0001) == 0x0FFF
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0
    assert cpu.sub_16(0x0000, 0x1000) == 0xF000
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

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
        rom_file[0x0100] = op
        rom_file[0x0101] = 0xAA
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
        rom_file[0x0100] = op
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
        rom_file[0x0100] = op
        rom_file[0x0200] = 0xAA
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_16('HL', 0x0200)
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
        rom_file[0x0100] = op
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
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0xAA)
        cpu.tick()
        assert cpu.get_reg_8('A') == 0xAA

def test_LD_A_rr():
    ops = {
        0x0A: 'BC',
        0x1A: 'DE',
        0x7E: 'HL'
    }

    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.mmu.set(0xC002, 0xAA)
        cpu.set_reg_16(reg, 0xC002)
        cpu.tick()
        assert cpu.get_reg_8('A') == 0xAA

def test_LD_A_nn():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xFA
    rom_file[0x0101] = 0x02
    rom_file[0x0102] = 0xC0
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC002, 0xAA)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xAA

def test_LD_A_n():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x3E
    rom_file[0x0101] = 0xAA
    cpu = CPU(MMU(rom_file))
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xAA

def test_LD_n_A():
    ops = {
        0x7F: 'A',
        0x47: 'B',
        0x4F: 'C',
        0x57: 'D',
        0x5F: 'E',
        0x67: 'H',
        0x6F: 'L'
    }

    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8('A', 0xAA)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0xAA

def test_LD_rr_A():
    ops = {
        0x02: 'BC',
        0x12: 'DE',
        0x77: 'HL'
    }

    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8('A', 0xAA)
        cpu.set_reg_16(reg, 0xC002)
        cpu.tick()
        assert cpu.mmu.get(0xC002) == 0xAA

def test_LD_nn_A():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xEA
    rom_file[0x0101] = 0x02
    rom_file[0x0102] = 0xC0
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xAA)
    cpu.tick()
    assert cpu.mmu.get(0xC002) == 0xAA

def test_LD_A_C():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xF2
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('C', 0x24)
    cpu.mmu.set(0xFF24, 0xAA)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xAA

def test_LD_C_A():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xE2
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xAA)
    cpu.set_reg_8('C', 0x24)
    cpu.tick()
    assert cpu.mmu.get(0xFF24) == 0xAA

def test_LDD_A_HL():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x3A
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0xC002)
    cpu.mmu.set(0xC002, 0xAA)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xAA
    assert cpu.get_reg_16('HL') == 0xC001

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x3A
    rom_file[0x0000] = 0x69
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0x0000)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x69
    assert cpu.get_reg_16('HL') == 0xFFFF

def test_LDD_HL_A():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x32
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0xC002)
    cpu.set_reg_8('A', 0xAA)
    cpu.tick()
    assert cpu.mmu.get(0xC002) == 0xAA
    assert cpu.get_reg_16('HL') == 0xC001

def test_LDI_A_HL():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x2A
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0xC002)
    cpu.mmu.set(0xC002, 0xAA)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xAA
    assert cpu.get_reg_16('HL') == 0xC003

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x2A
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0xFFFF)
    cpu.tick()
    assert cpu.get_reg_16('HL') == 0x0000

def test_LDI_HL_A():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x22
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0xC002)
    cpu.set_reg_8('A', 0xAA)
    cpu.tick()
    assert cpu.mmu.get(0xC002) == 0xAA
    assert cpu.get_reg_16('HL') == 0xC003

def test_LDH_n_A():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xE0
    rom_file[0x0101] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xAA)
    cpu.tick()
    assert cpu.mmu.get(0xFF12) == 0xAA

def test_LDH_A_n():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xF0
    rom_file[0x0101] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xFF12, 0xAA)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xAA

# 16-bit loads

def test_LD_n_nn():
    ops = {
        0x01: 'BC',
        0x11: 'DE',
        0x21: 'HL',
        0x31: 'SP'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        rom_file[0x0101] = 0x34
        rom_file[0x0102] = 0x12
        cpu = CPU(MMU(rom_file))
        cpu.tick()
        assert cpu.get_reg_16(reg) == 0x1234

def test_LD_SP_HL():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xF9
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0x1234)
    cpu.tick()
    assert cpu.get_reg_16('SP') == 0x1234

def test_LD_HL_SPn():
    # Test no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xF8
    rom_file[0x0101] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('SP', 0x1234)
    cpu.tick()
    assert cpu.get_reg_16('HL') == 0x1246
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test half-carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xF8
    rom_file[0x0101] = 0x01
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('SP', 0x0FFF)
    cpu.tick()
    assert cpu.get_reg_16('HL') == 0x1000
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

    # Test full-carry and zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xF8
    rom_file[0x0101] = 0x01
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('SP', 0xFFFF)
    cpu.tick()
    assert cpu.get_reg_16('HL') == 0x0000
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 1

def test_LD_nn_SP():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x08
    rom_file[0x0101] = 0x02
    rom_file[0x0102] = 0xC0
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('SP', 0xAABB)
    cpu.tick()
    assert cpu.mmu.get(0xC002) == 0xBB
    assert cpu.mmu.get(0xC003) == 0xAA

def test_PUSH_nn():
    ops = {
        0xF5: 'AF',
        0xC5: 'BC',
        0xD5: 'DE',
        0xE5: 'HL'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_16(reg, 0xAABB)
        cpu.set_reg_16('SP', 0xC002)
        cpu.tick()
        assert cpu.mmu.get(0xC001) == 0xAA
        assert cpu.mmu.get(0xC000) == 0xBB
        assert cpu.get_reg_16('SP') == 0xC000

def test_POP_nn():
    ops = {
        0xF1: 'AF',
        0xC1: 'BC',
        0xD1: 'DE',
        0xE1: 'HL'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        rom_file[0x00F0] = 0xBB
        rom_file[0x00F1] = 0xAA
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_16('SP', 0x00F0)
        cpu.tick()
        assert cpu.get_reg_16(reg) == 0xAABB
        assert cpu.get_reg_16('SP') == 0x00F2

# 8-bit ALU

def test_ADD_A_n():
    # Add A to itself
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x87
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x11)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x22
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Other registers
    ops = {
        0x80: 'B',
        0x81: 'C',
        0x82: 'D',
        0x83: 'E',
        0x84: 'H',
        0x85: 'L'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8('A', 0x11)
        cpu.set_reg_8(reg, 0x22)
        cpu.tick()
        assert cpu.get_reg_8('A') == 0x33
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

    # (HL)
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x86
    rom_file[0x0123] = 0x22
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x11)
    cpu.set_reg_16('HL', 0x0123)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x33
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Immediate value
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC6
    rom_file[0x0101] = 0x22
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x11)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x33
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test half-carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC6
    rom_file[0x0101] = 0x01
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x0F)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x10
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

    # Test full-carry and zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC6
    rom_file[0x0101] = 0x10
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xF0)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_ADC_A_n():
    # Add A to itself
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x8F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x11)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x23
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Other registers
    ops = {
        0x88: 'B',
        0x89: 'C',
        0x8A: 'D',
        0x8B: 'E',
        0x8C: 'H',
        0x8D: 'L'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8('A', 0x11)
        cpu.set_flag('C', 1)
        cpu.set_reg_8(reg, 0x22)
        cpu.tick()
        assert cpu.get_reg_8('A') == 0x34
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

    # (HL)
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x8E
    rom_file[0x0123] = 0x22
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x11)
    cpu.set_flag('C', 1)
    cpu.set_reg_16('HL', 0x0123)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x34
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Immediate value
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCE
    rom_file[0x0101] = 0x22
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x11)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x34
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test half-carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCE
    rom_file[0x0101] = 0x01
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x0E)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x10
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

    # Test full-carry and zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCE
    rom_file[0x0101] = 0x0F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xF0)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 1

def test_SUB_n():
    # Sub A from itself
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x97
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x11)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Other registers
    ops = {
        0x90: 'B',
        0x91: 'C',
        0x92: 'D',
        0x93: 'E',
        0x94: 'H',
        0x95: 'L'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8('A', 0x33)
        cpu.set_reg_8(reg, 0x22)
        cpu.tick()
        assert cpu.get_reg_8('A') == 0x11
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 1
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

    # (HL)
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x96
    rom_file[0x0123] = 0x22
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x33)
    cpu.set_reg_16('HL', 0x0123)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x11
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Immediate value
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xD6
    rom_file[0x0101] = 0x22
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x33)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x11
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test half-carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xD6
    rom_file[0x0101] = 0x01
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x10)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x0F
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

    # Test full-carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xD6
    rom_file[0x0101] = 0x10
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x00)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xF0
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_SBC_n():
    # Sub A from itself
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x9F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x11)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xFF
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 1

    # Other registers
    ops = {
        0x98: 'B',
        0x99: 'C',
        0x9A: 'D',
        0x9B: 'E',
        0x9C: 'H',
        0x9D: 'L'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8('A', 0x33)
        cpu.set_reg_8(reg, 0x22)
        cpu.set_flag('C', 1)
        cpu.tick()
        assert cpu.get_reg_8('A') == 0x10
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 1
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

    # (HL)
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x9E
    rom_file[0x0123] = 0x22
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x33)
    cpu.set_reg_16('HL', 0x0123)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x10
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Immediate value
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xDE
    rom_file[0x0101] = 0x22
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x33)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x10
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test half-carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xDE
    rom_file[0x0101] = 0x01
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x11)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x0F
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

    # Test full-carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xDE
    rom_file[0x0101] = 0x0F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x00)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xF0
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 1

def test_AND_n():
    # A
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xA7
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xCC)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xCC
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

    # Other registers
    ops = {
        0xA0: 'B',
        0xA1: 'C',
        0xA2: 'D',
        0xA3: 'E',
        0xA4: 'H',
        0xA5: 'L'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8('A', 0xCC)
        cpu.set_reg_8(reg, 0xAA)
        cpu.tick()
        assert cpu.get_reg_8('A') == 0x88
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 1
        assert cpu.get_flag('C') == 0

    # (HL)
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xA6
    rom_file[0x0123] = 0xAA
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xCC)
    cpu.set_reg_16('HL', 0x0123)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x88
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

    # Immediate value
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xE6
    rom_file[0x0101] = 0xAA
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xCC)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x88
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

    # Test zero flag
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xE6
    rom_file[0x0101] = 0xAA
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x55)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

def test_OR_n():
    # A
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xB7
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xCC)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xCC
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Other registers
    ops = {
        0xB0: 'B',
        0xB1: 'C',
        0xB2: 'D',
        0xB3: 'E',
        0xB4: 'H',
        0xB5: 'L'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8('A', 0xCC)
        cpu.set_reg_8(reg, 0xAA)
        cpu.tick()
        assert cpu.get_reg_8('A') == 0xEE
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

    # (HL)
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xB6
    rom_file[0x0123] = 0xAA
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xCC)
    cpu.set_reg_16('HL', 0x0123)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xEE
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Immediate value
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xF6
    rom_file[0x0101] = 0xAA
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xCC)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xEE
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test zero flag
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xF6
    rom_file[0x0101] = 0x00
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x00)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

def test_XOR_n():
    # A
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xAF
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xCC)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Other registers
    ops = {
        0xA8: 'B',
        0xA9: 'C',
        0xAA: 'D',
        0xAB: 'E',
        0xAC: 'H',
        0xAD: 'L'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8('A', 0xCC)
        cpu.set_reg_8(reg, 0xAA)
        cpu.tick()
        assert cpu.get_reg_8('A') == 0x66
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

    # (HL)
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xAE
    rom_file[0x0123] = 0xAA
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xCC)
    cpu.set_reg_16('HL', 0x0123)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x66
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Immediate value
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xEE
    rom_file[0x0101] = 0xAA
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xCC)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x66
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

def test_CP_n():
    # A
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xBF
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x10)
    cpu.tick()
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Other registers
    ops = {
        0xB8: 'B',
        0xB9: 'C',
        0xBA: 'D',
        0xBB: 'E',
        0xBC: 'H',
        0xBD: 'L'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8('A', 0x10)
        cpu.set_reg_8(reg, 0x10)
        cpu.tick()
        assert cpu.get_flag('Z') == 1
        assert cpu.get_flag('N') == 1
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8('A', 0x10)
        cpu.set_reg_8(reg, 0x0F)
        cpu.tick()
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 1
        assert cpu.get_flag('H') == 1
        assert cpu.get_flag('C') == 0

        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8('A', 0x10)
        cpu.set_reg_8(reg, 0x11)
        cpu.tick()
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 1
        assert cpu.get_flag('H') == 1
        assert cpu.get_flag('C') == 1

    # (HL)
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xBE
    rom_file[0x0123] = 0x10
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x10)
    cpu.set_reg_16('HL', 0x0123)
    cpu.tick()
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xBE
    rom_file[0x0123] = 0x0F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x10)
    cpu.set_reg_16('HL', 0x0123)
    cpu.tick()
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xBE
    rom_file[0x0123] = 0x11
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x10)
    cpu.set_reg_16('HL', 0x0123)
    cpu.tick()
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 1

    # Immediate value
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xFE
    rom_file[0x0101] = 0x10
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x10)
    cpu.tick()
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xFE
    rom_file[0x0101] = 0x0F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x10)
    cpu.tick()
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xFE
    rom_file[0x0101] = 0x11
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x10)
    cpu.tick()
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 1

def test_INC_n():
    ops = {
        0x3C: 'A',
        0x04: 'B',
        0x0C: 'C',
        0x14: 'D',
        0x1C: 'E',
        0x24: 'H',
        0x2C: 'L'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x01)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x02
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0

        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x0F)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x10
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 1

        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0xFF)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x00
        assert cpu.get_flag('Z') == 1
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 1

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x34
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC000, 0x01)
    cpu.set_reg_16('HL', 0xC000)
    cpu.tick()
    assert cpu.mmu.get(0xC000) == 0x02
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x34
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC000, 0x0F)
    cpu.set_reg_16('HL', 0xC000)
    cpu.tick()
    assert cpu.mmu.get(0xC000) == 0x10
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x34
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC000, 0xFF)
    cpu.set_reg_16('HL', 0xC000)
    cpu.tick()
    assert cpu.mmu.get(0xC000) == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1

def test_DEC_n():
    ops = {
        0x3D: 'A',
        0x05: 'B',
        0x0D: 'C',
        0x15: 'D',
        0x1D: 'E',
        0x25: 'H',
        0x2D: 'L'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x02)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x01
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 1
        assert cpu.get_flag('H') == 0

        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x10)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x0F
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 1
        assert cpu.get_flag('H') == 1

        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x00)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0xFF
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 1
        assert cpu.get_flag('H') == 1

        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x01)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x00
        assert cpu.get_flag('Z') == 1
        assert cpu.get_flag('N') == 1
        assert cpu.get_flag('H') == 0

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x35
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC000, 0x02)
    cpu.set_reg_16('HL', 0xC000)
    cpu.tick()
    assert cpu.mmu.get(0xC000) == 0x01
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 0

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x35
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC000, 0x10)
    cpu.set_reg_16('HL', 0xC000)
    cpu.tick()
    assert cpu.mmu.get(0xC000) == 0x0F
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 1

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x35
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC000, 0x00)
    cpu.set_reg_16('HL', 0xC000)
    cpu.tick()
    assert cpu.mmu.get(0xC000) == 0xFF
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 1

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x35
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC000, 0x01)
    cpu.set_reg_16('HL', 0xC000)
    cpu.tick()
    assert cpu.mmu.get(0xC000) == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 0

# 16-bit ALU

def test_ADD_HL_n():
    # Test each source register
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x09
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0x1122)
    cpu.set_reg_16('BC', 0x3344)
    cpu.tick()
    assert cpu.get_reg_16('HL') == 0x4466
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x19
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0x1122)
    cpu.set_reg_16('DE', 0x3344)
    cpu.tick()
    assert cpu.get_reg_16('HL') == 0x4466
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x29
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0x1122)
    cpu.tick()
    assert cpu.get_reg_16('HL') == 0x2244
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x39
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0x1122)
    cpu.set_reg_16('SP', 0x3344)
    cpu.tick()
    assert cpu.get_reg_16('HL') == 0x4466
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    #Test half-carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x09
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0x0F00)
    cpu.set_reg_16('BC', 0x0100)
    cpu.tick()
    assert cpu.get_reg_16('HL') == 0x1000
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

    #Test full-carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x09
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0xF000)
    cpu.set_reg_16('BC', 0x1000)
    cpu.tick()
    assert cpu.get_reg_16('HL') == 0x0000
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_ADD_SP_n():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xE8
    rom_file[0x0101] = 0x44
    rom_file[0x0102] = 0x33
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('SP', 0x1122)
    cpu.tick()
    assert cpu.get_reg_16('SP') == 0x4466
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    #Test half-carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xE8
    rom_file[0x0101] = 0x00
    rom_file[0x0102] = 0x01
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('SP', 0x0F00)
    cpu.tick()
    assert cpu.get_reg_16('SP') == 0x1000
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 1
    assert cpu.get_flag('C') == 0

    #Test full-carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xE8
    rom_file[0x0101] = 0x00
    rom_file[0x0102] = 0x10
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('SP', 0xF000)
    cpu.tick()
    assert cpu.get_reg_16('SP') == 0x0000
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_INC_nn():
    ops = {
        0x03: 'BC',
        0x13: 'DE',
        0x23: 'HL',
        0x33: 'SP'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_16(reg, 0x1111)
        cpu.tick()
        assert cpu.get_reg_16(reg) == 0x1112

def test_DEC_nn():
    ops = {
        0x0B: 'BC',
        0x1B: 'DE',
        0x2B: 'HL',
        0x3B: 'SP'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_16(reg, 0x1111)
        cpu.tick()
        assert cpu.get_reg_16(reg) == 0x1110

# Misc

def test_SWAP_n():
    # Note - This is a two-opcode instruction
    # First 0xCB, then a second opcode for the target
    ops = {
        0x37: 'A',
        0x30: 'B',
        0x31: 'C',
        0x32: 'D',
        0x33: 'E',
        0x34: 'H',
        0x35: 'L'
    }
    for op, reg in ops.items():
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0xAB)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0xBA

    # (HL)
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x36
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0xC001)
    cpu.mmu.set(0xC001, 0xAB)
    cpu.tick()
    assert cpu.mmu.get(0xC001) == 0xBA

def test_DAA():
    # Set/reset N flag to test post add/subtract DAA respectively
    # Addition
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x27
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x0C)
    cpu.set_flag('N', 0)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x12
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x27
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xC0)
    cpu.set_flag('N', 0)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x20
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x27
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x10)
    cpu.set_flag('N', 0)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x70
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x27
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x11)
    cpu.set_flag('N', 0)
    cpu.set_flag('H', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x17
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Subtraction
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x27
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xE0)
    cpu.set_flag('N', 1)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x80
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x27
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x0E)
    cpu.set_flag('N', 1)
    cpu.set_flag('H', 1)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x08
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x27
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x00)
    cpu.set_flag('N', 0)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test an actual addition
    rom_file = np.zeros(0x8000, dtype=np.uint8)

    rom_file[0x0100] = 0x3E # LD A, 0x90
    rom_file[0x0101] = 0x90
    rom_file[0x0102] = 0xC6 # ADD A, 0x80
    rom_file[0x0103] = 0x80
    rom_file[0x0104] = 0x27 # DAA

    cpu = CPU(MMU(rom_file))

    # Tick 3 times
    cpu.tick()
    cpu.tick()
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x70
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_CPL():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x2F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0xCA)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x35
    assert cpu.get_flag('N') == 1
    assert cpu.get_flag('H') == 1

def test_CCF():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x3F
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 0)
    cpu.tick()
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x3F
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

def test_SCF():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x37
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 0)
    cpu.tick()
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_NOP():
    # This feels like a weird test
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x00
    cpu = CPU(MMU(rom_file))
    cpu.tick()
    assert cpu.get_reg_16('PC') == 0x0101

# Rotates

def test_RLCA():
    # Test carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x07
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x96)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x2D
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x07
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x69)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xD2
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x07
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x00)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

def test_RLA():
    # Test no carry -> carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x17
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x96)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x2C
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test no carry -> no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x17
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x69)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xD2
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test carry -> carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x17
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 1)
    cpu.set_reg_8('A', 0x96)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x2D
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test carry -> no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x17
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 1)
    cpu.set_reg_8('A', 0x69)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xD3
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x17
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x80)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_RRCA():
    # Test no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x0F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x96)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x4B
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x0F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x69)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xB4
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x0F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x00)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

def test_RRA():
    # Test no carry -> no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x1F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x96)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x4B
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test no carry -> carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x1F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x69)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x34
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test carry -> no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x1F
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 1)
    cpu.set_reg_8('A', 0x96)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xCB
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test carry -> carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x1F
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 1)
    cpu.set_reg_8('A', 0x69)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0xB4
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x1F
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_8('A', 0x01)
    cpu.tick()
    assert cpu.get_reg_8('A') == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_RLC_n():
    ops = {
        0x07: 'A',
        0x00: 'B',
        0x01: 'C',
        0x02: 'D',
        0x03: 'E',
        0x04: 'H',
        0x05: 'L'
    }

    for op, reg in ops.items():
        # Test carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x96)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x2D
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

        # Test no carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x69)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0xD2
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

        # Test zero
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x00)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x00
        assert cpu.get_flag('Z') == 1
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

def test_RL_n():
    ops = {
        0x17: 'A',
        0x10: 'B',
        0x11: 'C',
        0x12: 'D',
        0x13: 'E',
        0x14: 'H',
        0x15: 'L'
    }

    for op, reg in ops.items():
        # Test no carry -> carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x96)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x2C
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

        # Test no carry -> no carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x69)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0xD2
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

        # Test carry -> carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_flag('C', 1)
        cpu.set_reg_8(reg, 0x96)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x2D
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

        # Test carry -> no carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_flag('C', 1)
        cpu.set_reg_8(reg, 0x69)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0xD3
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

        # Test zero
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x80)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x00
        assert cpu.get_flag('Z') == 1
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

def test_RRC_n():
    ops = {
        0x0F: 'A',
        0x08: 'B',
        0x09: 'C',
        0x0A: 'D',
        0x0B: 'E',
        0x0C: 'H',
        0x0D: 'L'
    }

    for op, reg in ops.items():
        # Test no carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x96)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x4B
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

        # Test carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x69)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0xB4
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

        # Test zero
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x00)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x00
        assert cpu.get_flag('Z') == 1
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

def test_RR_n():
    ops = {
        0x1F: 'A',
        0x18: 'B',
        0x19: 'C',
        0x1A: 'D',
        0x1B: 'E',
        0x1C: 'H',
        0x1D: 'L'
    }

    for op, reg in ops.items():
        # Test no carry -> no carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x96)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x4B
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

        # Test no carry -> carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x69)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x34
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

        # Test carry -> no carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_flag('C', 1)
        cpu.set_reg_8(reg, 0x96)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0xCB
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

        # Test carry -> carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_flag('C', 1)
        cpu.set_reg_8(reg, 0x69)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0xB4
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

        # Test zero
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x01)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x00
        assert cpu.get_flag('Z') == 1
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

def test_RLC_HL():
    # Test carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x06
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x96)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x2D
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x06
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x69)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0xD2
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x06
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x00)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

def test_RL_HL():
    # Test no carry -> carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x16
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x96)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x2C
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test no carry -> no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x16
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x69)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0xD2
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test carry -> carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x16
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x96)
    cpu.set_reg_16('HL', 0xC123)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x2D
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test carry -> no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x16
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x69)
    cpu.set_reg_16('HL', 0xC123)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0xD3
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x16
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x80)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_RRC_HL():
    # Test no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x0E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x96)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x4B
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x0E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x69)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0xB4
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x0E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x00)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

def test_RR_HL():
    # Test no carry -> no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x1E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x96)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x4B
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test no carry -> carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x1E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x69)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x34
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test carry -> no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x1E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x96)
    cpu.set_flag('C', 1)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0xCB
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test carry -> carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x1E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x69)
    cpu.set_flag('C', 1)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0xB4
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x1E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x01)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

# Shifts

def test_SLA_n():
    ops = {
        0x27: 'A',
        0x20: 'B',
        0x21: 'C',
        0x22: 'D',
        0x23: 'E',
        0x24: 'H',
        0x25: 'L'
    }

    for op, reg in ops.items():
        # Test carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x96)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x2C
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

        # Test no carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x69)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0xD2
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

        # Test zero
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x80)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x00
        assert cpu.get_flag('Z') == 1
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

def test_SRA_n():
    ops = {
        0x2F: 'A',
        0x28: 'B',
        0x29: 'C',
        0x2A: 'D',
        0x2B: 'E',
        0x2C: 'H',
        0x2D: 'L'
    }

    for op, reg in ops.items():
        # Test no carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x96)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0xCB
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

        # Test carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x69)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x34
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

        # Test zero
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x01)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x00
        assert cpu.get_flag('Z') == 1
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

def test_SRL_n():
    ops = {
        0x3F: 'A',
        0x38: 'B',
        0x39: 'C',
        0x3A: 'D',
        0x3B: 'E',
        0x3C: 'H',
        0x3D: 'L'
    }

    for op, reg in ops.items():
        # Test carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x96)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x4B
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 0

        # Test no carry
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x69)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x34
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

        # Test zero
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = op
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_8(reg, 0x01)
        cpu.tick()
        assert cpu.get_reg_8(reg) == 0x00
        assert cpu.get_flag('Z') == 1
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 0
        assert cpu.get_flag('C') == 1

def test_SLAs_HL():
    # Test carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x26
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x96)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x2C
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x26
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x69)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0xD2
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x26
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x80)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_SRA_HL():
    # Test no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x2E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x96)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0xCB
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x2E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x69)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x34
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x2E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x01)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

def test_SRL_HL():
    # Test no carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x3E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x96)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x4B
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 0

    # Test carry
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x3E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x69)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x34
    assert cpu.get_flag('Z') == 0
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

    # Test zero
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCB
    rom_file[0x0101] = 0x3E
    cpu = CPU(MMU(rom_file))
    cpu.mmu.set(0xC123, 0x01)
    cpu.set_reg_16('HL', 0xC123)
    cpu.tick()
    assert cpu.mmu.get(0xC123) == 0x00
    assert cpu.get_flag('Z') == 1
    assert cpu.get_flag('N') == 0
    assert cpu.get_flag('H') == 0
    assert cpu.get_flag('C') == 1

# Bit functions

def test_BIT():
    ops = {
        0x47: 'A',
        0x40: 'B',
        0x41: 'C',
        0x42: 'D',
        0x43: 'E',
        0x44: 'H',
        0x45: 'L'
    }

    for op, reg in ops.items():
        for i in range(0, 7):
            # Test for positive bit
            rom_file = np.zeros(0x8000, dtype=np.uint8)
            rom_file[0x0100] = 0xCB
            rom_file[0x0101] = op + (i * 0x08)
            cpu = CPU(MMU(rom_file))
            cpu.set_reg_8(reg, 0x01 << i)
            cpu.tick()
            assert cpu.get_flag('Z') == 0
            assert cpu.get_flag('N') == 0
            assert cpu.get_flag('H') == 1

            # Test for negative bit
            rom_file = np.zeros(0x8000, dtype=np.uint8)
            rom_file[0x0100] = 0xCB
            rom_file[0x0101] = op + (i * 0x08)
            cpu = CPU(MMU(rom_file))
            cpu.set_reg_8(reg, (0x01 << i) ^ 0xFF)
            cpu.tick()
            assert cpu.get_flag('Z') == 1
            assert cpu.get_flag('N') == 0
            assert cpu.get_flag('H') == 1

    for i in range(0, 7):
        # (HL)
        # Test for positive bit
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = 0x46 + (i * 0x08)
        cpu = CPU(MMU(rom_file))
        cpu.mmu.set(0xC123, 0x01 << i)
        cpu.set_reg_16('HL', 0xC123)
        cpu.tick()
        assert cpu.get_flag('Z') == 0
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 1

        # Test for negative bit
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = 0x46 + (i * 0x08)
        cpu = CPU(MMU(rom_file))
        cpu.mmu.set(0xC123, (0x01 << i) ^ 0xFF)
        cpu.set_reg_16('HL', 0xC123)
        cpu.tick()
        assert cpu.get_flag('Z') == 1
        assert cpu.get_flag('N') == 0
        assert cpu.get_flag('H') == 1

def test_SET():
    ops = {
        0xC7: 'A',
        0xC0: 'B',
        0xC1: 'C',
        0xC2: 'D',
        0xC3: 'E',
        0xC4: 'H',
        0xC5: 'L'
    }

    for op, reg in ops.items():
        for i in range(0, 7):
            # Test for positive bit
            rom_file = np.zeros(0x8000, dtype=np.uint8)
            rom_file[0x0100] = 0xCB
            rom_file[0x0101] = op + (i * 0x08)
            cpu = CPU(MMU(rom_file))
            cpu.tick()
            assert cpu.get_reg_8(reg) == 0x01 << i

    for i in range(0, 7):
        # (HL)
        # Test for positive bit
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = 0xC6 + (i * 0x08)
        cpu = CPU(MMU(rom_file))
        cpu.set_reg_16('HL', 0xC123)
        cpu.tick()
        assert cpu.mmu.get(cpu.get_reg_16('HL')) == 0x01 << i

def test_RES():
    ops = {
        0x87: 'A',
        0x80: 'B',
        0x81: 'C',
        0x82: 'D',
        0x83: 'E',
        0x84: 'H',
        0x85: 'L'
    }

    for op, reg in ops.items():
        for i in range(0, 7):
            # Test for positive bit
            rom_file = np.zeros(0x8000, dtype=np.uint8)
            rom_file[0x0100] = 0xCB
            rom_file[0x0101] = op + (i * 0x08)
            cpu = CPU(MMU(rom_file))
            cpu.set_reg_8(reg, 0xFF)
            cpu.tick()
            assert cpu.get_reg_8(reg) == (0x01 << i) ^ 0xFF

    for i in range(0, 7):
        # (HL)
        # Test for positive bit
        rom_file = np.zeros(0x8000, dtype=np.uint8)
        rom_file[0x0100] = 0xCB
        rom_file[0x0101] = 0x86 + (i * 0x08)
        cpu = CPU(MMU(rom_file))
        cpu.mmu.set(0xC123, 0xFF)
        cpu.set_reg_16('HL', 0xC123)
        cpu.tick()
        assert cpu.mmu.get(cpu.get_reg_16('HL')) == (0x01 << i) ^ 0xFF

# Jumps

def test_JP_nn():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC3
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.tick()
    assert cpu.pc == 0x1234

def test_JP_cc_nn():
    # NZ
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC2
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('Z', 0)
    cpu.tick()
    assert cpu.pc == 0x1234

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC2
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('Z', 1)
    cpu.tick()
    assert cpu.pc == 0x0103

    # Z
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCA
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('Z', 0)
    cpu.tick()
    assert cpu.pc == 0x0103

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCA
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('Z', 1)
    cpu.tick()
    assert cpu.pc == 0x1234

    # NC
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xD2
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 0)
    cpu.tick()
    assert cpu.pc == 0x1234

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xD2
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.pc == 0x0103

    # C
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xDA
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 0)
    cpu.tick()
    assert cpu.pc == 0x0103

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xDA
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.pc == 0x1234

def test_JP_HL():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xE9
    cpu = CPU(MMU(rom_file))
    cpu.set_reg_16('HL', 0x1234)
    cpu.tick()
    assert cpu.pc == 0x1234

def test_JR_n():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0012] = 0x18
    rom_file[0x0013] = 0x34
    cpu = CPU(MMU(rom_file))
    cpu.pc = 0x0012
    cpu.tick()
    assert cpu.pc == 0x0047

def test_JR_cc_n():
    # NZ
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x20
    rom_file[0x0101] = 0x34
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('Z', 0)
    cpu.tick()
    assert cpu.pc == 0x0135

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x20
    rom_file[0x0101] = 0x34
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('Z', 1)
    cpu.tick()
    assert cpu.pc == 0x0102

    # Z
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x28
    rom_file[0x0101] = 0x34
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('Z', 0)
    cpu.tick()
    assert cpu.pc == 0x0102

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x28
    rom_file[0x0101] = 0x34
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('Z', 1)
    cpu.tick()
    assert cpu.pc == 0x0135

    # NC
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x30
    rom_file[0x0101] = 0x34
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 0)
    cpu.tick()
    assert cpu.pc == 0x0135

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x30
    rom_file[0x0101] = 0x34
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.pc == 0x0102

    # C
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x38
    rom_file[0x0101] = 0x34
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 0)
    cpu.tick()
    assert cpu.pc == 0x0102

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x38
    rom_file[0x0101] = 0x34
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.pc == 0x0135

# Calls

def test_CALL_nn():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCD
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.tick()
    assert cpu.pc == 0x1234
    assert cpu.pop_stack() == 0x0103

def test_CALL_cc_nn():
    # NZ
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC4
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('Z', 0)
    cpu.tick()
    assert cpu.pc == 0x1234
    assert cpu.pop_stack() == 0x0103

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC4
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('Z', 1)
    cpu.tick()
    assert cpu.pc == 0x0103

    # Z
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCC
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('Z', 0)
    cpu.tick()
    assert cpu.pc == 0x0103

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xCC
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('Z', 1)
    cpu.tick()
    assert cpu.pc == 0x1234
    assert cpu.pop_stack() == 0x0103

    # NC
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xD4
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 0)
    cpu.tick()
    assert cpu.pc == 0x1234
    assert cpu.pop_stack() == 0x0103

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xD4
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.pc == 0x0103

    # C
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xDC
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 0)
    cpu.tick()
    assert cpu.pc == 0x0103

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xDC
    rom_file[0x0101] = 0x34
    rom_file[0x0102] = 0x12
    cpu = CPU(MMU(rom_file))
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.pc == 0x1234
    assert cpu.pop_stack() == 0x0103

# Restarts

def test_RST_n():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0150] = 0xC7
    cpu = CPU(MMU(rom_file))
    cpu.pc = 0x0150
    cpu.tick()
    assert cpu.pc == 0x0000
    assert cpu.pop_stack() == 0x0151

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0150] = 0xCF
    cpu = CPU(MMU(rom_file))
    cpu.pc = 0x0150
    cpu.tick()
    assert cpu.pc == 0x0008
    assert cpu.pop_stack() == 0x0151

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0150] = 0xD7
    cpu = CPU(MMU(rom_file))
    cpu.pc = 0x0150
    cpu.tick()
    assert cpu.pc == 0x0010
    assert cpu.pop_stack() == 0x0151

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0150] = 0xDF
    cpu = CPU(MMU(rom_file))
    cpu.pc = 0x0150
    cpu.tick()
    assert cpu.pc == 0x0018
    assert cpu.pop_stack() == 0x0151

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0150] = 0xE7
    cpu = CPU(MMU(rom_file))
    cpu.pc = 0x0150
    cpu.tick()
    assert cpu.pc == 0x0020
    assert cpu.pop_stack() == 0x0151

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0150] = 0xEF
    cpu = CPU(MMU(rom_file))
    cpu.pc = 0x0150
    cpu.tick()
    assert cpu.pc == 0x0028
    assert cpu.pop_stack() == 0x0151

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0150] = 0xF7
    cpu = CPU(MMU(rom_file))
    cpu.pc = 0x0150
    cpu.tick()
    assert cpu.pc == 0x0030
    assert cpu.pop_stack() == 0x0151

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0150] = 0xFF
    cpu = CPU(MMU(rom_file))
    cpu.pc = 0x0150
    cpu.tick()
    assert cpu.pc == 0x0038
    assert cpu.pop_stack() == 0x0151

# Returns

def test_RET():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC0
    cpu = CPU(MMU(rom_file))
    cpu.push_stack(0x1234)
    cpu.tick()
    assert cpu.pc == 0x1234

def test_RET_cc():
    # NZ
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC0
    cpu = CPU(MMU(rom_file))
    cpu.push_stack(0x1234)
    cpu.set_flag('Z', 0)
    cpu.tick()
    assert cpu.pc == 0x1234

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC0
    cpu = CPU(MMU(rom_file))
    cpu.push_stack(0x1234)
    cpu.set_flag('Z', 1)
    cpu.tick()
    assert cpu.pc == 0x0101

    # Z
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC8
    cpu = CPU(MMU(rom_file))
    cpu.push_stack(0x1234)
    cpu.set_flag('Z', 0)
    cpu.tick()
    assert cpu.pc == 0x0101

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xC8
    cpu = CPU(MMU(rom_file))
    cpu.push_stack(0x1234)
    cpu.set_flag('Z', 1)
    cpu.tick()
    assert cpu.pc == 0x1234

    # NC
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xD0
    cpu = CPU(MMU(rom_file))
    cpu.push_stack(0x1234)
    cpu.set_flag('C', 0)
    cpu.tick()
    assert cpu.pc == 0x1234

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xD0
    cpu = CPU(MMU(rom_file))
    cpu.push_stack(0x1234)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.pc == 0x0101

    # C
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xD8
    cpu = CPU(MMU(rom_file))
    cpu.push_stack(0x1234)
    cpu.set_flag('C', 0)
    cpu.tick()
    assert cpu.pc == 0x0101

    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xD8
    cpu = CPU(MMU(rom_file))
    cpu.push_stack(0x1234)
    cpu.set_flag('C', 1)
    cpu.tick()
    assert cpu.pc == 0x1234

def test_RETI():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0xD9
    cpu = CPU(MMU(rom_file))
    cpu.push_stack(0x1234)
    cpu.tick()
    assert cpu.pc == 0x1234
    # TODO: TEST FOR INTERRUPT ENABLE

def test_fibonacci():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0100] = 0x16 # LD D=13  - Set counter to 13 loops
    rom_file[0x0101] = 0x0D
    rom_file[0x0102] = 0x06 # LD B=0   - Set n1 to 0
    rom_file[0x0103] = 0x00
    rom_file[0x0104] = 0x0E # LD C=1   - Set n2 to 1
    rom_file[0x0105] = 0x01
    rom_file[0x0106] = 0x78 # LD B->A  - Load n1 to A  <---------
    rom_file[0x0107] = 0x81 # ADD C->A - Add n2 to A            |
    rom_file[0x0108] = 0x48 # LD B->C  - Move n1 over n2        |
    rom_file[0x0109] = 0x47 # LD A->B  - Store result as n1     |
    rom_file[0x010A] = 0x15 # DEC D    - Decrement counter      |
    rom_file[0x010B] = 0xC2 # JP NZ    - If counter != 0..      |
    rom_file[0x010C] = 0x06 #          - ..loop back to 0x0106 --
    rom_file[0x010D] = 0x01
    rom_file[0x010E] = 0x76 #          - ..else, halt

    cpu = CPU(MMU(rom_file))

    while cpu.pc != 0x010E:
        cpu.tick()

    assert cpu.get_reg_8('B') == 233    # F13 = 233
