from typing import TYPE_CHECKING

from extro.utils.Signal import Signal
from extro.instances.core.components.Component import Component
from extro.shared.Vector2C import Vector2
from extro.shared.Coord import Coord
import extro.Console as Console
import extro.internal.systems.Transform as TransformSystem
import extro.internal.ComponentManager as ComponentManager

if TYPE_CHECKING:
    import extro.internal.InstanceManager as InstanceManager


class Transform(Component):
    __slots__ = Component.__slots__ + (
        "_position",
        "_size",
        "_rotation",
        "_scale",
        "_anchor",
        "_position_offset",
        "_bounding",
        "_actual_position",
        "_actual_size",
        "_parent",
        "_children",
        "on_update",
    )

    _key = "transform"

    _position: Coord
    _size: Coord
    _rotation: float
    _scale: Vector2
    _anchor: Vector2
    _position_offset: tuple[float, float]
    _bounding: tuple[float, float, float, float]
    _actual_position: tuple[float, float]
    _actual_size: tuple[float, float]
    _parent: "InstanceManager.InstanceIDType | None"
    _children: "list[InstanceManager.InstanceIDType]"

    on_update: Signal

    def __init__(
        self,
        owner: "InstanceManager.InstanceIDType",
        position: Coord,
        size: Coord,
        rotation: float = 0,
        scale: Vector2 = Vector2(1, 1),
        anchor: Vector2 = Vector2(0, 0),
    ):
        super().__init__(owner, ComponentManager.ComponentType.TRANSFORM)

        self._position = position
        self._size = size
        self._rotation = rotation
        self._scale = scale
        self._anchor = anchor
        self._position_offset = (0, 0)
        self._bounding = (0, 0, 0, 0)
        self._actual_position = (0, 0)
        self._actual_size = (0, 0)

        self.on_update = Signal()

        # Force an initial calculation, only need size because it will trigger position recalculation
        self.add_flag(TransformSystem.TransformDirtyFlags.SIZE)

    def destroy(self):
        super().destroy()
        self.on_update.destroy()

    def translate(self, translation: Coord):
        self._position.absolute_x += translation.absolute_x
        self._position.absolute_y += translation.absolute_y
        self.add_flag(TransformSystem.TransformDirtyFlags.POSITION)

    def is_point_inside(self, point: Vector2) -> bool:
        x, y, width, height = self._bounding
        return (
            point.x >= x
            and point.x <= x + width
            and point.y >= y
            and point.y <= y + height
        )

    def add_child(self, instance_id: "InstanceManager.InstanceIDType"):
        if instance_id in self._children:
            return

        self._children.append(instance_id)

    @property
    def anchor(self) -> Vector2:
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
        self.add_flag(TransformSystem.TransformDirtyFlags.POSITION)

    @property
    def position(self) -> Coord:
        return self._position

    @position.setter
    def position(self, position: Coord):
        self._position = position
        self.add_flag(TransformSystem.TransformDirtyFlags.POSITION)

    @property
    def size(self) -> Coord:
        return self._size

    @size.setter
    def size(self, size: Coord):
        self._size = size
        self.add_flag(TransformSystem.TransformDirtyFlags.SIZE)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale: Vector2):
        self._scale = scale
        self.add_flag(TransformSystem.TransformDirtyFlags.SIZE)

    @property
    def bounding(self) -> tuple[float, float, float, float]:
        return self._bounding

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: float):
        self._rotation = rotation
        self.add_flag(TransformSystem.TransformDirtyFlags.ROTATION)
