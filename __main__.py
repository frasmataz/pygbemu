from events import Events
from graphics import Graphics
import mmu
import sys
import time
from timeit import default_timer as timer

global GB_PARAMS 
GB_PARAMS = {
            'screen_res': (160, 144),
            'clk_spd_mhz': '4.194'
            }

PREFS = {
        'debug_perf': True
        }

def run():
    if PREFS['debug_perf']:
        gfx_init_time_start = timer()
        print('Initializing renderer..')

    gfx = Graphics(GB_PARAMS)

    if PREFS['debug_perf']:
        gfx_init_time_end = timer()
        print('Renderer initiatization finished in ',
                "%.4f" % (gfx_init_time_end - gfx_init_time_start),
                "seconds")

    running = True
    while running:
        if PREFS['debug_perf']:
            frame_time_start = timer()

        events = gfx.get_events()
        if events == Events.QUIT:
            running = false
            break

        gfx.draw_test_pattern()

        if PREFS['debug_perf']:
            frame_time_end = timer()
            print("%.2f" % (1 / (frame_time_end - frame_time_start)), "fps")

if __name__ == '__main__':
    sys.exit(run())
