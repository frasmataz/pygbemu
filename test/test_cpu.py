from src.cpu import CPU

def test_registers():
    cpu = CPU()

    cpu.a = 0x55
    cpu.f = 0xAA
    assert cpu.get_af() == 0x55AA

    cpu.set_af(0xAA55)
    assert cpu.a == 0xAA
    assert cpu.f == 0x55

    cpu.b = 0x55
    cpu.c = 0xAA
    assert cpu.get_bc() == 0x55AA

    cpu.set_bc(0xAA55)
    assert cpu.b == 0xAA
    assert cpu.c == 0x55

    cpu.d = 0x55
    cpu.e = 0xAA
    assert cpu.get_de() == 0x55AA

    cpu.set_de(0xAA55)
    assert cpu.d == 0xAA
    assert cpu.e == 0x55

    cpu.h = 0x55
    cpu.l = 0xAA
    assert cpu.get_hl() == 0x55AA

    cpu.set_hl(0xAA55)
    assert cpu.h == 0xAA
    assert cpu.l == 0x55

    assert cpu.sp == 0x0000
    assert cpu.pc == 0x0000