from typing import TYPE_CHECKING, Any

from extro.instances.core.Instance import Instance
from extro.internal.utils.BitMask import BitMask
import extro.internal.systems.Render as RenderSystem
from extro.internal.utils.InstanceRegistry import InstanceRegistry
import extro.internal.InstanceManager as InstanceManager
import extro.internal.ComponentManager as ComponentManager
import extro.Console as Console

if TYPE_CHECKING:
    from extro.instances.core.Instance import Instance
    from extro.internal.InstanceManager import InstanceIDType
    from extro.instances.core.components.Drawable import Drawable


def is_instance_renderable(instance_id: "InstanceIDType") -> bool:
    instance = InstanceManager.instances[instance_id]
    return (
        instance.get_component("drawable") is not None
        and instance.get_component("transform") is not None
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
    _type: RenderSystem.RenderTargetType
    bitmask: BitMask
    _render_order: "list[InstanceIDType]"

    def __init__(
        self,
        type: RenderSystem.RenderTargetType,
        zindex: int = 0,
        is_visible: bool = True,
    ):
        super().__init__()

        self._instances = InstanceRegistry(
            f"RenderTarget({self._id})",
            preregister_check=is_instance_renderable,
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
        RenderSystem.render_targets.unregister(self._id)

    def add(self, instance: "Instance"):
        self._instances.register(instance._id)

    def remove(self, instance: "Instance"):
        self._instances.unregister(instance._id)

    def add_component(self, name: str, component: Any):
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
