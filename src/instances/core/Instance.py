import src.internal.handlers.InstanceManager as InstanceManager
from src.internal.helpers.InvalidationManager import InvalidationManager
from src.internal.helpers.Signal import Signal
from src.internal.helpers.Janitor import Janitor
from src.internal.shared_types import (
    EmptyFunction,
    InstanceUpdateType,
    RenderTargetType,
)
from src.values.Vector2 import Vector2
import src.internal.Console as Console
from src.instances.core.components.Collider import Collider
from src.instances.core.components.PhysicsBody import PhysicsBody
import src.internal.handlers.CollisionHandler as CollisionHandler
import src.internal.services.ScreenService as ScreenService
import src.internal.handlers.PhysicsHandler as PhysicsHandler


class Instance(InvalidationManager):
    __slots__ = (
        "id",
        "_anchor",
        "_position",
        "_size",
        "_rotation",
        "_scale",
        "_parent",
        "_parent_connections",
        "_actual_position",
        "_position_offset",
        "_actual_size",
        "_is_size_relative",
        "_is_position_relative",
        "_bounding",
        "on_update",
        "on_destroy",
        "_janitor",
    )

    id: str
    _anchor: Vector2
    _position: Vector2
    _size: Vector2
    _rotation: int
    _scale: Vector2
    _parent: "Instance | None"
    _parent_connections: dict[str, str]
    _actual_position: Vector2
    _actual_size: Vector2
    _is_size_relative: bool
    _is_position_relative: bool
    _bounding: tuple[float, float, float, float]

    _collider: "Collider | None"
    _physics_body: "PhysicsBody | None"

    on_update: Signal
    on_destroy: Signal
    _janitor: Janitor

    def __init__(
        self,
        anchor: Vector2 = Vector2(0, 0),
        position: Vector2 = Vector2(0, 0),
        size: Vector2 = Vector2(1, 1),
        rotation: int = 0,
        scale: Vector2 = Vector2(1, 1),
        is_size_relative: bool = False,
        is_position_relative: bool = False,
    ):
        super().__init__()
        InstanceManager.register(self)

        self._is_size_relative = is_size_relative
        self._is_position_relative = is_position_relative
        self._anchor = anchor
        self._position = position
        self._size = size
        self._rotation = rotation
        self._scale = scale
        self._actual_position = Vector2(0, 0)
        self._actual_size = Vector2(0, 0)
        self._parent = None
        self._parent_connections = {}
        self._collider = None
        self._physics_body = None
        self._bounding = (0, 0, 0, 0)

        self.on_destroy = Signal()
        self.on_update = Signal()

        janitor: Janitor = Janitor()
        janitor.add(self.on_update)
        janitor.add(self.on_destroy.fire)
        janitor.add(self.on_destroy)
        self._janitor = janitor

        # Position depends on size and for that reason `_recalculate_position` is called at the end of `_recalculate_size`
        self.invalidate(self._recalculate_size, 2)

    def destroy(self):
        super().destroy()
        self._janitor.destroy()
        InstanceManager.unregister(self.id)

    def invalidate(self, callback: "EmptyFunction", priority: int = 0):
        super().invalidate(callback=callback, priority=priority)
        InstanceManager.queue_instance_for_update(self)

    def parent_to(self, parent: "Instance | None"):
        if parent is None:
            self._parent = None
            return

        self._parent = parent
        self._parent_connections["on_update"] = parent.on_update.connect(
            self._handle_parent_update
        )
        self._parent_connections["on_destroy"] = parent.on_destroy.connect(self.destroy)

        self.invalidate(self._recalculate_position)

    def translate(self, move_by: Vector2):
        self.position += move_by

    def add_child(self, child: "Instance"):
        child.parent_to(self)

    def is_point_inside(self, point: Vector2) -> bool:
        return (
            point.x >= self._bounding[0]
            and point.x <= self._bounding[0] + self._bounding[2]
            and point.y >= self._bounding[1]
            and point.y <= self._bounding[1] + self._bounding[3]
        )

    def add_collider(self, is_collidable: bool = True, collision_group=""):
        if self._collider:
            Console.log(
                f"Instance {self.id} already has a collider",
                Console.LogType.ERROR,
            )
            return

        self._collider = Collider(
            self.id,
            self._actual_position,
            self._actual_size,
            self._rotation,
            is_collidable,
            collision_group,
        )

        CollisionHandler.register(self.id)
        self._janitor.add(self._collider.destroy)
        self._janitor.add(CollisionHandler.unregister, self.id)

    def add_physics_body(self, mass: float):
        if self._physics_body:
            Console.log(
                f"Instance {self.id} already has a physics body",
                Console.LogType.ERROR,
            )
            return

        self._physics_body = PhysicsBody(self.id, mass)

        PhysicsHandler.register(self.id)
        self._janitor.add(self._physics_body.destroy)
        self._janitor.add(PhysicsHandler.unregister, self.id)

    def _recalculate_bounding(self):
        self._bounding = (
            self._actual_position.x - (self._actual_size.x / 2),
            self._actual_position.y - (self._actual_size.y / 2),
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

    def _recalculate_position(
        self,
        position_offset: Vector2 = Vector2(0, 0),
        conversion_type: RenderTargetType | None = RenderTargetType.WORLD,
    ):
        if self._is_position_relative and self._parent:
            [parent_x, parent_y, parent_width, parent_height] = self._parent._bounding
            self._actual_position.x = parent_x + (parent_width * self._position.x)
            self._actual_position.y = parent_y + (parent_height * self._position.y)
        elif not self._is_position_relative:
            self._actual_position = self._position.copy()

            if conversion_type == RenderTargetType.WORLD:
                self._actual_position = ScreenService.world_to_screen_coords(
                    self._actual_position
                )
            elif conversion_type == RenderTargetType.INDEPENDENT:
                self._actual_position = ScreenService.normalized_to_screen_coords(
                    self._actual_position
                )

            if self._parent:
                self._actual_position.x += self._parent._bounding[0]
                self._actual_position.y += self._parent._bounding[1]

        self._actual_position.x -= (
            self._actual_size.x * self._anchor.x
        ) - position_offset.x
        self._actual_position.y -= (
            self._actual_size.y * self._anchor.y
        ) - position_offset.y

        self._recalculate_bounding()
        self._apply_position()

    def _recalculate_size(
        self,
        conversion_type: RenderTargetType | None = RenderTargetType.WORLD,
    ):
        scaled_x: float = self._size.x * self._scale.x
        scaled_y: float = self._size.y * self._scale.y

        if self._is_size_relative and self._parent:
            [_, _, parent_width, parent_height] = self._parent._bounding
            self._actual_size.x = parent_width * scaled_x
            self._actual_size.y = parent_height * scaled_y
        elif not self._is_size_relative:
            self._actual_size.x = scaled_x
            self._actual_size.y = scaled_y

            if conversion_type == RenderTargetType.WORLD:
                self._actual_size = ScreenService.world_to_screen_coords(
                    self._actual_size
                )
            elif conversion_type == RenderTargetType.INDEPENDENT:
                self._actual_size = ScreenService.normalized_to_screen_coords(
                    self._actual_size
                )

        self._apply_size()
        # Position depends on the size so it needs to be recalculated
        self._recalculate_position()

        # `_recalculate_bounding` is not called here because it is called in `_recalculate_position`

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
        self.invalidate(self._recalculate_position)

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, position: Vector2):
        self._position = position
        self.invalidate(self._recalculate_position, 1)

    @property
    def size(self) -> Vector2:
        return self._size

    @size.setter
    def size(self, size: Vector2):
        self._size = size
        self.invalidate(self._recalculate_size, 2)

    @property
    def rotation(self) -> int:
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
    def bounding(self) -> tuple[float, float, float, float]:
        return self._bounding

    @property
    def collider(self) -> "Collider":
        assert self._collider is not None, "Instance does not have a collider"
        return self._collider

    @property
    def physics_body(self) -> "PhysicsBody":
        assert self._physics_body is not None, "Instance does not have a physics body"
        return self._physics_body

    def _apply_size(self):
        if self._collider:
            self._collider._apply_size(self._actual_size)

        self.on_update.fire(InstanceUpdateType.SIZE)

    def _apply_position(self):
        if self._collider:
            self._collider._apply_position(self._actual_position)

        self.on_update.fire(InstanceUpdateType.POSITION)

    def _apply_rotation(self):
        if self._collider:
            self._collider._apply_rotation(self._rotation)

        self.on_update.fire(InstanceUpdateType.ROTATION)
