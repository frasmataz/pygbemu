from events import Events
import pygame
from pygame import PixelArray

class Graphics:
    def draw_test_pattern(self):
        #for x in range(0, self.GB_PARAMS['screen_res'][0]):
        #    for y in range(0, self.GB_PARAMS['screen_res'][1]):
        #        self.renderer.draw_point(
        #                [x,y], 
        #                sdl2.ext.Color(
        #                    (x/self.GB_PARAMS['screen_res'][0])*255, 
        #                    (y/self.GB_PARAMS['screen_res'][1])*255, 
        #                    255
        #                )
        #            )

        #self.renderer.present()

        screen_buf = PixelArray(self.screen)
        for x in range(0, self.GB_PARAMS['screen_res'][0]):
            for y in range(0, self.GB_PARAMS['screen_res'][1]):
                screen_buf[x][y] = (
                            (x/self.GB_PARAMS['screen_res'][0])*255,
                            (y/self.GB_PARAMS['screen_res'][1])*255,
                            255
                        )
        self.clock.tick(60)
        pygame.display.flip()

    def get_events(self):
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Events.QUIT
        except:
            log.debug("Can't get events, video system not initialised.")

    def __init__(self, GB_PARAMS):
        self.GB_PARAMS = GB_PARAMS
        
        pygame.init()
        self.screen = pygame.display.set_mode(self.GB_PARAMS['screen_res'])
        pygame.display.set_caption('pygbemu')
        self.clock = pygame.time.Clock()
