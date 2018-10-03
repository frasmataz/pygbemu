import sdl2
import sdl2.ext
import sdl2.sdlgfx

class Graphics:
    def draw_test_pattern(self):
        for x in range(0, self.GB_PARAMS['screen_res'][0]):
            for y in range(0, self.GB_PARAMS['screen_res'][1]):
                self.renderer.draw_point(
                        [x,y], 
                        sdl2.ext.Color(
                            (x/self.GB_PARAMS['screen_res'][0])*255, 
                            (y/self.GB_PARAMS['screen_res'][1])*255, 
                            255
                        )
                    )

        self.renderer.present()

    def __init__(self, GB_PARAMS):
        self.GB_PARAMS = GB_PARAMS
        sdl2.ext.init()
        self.window = sdl2.ext.Window("pygbemu", size=GB_PARAMS['screen_res'])
        self.window.show()
       
        self.renderer = sdl2.ext.Renderer(self.window)
        self.draw_test_pattern()

