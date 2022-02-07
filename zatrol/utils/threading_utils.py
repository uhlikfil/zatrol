import threading
from logging import getLogger

logger = getLogger(f"{__package__}.{__name__}")


def schedule(fn, after_h: float) -> None:
    interval_s = 60 * 60 * after_h
    logger.info("%s will run again in %d seconds", fn.__name__, interval_s)
    threading.Timer(interval_s, fn).start()
