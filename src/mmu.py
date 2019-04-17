import numpy as np
from src.exceptions.memory_access_error import MemoryAccessError

class MMU:

    def __init__(self, rom_file):
        self.ROM = rom_file
        self.WORK_RAM = np.zeros(8192, dtype=np.uint8)
        self.EXT_RAM = np.zeros(8192, dtype=np.uint8)
        self.CHAR_RAM = np.zeros(6144, dtype=np.uint8)
        self.BG_MAP_1 = np.zeros(1024, dtype=np.uint8)
        self.BG_MAP_2 = np.zeros(1024, dtype=np.uint8)
        self.OAM = np.zeros(1024, dtype=np.uint8)
        self.HIGH_RAM = np.zeros(127, dtype=np.uint8)
        self.INTERRUPT = 0x00

    def get(self, addr):
        # Memory map reference: http://gameboy.mongenel.com/dmg/asmmemmap.html

        # Cartridge ROM bank 0 0x0000-0x3FFF
        if addr >= 0x0000 and addr <= 0x3FFF:
            addr_adj = addr
            return self.ROM[addr_adj]

        # Cartridge ROM switchable bank 0x4000-0x7FFF
        elif addr >= 0x4000 and addr <= 0x7FFF:
            # TODO: Implement bank switching; currently just 32K max rom size
            addr_adj = addr
            return self.ROM[addr_adj]

        # Character RAM 0x8000-0x97FF
        elif addr >= 0x8000 and addr <= 0x97FF:
            addr_adj = addr - 0x8000
            return self.CHAR_RAM[addr_adj]

        # BG Map Data 1 0x9800-0x9BF
        elif addr >= 0x9800 and addr <= 0x9BFF:
            addr_adj = addr - 0x9800
            return self.BG_MAP_1[addr_adj]

        # BG Map Data 2 0x9C00-0x9FFF
        elif addr >= 0x9C00 and addr <= 0x9FFF:
            addr_adj = addr - 0x9C00
            return self.BG_MAP_2[addr_adj]

        # External RAM (if available) 0xA000-0xBFFF
        elif addr >= 0xA000 and addr <= 0xBFFF:
            addr_adj = addr - 0xA000
            return self.EXT_RAM[addr_adj]

        # Work RAM 0xC000-0xDFFF
        elif addr >= 0xC000 and addr <= 0xDFFF:
            addr_adj = addr - 0xC000
            return self.WORK_RAM[addr_adj]

        # Echo RAM (Reserved, shouldn't be used) 0xE000-0xFDFF
        elif addr >= 0xE000 and addr <= 0xFDFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # OAM - Object Attribute Memory 0xFE00-0xFE9F
        elif addr >= 0xFE00 and addr <= 0xFE9F:
            addr_adj = addr - 0xFE00
            return self.OAM[addr_adj]

        # Unusable Memory 0xFEA0-0xFEFF
        elif addr >= 0xFEA0 and addr <= 0xFEFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Hardware I/O Registers 0xFF00-0xFF7F
        elif addr >= 0xFF00 and addr <= 0xFF7F:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # High RAM 0xFF80-0xFFFE
        elif addr >= 0xFF80 and addr <= 0xFFFE:
            addr_adj = addr - 0xFF80
            return self.HIGH_RAM[addr_adj]

        # Interrupt register 0xFFFF
        elif addr == 0xFFFF:
            return self.INTERRUPT

        else:
            raise MemoryAccessError('Crazy out of range address requested from MMU: ' + str(addr))


    def set(self, addr, val):
        # Cartridge ROM bank 0 0x0000-0x3FFF
        if addr >= 0x0000 and addr <= 0x3FFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Cartridge ROM switchable bank 0x4000-0x7FFF
        elif addr >= 0x4000 and addr <= 0x7FFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Character RAM 0x8000-0x97FF
        elif addr >= 0x8000 and addr <= 0x97FF:
            # return self.VRAM[addr - 0x8000]
            addr_adj = addr - 0x8000
            self.CHAR_RAM[addr_adj] = val

        # BG Map Data 1 0x9800-0x9BFF
        elif addr >= 0x9800 and addr <= 0x9BFF:
            addr_adj = addr - 0x9800
            self.BG_MAP_1[addr_adj] = val

        # BG Map Data 2 0x9C00-0x9FFF
        elif addr >= 0x9C00 and addr <= 0x9FFF:
            addr_adj = addr - 0x9C00
            self.BG_MAP_2[addr_adj] = val

        # External RAM (if available) 0xA000-0xBFFF
        elif addr >= 0xA000 and addr <= 0xBFFF:
            addr_adj = addr - 0xA000
            self.EXT_RAM[addr_adj] = val

        # Work RAM 0xC000-0xDFFF
        elif addr >= 0xC000 and addr <= 0xDFFF:
            addr_adj = addr - 0xC000
            self.WORK_RAM[addr_adj] = val

        # Echo RAM (Reserved, shouldn't be used) 0xE000-0xFDFF
        elif addr >= 0xE000 and addr <= 0xFDFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # OAM - Object Attribute Memory 0xFE00-0xFE9F
        elif addr >= 0xFE00 and addr <= 0xFE9F:
            addr_adj = addr - 0xFE00
            self.OAM[addr_adj] = val

        # Unusable Memory 0xFEA0-0xFEFF
        elif addr >= 0xFEA0 and addr <= 0xFEFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Hardware I/O Registers 0xFF00-0xFF7F
        elif addr >= 0xFF00 and addr <= 0xFF7F:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # High RAM 0xFF80-0xFFFE
        elif addr >= 0xFF80 and addr <= 0xFFFE:
            addr_adj = addr - 0xFF80
            self.HIGH_RAM[addr_adj] = val

        # Interrupt register 0xFFFF
        elif addr == 0xFFFF:
            self.INTERRUPT = val

        else:
            raise MemoryAccessError('Crazy out of range address requested from MMU: ' + str(addr))