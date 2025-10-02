from typing import TYPE_CHECKING

from extro.internal.utils.BitMask import BitMask

if TYPE_CHECKING:
    from extro.internal.InstanceManager import InstanceIDType


class Component(BitMask):
    __slots__ = BitMask.__slots__ + ("_owner",)

    _owner: "InstanceIDType"

    def __init__(self, owner: "InstanceIDType"):
        super().__init__()
        self._owner = owner

    def destroy(self):
        pass
