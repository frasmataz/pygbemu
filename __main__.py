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

    test_pattern = gfx.get_test_pattern()
    last_fps_message_time = timer()
    running = True
    while running:
        if PREFS['debug_perf']:
            frame_time_start = timer()

        events = gfx.get_events()
        if events == Events.QUIT:
            running = False
            break

        gfx.draw(test_pattern)

        if PREFS['debug_perf']:
            frame_time_end = timer()
            if (timer() - last_fps_message_time) > 1:
                print("%.2f" % (1 / (frame_time_end - frame_time_start)), "fps")
                last_fps_message_time = timer()

if __name__ == '__main__':
    sys.exit(run())
