import extro.Console as Console
import extro.internal.systems.Render as RenderSystem
from extro.core.Instance.Drawable import DrawableInstance
from extro.utils.Janitor import Janitor
from extro.shared.types import RenderTargetType


class Scene:
    __slots__ = (
        "is_visible",
        "_instances",
        "_render_order",
        "_type",
        "_zindex",
        "_id",
        "_janitor",
    )

    _id: str
    _zindex: int
    _instances: "dict[int, DrawableInstance]"
    _render_order: list[int]
    _type: RenderTargetType
    is_visible: bool
    _janitor: Janitor

    def __init__(
        self,
        zindex: int = 0,
        type: RenderTargetType = RenderTargetType.WORLD,
        is_visible: bool = True,
    ):
        self._zindex = zindex
        self._type = type
        self._instances = {}
        self._render_order = []
        self.is_visible = is_visible

        self._janitor = Janitor()
        RenderSystem.register(self)
        self._janitor.add(RenderSystem.unregister, self.id)

    def destroy(self):
        """Destroy the scene and all its instances."""
        self._janitor.destroy()

        for instance in list(self._instances.values()):
            instance.destroy()

    def add(self, instance: "DrawableInstance"):
        """Add a drawable instance to the scene."""
        if not isinstance(instance, DrawableInstance):
            Console.log(
                f"Instance {instance} is not a `Drawable` and cannot be added to {self.id}",
                Console.LogType.ERROR,
            )
            return
        elif getattr(instance, "_scene", False):
            Console.log(
                f"Instance {instance.id} is already part of scene {instance._scene.id}",
                Console.LogType.WARNING,
            )
            return

        instance._scene = self
        self._instances[instance.id] = instance
        Console.log(f"Instance {instance.id} was added to {self.id}")
        self._recalculate_render_order()

    def remove(self, instance_id: int):
        """Remove a drawable instance from the scene."""
        if instance_id not in self._instances:
            Console.log(
                f"Instance {instance_id} is not a part of {self.id}",
                Console.LogType.WARNING,
            )
            return

        del self._instances[instance_id]
        Console.log(f"Instance {instance_id} was removed from {self.id}")
        self._recalculate_render_order()

    def _recalculate_render_order(self):
        self._render_order = RenderSystem.calculate_render_order(
            list(self._instances.values())
        )

    def draw(self):
        """
        Draw the scene to the screen.

        This is intended for internal use only, but for debugging purposes it has been exposed.
        """
        if not self.is_visible:
            return

        for instance_id in self._render_order:
            instance = self._instances[instance_id]

            if not instance.is_visible:
                continue

            instance.draw()

    @property
    def zindex(self) -> int:
        return self._zindex

    @zindex.setter
    def zindex(self, zindex: int):
        self._zindex = zindex
        RenderSystem.recalculate_render_order()

    @property
    def type(self) -> RenderTargetType:
        return self._type

    @type.setter
    def type(self, type: RenderTargetType):
        self._type = type
        RenderSystem.recalculate_render_order()

    @property
    def id(self) -> str:
        return self._id
