from abc import abstractmethod, ABCMeta
from typing import TYPE_CHECKING

from src.values.Vector2 import Vector2
from src.values.Color import Color
import src.internal.Console as Console
from src.instances.core.Instance import Instance
from src.internal.shared_types import InstanceUpdateType, RenderTargetType

if TYPE_CHECKING:
    from src.instances.core.Scene import Scene


class DrawableInstance(Instance, metaclass=ABCMeta):
    __slots__ = (
        "_color",
        "_zindex",
        "_scene",
        "_render_origin",
    )

    _color: Color
    _zindex: int
    _scene: "Scene"
    _render_origin: Vector2

    def __init__(
        self,
        color: Color = Color(255, 255, 255),
        zindex: int = 0,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._color = color
        self._zindex = zindex
        self._render_origin = Vector2(0, 0)

    def destroy(self):
        if self._scene:
            self._scene.remove(self.id)

        super().destroy()

    def parent_to(self, parent: "Instance | None"):
        super().parent_to(parent)

        if self._parent is None:
            return

        my_scene: "Scene | None" = getattr(self, "_scene", None)
        parent_scene: "Scene | None" = getattr(self._parent, "_scene", None)

        if parent_scene and my_scene is not parent_scene:
            if my_scene:
                my_scene.remove(self.id)

            parent_scene.add(self)
            Console.log(f"{self.id} was added to {parent_scene.id} because of parent")

        parent_zindex: int | None = getattr(self._parent, "zindex", None)

        if parent_zindex:
            self.zindex = parent_zindex + 1
            Console.log(f"{self.id} zindex was set to {self.zindex} because of parent")

    def _recalculate_position(self, *_: object, **__: object):
        super()._recalculate_position(self._render_origin, self._scene._type)

    def _recalculate_size(self, *_: object, **__: object):
        super()._recalculate_size(self._scene._type)

    def _apply_size(self):
        self._render_origin.x = self._actual_size.x / 2
        self._render_origin.y = self._actual_size.y / 2
        super()._apply_size()

    @property
    def zindex(self):
        return self._zindex

    @zindex.setter
    def zindex(self, zindex: int):
        self._zindex = zindex
        self._scene._recalculate_render_order()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: Color):
        self._color = color
        self.invalidate(self._apply_color)

    def _apply_color(self):
        self.on_update.fire(InstanceUpdateType.COLOR)

    @abstractmethod
    def draw(self):
        # This error is raised because this is not something that should occur during runtime
        raise NotImplementedError("Draw method must be implemented by subclass")
