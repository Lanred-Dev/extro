from extro.utils.InvalidationManager import InstanceInvalidationManager
from extro.utils.Signal import Signal
from extro.utils.Janitor import Janitor
from extro.shared.types import InstanceUpdateType, RenderTargetType
from extro.shared.Vector2 import Vector2
from extro.shared.Coord import Coord, CoordType
import extro.Console as Console
import extro.internal.InstanceManager as InstanceManager
from extro.core.components.Collider import Collider
from extro.core.components.PhysicsBody import PhysicsBody
import extro.internal.systems.Collision as CollisionSystem
import extro.internal.systems.Physics as PhysicsSystem
import extro.services.CollisionGroup as CollisionGroupService

SIZE_RECALCULATION_PRIORITY: int = 2
POSITION_RECALCULATION_PRIORITY: int = 1


class Instance:
    __slots__ = (
        "_id",
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
        "_bounding",
        "on_update",
        "on_destroy",
        "_janitor",
        "_invalidation_manager",
        "_collider",
        "_physics_body",
    )

    _id: int
    _anchor: Vector2
    _position: Coord
    _size: Coord
    _rotation: int
    _scale: Vector2
    _parent: "Instance | None"
    _parent_connections: dict[str, str]
    _actual_position: Vector2
    _actual_size: Vector2
    _bounding: tuple[float, float, float, float]
    _collider: Collider | None
    _physics_body: PhysicsBody | None

    on_update: Signal
    on_destroy: Signal
    _janitor: Janitor
    _invalidation_manager: InstanceInvalidationManager

    def __init__(
        self,
        anchor: Vector2 = Vector2(0, 0),
        position: Coord = Coord(0, 0, CoordType.NORMALIZED),
        size: Coord = Coord(0, 0, CoordType.NORMALIZED),
        rotation: int = 0,
        scale: Vector2 = Vector2(1, 1),
    ):
        InstanceManager.register(self)

        self._anchor = anchor
        self._position = position
        self._size = size
        self._rotation = rotation
        self._scale = scale
        self._actual_position = Vector2(0, 0)
        self._actual_size = Vector2(0, 0)
        self._parent = None
        self._parent_connections = {}
        self._bounding = (0, 0, 0, 0)
        self._collider = None
        self._physics_body = None

        self.on_destroy = Signal()
        self.on_update = Signal()

        self._invalidation_manager = InstanceInvalidationManager(self._id)

        self._janitor = Janitor()
        self._janitor.add(self.on_update)
        self._janitor.add(self.on_destroy.fire)
        self._janitor.add(self.on_destroy)
        self._janitor.add(self._disconnect_parent_connections)
        self._janitor.add(self._invalidation_manager)

        # Position depends on size and for that reason `_recalculate_position` is called at the end of `_recalculate_size`
        self._invalidation_manager.invalidate(
            self._recalculate_size, SIZE_RECALCULATION_PRIORITY
        )

    def destroy(self):
        self._janitor.destroy()
        InstanceManager.unregister(self._id)

    def parent_to(self, parent: "Instance | None"):
        if parent is None:
            self._parent = None
            return

        self._parent = parent
        self._parent_connections["on_update"] = parent.on_update.connect(
            self._handle_parent_update
        )
        self._parent_connections["on_destroy"] = parent.on_destroy.connect(self.destroy)

        self._invalidation_manager.invalidate(
            self._recalculate_size, SIZE_RECALCULATION_PRIORITY
        )

    def translate(self, vector: Coord):
        self.position._vector += vector._vector

    def add_child(self, child: "Instance"):
        child.parent_to(self)

    def is_point_inside(self, point: Vector2) -> bool:
        return (
            point.x >= self._bounding[0]
            and point.x <= self._bounding[0] + self._bounding[2]
            and point.y >= self._bounding[1]
            and point.y <= self._bounding[1] + self._bounding[3]
        )

    def add_collider(
        self,
        is_collidable: bool = True,
        collision_group: str = CollisionGroupService.DEFAULT_COLLISION_GROUP,
    ):
        if self._collider is not None:
            Console.log(
                f"Instance {self._id} already has a collider", Console.LogType.WARNING
            )
            return

        self._collider = Collider(
            owner_id=self._id,
            position=self._actual_position,
            size=self._actual_size,
            rotation=self._rotation,
            is_collidable=is_collidable,
            collision_group=collision_group,
        )
        self._janitor.add(self._collider)
        self._janitor.add(CollisionSystem.unregister, self._id)
        CollisionSystem.register(self._id)

    def add_physics_body(self, mass: float = 1, is_anchored: bool = False):
        if self._physics_body is not None:
            Console.log(
                f"Instance {self._id} already has a physics body",
                Console.LogType.WARNING,
            )
            return

        self._physics_body = PhysicsBody(
            owner_id=self._id, mass=mass, is_anchored=is_anchored
        )
        self._janitor.add(self._physics_body)
        self._janitor.add(PhysicsSystem.unregister, self._id)
        PhysicsSystem.register(self._id)

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
    ):
        coord_type: CoordType = self._position.type

        if coord_type == CoordType.PARENT and self._parent:
            [parent_x, parent_y, parent_width, parent_height] = self._parent._bounding
            self._actual_position.x = parent_x + (
                parent_width * self._position.vector.x
            )
            self._actual_position.y = parent_y + (
                parent_height * self._position.vector.y
            )
        elif coord_type != CoordType.PARENT:
            self._actual_position = self._position.vector

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
    ):
        self._actual_size = self._size.vector * self._scale

        if self._size.type == CoordType.PARENT and self._parent:
            [_, _, parent_width, parent_height] = self._parent._bounding
            self._actual_size.x *= parent_width
            self._actual_size.y *= parent_height

        self._apply_size()
        # Position depends on the size so it needs to be recalculated
        self._recalculate_position()

        # `_recalculate_bounding` is not called here because it is called in `_recalculate_position`

    @property
    def id(self) -> int:
        return self._id

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
        self._invalidation_manager.invalidate(self._recalculate_position)

    @property
    def position(self) -> Coord:
        return self._position

    @position.setter
    def position(self, position: Coord):
        self._position = position
        self._invalidation_manager.invalidate(
            self._recalculate_position, POSITION_RECALCULATION_PRIORITY
        )

    @property
    def size(self) -> Coord:
        return self._size

    @size.setter
    def size(self, size: Coord):
        self._size = size
        self._invalidation_manager.invalidate(
            self._recalculate_size, SIZE_RECALCULATION_PRIORITY
        )

    @property
    def rotation(self) -> int:
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: int):
        self._rotation = rotation
        self._invalidation_manager.invalidate(self._apply_rotation)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale: Vector2):
        self._scale = scale
        self._invalidation_manager.invalidate(
            self._recalculate_size, SIZE_RECALCULATION_PRIORITY
        )

    @property
    def bounding(self) -> tuple[float, float, float, float]:
        return self._bounding

    # Better way to do `collider` and `physics_body`? Probably.
    @property
    def collider(self) -> Collider:
        assert self._collider is not None, "Instance does not have a collider"
        return self._collider

    @property
    def physics_body(self) -> PhysicsBody:
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
