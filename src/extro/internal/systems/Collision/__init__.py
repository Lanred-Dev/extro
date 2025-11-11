from typing import TYPE_CHECKING
from collections import defaultdict

import extro.internal.InstanceManager as InstanceManager
import extro.services.CollisionGroup as CollisionGroupService
import extro.internal.systems.Collision.CollisionSolver as CollisionSolver
import extro.internal.ComponentManager as ComponentManager

if TYPE_CHECKING:
    from extro.instances.core.components.Collider import Collider
    from extro.instances.core.components.Transform import Transform

    Collision = tuple[int, int]
    GridCell = tuple[int, int]

    CollisionsData = dict[
        Collision, tuple[float, tuple[float, float], tuple[float, float]]
    ]


CELL_SIZE: int = 60

collisions: "set[Collision]" = set()


def on_transform_change(collider: "Collider", transform: "Transform"):
    CollisionSolver.recompute_collision_mask(
        collider._owner,
        transform._actual_size[0],
        transform._actual_size[1],
        transform._actual_position[0],
        transform._actual_position[1],
        transform.rotation,
    )


def update() -> "CollisionsData":
    global collisions

    old_collisions = list(collisions)
    collisions.clear()
    collisions_data: "CollisionsData" = {}

    new_collisions = CollisionSolver.check_collisions(
        [
            instance_id
            for instance_id, collider in ComponentManager.colliders.items()
            if collider.is_collidable
        ]
    )

    for collision, penetration, normal, contact_point in new_collisions:
        instance1_id = collision[0]
        instance2_id = collision[1]
        instance1_collider = ComponentManager.colliders[instance1_id]
        instance2_collider = ComponentManager.colliders[instance2_id]

        if not CollisionGroupService.is_collidable(
            instance1_collider._collision_group,
            instance2_collider._collision_group,
        ):
            continue

        collisions.add(collision)
        collisions_data[collision] = (
            penetration,
            normal,
            contact_point,
        )

        if collision not in old_collisions:
            instance1_collider.on_collision.fire(
                instance2_id, penetration, normal, contact_point
            )
            instance2_collider.on_collision.fire(
                instance1_id, penetration, normal, contact_point
            )

    # Fire collision end events
    for collision in old_collisions:
        if collision in collisions:
            continue

        instance1_id = collision[0]
        instance2_id = collision[1]
        ComponentManager.colliders[instance1_id].on_collision_end.fire(instance2_id)
        ComponentManager.colliders[instance2_id].on_collision_end.fire(instance1_id)

    return collisions_data
