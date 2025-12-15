from typing import TYPE_CHECKING

import extro.services.CollisionGroup as CollisionGroupService
import extro.internal.systems.Collision.CollisionSolver as CollisionSolver
import extro.internal.ComponentManager as ComponentManager

if TYPE_CHECKING:
    import extro.internal.InstanceManager as InstanceManager
    from extro.shared.Vector2 import Vector2
    import extro.internal.systems.Transform as TransformSystem

    Collision = tuple[InstanceManager.InstanceID, InstanceManager.InstanceID]
    CollisionsData = list[tuple[Collision, float, "Vector2", "Vector2"]]


collisions: "set[Collision]" = set()


def update(transform_updates: "TransformSystem.TransformUpdates") -> "CollisionsData":
    global collisions

    old_collisions = list(collisions)
    collisions.clear()

    collisions_data = CollisionSolver.check_collisions(
        {
            instance_id: collider.is_collidable
            for instance_id, collider in ComponentManager.colliders.items()
            if collider.is_collidable
        },
        transform_updates
    )

    for collision, *data in collisions_data:
        instance1_id = collision[0]
        instance2_id = collision[1]
        instance1_collider = ComponentManager.colliders[instance1_id]
        instance2_collider = ComponentManager.colliders[instance2_id]

        if not CollisionGroupService.is_collidable(
            instance1_collider._collision_group,
            instance2_collider._collision_group,
        ):
            collisions_data.remove((collision, *data))
            continue

        collisions.add(collision)

        if collision not in old_collisions:
            instance1_collider.on_collision.fire(instance2_id, *data)
            instance2_collider.on_collision.fire(instance1_id, *data)

    # Fire collision end events
    for collision in old_collisions:
        if collision in collisions:
            continue

        instance1_id = collision[0]
        instance2_id = collision[1]
        ComponentManager.colliders[instance1_id].on_collision_end.fire(instance2_id)
        ComponentManager.colliders[instance2_id].on_collision_end.fire(instance1_id)

    return collisions_data
