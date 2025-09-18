import src.internal.Console as Console
import src.internal.handlers.Renderer as Renderer
from src.internal.shared_types import RenderTargetType
from src.instances.core.DrawableInstance import DrawableInstance


class Scene:
    id: str
    _zindex: int
    _instances: "dict[str, DrawableInstance]"
    _render_order: list[str]
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

    def add(self, instance: "DrawableInstance"):
        if not isinstance(instance, DrawableInstance):
            Console.log(
                f"{instance} is not a `DrawableInstance` and cannot be added to {self.id}",
                Console.LogType.ERROR,
            )
            return
        elif getattr(instance, "_scene", False):
            Console.log(
                f"{instance.id} is already part of scene {instance._scene.id}",
                Console.LogType.WARNING,
            )
            return

        instance._scene = self
        self._instances[instance.id] = instance
        Console.log(f"{instance.id} was added to {self.id}")
        self._recalculate_render_order()

    def remove(self, instance_id: str):
        instance = self._instances.get(instance_id)

        if not instance:
            Console.log(
                f"{instance_id} is not a part of {self.id}", Console.LogType.WARNING
            )
            return

        del self._instances[instance.id]
        Console.log(f"{instance.id} was removed from {self.id}")
        self._recalculate_render_order()

    def _recalculate_render_order(self):
        self._render_order = Renderer.calculate_render_order(
            list(self._instances.values())
        )

    def draw(self):
        for instance_id in self._render_order:
            self._instances[instance_id].draw()

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
