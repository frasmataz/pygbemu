import numpy as np
from Exceptions.memory_access_error import MemoryAccessError

class MMU:

    def __init__(self, rom_file):
        self.ROM = rom_file
        self.RAM = np.zeros(8192,dtype=np.uint8)
        self.VRAM = np.zeros(8192,dtype=np.uint8)

    def get(self, addr):
        # Memory map reference: http://gameboy.mongenel.com/dmg/asmmemmap.html

        # Interrupt and RST Address 0 0x0000-0x00FF
        if addr >= 0x0000 and addr <= 0x00FF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Cartridge headers 0x0100-0x014F
        elif addr >= 0x0100 and addr <= 0x014F:
            # return self.ROM[addr]
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Cartrige ROM bank 0 0x0150-0x3FFF
        elif addr >= 0x0150 and addr <= 0x3FFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Cartrige ROM switchable bank 0x4000-0x7FFF
        elif addr >= 0x4000 and addr <= 0x7FFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Character RAM 0x8000-0x97FF
        elif addr >= 0x8000 and addr <= 0x97FF:
            # return self.VRAM[addr - 0x8000]
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # BG Map Data 1 0x9800-0x9BF
        elif addr >= 0x9800 and addr <= 0x9BFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # BG Map Data 2 0x9C00-0x9FFF
        elif addr >= 0x9C00 and addr <= 0x9FFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Cartridge RAM (if available) 0xA000-0xBFFF
        elif addr >= 0xA000 and addr <= 0xBFFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Internal RAM Bank 0 0xC000-0xCFFF
        elif addr >= 0xC000 and addr <= 0xCFFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Internal RAM Bank 1-7 (Switchable CGB only) 0xD000-0xDFFF
        elif addr >= 0xD000 and addr <= 0xDFFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Echo RAM (Reserved, shouldn't be used) 0xE000-0xFDFF
        elif addr >= 0xE000 and addr <= 0xFDFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # OAM - Object Attribute Memory 0xFE00-0xFE9F
        elif addr >= 0xFE00 and addr <= 0xFE9F:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Unusable Memory 0xFEA0-0xFEFF
        elif addr >= 0xFEA0 and addr <= 0xFEFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Hardware I/O Registers 0xFF00-0xFF7F
        elif addr >= 0xFF00 and addr <= 0xFF7F:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Zero Page 0xFF80-0xFFFE
        elif addr >= 0xFF80 and addr <= 0xFFFE:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Interrupt register 0xFFFF
        elif addr == 0xFFFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        else:
            raise MemoryAccessError('Crazy out of range address requested from MMU: ' + str(addr))


    def set(self, addr):

        # Interrupt and RST Address 0 0x0000-0x00FF
        if addr >= 0x0000 and addr <= 0x00FF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Cartridge headers 0x0100-0x014F
        elif addr >= 0x0100 and addr <= 0x014F:
            # return self.ROM[addr]
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Cartrige ROM bank 0 0x0150-0x3FFF
        elif addr >= 0x0150 and addr <= 0x3FFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Cartrige ROM switchable bank 0x4000-0x7FFF
        elif addr >= 0x4000 and addr <= 0x7FFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Character RAM 0x8000-0x97FF
        elif addr >= 0x8000 and addr <= 0x97FF:
            # return self.VRAM[addr - 0x8000]
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # BG Map Data 1 0x9800-0x9BFF
        elif addr >= 0x9800 and addr <= 0x9BFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # BG Map Data 2 0x9C00-0x9FFF
        elif addr >= 0x9C00 and addr <= 0x9FFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Cartridge RAM (if available) 0xA000-0xBFFF
        elif addr >= 0xA000 and addr <= 0xBFFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Internal RAM Bank 0 0xC000-0xCFFF
        elif addr >= 0xC000 and addr <= 0xCFFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Internal RAM Bank 1-7 (Switchable CGB only) 0xD000-0xDFFF
        elif addr >= 0xD000 and addr <= 0xDFFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Echo RAM (Reserved, shouldn't be used) 0xE000-0xFDFF
        elif addr >= 0xE000 and addr <= 0xFDFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # OAM - Object Attribute Memory 0xFE00-0xFE9F
        elif addr >= 0xFE00 and addr <= 0xFE9F:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Unusable Memory 0xFEA0-0xFEFF
        elif addr >= 0xFEA0 and addr <= 0xFEFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Hardware I/O Registers 0xFF00-0xFF7F
        elif addr >= 0xFF00 and addr <= 0xFF7F:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Zero Page 0xFF80-0xFFFE
        elif addr >= 0xFF80 and addr <= 0xFFFE:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        # Interrupt register 0xFFFF
        elif addr == 0xFFFF:
            raise NotImplementedError('Access of unimplemented memory space ' + str(addr))

        else:
            print('Crazy out of range address requested from MMU: ' + str(addr))