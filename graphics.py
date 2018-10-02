from __future__ import division
import sdl2
import sdl2.ext
import sdl2.sdlgfx

def draw_test_pattern(renderer, GB_PARAMS):
    for x in range(0, GB_PARAMS['screen_res'][0]):
        for y in range(0, GB_PARAMS['screen_res'][1]):
            renderer.draw_point([x,y], sdl2.ext.Color((x/GB_PARAMS['screen_res'][0])*255, (y/GB_PARAMS['screen_res'][1]*255), 255))

    renderer.present()

def init(GB_PARAMS):
    sdl2.ext.init()
    window = sdl2.ext.Window("pygbemu", size=GB_PARAMS['screen_res'])
    window.show()
    
    renderer = sdl2.ext.Renderer(window)
    draw_test_pattern(renderer, GB_PARAMS)

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

