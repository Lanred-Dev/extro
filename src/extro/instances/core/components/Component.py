from extro.internal.utils.BitMask import BitMask
import extro.internal.ComponentManager as ComponentManager
import extro.internal.InstanceManager as InstanceManager


class Component(BitMask):
    __slots__ = BitMask.__slots__ + (
        "_owner",
        "_type",
    )

    _key: str  # Key should be overridden in subclasses
    _owner: InstanceManager.InstanceID
    _type: ComponentManager.ComponentType

    def __init__(
        self,
        owner: InstanceManager.InstanceID,
        type: ComponentManager.ComponentType,
    ):
        super().__init__()

        self._owner = owner
        self._type = type
        ComponentManager.register(owner, type, self)

    def destroy(self):
        ComponentManager.unregister(self._owner, self._type)
        InstanceManager.instances[self._owner].remove_component(self)
