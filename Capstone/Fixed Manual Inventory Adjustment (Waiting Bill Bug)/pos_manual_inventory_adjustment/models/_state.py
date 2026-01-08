import threading
import time

_thread_local = threading.local()


def set_skip_po_updates(flag: bool) -> None:
    _thread_local.skip_po_updates = bool(flag)
    if flag:
        # Also set a timestamp so we can check how recent it is
        _thread_local.skip_po_timestamp = time.time()


def get_skip_po_updates() -> bool:
    return bool(getattr(_thread_local, 'skip_po_updates', False))


def get_skip_po_timestamp() -> float:
    return float(getattr(_thread_local, 'skip_po_timestamp', 0.0))
