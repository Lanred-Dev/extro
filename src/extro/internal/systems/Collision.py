from typing import TYPE_CHECKING

import extro.Console as Console
import extro.internal.InstanceManager as InstanceManager
import extro.internal.systems.Physics as PhysicsSystem
import extro.services.CollisionGroup as CollisionGroupService

if TYPE_CHECKING:
    from extro.shared.Vector2 import Vector2

    Collision = tuple[int, int]
    GridCell = tuple[int, int]

CELL_SIZE: int = 60


def is_instance_collidable(instance_id: int) -> bool:
    return (
        getattr(InstanceManager.instances[instance_id], "_collider", None) is not None
    )


instances: set[int] = set()
collidable: list[int] = []
collisions: "list[Collision]" = []
old_collisions: "list[Collision]" = []


def register(instance_id: int):
    global instances

    if not is_instance_collidable(instance_id):
        Console.log(
            f"{instance_id} cannot be registered as collidable because it is not",
            Console.LogType.WARNING,
        )
        return
    elif instance_id in instances:
        Console.log(
            f"{instance_id} is already registered as a collidable instance",
            Console.LogType.WARNING,
        )
        return

    instances.add(instance_id)
    Console.log(f"{instance_id} was registered as collidable")
    recompute_collidable_instances()


def unregister(instance_id: int):
    global collisions, instances

    if instance_id not in instances:
        Console.log(
            f"{instance_id} does not exist as a collidable instance",
            Console.LogType.ERROR,
        )
        return

    instances.remove(instance_id)
    Console.log(f"{instance_id} was unregistered as collidable")
    recompute_collidable_instances()

    # Must also remove any collisions that involve this instance and fire collision end events
    for collision in collisions.copy():
        if instance_id not in collision:
            continue

        instance1 = InstanceManager.instances[collision[0]]
        instance2 = InstanceManager.instances[collision[1]]
        instance1.collider.on_collision_end.fire(instance2)
        instance2.collider.on_collision_end.fire(instance1)
        collisions.remove(collision)


def check_collisions():
    global collisions

    grid: "dict[GridCell, list[int]]" = {}

    for index, instance_id in enumerate(collidable):
        instance = InstanceManager.instances[instance_id]
        collision_mask = instance.collider._collision_mask
        cell_x: int = int(collision_mask.position.x // CELL_SIZE)
        cell_y: int = int(collision_mask.position.y // CELL_SIZE)
        max_x: int = int(
            (collision_mask.position.x + collision_mask.size.x) // CELL_SIZE
        )
        max_y: int = int(
            (collision_mask.position.y + collision_mask.size.y) // CELL_SIZE
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

            for instance2_index in range(instance1_index + 1, len(cell_instances)):
                instance2_id = cell_instances[instance2_index]

                if instance2_id not in InstanceManager.instances:
                    continue

                instance2 = InstanceManager.instances[instance2_id]

                collision_data = instance1.collider._collision_mask.collides_with(
                    instance2.collider._collision_mask
                )

                if (
                    not CollisionGroupService.is_collidable(
                        instance1.collider.collision_group,
                        instance2.collider.collision_group,
                    )
                    or collision_data is None
                ):
                    continue

                # Prevent duplicate collision pairs, ex (A, B) and (B, A)
                if instance1_id < instance2_id:
                    collision = (instance1_id, instance2_id)
                else:
                    collision = (instance2_id, instance1_id)

                if collision in collisions:
                    continue

                collisions.append(collision)
                collisions_data[collision] = collision_data

                if collision not in old_collisions and collision in collisions:
                    instance1.collider.on_collision.fire(instance2)
                    instance2.collider.on_collision.fire(instance1)

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
        instance1.collider.on_collision_end.fire(instance2)
        instance2.collider.on_collision_end.fire(instance1)

    PhysicsSystem.resolve_collisions(collisions, collisions_data)


def recompute_collidable_instances():
    global collidable
    collidable.clear()

    for instance_id in instances:
        if not is_instance_collidable(instance_id):
            continue

        collidable.append(instance_id)

    Console.log(
        f"Collision system is handling {len(collidable)} instances",
        Console.LogType.DEBUG,
    )
