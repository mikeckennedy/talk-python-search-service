from .search_sources import SearchSources
import time
from threading import Thread
import datetime

__exit_signaled = False
__bg_task = None
__freq_in_seconds = 60 * 60


def signal_exit():
    global __exit_signaled
    __exit_signaled = True

    if not __bg_task:
        return

    __bg_task.join()


def set_frequency(freq_in_seconds):
    global __freq_in_seconds

    if freq_in_seconds < 60:
        raise Exception("Frequency must be at least 1 minute.")

    __freq_in_seconds = freq_in_seconds


def start_search_task():
    print("Starting search task...")

    global __bg_task
    bg = Thread(target=__task_loop)
    bg.daemon = True
    bg.start()
    __bg_task = bg


def __task_loop():
    print("Search task started (bg thread, frequency: {} sec)".format(__freq_in_seconds))
    last_action = datetime.datetime.now()

    while not __exit_signaled:
        time.sleep(.05)
        now = datetime.datetime.now()
        dt = now - last_action
        if dt.total_seconds() > __freq_in_seconds:
            last_action = now
            SearchSources.build_records(force=True)
            SearchSources.trim_data()

    print("Search task exited (bg thread)")
