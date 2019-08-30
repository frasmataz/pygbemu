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
        val = (val1 << 8) | val2
        return val

    def tick(self):
        op = self.fetch_8()

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


    ## OPCODE FUNCTIONS

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