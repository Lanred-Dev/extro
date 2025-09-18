import src.internal.Console as Console
import src.internal.handlers.InstanceManager as InstanceManager
import src.internal.handlers.PhysicsHandler as PhysicsHandler


def _is_instance_collidable(instance_id: str) -> bool:
    return (
        getattr(InstanceManager.instances[instance_id], "_collider", None) is not None
    )


_instances: set[str] = set()
_collidable: dict[str, list[str]] = {}
_collisions: list[tuple[str, str]] = []


def register(instance_id: str):
    global _instances

    if not _is_instance_collidable(instance_id):
        Console.log(
            f"{instance_id} cannot be registered as collidable because it is not",
            Console.LogType.ERROR,
        )
        return
    elif instance_id in _instances:
        Console.log(
            f"{instance_id} is already registered as a collidable instance",
            Console.LogType.WARNING,
        )
        return

    _instances.add(instance_id)
    Console.log(f"{instance_id} was registered as collidable")
    _recompute_collidable_instances()


def unregister(instance_id: str):
    global _collisions, _instances

    if instance_id not in _instances:
        Console.log(
            f"{instance_id} does not exist as a collidable instance",
            Console.LogType.ERROR,
        )
        return

    _instances.remove(instance_id)
    Console.log(f"{instance_id} was unregistered as collidable")
    _recompute_collidable_instances()

    # Must also remove any collisions that involve this instance and fire collision end events
    for collision in _collisions.copy():
        if instance_id not in collision:
            continue

        instance1 = InstanceManager.instances[collision[0]]
        instance2 = InstanceManager.instances[collision[1]]
        instance1.collider.on_collision_end.fire(instance2)
        instance2.collider.on_collision_end.fire(instance1)
        _collisions.remove(collision)


def _update():
    global _collisions
    new_collisions: list[tuple[str, str]] = []

    for collision_group, instances in _collidable.items():
        for index, instance1_id in enumerate(instances):
            for instance2_id in instances[index + 1 :]:
                instance1 = InstanceManager.instances[instance1_id]
                instance2 = InstanceManager.instances[instance2_id]

                if instance1.collider._collision_mask.collides_with(
                    instance2.collider._collision_mask
                ):
                    new_collisions.append((instance1_id, instance2_id))

    old_collisions = _collisions.copy()
    _collisions = new_collisions

    # Handle collision end
    for collision in old_collisions:
        if collision in new_collisions:
            continue

        instance1 = InstanceManager.instances[collision[0]]
        instance2 = InstanceManager.instances[collision[1]]
        instance1.collider.on_collision_end.fire(instance2)
        instance2.collider.on_collision_end.fire(instance1)

    # Handle collision start
    for collision in new_collisions:
        if collision in old_collisions:
            continue

        instance1 = InstanceManager.instances[collision[0]]
        instance2 = InstanceManager.instances[collision[1]]
        instance1.collider.on_collision.fire(instance2)
        instance2.collider.on_collision.fire(instance1)

    # Only objects with physics bodies are affected by collisions (in terms of physics)
    PhysicsHandler._resolve_collisions(_collisions)


def _recompute_collidable_instances():
    global _collidable
    _collidable.clear()

    for instance_id in _instances:
        if not _is_instance_collidable(instance_id):
            continue

        collision_group: str = InstanceManager.instances[
            instance_id
        ].collider._collision_group

        if collision_group not in _collidable:
            _collidable[collision_group] = []

        _collidable[collision_group].append(instance_id)

    Console.log(
        f"CollisionHandler is handling {sum(len(ids) for ids in _collidable.values())} instances"
    )


__all__ = [
    "_recompute_collidable_instances",
    "_update",
    "register",
    "unregister",
]
