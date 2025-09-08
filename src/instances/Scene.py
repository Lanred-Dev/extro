import pyglet
from typing import List, TYPE_CHECKING

from src.internal.Console import Console, LogType
from src.internal.Renderer import Renderer

if TYPE_CHECKING:
    from src.instances.core.Instance import Instance
    from src.shared_types import EmptyFunction


class Scene:
    id: str
    _zindex: int
    _batch: pyglet.graphics.Batch
    _instances: List[str]

    def __init__(self):
        self._zindex = 0
        self._batch = pyglet.graphics.Batch()
        self._instances = []
        Renderer.register_render_target(self)

    def destroy(self):
        Renderer.unregister_render_target(self)

    def add_instance(self, instance: "Instance"):
        if getattr(instance, "_scene", False):
            Console.log(
                f"{instance.id} is already part of scene {instance._scene.id}",
                LogType.WARNING,
            )
            return

        instance._scene = self
        self._instances.append(instance.id)
        Console.log(f"{instance.id} was added to {self.id}")

        instance._apply_new_batch()

    def remove_instance(self, instance: "Instance"):
        if instance._scene.id != self.id:
            Console.log(f"{instance.id} does not exist in {self.id}", LogType.WARNING)
            return

        self._instances.remove(instance.id)
        Console.log(f"{instance.id} was removed from {self.id}")

    @property
    def zindex(self):
        return self._zindex

    @zindex.setter
    def zindex(self, zindex: int):
        self._zindex = zindex
        Renderer.update_render_order()
