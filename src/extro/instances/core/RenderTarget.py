from typing import TYPE_CHECKING, Any

from extro.instances.core.Instance import Instance
from extro.internal.utils.BitMask import BitMask
import extro.internal.systems.Render as RenderSystem
import extro.services.Render as RenderService
from extro.internal.utils.InstanceRegistry import InstanceRegistry
import extro.internal.InstanceManager as InstanceManager
import extro.internal.ComponentManager as ComponentManager
import extro.Console as Console

if TYPE_CHECKING:
    from extro.instances.core.Instance import Instance
    import extro.internal.InstanceManager as InstanceManager
    from extro.instances.core.components.Hierarchy import Hierarchy


def is_instance_valid(instance_id: "InstanceManager.InstanceID") -> bool:
    instance = InstanceManager.instances[instance_id]

    return (
        instance.get_component("drawable") is not None
        and instance.get_component("transform") is not None
        and instance.get_component("hierarchy") is not None
    )


class RenderTarget(Instance):
    __slots__ = Instance.__slots__ + (
        "_type",
        "_id",
        "is_visible",
        "_zindex",
        "instances",
    )

    _id: int
    is_visible: bool
    _zindex: int
    _instances: InstanceRegistry
    _type: RenderService.RenderTargetType
    bitmask: BitMask
    _render_order: "list[InstanceManager.InstanceID]"

    def __init__(
        self,
        type: RenderService.RenderTargetType,
        zindex: int = 0,
        is_visible: bool = True,
    ):
        super().__init__()

        self._instances = InstanceRegistry(
            f"RenderTarget({self._id})",
            preregister_check=is_instance_valid,
            on_list_change=lambda: self.bitmask.add_flag(
                RenderSystem.RenderTargetDirtyFlags.RENDER_ORDER
            ),
        )
        self._type = type
        self._zindex = zindex
        self.is_visible = is_visible
        self.bitmask = BitMask()
        self._render_order = []

        RenderSystem.render_targets.register(self._id)

    def destroy(self):
        super().destroy()

        for instance_id in self._instances.instances[:]:
            instance: "Instance" = InstanceManager.instances[instance_id]  # type: ignore
            self.remove(instance)

        RenderSystem.render_targets.unregister(self._id)

    def add(self, instance: "Instance"):
        self._instances.register(instance._id)

        hierarchy: "Hierarchy | None" = instance.get_component("hierarchy")
        if hierarchy and instance._id in self._instances.instances:
            hierarchy._render_target = self._id

            for child_id in hierarchy.children:
                child_instance: "Instance" = InstanceManager.instances[child_id]  # type: ignore
                self.add(child_instance)

    def remove(self, instance: "Instance"):
        self._instances.unregister(instance._id)

        hierarchy: "Hierarchy | None" = instance.get_component("hierarchy")
        if hierarchy and instance._id not in self._instances.instances:
            hierarchy._render_target = None

    def add_component(self, component: Any):
        Console.log("`RenderTarget` cannot have components", Console.LogType.ERROR)
        return

    def get_component(self, name: str) -> Any | None:
        Console.log("`RenderTarget` cannot have components", Console.LogType.ERROR)
        return

    def get_component_unsafe(self, name: str) -> Any:
        Console.log("`RenderTarget` cannot have components", Console.LogType.ERROR)
        return

    def draw(self):
        for instance_id in self._render_order[:]:
            drawable = ComponentManager.drawables[instance_id]

            if not drawable.is_visible:
                continue

            drawable._render_command()

    @property
    def id(self) -> int:
        return self._id

    @property
    def zindex(self) -> int:
        return self._zindex

    @zindex.setter
    def zindex(self, zindex: int):
        self._zindex = zindex
        self.bitmask.add_flag(RenderSystem.RenderTargetDirtyFlags.ZINDEX)
