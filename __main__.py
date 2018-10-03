from graphics import Graphics
import mmu
import sys
import sdl2
import sdl2.ext

global GB_PARAMS 
GB_PARAMS = {
    'screen_res': (160, 144),
    'clk_spd_mhz': '4.194'
}

def run():
    gfx = Graphics(GB_PARAMS)

    running = True
    while running:
      for e in sdl2.ext.get_events():
        if e.type == sdl2.SDL_QUIT:
          running = False
          break
        if e.type == sdl2.SDL_KEYDOWN:
          if e.key.keysym.sym == sdl2.SDLK_ESCAPE:
            running = False
            break


if __name__ == '__main__':
    sys.exit(run())
