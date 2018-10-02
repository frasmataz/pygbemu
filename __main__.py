import graphics
import mmu
import sys

GB_PARAMS = {
    'screen_res': (160, 144)
}

def run():
    gfx = graphics.init(GB_PARAMS)

if __name__ == '__main__':
    sys.exit(run())
