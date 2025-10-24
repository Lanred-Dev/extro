from extro.internal.utils.BitMask import BitMask
import extro.internal.ComponentManager as ComponentManager
import extro.internal.InstanceManager as InstanceManager


class Component(BitMask):
    __slots__ = BitMask.__slots__ + (
        "_owner",
        "_type",
    )

    _key: str  # Key should be overridden in subclasses
    _owner: InstanceManager.InstanceIDType
    _type: ComponentManager.ComponentType

    def __init__(
        self,
        owner: InstanceManager.InstanceIDType,
        type: ComponentManager.ComponentType,
    ):
        super().__init__()

        self._owner = owner
        ComponentManager.register(owner, type, self)

    def destroy(self):
        ComponentManager.unregister(self._owner, self._type)
        InstanceManager.instances[self._owner].remove_component(self)
