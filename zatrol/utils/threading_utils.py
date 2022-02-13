import threading
import time
from logging import getLogger

logger = getLogger(f"{__package__}.{__name__}")


def run_periodically(interval_minutes: float, fn, fn_args=[], fn_kwargs={}) -> None:
    def run_and_schedule():
        start_time = time.perf_counter()
        fn(*fn_args, **fn_kwargs)
        duration = time.perf_counter() - start_time
        remaining_time = 60 * interval_minutes - duration
        logger.info("%s will run again in %d minutes", fn.__name__, remaining_time / 60)
        threading.Timer(remaining_time, run_and_schedule).start()

    run_and_schedule()
