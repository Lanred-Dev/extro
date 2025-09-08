from contextlib import contextmanager
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.shared_types import EmptyFunction


class InvalidationManager:
    _suspend_updates: bool
    _is_dirty: bool
    _callbacks: List["EmptyFunction"]

    def __init__(self):
        self._callbacks = []
        self._is_dirty = False
        self._suspend_updates = False

    def destroy(self):
        self._suspend_updates = True
        self._callbacks.clear()

    def invalidate(self, callback: "EmptyFunction"):
        if callback in self._callbacks:
            return

        self._is_dirty = True
        self._callbacks.append(callback)

    @contextmanager
    def batch_update(self):
        self._suspend_updates = True

        try:
            yield
        finally:
            self._suspend_updates = False
            self.flush()

    def flush(self):
        if not self._is_dirty or self._suspend_updates:
            return

        for callback in list(self._callbacks):
            callback()

        self._callbacks.clear()
        self._is_dirty = False
