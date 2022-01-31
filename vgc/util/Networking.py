import contextlib
import threading


class WouldBlockError(Exception):
    pass


@contextlib.contextmanager
def non_blocking_lock(lock=threading.Lock()):
    if not lock.acquire(blocking=False):
        raise WouldBlockError
    try:
        yield lock
    finally:
        lock.release()
