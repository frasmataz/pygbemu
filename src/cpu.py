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