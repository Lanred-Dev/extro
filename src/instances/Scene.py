from typing import List, Dict, TYPE_CHECKING

import src.internal.Console as Console
import src.internal.Renderer as Renderer
from src.shared_types import RenderTargetType

if TYPE_CHECKING:
    from src.instances.core.Instance import Instance


class Scene:
    id: str
    _zindex: int
    _instances: "Dict[str, Instance]"
    _render_order: List[str]
    _type: RenderTargetType

    def __init__(
        self,
        zindex: int = 0,
        type: RenderTargetType = RenderTargetType.WORLD,
    ):
        self._zindex = zindex
        self._type = type
        self._instances = {}
        self._render_order = []
        Renderer.register_render_target(self)

    def destroy(self):
        Renderer.unregister_render_target(self.id)

    def add_instance(self, instance: "Instance"):
        if getattr(instance, "_scene", False):
            Console.log(
                f"{instance.id} is already part of scene {instance._scene.id}",
                Console.LogType.WARNING,
            )
            return

        instance._scene = self
        self._instances[instance.id] = instance
        Console.log(f"{instance.id} was added to {self.id}")
        self._render_order = Renderer.calculate_render_order(
            list(self._instances.values())
        )

    def remove_instance(self, instance: "Instance"):
        if instance._scene.id != self.id:
            Console.log(
                f"{instance.id} does not exist in {self.id}", Console.LogType.WARNING
            )
            return

        del self._instances[instance.id]
        Console.log(f"{instance.id} was removed from {self.id}")
        self._render_order = Renderer.calculate_render_order(
            list(self._instances.values())
        )

    def draw(self):
        for instance_id in self._render_order:
            instance: "Instance" = self._instances[instance_id]
            instance.draw()

    @property
    def zindex(self):
        return self._zindex

    @zindex.setter
    def zindex(self, zindex: int):
        self._zindex = zindex
        Renderer._recalculate_render_target_order()

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type: RenderTargetType):
        self._type = type
        Renderer._recalculate_render_target_order()
