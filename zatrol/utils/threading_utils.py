import threading
from logging import getLogger

logger = getLogger(f"{__package__}.{__name__}")


def schedule(after_minutes: float, fn, fn_args=None, fn_kwargs=None) -> None:
    interval_s = 60 * after_minutes
    logger.info("%s will run again in %d seconds", fn.__name__, interval_s)
    threading.Timer(interval_s, fn, args=fn_args, kwargs=fn_kwargs).start()
