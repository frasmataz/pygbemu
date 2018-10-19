from events import Events
from graphics import Graphics
import sys
from timeit import default_timer as timer

global GB_PARAMS 
GB_PARAMS = {
            'screen_res': (160, 144),
            'clk_spd_mhz': '4.194'
            }

PREFS = {
        'debug_perf': True
        }

def load_rom(filepath):
    fh = open(filepath, 'rb')
    data = fh.read()
    print('Loaded ' + str(len(data)) + ' bytes.')
    return data


def run():
    # Load the ROM file into memory
    try:
        print('Opening ' + sys.argv[1])
        rom_file = load_rom(sys.argv[1])
    except IndexError:
        print('No ROM file specified!')
        return 1

    # Initialise the graphics module
    gfx = Graphics(GB_PARAMS)

    # Prepare graphics test pattern
    test_pattern = gfx.get_test_pattern()

    # Initialise performance timers if requested
    if PREFS['debug_perf']:
        last_fps_message_time = timer()

    # MAIN EXECUTION LOOP BEGINS
    running = True
    while running:
        # Start frame timer
        if PREFS['debug_perf']:
            frame_time_start = timer()

        # Handle input events
        events = gfx.get_events()
        if events == Events.QUIT:
            running = False
            break

        # Render frame
        gfx.draw(test_pattern)

        # Measure frame rate
        if PREFS['debug_perf']:
            frame_time_end = timer()
            if (timer() - last_fps_message_time) > 1:
                print("%.2f" % (1 / (frame_time_end - frame_time_start)), "fps")
                last_fps_message_time = timer()

    # MAIN EXECUTION LOOP ENDS

if __name__ == '__main__':
    sys.exit(run())
