import numpy as np

class CPU:
    def __init__(self, mmu):
        self.regs = {
            'A': 0x00,
            'B': 0x00,
            'C': 0x00,
            'D': 0x00,
            'E': 0x00,
            'F': 0x00,
            'H': 0x00,
            'L': 0x00
        }

        self.sp = 0x0000
        self.pc = 0x0000

        self.mmu = mmu

    def get_reg_8(self, reg):
        return self.regs[reg]

    def set_reg_8(self, reg, val):
        self.regs[reg] = val

    def get_reg_16(self, reg):
        if (reg == 'AF'):
            return (self.regs['A'] << 8) | self.regs['F']
        elif (reg == 'BC'):
            return (self.regs['B'] << 8) | self.regs['C']
        elif (reg == 'DE'):
            return (self.regs['D'] << 8) | self.regs['E']
        elif (reg == 'HL'):
            return (self.regs['H'] << 8) | self.regs['L']
        elif (reg == 'SP'):
            return self.sp
        elif (reg == 'PC'):
            return self.pc

    def set_reg_16(self, reg, val):
        if (reg == 'AF'):
            self.regs['A'] = (val & 0xFF00) >> 8
            self.regs['F'] = val & 0x00FF
        elif (reg == 'BC'):
            self.regs['B'] = (val & 0xFF00) >> 8
            self.regs['C'] = val & 0x00FF
        elif (reg == 'DE'):
            self.regs['D'] = (val & 0xFF00) >> 8
            self.regs['E'] = val & 0x00FF
        elif (reg == 'HL'):
            self.regs['H'] = (val & 0xFF00) >> 8
            self.regs['L'] = val & 0x00FF
        elif (reg == 'SP'):
            self.sp = val
        elif (reg == 'PC'):
            self.pc = val

    def fetch_8(self):
        val = self.mmu.get(self.pc)
        self.pc = self.pc + 1
        return val

    def fetch_16(self):
        val1 = self.mmu.get(self.pc)
        val2 = self.mmu.get(self.pc + 1)
        self.pc = self.pc + 2
        val = (val2 << 8) | val1 # Least sig byte popped first, might be wrong
        return val

    def get_flag(self, flag):
        if (flag == 'Z'):
            return (self.get_reg_8('F') & 0b10000000) >> 7
        elif (flag == 'N'):
            return (self.get_reg_8('F') & 0b01000000) >> 6
        elif (flag == 'H'):
            return (self.get_reg_8('F') & 0b00100000) >> 5
        elif (flag == 'C'):
            return (self.get_reg_8('F') & 0b00010000) >> 4
        else:
            raise NotImplementedError('Unknown flag get: ' + flag)

    def set_flag(self, flag, val):
        if (flag == 'Z'):
            self.set_reg_8('F', self.get_reg_8('F') & 0b01111111 | (val << 7))
        elif (flag == 'N'):
            self.set_reg_8('F', self.get_reg_8('F') & 0b10111111 | (val << 6))
        elif (flag == 'H'):
            self.set_reg_8('F', self.get_reg_8('F') & 0b11011111 | (val << 5))
        elif (flag == 'C'):
            self.set_reg_8('F', self.get_reg_8('F') & 0b11101111 | (val << 4))
        else:
            raise NotImplementedError('Unknown flag set: ' + flag)

    def push_stack(self, addr):
        SP = self.get_reg_16('SP')
        self.mmu.set(SP - 1, (addr & 0xFF00) >> 8)
        self.mmu.set(SP - 2, (addr & 0xFF))
        self.set_reg_16('SP', SP - 2)

    def pop_stack(self):
        SP = self.get_reg_16('SP')
        lo = self.mmu.get(SP)
        hi = self.mmu.get(SP + 1)
        self.set_reg_16('SP', SP + 2)
        return (hi << 8) | lo

    def add_8(self, val1, val2, use_carry = False):
        total = (val1 + val2 + int(use_carry))
        wrappedTotal = total % 0x100
        self.set_flag('Z', int(wrappedTotal == 0))
        self.set_flag('N', 0)
        self.set_flag('H', int((val1 & 0x0F) + (val2 & 0x0F) + (int(use_carry) & 0x0F) > 0x0F))
        self.set_flag('C', int(total > 0xFF))
        return wrappedTotal

    def add_16(self, val1, val2, use_carry = False):
        total = (val1 + val2 + int(use_carry))
        wrappedTotal = total % 0x10000
        self.set_flag('Z', int(wrappedTotal == 0))
        self.set_flag('N', 0)
        self.set_flag('H', int((val1 & 0xFFF) + (val2 & 0xFFF) + (int(use_carry) & 0x0FFF) > 0x0FFF))
        self.set_flag('C', int(total > 0xFFFF))
        return wrappedTotal

    def sub_8(self, val1, val2, use_carry = False):
        total = (val1 - val2 - int(use_carry))
        wrappedTotal = total % 0x100
        self.set_flag('Z', int(wrappedTotal == 0))
        self.set_flag('N', 1)
        self.set_flag('H', int((val1 & 0xF) < ((val2 & 0xF) + int(use_carry))))
        self.set_flag('C', int(total < 0x00))
        return wrappedTotal

    def sub_16(self, val1, val2, use_carry = False):
        total = (val1 - val2 - int(use_carry))
        wrappedTotal = total % 0x10000
        self.set_flag('Z', int(wrappedTotal == 0))
        self.set_flag('N', 1)
        self.set_flag('H', int((val1 & 0xFFF) < ((val2 & 0xFFF) + int(use_carry))))
        self.set_flag('C', int(total < 0x0000))
        return wrappedTotal

    def tick(self):
        op = self.fetch_8()

        ## 8-bit loads
        # LD nn, n
        if (op == 0x06):
            n = self.fetch_8()
            self.LD_nn_n('B', n)
        elif (op == 0x0E):
            n = self.fetch_8()
            self.LD_nn_n('C', n)
        elif (op == 0x16):
            n = self.fetch_8()
            self.LD_nn_n('D', n)
        elif (op == 0x1E):
            n = self.fetch_8()
            self.LD_nn_n('E', n)
        elif (op == 0x26):
            n = self.fetch_8()
            self.LD_nn_n('H', n)
        elif (op == 0x2E):
            n = self.fetch_8()
            self.LD_nn_n('L', n)

        # LD r1, r2
        elif (op == 0x7F):
            self.LD_r1_r2('A', 'A')
        elif (op == 0x78):
            self.LD_r1_r2('A', 'B')
        elif (op == 0x79):
            self.LD_r1_r2('A', 'C')
        elif (op == 0x7A):
            self.LD_r1_r2('A', 'D')
        elif (op == 0x7B):
            self.LD_r1_r2('A', 'E')
        elif (op == 0x7C):
            self.LD_r1_r2('A', 'H')
        elif (op == 0x7D):
            self.LD_r1_r2('A', 'L')
        elif (op == 0x40):
            self.LD_r1_r2('B', 'B')
        elif (op == 0x41):
            self.LD_r1_r2('B', 'C')
        elif (op == 0x42):
            self.LD_r1_r2('B', 'D')
        elif (op == 0x43):
            self.LD_r1_r2('B', 'E')
        elif (op == 0x44):
            self.LD_r1_r2('B', 'H')
        elif (op == 0x45):
            self.LD_r1_r2('B', 'L')
        elif (op == 0x48):
            self.LD_r1_r2('C', 'B')
        elif (op == 0x49):
            self.LD_r1_r2('C', 'C')
        elif (op == 0x4A):
            self.LD_r1_r2('C', 'D')
        elif (op == 0x4B):
            self.LD_r1_r2('C', 'E')
        elif (op == 0x4C):
            self.LD_r1_r2('C', 'H')
        elif (op == 0x4D):
            self.LD_r1_r2('C', 'L')
        elif (op == 0x50):
            self.LD_r1_r2('D', 'B')
        elif (op == 0x51):
            self.LD_r1_r2('D', 'C')
        elif (op == 0x52):
            self.LD_r1_r2('D', 'D')
        elif (op == 0x53):
            self.LD_r1_r2('D', 'E')
        elif (op == 0x54):
            self.LD_r1_r2('D', 'H')
        elif (op == 0x55):
            self.LD_r1_r2('D', 'L')
        elif (op == 0x58):
            self.LD_r1_r2('E', 'B')
        elif (op == 0x59):
            self.LD_r1_r2('E', 'C')
        elif (op == 0x5A):
            self.LD_r1_r2('E', 'D')
        elif (op == 0x5B):
            self.LD_r1_r2('E', 'E')
        elif (op == 0x5C):
            self.LD_r1_r2('E', 'H')
        elif (op == 0x5D):
            self.LD_r1_r2('E', 'L')
        elif (op == 0x60):
            self.LD_r1_r2('H', 'B')
        elif (op == 0x61):
            self.LD_r1_r2('H', 'C')
        elif (op == 0x62):
            self.LD_r1_r2('H', 'D')
        elif (op == 0x63):
            self.LD_r1_r2('H', 'E')
        elif (op == 0x64):
            self.LD_r1_r2('H', 'H')
        elif (op == 0x65):
            self.LD_r1_r2('H', 'L')
        elif (op == 0x68):
            self.LD_r1_r2('L', 'B')
        elif (op == 0x69):
            self.LD_r1_r2('L', 'C')
        elif (op == 0x6A):
            self.LD_r1_r2('L', 'D')
        elif (op == 0x6B):
            self.LD_r1_r2('L', 'E')
        elif (op == 0x6C):
            self.LD_r1_r2('L', 'H')
        elif (op == 0x6D):
            self.LD_r1_r2('L', 'L')

        # LD r, (HL)   #Technically part of LD r1, r2
        elif (op == 0x7E):
            self.LD_r_HL('A')
        elif (op == 0x46):
            self.LD_r_HL('B')
        elif (op == 0x4E):
            self.LD_r_HL('C')
        elif (op == 0x56):
            self.LD_r_HL('D')
        elif (op == 0x5E):
            self.LD_r_HL('E')
        elif (op == 0x66):
            self.LD_r_HL('H')
        elif (op == 0x6E):
            self.LD_r_HL('L')

        # LD (HL), r   #Technically part of LD r1, r2
        elif (op == 0x70):
            self.LD_HL_r('B')
        elif (op == 0x71):
            self.LD_HL_r('C')
        elif (op == 0x72):
            self.LD_HL_r('D')
        elif (op == 0x73):
            self.LD_HL_r('E')
        elif (op == 0x74):
            self.LD_HL_r('H')
        elif (op == 0x75):
            self.LD_HL_r('L')

        # LD (HL), n   #Technically part of LD r1, r2
        elif (op == 0x36):
            self.LD_HL_n()

        # LD A, n
        elif (op == 0x0A):
            self.LD_A_rr('BC')
        elif (op == 0x1A):
            self.LD_A_rr('DE')
        elif (op == 0x7E):
            self.LD_A_rr('HL')
        elif (op == 0xFA):
            self.LD_A_nn()
        elif (op == 0x3E):
            self.LD_A_n()

        # LD n, A
        elif (op == 0x47):
            self.LD_n_A('B')
        elif (op == 0x4F):
            self.LD_n_A('C')
        elif (op == 0x57):
            self.LD_n_A('D')
        elif (op == 0x5F):
            self.LD_n_A('E')
        elif (op == 0x67):
            self.LD_n_A('H')
        elif (op == 0x6F):
            self.LD_n_A('L')
        elif (op == 0x02):
            self.LD_rr_A('BC')
        elif (op == 0x12):
            self.LD_rr_A('DE')
        elif (op == 0x77):
            self.LD_rr_A('HL')
        elif (op == 0xEA):
            self.LD_nn_A()

        # LD A,C & LD C, A
        elif (op == 0xF2):
            self.LD_A_C()
        elif (op == 0xE2):
            self.LD_C_A()

        # LDD & LDI
        elif (op == 0x3A):
            self.LDD_A_HL()
        elif (op == 0x32):
            self.LDD_HL_A()
        elif (op == 0x2A):
            self.LDI_A_HL()
        elif (op == 0x22):
            self.LDI_HL_A()

        # LDH
        elif (op == 0xE0):
            self.LDH_n_A()
        elif (op == 0xF0):
            self.LDH_A_n()

        ## 16-bit loads
        # LD n, nn
        elif (op == 0x01):
            self.LD_n_nn('BC')
        elif (op == 0x11):
            self.LD_n_nn('DE')
        elif (op == 0x21):
            self.LD_n_nn('HL')
        elif (op == 0x31):
            self.LD_n_nn('SP')

        # LD SP
        elif (op == 0xF9):
            self.LD_SP_HL()
        elif (op == 0xF8):
            self.LD_HL_SPn()
        elif (op == 0x08):
            self.LD_nn_SP()

        # Stack
        elif (op == 0xF5):
            self.PUSH_nn('AF')
        elif (op == 0xC5):
            self.PUSH_nn('BC')
        elif (op == 0xD5):
            self.PUSH_nn('DE')
        elif (op == 0xE5):
            self.PUSH_nn('HL')
        elif (op == 0xF1):
            self.POP_nn('AF')
        elif (op == 0xC1):
            self.POP_nn('BC')
        elif (op == 0xD1):
            self.POP_nn('DE')
        elif (op == 0xE1):
            self.POP_nn('HL')

        ## 8-bit ALU
        # Addition
        elif (op == 0x87):
            self.ADD_A_r('A')
        elif (op == 0x80):
            self.ADD_A_r('B')
        elif (op == 0x81):
            self.ADD_A_r('C')
        elif (op == 0x82):
            self.ADD_A_r('D')
        elif (op == 0x83):
            self.ADD_A_r('E')
        elif (op == 0x84):
            self.ADD_A_r('H')
        elif (op == 0x85):
            self.ADD_A_r('L')
        elif (op == 0x86):
            self.ADD_A_HL()
        elif (op == 0xC6):
            self.ADD_A_n()
        elif (op == 0x8F):
            self.ADC_A_r('A')
        elif (op == 0x88):
            self.ADC_A_r('B')
        elif (op == 0x89):
            self.ADC_A_r('C')
        elif (op == 0x8A):
            self.ADC_A_r('D')
        elif (op == 0x8B):
            self.ADC_A_r('E')
        elif (op == 0x8C):
            self.ADC_A_r('H')
        elif (op == 0x8D):
            self.ADC_A_r('L')
        elif (op == 0x8E):
            self.ADC_A_HL()
        elif (op == 0xCE):
            self.ADC_A_n()

        # Subtraction
        elif (op == 0x97):
            self.SUB_A_r('A')
        elif (op == 0x90):
            self.SUB_A_r('B')
        elif (op == 0x91):
            self.SUB_A_r('C')
        elif (op == 0x92):
            self.SUB_A_r('D')
        elif (op == 0x93):
            self.SUB_A_r('E')
        elif (op == 0x94):
            self.SUB_A_r('H')
        elif (op == 0x95):
            self.SUB_A_r('L')
        elif (op == 0x96):
            self.SUB_A_HL()
        elif (op == 0xD6):
            self.SUB_A_n()
        elif (op == 0x9F):
            self.SBC_A_r('A')
        elif (op == 0x98):
            self.SBC_A_r('B')
        elif (op == 0x99):
            self.SBC_A_r('C')
        elif (op == 0x9A):
            self.SBC_A_r('D')
        elif (op == 0x9B):
            self.SBC_A_r('E')
        elif (op == 0x9C):
            self.SBC_A_r('H')
        elif (op == 0x9D):
            self.SBC_A_r('L')
        elif (op == 0x9E):
            self.SBC_A_HL()
        elif (op == 0xDE):
            self.SBC_A_n()

        # AND/OR/XOR
        elif (op == 0xA7):
            self.AND_r('A')
        elif (op == 0xA0):
            self.AND_r('B')
        elif (op == 0xA1):
            self.AND_r('C')
        elif (op == 0xA2):
            self.AND_r('D')
        elif (op == 0xA3):
            self.AND_r('E')
        elif (op == 0xA4):
            self.AND_r('H')
        elif (op == 0xA5):
            self.AND_r('L')
        elif (op == 0xA6):
            self.AND_HL()
        elif (op == 0xE6):
            self.AND_n()
        elif (op == 0xB7):
            self.OR_r('A')
        elif (op == 0xB0):
            self.OR_r('B')
        elif (op == 0xB1):
            self.OR_r('C')
        elif (op == 0xB2):
            self.OR_r('D')
        elif (op == 0xB3):
            self.OR_r('E')
        elif (op == 0xB4):
            self.OR_r('H')
        elif (op == 0xB5):
            self.OR_r('L')
        elif (op == 0xB6):
            self.OR_HL()
        elif (op == 0xF6):
            self.OR_n()
        elif (op == 0xAF):
            self.XOR_r('A')
        elif (op == 0xA8):
            self.XOR_r('B')
        elif (op == 0xA9):
            self.XOR_r('C')
        elif (op == 0xAA):
            self.XOR_r('D')
        elif (op == 0xAB):
            self.XOR_r('E')
        elif (op == 0xAC):
            self.XOR_r('H')
        elif (op == 0xAD):
            self.XOR_r('L')
        elif (op == 0xAE):
            self.XOR_HL()
        elif (op == 0xEE):
            self.XOR_n()
        elif (op == 0xBF):
            self.CP_r('A')
        elif (op == 0xB8):
            self.CP_r('B')
        elif (op == 0xB9):
            self.CP_r('C')
        elif (op == 0xBA):
            self.CP_r('D')
        elif (op == 0xBB):
            self.CP_r('E')
        elif (op == 0xBC):
            self.CP_r('H')
        elif (op == 0xBD):
            self.CP_r('L')
        elif (op == 0xBE):
            self.CP_HL()
        elif (op == 0xFE):
            self.CP_n()
        elif (op == 0x3C):
            self.INC_r('A')
        elif (op == 0x04):
            self.INC_r('B')
        elif (op == 0x0C):
            self.INC_r('C')
        elif (op == 0x14):
            self.INC_r('D')
        elif (op == 0x1C):
            self.INC_r('E')
        elif (op == 0x24):
            self.INC_r('H')
        elif (op == 0x2C):
            self.INC_r('L')
        elif (op == 0x34):
            self.INC_HL()
        elif (op == 0x3D):
            self.DEC_r('A')
        elif (op == 0x05):
            self.DEC_r('B')
        elif (op == 0x0D):
            self.DEC_r('C')
        elif (op == 0x15):
            self.DEC_r('D')
        elif (op == 0x1D):
            self.DEC_r('E')
        elif (op == 0x25):
            self.DEC_r('H')
        elif (op == 0x2D):
            self.DEC_r('L')
        elif (op == 0x35):
            self.DEC_HL()

        ## 16-bit ALU
        elif (op == 0x09):
            self.ADD_HL_n('BC')
        elif (op == 0x19):
            self.ADD_HL_n('DE')
        elif (op == 0x29):
            self.ADD_HL_n('HL')
        elif (op == 0x39):
            self.ADD_HL_n('SP')
        elif (op == 0xE8):
            self.ADD_SP_n()
        else:
            raise NotImplementedError('Unknown opcode: ' + hex(op))



    ## OPCODE FUNCTIONS
    # 8-bit loads

    def LD_nn_n(self, r, val):
        self.regs[r] = val

    def LD_r1_r2(self, r1, r2):
        self.regs[r1] = self.regs[r2]

    def LD_HL_r(self, r): #Technically part of LD r1, r2
        addr = self.get_reg_16('HL')
        self.mmu.set(addr, self.regs[r])

    def LD_r_HL(self, r): #Technically part of LD r1, r2
        addr = self.get_reg_16('HL')
        self.regs[r] = self.mmu.get(addr)

    def LD_HL_n(self): #Technically part of LD r1, r2
        n = self.fetch_8()
        addr = self.get_reg_16('HL')
        self.mmu.set(addr, n)

    def LD_A_rr(self, reg):
        addr = self.get_reg_16(reg)
        self.set_reg_8('A', self.mmu.get(addr))

    def LD_A_nn(self):
        addr = self.fetch_16()
        self.set_reg_8('A', self.mmu.get(addr))

    def LD_A_n(self):
        self.set_reg_8('A', self.fetch_8())

    def LD_n_A(self, reg):
        self.set_reg_8(reg, self.get_reg_8('A'))

    def LD_rr_A(self, reg):
        addr = self.get_reg_16(reg)
        self.mmu.set(addr, self.get_reg_8('A'))

    def LD_nn_A(self):
        addr = self.fetch_16()
        self.mmu.set(addr, self.get_reg_8('A'))

    def LD_A_C(self):
        self.set_reg_8('A', self.mmu.get(0xFF00 + self.get_reg_8('C')))

    def LD_C_A(self):
        self.mmu.set(0xFF00 + self.get_reg_8('C'), self.get_reg_8('A'))

    def LDD_A_HL(self):
        self.set_reg_8('A', self.mmu.get(self.get_reg_16('HL')))
        HL = self.get_reg_16('HL')
        self.set_reg_16('HL', HL - (1 if (HL > 0x00) else -0xFFFF))

    def LDD_HL_A(self):
        self.mmu.set(self.get_reg_16('HL'), self.get_reg_8('A'))
        HL = self.get_reg_16('HL')
        self.set_reg_16('HL', HL - (1 if (HL > 0x00) else -0xFFFF))

    def LDI_A_HL(self):
        self.set_reg_8('A', self.mmu.get(self.get_reg_16('HL')))
        HL = self.get_reg_16('HL')
        self.set_reg_16('HL', HL + (1 if (HL < 0xFFFF) else -0xFFFF))

    def LDI_HL_A(self):
        self.mmu.set(self.get_reg_16('HL'), self.get_reg_8('A'))
        HL = self.get_reg_16('HL')
        self.set_reg_16('HL', HL + (1 if (HL < 0xFFFF) else -0xFFFF))

    def LDH_n_A(self):
        n = self.fetch_8()
        self.mmu.set(0xFF00 + n, self.get_reg_8('A'))

    def LDH_A_n(self):
        n = self.fetch_8()
        self.set_reg_8('A', self.mmu.get(0xFF00 + n))

    # 16-bit loads

    def LD_n_nn(self, reg):
        self.set_reg_16(reg, self.fetch_16())

    def LD_SP_HL(self):
        self.set_reg_16('SP', self.get_reg_16('HL'))

    def LD_HL_SPn(self):
        self.set_reg_16('HL', self.add_16(self.fetch_8(), self.get_reg_16('SP')))

    def LD_nn_SP(self):
        val = self.get_reg_16('SP')
        addr = self.fetch_16()
        self.mmu.set(addr, (val & 0x00FF))
        self.mmu.set(addr + 1, (val & 0xFF00) >> 8)

    def PUSH_nn(self, reg):
        self.push_stack(self.get_reg_16(reg))

    def POP_nn(self, reg):
        self.set_reg_16(reg, self.pop_stack())

    def ADD_A_r(self, reg):
        self.set_reg_8('A', self.add_8(
            self.get_reg_8('A'),
            self.get_reg_8(reg)
        ))

    def ADD_A_HL(self):
        self.set_reg_8('A', self.add_8(
            self.get_reg_8('A'),
            self.mmu.get(self.get_reg_16('HL'))
        ))

    def ADD_A_n(self):
        self.set_reg_8('A', self.add_8(
            self.get_reg_8('A'),
            self.fetch_8()
        ))

    def ADC_A_r(self, reg):
        self.set_reg_8('A', self.add_8(
            self.get_reg_8('A'),
            self.get_reg_8(reg),
            True
        ))

    def ADC_A_HL(self):
        self.set_reg_8('A', self.add_8(
            self.get_reg_8('A'),
            self.mmu.get(self.get_reg_16('HL')),
            True
        ))

    def ADC_A_n(self):
        self.set_reg_8('A', self.add_8(
            self.get_reg_8('A'),
            self.fetch_8(),
            True
        ))

    def SUB_A_r(self, reg):
        self.set_reg_8('A', self.sub_8(
            self.get_reg_8('A'),
            self.get_reg_8(reg)
        ))

    def SUB_A_HL(self):
        self.set_reg_8('A', self.sub_8(
            self.get_reg_8('A'),
            self.mmu.get(self.get_reg_16('HL'))
        ))

    def SUB_A_n(self):
        self.set_reg_8('A', self.sub_8(
            self.get_reg_8('A'),
            self.fetch_8()
        ))

    def SBC_A_r(self, reg):
        self.set_reg_8('A', self.sub_8(
            self.get_reg_8('A'),
            self.get_reg_8(reg),
            True
        ))

    def SBC_A_HL(self):
        self.set_reg_8('A', self.sub_8(
            self.get_reg_8('A'),
            self.mmu.get(self.get_reg_16('HL')),
            True
        ))

    def SBC_A_n(self):
        self.set_reg_8('A', self.sub_8(
            self.get_reg_8('A'),
            self.fetch_8(),
            True
        ))

    def AND_r(self, reg):
        result = self.get_reg_8('A') & self.get_reg_8(reg)
        self.set_reg_8('A', result)
        self.set_flag('Z', int(result == 0x00))
        self.set_flag('N', 0)
        self.set_flag('H', 1)
        self.set_flag('C', 0)

    def AND_HL(self):
        result = self.get_reg_8('A') & self.mmu.get(self.get_reg_16('HL'))
        self.set_reg_8('A', result)
        self.set_flag('Z', int(result == 0x00))
        self.set_flag('N', 0)
        self.set_flag('H', 1)
        self.set_flag('C', 0)

    def AND_n(self):
        result = self.get_reg_8('A') & self.fetch_8()
        self.set_reg_8('A', result)
        self.set_flag('Z', int(result == 0x00))
        self.set_flag('N', 0)
        self.set_flag('H', 1)
        self.set_flag('C', 0)

    def OR_r(self, reg):
        result = self.get_reg_8('A') | self.get_reg_8(reg)
        self.set_reg_8('A', result)
        self.set_flag('Z', int(result == 0x00))
        self.set_flag('N', 0)
        self.set_flag('H', 0)
        self.set_flag('C', 0)

    def OR_HL(self):
        result = self.get_reg_8('A') | self.mmu.get(self.get_reg_16('HL'))
        self.set_reg_8('A', result)
        self.set_flag('Z', int(result == 0x00))
        self.set_flag('N', 0)
        self.set_flag('H', 0)
        self.set_flag('C', 0)

    def OR_n(self):
        result = self.get_reg_8('A') | self.fetch_8()
        self.set_reg_8('A', result)
        self.set_flag('Z', int(result == 0x00))
        self.set_flag('N', 0)
        self.set_flag('H', 0)
        self.set_flag('C', 0)

    def XOR_r(self, reg):
        result = self.get_reg_8('A') ^ self.get_reg_8(reg)
        self.set_reg_8('A', result)
        self.set_flag('Z', int(result == 0x00))
        self.set_flag('N', 0)
        self.set_flag('H', 0)
        self.set_flag('C', 0)

    def XOR_HL(self):
        result = self.get_reg_8('A') ^ self.mmu.get(self.get_reg_16('HL'))
        self.set_reg_8('A', result)
        self.set_flag('Z', int(result == 0x00))
        self.set_flag('N', 0)
        self.set_flag('H', 0)
        self.set_flag('C', 0)

    def XOR_n(self):
        result = self.get_reg_8('A') ^ self.fetch_8()
        self.set_reg_8('A', result)
        self.set_flag('Z', int(result == 0x00))
        self.set_flag('N', 0)
        self.set_flag('H', 0)
        self.set_flag('C', 0)

    def CP_r(self, reg):
        a = self.get_reg_8('A')
        self.SUB_A_r(reg)
        self.set_reg_8('A', a)

    def CP_HL(self):
        a = self.get_reg_8('A')
        self.SUB_A_HL()
        self.set_reg_8('A', a)

    def CP_n(self):
        a = self.get_reg_8('A')
        self.SUB_A_n()
        self.set_reg_8('A', a)

    def INC_r(self, reg):
        result = (self.get_reg_8(reg) + 1) % 0x100
        self.set_flag('Z', (result == 0x00))
        self.set_flag('N', False)
        self.set_flag('H', int(((self.get_reg_8(reg) & 0x0F) + 0x01) > 0x0F))
        self.set_reg_8(reg, result)

    def INC_HL(self):
        result = (self.mmu.get(self.get_reg_16('HL')) + 1) % 0x100
        self.set_flag('Z', (result == 0x00))
        self.set_flag('N', False)
        self.set_flag('H', int(((self.mmu.get(self.get_reg_16('HL')) & 0x0F) + 0x01) > 0x0F))
        self.mmu.set(self.get_reg_16('HL'), result)

    def DEC_r(self, reg):
        result = (self.get_reg_8(reg) - 1) % 0x100
        self.set_flag('Z', (result == 0x00))
        self.set_flag('N', True)
        self.set_flag('H', int(self.get_reg_8(reg) & 0x0F) == 0)
        self.set_reg_8(reg, result)

    def DEC_HL(self):
        result = (self.mmu.get(self.get_reg_16('HL')) - 1) % 0x100
        self.set_flag('Z', (result == 0x00))
        self.set_flag('N', True)
        self.set_flag('H', int((self.mmu.get(self.get_reg_16('HL')) & 0x0F) == 0))
        self.mmu.set(self.get_reg_16('HL'), result)

    def ADD_HL_n(self, reg):
        # Ensure Z isn't affected
        z = self.get_flag('Z')
        self.set_reg_16('HL', self.add_16(
            self.get_reg_16('HL'),
            self.get_reg_16(reg),
            False
        ))
        self.set_flag('Z', z)

    def ADD_SP_n(self):
        self.set_reg_16('SP', self.add_16(
            self.get_reg_16('SP'),
            self.fetch_16(),
            False
        ))
        self.set_flag('Z', 0)