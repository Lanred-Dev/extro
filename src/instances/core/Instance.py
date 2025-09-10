from abc import abstractmethod, ABCMeta
from typing import TYPE_CHECKING, Tuple, Dict
from enum import Enum

import src.internal.InstanceHandler as InstanceHandler
from src.internal.components.InvalidationManager import InvalidationManager
from src.internal.components.Signal import Signal
from src.internal.components.Janitor import Janitor
from src.shared_types import EmptyFunction
from src.values.Vector2 import Vector2
from src.values.Color import Color
import src.internal.Console as Console
import src.internal.Renderer as Renderer

if TYPE_CHECKING:
    from src.instances.Scene import Scene


class InstanceUpdateType(Enum):
    POSITION = 0
    SIZE = 1
    ROTATION = 2
    COLOR = 3


class Instance(InvalidationManager, metaclass=ABCMeta):
    __slots__ = (
        "id",
        "_anchor",
        "_position",
        "_size",
        "_color",
        "_rotation",
        "_scale",
        "_scene",
        "_parent",
        "_parent_connections",
        "_actual_position",
        "_actual_size",
        "_is_size_relative",
        "_is_position_relative",
        "on_update",
        "on_destroy",
        "_janitor",
    )

    id: str
    _anchor: Vector2
    _position: Vector2
    _size: Vector2
    _color: Color
    _rotation: int
    _scale: Vector2
    _zindex: int
    _scene: "Scene"
    _parent: "Instance | None"
    _parent_connections: Dict[str, str]
    _actual_position: Vector2
    _actual_size: Vector2
    _actual_origin: Vector2
    _is_size_relative: bool
    _is_position_relative: bool
    _bounding: Tuple[float, float, float, float]

    on_update: Signal
    on_destroy: Signal
    _janitor: Janitor

    def __init__(
        self,
        anchor: Vector2 = Vector2(0, 0),
        position: Vector2 = Vector2(0, 0),
        size: Vector2 = Vector2(1, 1),
        color: Color = Color(255, 255, 255),
        rotation: int = 0,
        scale: Vector2 = Vector2(1, 1),
        zindex: int = 0,
    ):
        super().__init__()
        InstanceHandler.register_instance(self)

        self._anchor = anchor
        self._position = position
        self._size = size
        self._color = color
        self._rotation = rotation
        self._scale = scale
        self._zindex = zindex
        self._is_size_relative = False
        self._is_position_relative = False
        self._actual_position = Vector2(0, 0)
        self._actual_size = Vector2(0, 0)
        self._actual_origin = Vector2(0, 0)
        self._parent = None
        self._parent_connections = {}

        self.on_destroy = Signal()
        self.on_update = Signal()

        janitor: Janitor = Janitor()
        janitor.add(self.on_update)
        janitor.add(self.on_destroy.fire)
        janitor.add(self.on_destroy)
        janitor.add(InstanceHandler.unregister_instance, self.id)
        self._janitor = janitor

        # Position depends on size and for that reason `_recalculate_position` is called at the end of `_recalculate_size`
        self.invalidate(self._recalculate_size, 2)

    def destroy(self):
        super().destroy()
        self._janitor.destroy()

    def invalidate(self, callback: "EmptyFunction", priority: int = 0):
        super().invalidate(callback=callback, priority=priority)
        InstanceHandler.queue_instance_for_update(self)

    def parent_to(self, parent: "Instance | None"):
        if parent is None:
            self._parent = None
            return

        my_scene = getattr(self, "_scene", None)
        parent_scene = getattr(parent, "_scene", None)

        if my_scene != None and parent_scene != None and my_scene != parent_scene:
            parent._scene.add_instance(self)
            Console.log(f"{self.id} was added to {parent._scene.id} because of parent")

        self._parent = parent
        self._parent_connections["on_update"] = parent.on_update.connect(
            self._handle_parent_update
        )
        self._parent_connections["on_destroy"] = parent.on_destroy.connect(self.destroy)
        Console.log(f"{self.id} was parented to {parent._scene.id}")

        self.invalidate(self._recalculate_position)

    def translate(self, move_by: Vector2):
        self.position += move_by

    def add_child(self, child: "Instance"):
        child.parent_to(self)

    def _recalculate_bounding(self):
        self._bounding = (
            self._actual_position.x,
            self._actual_position.y,
            self._actual_size.x,
            self._actual_size.y,
        )

    def _handle_parent_update(self, property: InstanceUpdateType):
        if property != InstanceUpdateType.POSITION:
            return

        # Recalculate immediately to prevent frame delays
        self._recalculate_position()

    def _disconnect_parent_connections(self):
        if self._parent is None:
            return

        for signal, connection_id in self._parent_connections.items():
            getattr(self._parent, signal).disconnect(connection_id)

        self._parent_connections.clear()

    def _recalculate_position(self):
        self._actual_position.x = self._position.x
        self._actual_position.y = self._position.y

        if self._scene._type == Renderer.RenderTargetType.WORLD:
            Renderer.world_to_screen_coords(self._actual_position)
        else:
            Renderer.normalized_to_screen_coords(self._actual_position)

        if self._is_position_relative and self._parent:
            [parent_x, parent_y, parent_width, parent_height] = self._parent._bounding
            self._actual_position.x = parent_x + (
                parent_width * self._actual_position.x
            )
            self._actual_position.y = parent_y + (
                parent_height * self._actual_position.y
            )
        elif not self._is_position_relative and self._parent:
            self._actual_position += self._parent._actual_position

        # The instance will be drawn at its center so that needs to be accounted for along with the anchor
        self._actual_position.x -= (
            self._actual_size.x * self._anchor.x
        ) - self._actual_origin.x
        self._actual_position.y -= (
            self._actual_size.y * self._anchor.y
        ) - self._actual_origin.y

        self._apply_position()
        self._recalculate_bounding()

    def _recalculate_size(self):
        if self._is_size_relative and self._parent:
            [_, _, parent_width, parent_height] = self._parent._bounding
            self._actual_size.x = parent_width * self._size.x
            self._actual_size.y = parent_height * self._size.y
        else:
            self._actual_size.x = self._size.x
            self._actual_size.y = self._size.y

        self._actual_size.x *= self._scale.x

        if self._scene._type == Renderer.RenderTargetType.WORLD:
            Renderer.world_to_screen_coords(self._actual_size)
        else:
            Renderer.normalized_to_screen_coords(self._actual_size)

        self._actual_origin.x = self._actual_size.x / 2
        self._actual_origin.y = self._actual_size.y / 2

        self._apply_size()
        # Position depends on the size so it needs to be recalculated
        self._recalculate_position()

        # `_recalculate_bounding` is not called here because it is called in `_recalculate_position`

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, anchor: Vector2):
        if anchor.x > 1 or anchor.x < 0 or anchor.y > 1 or anchor.y < 0:
            Console.log(
                "Anchor much be between Vector2(0, 0) and Vector2(1, 1)",
                Console.LogType.ERROR,
            )
            return

        self._anchor = anchor
        self.invalidate(self._recalculate_position)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: Vector2):
        self._is_position_relative = position.x < 0 and position.y < 0

        if self._is_position_relative:
            position.x = abs(position.x)
            position.y = abs(position.y)

        self._position = position
        self.invalidate(self._recalculate_position, 1)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: Vector2):
        self._is_size_relative = size.x < 0 and size.y < 0

        if self._is_size_relative:
            size.x = abs(size.x)
            size.y = abs(size.y)

        self._size = size
        self.invalidate(self._recalculate_size, 2)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: Color):
        self._color = color
        self.invalidate(self._apply_color)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: int):
        self._rotation = rotation
        self.invalidate(self._apply_rotation)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale: Vector2):
        self._scale = scale
        self._recalculate_size()

    @property
    def bounding(self) -> Tuple[float, float, float, float]:
        return self._bounding

    def _apply_size(self):
        self.on_update.fire(InstanceUpdateType.SIZE)

    def _apply_position(self):
        self.on_update.fire(InstanceUpdateType.POSITION)

    def _apply_color(self):
        self.on_update.fire(InstanceUpdateType.COLOR)

    def _apply_rotation(self):
        self.on_update.fire(InstanceUpdateType.ROTATION)

    @abstractmethod
    def draw(self):
        raise NotImplementedError("Draw method must be implemented by subclass")
