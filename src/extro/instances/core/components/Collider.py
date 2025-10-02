from typing import TYPE_CHECKING

from extro.utils.Signal import Signal
import extro.internal.systems.Collision as CollisionSystem
import extro.services.CollisionGroup as CollisionGroupService
import extro.Console as Console
from extro.instances.core.components.Component import Component

if TYPE_CHECKING:
    from extro.shared.Vector2C import Vector2


class Collider(Component):
    __slots__ = Component.__slots__ + (
        "_is_collidable",
        "_collision_group",
        "_axes",
        "_vertices",
        "on_collision",
        "on_collision_end",
    )

    _is_collidable: bool
    _collision_group: str
    _axes: "list[Vector2]"
    _vertices: "list[Vector2]"

    on_collision: Signal
    on_collision_end: Signal

    def __init__(
        self,
        owner: int,
        is_collidable: bool,
        collision_group: str,
    ):
        super().__init__(owner)

        self._is_collidable = is_collidable
        self.collision_group = collision_group

        self.on_collision = Signal()
        self.on_collision_end = Signal()

    def destroy(self):
        self.on_collision.destroy()
        self.on_collision_end.destroy()

    @property
    def is_collidable(self) -> bool:
        return self._is_collidable

    @is_collidable.setter
    def is_collidable(self, is_collidable: bool):
        self._is_collidable = is_collidable
        self.add_flag(CollisionSystem.ColliderDirtyFlags.IS_COLLIDABLE)

    @property
    def collision_group(self) -> str:
        return self._collision_group

    @collision_group.setter
    def collision_group(self, collision_group: str):
        if not CollisionGroupService.is_group(collision_group):
            Console.log(
                f"Collision group '{collision_group}' does not exist. Defaulting to '{CollisionGroupService.DEFAULT_COLLISION_GROUP}'",
                Console.LogType.WARNING,
            )
            collision_group = CollisionGroupService.DEFAULT_COLLISION_GROUP

        self._collision_group = collision_group
