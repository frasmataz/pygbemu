from events import Events
import pygame
from pygame import PixelArray
import numpy as np

class Graphics:
    def get_test_pattern(self):
        pixel_values = np.zeros(shape=(self.GB_PARAMS['screen_res'][0], self.GB_PARAMS['screen_res'][1],3), dtype='uint8')

        for x in range(0, self.GB_PARAMS['screen_res'][0]):
            for y in range(0, self.GB_PARAMS['screen_res'][1]):
                pixel_values[x][y] = [int(x%2 + y%2*128),int(x%2 + y%2*128),int(x%2 + y%2*128)]

        return pixel_values

    def draw(self, pixel_values):
        pygame.surfarray.blit_array(self.screen, pixel_values)
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
