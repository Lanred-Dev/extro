from typing import TYPE_CHECKING

import extro.internal.InstanceManager as InstanceManager
import extro.internal.systems.Physics as PhysicsSystem
import extro.services.CollisionGroup as CollisionGroupService
import extro.internal.systems.Collision.CollisionMask as CollisionMask
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

collisions: "list[Collision]" = []
old_collisions: "list[Collision]" = []


def on_transform_change(collider: "Collider", transform: "Transform"):
    collider._vertices = CollisionMask.compute_vertices(
        transform._actual_size[0],
        transform._actual_size[1],
        transform._actual_position[0],
        transform._actual_position[1],
        transform.rotation,
    )
    collider._axes = CollisionMask.compute_axes(collider._vertices)


def update():
    global collisions
    grid: "dict[GridCell, list[int]]" = {}

    for instance_id, collider in ComponentManager.colliders.items():
        if not collider.is_collidable:
            continue

        transform = ComponentManager.transforms[instance_id]
        cell_x: int = int(transform._actual_position[0] // CELL_SIZE)
        cell_y: int = int(transform._actual_position[1] // CELL_SIZE)
        max_x: int = int(
            (transform._actual_position[0] + transform._actual_size[0]) // CELL_SIZE
        )
        max_y: int = int(
            (transform._actual_position[1] + transform._actual_size[1]) // CELL_SIZE
        )

        for x in range(cell_x, max_x + 1):
            for y in range(cell_y, max_y + 1):
                cell: "GridCell" = (x, y)

                if cell not in grid:
                    grid[cell] = []

                grid[cell].append(instance_id)

    old_collisions = collisions[:]
    collisions.clear()
    collisions_data: "CollisionsData" = {}

    for cell_instances in grid.values():
        for instance1_index, instance1_id in enumerate(cell_instances):
            instance1_collider = ComponentManager.colliders[instance1_id]

            for instance2_id in cell_instances[instance1_index + 1 :]:
                instance2_collider = ComponentManager.colliders[instance2_id]

                if not CollisionGroupService.is_collidable(
                    instance1_collider._collision_group,
                    instance2_collider._collision_group,
                ):
                    continue

                does_collide, normal, penetration, collision_normal, contact_point = (
                    CollisionMask.does_collide(
                        instance1_collider._vertices,
                        instance1_collider._axes,
                        ComponentManager.transforms[instance1_id]._actual_position,
                        instance2_collider._vertices,
                        instance2_collider._axes,
                        ComponentManager.transforms[instance2_id]._actual_position,
                    )
                )

                if not does_collide:
                    continue

                # Prevent duplicate collision pairs, ex (A, B) and (B, A)
                if instance1_id < instance2_id:
                    collision = (instance1_id, instance2_id)
                else:
                    collision = (instance2_id, instance1_id)

                if collision in collisions:
                    continue

                collisions.append(collision)
                collisions_data[collision] = (
                    penetration,
                    collision_normal,
                    contact_point,
                )

                if collision not in old_collisions and collision in collisions:
                    instance1_collider.on_collision.fire(
                        instance1_collider, normal, penetration
                    )
                    instance2_collider.on_collision.fire(
                        instance2_collider, normal, penetration
                    )

    # Fire collision end events
    for collision in old_collisions:
        if collision in collisions:
            continue

        if (
            collision[0] not in InstanceManager.instances
            or collision[1] not in InstanceManager.instances
        ):
            continue

        instance1 = InstanceManager.instances[collision[0]]
        instance2 = InstanceManager.instances[collision[1]]
        instance1.get_component_unsafe("collider").on_collision_end.fire(instance2)
        instance2.get_component_unsafe("collider").on_collision_end.fire(instance1)

    if len(collisions_data) > 0:
        PhysicsSystem.resolve_collisions(collisions_data)
