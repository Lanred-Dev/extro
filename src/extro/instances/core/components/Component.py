from typing import TYPE_CHECKING

from extro.internal.utils.BitMask import BitMask
import extro.internal.ComponentManager as ComponentManager

if TYPE_CHECKING:
    from extro.internal.InstanceManager import InstanceIDType


class Component(BitMask):
    def __init__(self, owner: "InstanceIDType", type: ComponentManager.ComponentType):
        super().__init__()
        ComponentManager.register(owner, type, self)

    def destroy(self):
        pass
