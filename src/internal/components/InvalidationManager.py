from contextlib import contextmanager
from typing import List, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from src.shared_types import EmptyFunction


class InvalidationManager:
    _suspend_updates: bool
    _is_dirty: bool
    _callbacks: List[Tuple[int, "EmptyFunction"]]

    def __init__(self):
        self._callbacks = []
        self._is_dirty = False
        self._suspend_updates = False

    def destroy(self):
        self._suspend_updates = True
        self._callbacks.clear()

    def invalidate(self, callback: "EmptyFunction", priority: int = 0):
        if callback in self._callbacks:
            return

        self._is_dirty = True
        self._callbacks.append((priority, callback))

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

        for priority, callback in sorted(self._callbacks, key=lambda x: x[0]):
            callback()

        self._callbacks.clear()
        self._is_dirty = False
