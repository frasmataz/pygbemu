import numpy as np

class CPU:
    def __init__(self):
        self.a = 0x00
        self.b = 0x00
        self.c = 0x00
        self.d = 0x00
        self.e = 0x00
        self.f = 0x00
        self.h = 0x00
        self.l = 0x00
        self.sp = 0x0000
        self.pc = 0x0000

    def get_af(self):
        return (self.a << 8) | self.f

    def set_af(self, val):
        self.a = (val & 0xFF00) >> 8
        self.f = val  & 0x00FF

    def get_bc(self):
        return (self.b << 8) | self.c

    def set_bc(self, val):
        self.b = (val & 0xFF00) >> 8
        self.c = val & 0x00FF

    def get_de(self):
        return (self.d << 8) | self.e

    def set_de(self, val):
        self.d = (val & 0xFF00) >> 8
        self.e = val & 0x00FF

    def get_hl(self):
        return (self.h << 8) | self.l

    def set_hl(self, val):
        self.h = (val & 0xFF00) >> 8
        self.l = val & 0x00FF