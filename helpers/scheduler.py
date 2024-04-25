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

    def add_task(self, task):
        with self.lock:
            self.tasks.append(task)

    def remove_task(self, task):
        with self.lock:
            self.tasks.remove(task)

    def run(self):
        while True:
            with self.lock:
                for task in self.tasks:
                    if task.should_run():
                        task.start()
                        interruptible_sleep(0.5)
            interruptible_sleep(1)  # Sleep for a while to prevent high CPU usage