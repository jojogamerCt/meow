import threading
import time
from helpers.sleep_helper import interruptible_sleep

class Task:
    def __init__(self, func, interval_func):
        self.func = func
        self.interval_func = interval_func
        self.last_run = 0
        self.enabled = True  # Add an enabled attribute

    def start(self):
        if self.enabled:  # Only run the task if it's enabled
            self.func()
            self.last_run = time.time()

    def should_run(self):
        return self.enabled and (time.time() - self.last_run) > self.interval_func()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

class Scheduler:
    def __init__(self):
        self.tasks = []
        self.lock = threading.Lock()
        
        # Human-like session / break parameters
        import random
        self.session_start_time = time.time()
        self.session_duration = random.randint(30 * 60, 45 * 60)  # Active session: 30 to 45 minutes
        self.is_resting = False
        self.rest_start_time = 0
        self.rest_duration = 0

    def add_task(self, task):
        with self.lock:
            self.tasks.append(task)

    def remove_task(self, task):
        with self.lock:
            self.tasks.remove(task)

    def run(self):
        import random
        from logger import Logger
        logger = Logger().get_logger()
        
        # Log initial session parameters
        logger.info(f"🎮 Bot session started. Active session duration: {self.session_duration / 60:.1f} minutes.")

        while True:
            now = time.time()
            if self.is_resting:
                # Check if break is over
                elapsed_rest = now - self.rest_start_time
                if elapsed_rest >= self.rest_duration:
                    self.is_resting = False
                    self.session_start_time = time.time()
                    self.session_duration = random.randint(30 * 60, 45 * 60)
                    logger.info("☕ Break finished! Starting a new active session of {:.1f} minutes...".format(self.session_duration / 60))
                else:
                    remaining_rest = (self.rest_duration - elapsed_rest) / 60
                    # Log every 5 minutes (300 seconds) during rest
                    if int(elapsed_rest) % 300 == 0:
                        logger.info("☕ Currently taking a human-like break. {:.1f} minutes remaining...".format(remaining_rest))
                    interruptible_sleep(1)
                    continue
            else:
                # Check if current session has exceeded duration
                elapsed_session = now - self.session_start_time
                if elapsed_session >= self.session_duration:
                    self.is_resting = True
                    self.rest_start_time = time.time()
                    self.rest_duration = random.randint(20 * 60, 30 * 60)
                    logger.warning("☕ Active session finished ({:.1f} mins). Taking a human-like break for {:.1f} minutes...".format(elapsed_session / 60, self.rest_duration / 60))
                    interruptible_sleep(1)
                    continue

            with self.lock:
                for task in self.tasks:
                    if task.should_run():
                        task.start()
                        # Random delay between tasks (0.5 to 1.5 seconds) to be more human-like
                        interruptible_sleep(random.uniform(0.5, 1.5))
            interruptible_sleep(1)  # Sleep for a while to prevent high CPU usage