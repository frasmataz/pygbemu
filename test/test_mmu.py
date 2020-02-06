import numpy as np
import pytest
from mmu import MMU
from exceptions.memory_access_error import MemoryAccessError

def test_read_range():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    mmu = MMU(rom_file)
    for i in range(0, 0xFFFF):
        try:
            mmu.get(i)
        except NotImplementedError:
            pass

def test_write_range():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    mmu = MMU(rom_file)
    for i in range(0, 0xFFFF):
        try:
            mmu.set(i, 0x00)
            mmu.set(i, 0xFF)
        except NotImplementedError:
            pass

def test_out_of_range():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    mmu = MMU(rom_file)
    with pytest.raises(MemoryAccessError):
        mmu.get(-1)
    with pytest.raises(MemoryAccessError):
        mmu.get(0x10000)
    with pytest.raises(MemoryAccessError):
        mmu.set(-1, 0)
    with pytest.raises(MemoryAccessError):
        mmu.set(0x10000, 0)

def test_rom_access():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    rom_file[0x0000] = 0x11
    rom_file[0x0100] = 0x66
    rom_file[0x0150] = 0xAA
    rom_file[0x7FFF] = 0xFF

    mmu = MMU(rom_file)
    assert mmu.get(0x0000) == 0x11
    assert mmu.get(0x0100) == 0x66
    assert mmu.get(0x0150) == 0xAA
    assert mmu.get(0x7FFF) == 0xFF

def test_work_ram():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    mmu = MMU(rom_file)

    mmu.set(0xC000, 0xA0)
    assert mmu.get(0xC000) == 0xA0

    mmu.set(0xDFFF, 0xA0)
    assert mmu.get(0xDFFF) == 0xA0

def test_external_ram():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    mmu = MMU(rom_file)

    mmu.set(0xA000, 0xA0)
    assert mmu.get(0xA000) == 0xA0

    mmu.set(0xBFFF, 0xA0)
    assert mmu.get(0xBFFF) == 0xA0

def test_char_ram():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    mmu = MMU(rom_file)

    mmu.set(0x8000, 0xA0)
    assert mmu.get(0x8000) == 0xA0

    mmu.set(0x97FF, 0xA0)
    assert mmu.get(0x97FF) == 0xA0

def test_bg_map_1():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    mmu = MMU(rom_file)

    mmu.set(0x9800, 0xA0)
    assert mmu.get(0x9800) == 0xA0

    mmu.set(0x9BFF, 0xA0)
    assert mmu.get(0x9BFF) == 0xA0

def test_bg_map_2():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    mmu = MMU(rom_file)

    mmu.set(0x9C00, 0xA0)
    assert mmu.get(0x9C00) == 0xA0

    mmu.set(0x9FFF, 0xA0)
    assert mmu.get(0x9FFF) == 0xA0

def test_oam():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    mmu = MMU(rom_file)

    mmu.set(0xFE00, 0xA0)
    assert mmu.get(0xFE00) == 0xA0

    mmu.set(0xFE9F, 0xA0)
    assert mmu.get(0xFE9F) == 0xA0

def test_high_ram():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    mmu = MMU(rom_file)

    mmu.set(0xFF80, 0xA0)
    assert mmu.get(0xFF80) == 0xA0

    mmu.set(0xFFFE, 0xA0)
    assert mmu.get(0xFFFE) == 0xA0

def test_interrupt_register():
    rom_file = np.zeros(0x8000, dtype=np.uint8)
    mmu = MMU(rom_file)

    mmu.set(0xFFFF, 0xA0)
    assert mmu.get(0xFFFF) == 0xA0
