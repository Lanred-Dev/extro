from typing import TYPE_CHECKING
from enum import IntFlag, auto

import extro.Console as Console
import extro.internal.InstanceManager as InstanceManager

# import extro.internal.systems.Physics as PhysicsSystem
import extro.services.CollisionGroup as CollisionGroupService
from extro.internal.utils.InstanceRegistry import InstanceRegistry
import extro.internal.systems.Collision.CollisionMask as CollisionMask

if TYPE_CHECKING:
    from extro.shared.Vector2C import Vector2
    from extro.instances.core.components.Collider import Collider
    from extro.instances.core.components.Transform import Transform

    Collision = tuple[int, int]
    GridCell = tuple[int, int]


class ColliderDirtyFlags(IntFlag):
    IS_COLLIDABLE = auto()


CELL_SIZE: int = 60


def is_instance_collidable(instance_id: int) -> bool:
    instance = InstanceManager.instances[instance_id]
    return (
        instance.get_component("collider") is not None
        and instance.get_component("transform") is not None
    )


instances: InstanceRegistry = InstanceRegistry(
    "Collision System",
    preregister_check=lambda instance_id: not is_instance_collidable(instance_id),
    on_list_change=lambda: recompute_collidable_instances(),
)
collidable: list[int] = []
collisions: "list[Collision]" = []
old_collisions: "list[Collision]" = []


def on_transform_change(collider: "Collider", transform: "Transform"):
    collider._axes = CollisionMask.compute_axes(
        CollisionMask.compute_vertices(
            transform.size.x,
            transform.size.y,
            transform.position.x,
            transform.position.y,
            transform.rotation,
        )
    )
    collider._vertices = CollisionMask.compute_vertices(
        transform.size.x,
        transform.size.y,
        transform.position.x,
        transform.position.y,
        transform.rotation,
    )


def update():
    global collisions
    grid: "dict[GridCell, list[int]]" = {}

    for instance_id in instances.instances:
        # Even if it is dirty, if its not collidable, and it can be recomputed later
        if instance_id not in collidable:
            continue

        instance = InstanceManager.instances[instance_id]
        collider: "Collider" = instance.get_component_unsafe("collider")

        if collider.has_flag(ColliderDirtyFlags.IS_COLLIDABLE):
            recompute_collidable_instances()
            collider.clear_flags()

        transform: "Transform" = instance.get_component_unsafe("transform")
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

                grid[cell].append(instance.id)

    old_collisions = collisions[:]
    collisions.clear()
    collisions_data: "dict[Collision, tuple[Vector2, float]]" = {}

    for cell_instances in grid.values():
        for instance1_index in range(len(cell_instances)):
            instance1_id = cell_instances[instance1_index]

            if instance1_id not in InstanceManager.instances:
                continue

            instance1 = InstanceManager.instances[instance1_id]
            instance1_collider: "Collider" = instance1.get_component_unsafe("collider")

            for instance2_index in range(instance1_index + 1, len(cell_instances)):
                instance2_id = cell_instances[instance2_index]

                if instance2_id not in InstanceManager.instances:
                    continue

                instance2 = InstanceManager.instances[instance2_id]
                instance2_collider: "Collider" = instance2.get_component_unsafe(
                    "collider"
                )

                if not CollisionGroupService.is_collidable(
                    instance1_collider._collision_group,
                    instance2_collider._collision_group,
                ):
                    continue

                [does_collide, normal, penetration] = CollisionMask.does_collide(
                    instance1_collider._vertices,
                    instance1_collider._axes,
                    instance1.get_component_unsafe("transform")._actual_position,
                    instance2_collider._vertices,
                    instance2_collider._axes,
                    instance2.get_component_unsafe("transform")._actual_position,
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
                collisions_data[collision] = (normal, penetration)

                if collision not in old_collisions and collision in collisions:
                    instance1_collider.on_collision.fire(instance2)
                    instance2_collider.on_collision.fire(instance1)

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

    # PhysicsSystem.resolve_collisions(collisions, collisions_data)


def recompute_collidable_instances():
    global collidable
    collidable.clear()

    for instance_id in instances.instances:
        if not is_instance_collidable(instance_id):
            continue

        collidable.append(instance_id)

    Console.log(
        f"Collision system is tracking {len(collidable)} collidable instances",
        Console.LogType.DEBUG,
    )
