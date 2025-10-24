from enum import IntFlag


class BitMask:
    __slots__ = ("_flags",)

    _flags: int

    def __init__(self):
        self.clear_flags()

    def add_flag(self, flag: IntFlag):
        self._flags |= flag

    def remove_flag(self, flag: IntFlag):
        self._flags &= ~flag

    def has_flag(self, flag: IntFlag) -> bool:
        return (self._flags & flag) == flag

    def is_empty(self) -> bool:
        return self._flags == 0

    def clear_flags(self):
        self._flags = 0
