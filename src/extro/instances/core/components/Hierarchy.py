from typing import TYPE_CHECKING

from extro.instances.core.components.Component import Component
import extro.internal.ComponentManager as ComponentManager
from extro.instances.core.Instance import Instance
import extro.Console as Console
import extro.internal.InstanceManager as InstanceManager

if TYPE_CHECKING:
    from extro.instances.core.RenderTarget import RenderTarget


class Hierarchy(Component):
    __slots__ = Component.__slots__ + (
        "_owner",
        "_parent",
        "_children",
        "_render_target",
    )

    _key = "hierarchy"

    _owner: InstanceManager.InstanceID
    _parent: InstanceManager.InstanceID | None
    _children: list[InstanceManager.InstanceID]
    _render_target: InstanceManager.InstanceID | None

    def __init__(
        self,
        owner: InstanceManager.InstanceID,
        parent: Instance | None = None,
    ):
        super().__init__(owner, ComponentManager.ComponentType.HIERARCHY)

        self._owner = owner
        self._children = []
        self.parent = parent
        self._render_target = None

    def destroy(self):
        super().destroy()

        for child_id in self._children[:]:
            InstanceManager.instances[child_id].destroy()

        if self._render_target:
            render_target: "RenderTarget" = InstanceManager.instances[self._render_target]  # type: ignore
            render_target.remove(InstanceManager.instances[self._owner])

    @property
    def parent(self) -> InstanceManager.InstanceID | None:
        return self._parent

    @parent.setter
    def parent(self, parent: Instance | None):
        if parent is None:
            self._parent = None
            return

        if parent._id not in ComponentManager.hierarchies:
            Console.log(
                f"Cannot set parent to instance {parent._id} as it has no Hierarchy component",
                Console.LogType.ERROR,
            )
            return
        elif parent._id == self._owner:
            Console.log(
                f"Cannot set parent to instance {parent._id} as it is the same as the owner",
                Console.LogType.ERROR,
            )
            return

        self._parent = parent._id if parent is not None else None
        ComponentManager.hierarchies[parent._id]._children.append(self._owner)

    @property
    def children(self) -> "list[InstanceManager.InstanceID]":
        return self._children

    def add_child(self, child: Instance):
        if child._id not in ComponentManager.hierarchies:
            Console.log(
                f"Cannot add child instance {child._id} as it has no Hierarchy component",
                Console.LogType.ERROR,
            )
            return
        elif child._id == self._owner:
            Console.log(
                f"Cannot add child instance {child._id} as it is the same as the owner",
                Console.LogType.ERROR,
            )
            return

        self._children.append(child._id)
        ComponentManager.hierarchies[child._id]._parent = self._owner

    def remove_child(self, child: Instance):
        if child._id not in self._children:
            Console.log(
                f"Cannot remove child instance {child._id} as it is not a child of owner {self._owner}",
                Console.LogType.ERROR,
            )
            return

        self._children.remove(child._id)
        ComponentManager.hierarchies[child._id]._parent = None
