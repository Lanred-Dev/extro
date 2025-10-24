from typing import Any

from extro.utils.Signal import Signal
from extro.utils.Janitor import Janitor
import extro.internal.InstanceManager as InstanceManager


class Instance:
    __slots__ = (
        "_id",
        "on_destroy",
        "_janitor",
        "_components",
    )

    _id: int
    on_destroy: Signal
    _janitor: Janitor
    _components: dict[str, Any]

    def __init__(
        self,
    ):
        InstanceManager.register(self)

        self.on_destroy = Signal()
        self._components = {}

        self._janitor = Janitor()
        self._janitor.add(self.on_destroy.fire)
        self._janitor.add(self.on_destroy)

    def destroy(self):
        self._janitor.destroy()
        InstanceManager.unregister(self._id)

    def add_component(self, component: Any):
        self._components[component._key] = component
        self._janitor.add(component.destroy)

    def remove_component(self, component: Any):
        """Removes a component from the instance. Note that this does not destroy the component."""
        del self._components[component._key]

    def get_component(self, name: str) -> Any | None:
        return self._components.get(name, None)

    def get_component_unsafe(self, name: str) -> Any:
        """Get a component without checking if it exists. May raise KeyError."""
        return self._components[name]

    @property
    def id(self) -> int:
        return self._id
