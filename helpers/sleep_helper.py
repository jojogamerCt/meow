import time
import msvcrt
from logger import Logger

logger = Logger.getInstance().get_logger()
from catch_statistics import CatchStatistics

catch_statistics = CatchStatistics()

def pause_execution():
    logger.warning('Execution paused. Press enter to continue...')
    input("")
    logger.info('Execution resumed...')
    # Sleep 3 seconds to avoid double key press
    time.sleep(3)

def show_statistics_execution():
    logger.warning('Execution paused. Press enter to continue...')
    
    catch_statistics.print_statistics()
    
    input("")
    logger.info('Execution resumed...')
    # Sleep 3 seconds to avoid double key press
    time.sleep(3)
    return

# Map keys to functions
commands = {
    'p': pause_execution,
    'P': pause_execution,
    's': show_statistics_execution,
    'S': show_statistics_execution
}

def interruptible_sleep(sleep_time):
    start_time = time.time()
    while time.time() - start_time < sleep_time:
        time.sleep(0.1)  # Check every 0.1 seconds
        if msvcrt.kbhit():
            key_pressed = msvcrt.getch().decode('utf-8')
            if key_pressed in commands:
                commands[key_pressed]()  # Call the corresponding function