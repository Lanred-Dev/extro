from typing import TYPE_CHECKING

from extro.internal.utils.BitMask import BitMask
import extro.internal.ComponentManager as ComponentManager

if TYPE_CHECKING:
    import extro.internal.InstanceManager as InstanceManager


class Component(BitMask):
    _key: str

    def __init__(
        self,
        owner: "InstanceManager.InstanceIDType",
        type: ComponentManager.ComponentType,
    ):
        super().__init__()
        ComponentManager.register(owner, type, self)

    def destroy(self):
        pass
