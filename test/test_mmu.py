import numpy as np
import pytest
from src.mmu import MMU

def test_read_range():
    rom_file = np.zeros(32768, dtype=np.uint8)
    mmu = MMU(rom_file)
    for i in range(0, 0xFFFF):
        try:
            mmu.get(i)
        except NotImplementedError:
            pass

def test_write_range():
    rom_file = np.zeros(32768, dtype=np.uint8)
    mmu = MMU(rom_file)
    for i in range(0, 0xFFFF):
        try:
            mmu.set(i, 0x00)
            mmu.set(i, 0xFF)
        except NotImplementedError:
            pass