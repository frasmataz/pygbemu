from events import Events
import pygame
import numpy as np

class Graphics:
    def get_test_pattern(self, mmu):
        pixel_values = np.zeros(shape=(self.GB_PARAMS['screen_res'][0], self.GB_PARAMS['screen_res'][1],3), dtype='uint8')

        for x in range(0, self.GB_PARAMS['screen_res'][0]):
            for y in range(0, self.GB_PARAMS['screen_res'][1]):
                # Print ROM bytes as pixel data as a test pattern
                pixel_values[x][y] = [mmu.get((x*160)+y+0x150)&224,      #RED = Highest 3 bits  (byte AND 11100000)
                                      (mmu.get((x*160)+y+0x150)&28)<<3,  #BLUE = Middle 3 bits  (byte AND 00011100 << 3)
                                      (mmu.get((x*160)+y+0x150)&3)<<6]   #GREEN = Lowest 2 bits (byte AND 00000011 << 6)

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
            print("Can't get events, video system not initialised.")

    def __init__(self, GB_PARAMS):
        self.GB_PARAMS = GB_PARAMS
        
        pygame.init()
        self.screen = pygame.display.set_mode(self.GB_PARAMS['screen_res'])
        pygame.display.set_caption('pygbemu')
        self.clock = pygame.time.Clock()
