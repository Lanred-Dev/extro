from contextlib import contextmanager
from typing import TYPE_CHECKING

import extro.internal.InstanceManager as InstanceManager

if TYPE_CHECKING:
    from extro.shared.types import EmptyFunction


class InvalidationManager:
    _suspend_updates: bool
    _is_dirty: bool
    _callbacks: "list[tuple[int, EmptyFunction]]"

    def __init__(self):
        self._callbacks = []
        self._is_dirty = False
        self._suspend_updates = False

    def destroy(self):
        self._suspend_updates = True
        self._callbacks.clear()

    def invalidate(self, callback: "EmptyFunction", priority: int = 0):
        """Mark the manager as dirty and schedules a callback to be called on the next flush."""
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
        """If the manager is dirty and not suspended, calls all scheduled callbacks."""
        if not self._is_dirty or self._suspend_updates:
            return

        for _, callback in sorted(self._callbacks, key=lambda x: x[0]):
            callback()

        self._callbacks.clear()
        self._is_dirty = False


class InstanceInvalidationManager(InvalidationManager):
    _owner_id: int

    def __init__(self, owner_id: int):
        super().__init__()
        self._owner_id = owner_id

    def invalidate(self, callback: "EmptyFunction", priority: int = 0):
        super().invalidate(callback, priority)
        InstanceManager.queue_for_update(self._owner_id)


__all__ = ["InvalidationManager", "InstanceInvalidationManager"]
