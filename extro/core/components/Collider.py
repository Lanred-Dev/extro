from typing import TYPE_CHECKING

from extro.core.components.CollisionMask import CollisionMask
from extro.utils.Signal import Signal
import extro.internal.systems.Collision as CollisionSystem
import extro.services.CollisionGroup as CollisionGroupService
import extro.Console as Console

if TYPE_CHECKING:
    from extro.shared.Vector2 import Vector2


class Collider:
    __slots__ = (
        "_owner_id",
        "_is_collidable",
        "_collision_group",
        "_collision_mask",
        "_colliding_width",
        "on_collision",
        "on_collision_end",
    )

    _owner_id: int
    _is_collidable: bool
    _collision_group: str
    _collision_mask: CollisionMask

    on_collision: Signal
    on_collision_end: Signal

    def __init__(
        self,
        owner_id: int,
        position: "Vector2",
        size: "Vector2",
        rotation: float,
        is_collidable: bool,
        collision_group: str,
    ):
        if not CollisionGroupService.is_group(collision_group):
            Console.log(
                f"Collision group '{collision_group}' does not exist. Defaulting to '{CollisionGroupService.DEFAULT_COLLISION_GROUP}'",
                Console.LogType.WARNING,
            )
            collision_group = CollisionGroupService.DEFAULT_COLLISION_GROUP

        self._is_collidable = is_collidable
        self._collision_group = collision_group
        self._collision_mask = CollisionMask(
            position=position, size=size, rotation=rotation
        )

        self.on_collision = Signal()
        self.on_collision_end = Signal()

        self._owner_id = owner_id

    def destroy(self):
        self.on_collision.destroy()
        self.on_collision_end.destroy()

    @property
    def is_collidable(self) -> bool:
        return self._is_collidable

    @is_collidable.setter
    def is_collidable(self, is_collidable: bool):
        self._is_collidable = is_collidable
        CollisionSystem.recompute_collidable_instances()

    @property
    def collision_group(self) -> str:
        return self._collision_group

    @collision_group.setter
    def collision_group(self, collision_group: str):
        self._collision_group = collision_group
        CollisionSystem.recompute_collidable_instances()

    def _apply_size(self, size: "Vector2"):
        self._collision_mask.size = size

    def _apply_position(self, position: "Vector2"):
        self._collision_mask.position = position

    def _apply_rotation(self, rotation: float):
        self._collision_mask.rotation = rotation
