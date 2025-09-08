from abc import abstractmethod, ABCMeta
from typing import TYPE_CHECKING, Tuple, Dict
from enum import Enum

from src.internal.InstanceHandler import InstanceHandler
from src.internal.components.InvalidationManager import InvalidationManager
from src.internal.components.Signal import Signal
from src.internal.components.Janitor import Janitor
from src.shared_types import EmptyFunction
from src.values.Vector2 import Vector2
from src.values.Color import Color
from src.internal.Console import Console, LogType

if TYPE_CHECKING:
    from src.instances.Scene import Scene


class InstanceUpdateType(Enum):
    POSITION = 0
    SIZE = 1
    ROTATION = 2


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
    _scene: "Scene"
    _parent: "Instance | None"
    _parent_connections: Dict[str, str]
    _actual_position: Vector2
    _actual_size: Vector2
    _is_size_relative: bool
    _is_position_relative: bool
    _bounding: Tuple[float, float, float, float]
    _position_offset: Vector2

    on_update: Signal
    on_destroy: Signal
    _janitor: Janitor

    def __init__(
        self,
        anchor: Vector2 = Vector2(0, 0),
        _position: Vector2 = Vector2(0, 0),
        _size: Vector2 = Vector2(1, 1),
        _color: Color = Color(255, 255, 255),
        _rotation: int = 0,
        _scale: Vector2 = Vector2(1, 1),
    ):
        super().__init__()
        InstanceHandler.register_instance(self)

        self._anchor = anchor
        self._position = _position
        self._size = _size
        self._color = _color
        self._rotation = _rotation
        self._scale = _scale
        self._is_size_relative = False
        self._is_position_relative = False
        self._actual_position = Vector2(0, 0)
        self._actual_size = Vector2(0, 0)
        self._position_offset = Vector2(0, 0)
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

        # On next frame, calculate size and position for the first time
        self.invalidate(self._recalculate_size)
        self.invalidate(self._recalculate_position)

    def destroy(self):
        super().destroy()
        self._janitor.destroy()

    def invalidate(self, callback: EmptyFunction):
        super().invalidate(callback)
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

        self._recalculate_position()

    def _disconnect_parent_connections(self):
        if self._parent is None:
            return

        for signal, connection_id in self._parent_connections.items():
            getattr(self._parent, signal).disconnect(connection_id)

        self._parent_connections.clear()

    def _recalculate_position(self):
        if self._is_position_relative and self._parent:
            [parent_x, parent_y, parent_width, parent_height] = self._parent._bounding
            self._actual_position.x = (
                parent_x
                + (parent_width * self._position.x)
                - (self._actual_size.x * self._anchor.x)
            )
            self._actual_position.y = (
                parent_y
                + (parent_height * self._position.y)
                - (self._actual_size.y * self._anchor.y)
            )
        else:
            self._actual_position.x = self._position.x - (
                self._actual_size.x * self._anchor.x
            )
            self._actual_position.y = self._position.y - (
                self._actual_size.y * self._anchor.y
            )

            if self._parent:
                self._actual_position += self._parent._actual_position

        self._actual_position += self._position_offset
        self._recalculate_bounding()
        self._apply_position()

    def _recalculate_size(self):
        if self._is_size_relative and self._parent:
            [_, _, parent_width, parent_height] = self._parent._bounding
            self._actual_size.x = parent_width * self._size.x
            self._actual_size.y = parent_height * self._size.y
        else:
            self._actual_size.x = self._size.x
            self._actual_size.y = self._size.y

        self._actual_size.x *= self._scale.x
        self._actual_size.y *= self._scale.y
        self._recalculate_bounding()
        self._apply_size()

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, anchor: Vector2):
        if anchor.x > 1 or anchor.x < 0 or anchor.y > 1 or anchor.y < 0:
            Console.log(
                "Anchor much be between Vector2(0, 0) and Vector2(1, 1)", LogType.ERROR
            )
            return

        self._anchor = anchor
        self.invalidate(self._recalculate_position)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: Vector2):
        if position.x < 0 and position.y < 0:
            self._is_position_relative = True
            position.x = abs(position.x)
            position.y = abs(position.y)
        else:
            self._is_position_relative = False

        self._position = position
        self.invalidate(self._recalculate_position)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: Vector2):
        if size.x < 0 and size.y < 0:
            self._is_position_relative = True
            size.x = abs(size.x)
            size.y = abs(size.y)
        else:
            self._is_position_relative = False

        self._size = size
        self.invalidate(self._recalculate_size)

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

    @abstractmethod
    def _apply_new_batch(self):
        pass

    @abstractmethod
    def _apply_size(self):
        self.on_update.fire(InstanceUpdateType.SIZE)

    @abstractmethod
    def _apply_position(self):
        self.on_update.fire(InstanceUpdateType.POSITION)

    @abstractmethod
    def _apply_color(self):
        pass

    @abstractmethod
    def _apply_rotation(self):
        self.on_update.fire(InstanceUpdateType.ROTATION)
