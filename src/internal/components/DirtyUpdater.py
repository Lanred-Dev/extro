from contextlib import contextmanager
from src.shared_types import EmptyFunction
from typing import List


class DirtyUpdater:
    __suspend_updates: bool
    __dirty: List[EmptyFunction]

    def __init__(self):
        self.__dirty = []
        self.__suspend_updates = False

    def mark_dirty(self, callback: EmptyFunction):
        if callback in self.__dirty:
            return

        self.__dirty.append(callback)

    @contextmanager
    def batch_update(self):
        self.__suspend_updates = True

        try:
            yield
        finally:
            self.__suspend_updates = False
            self.recompute_if_needed()

    def recompute_if_needed(self):
        if len(self.__dirty) > 0 and not self.__suspend_updates:
            for callback in self.__dirty:
                callback()

            self.__dirty.clear()
