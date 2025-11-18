from typing import TYPE_CHECKING

from extro.utils.Signal import Signal
import extro.services.CollisionGroup as CollisionGroupService
import extro.Console as Console
from extro.instances.core.components.Component import Component
import extro.internal.ComponentManager as ComponentManager
import extro.internal.systems.Collision.CollisionSolver as CollisionSolver
from extro.shared.Vector2 import Vector2

if TYPE_CHECKING:
    import extro.internal.InstanceManager as InstanceManager


class Collider(Component):
    __slots__ = Component.__slots__ + (
        "is_collidable",
        "_collision_group",
        "on_collision",
        "on_collision_end",
    )

    _key = "collider"

    is_collidable: bool
    _collision_group: "CollisionGroupService.CollisionGroupID"

    on_collision: Signal
    on_collision_end: Signal

    def __init__(
        self,
        owner: "InstanceManager.InstanceID",
        is_collidable: bool = True,
        collision_group: str = CollisionGroupService.DEFAULT_COLLISION_GROUP,
    ):
        super().__init__(owner, ComponentManager.ComponentType.COLLIDER)

        self.is_collidable = is_collidable
        self.collision_group = collision_group

        self.on_collision = Signal()
        self.on_collision_end = Signal()

        transform = ComponentManager.transforms[owner]
        CollisionSolver.create_collision_mask(
            owner,
            Vector2(transform.size.absolute_x, transform.size.absolute_y),
            Vector2(transform.position.absolute_x, transform.position.absolute_y),
            transform.rotation,
        )

    def destroy(self):
        super().destroy()

        self.on_collision.destroy()
        self.on_collision_end.destroy()
        CollisionSolver.destroy_collision_mask(self._owner)

    @property
    def collision_group(self) -> str:
        return CollisionGroupService.id_to_name(self._collision_group)

    @collision_group.setter
    def collision_group(self, collision_group: str):
        if not CollisionGroupService.is_group(collision_group):
            Console.log(
                f"Collision group '{collision_group}' does not exist. Defaulting to '{CollisionGroupService.DEFAULT_COLLISION_GROUP}'",
                Console.LogType.WARNING,
            )
            collision_group = CollisionGroupService.DEFAULT_COLLISION_GROUP

        self._collision_group = CollisionGroupService.name_to_id(collision_group)
