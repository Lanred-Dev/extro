from typing import TYPE_CHECKING, List, Tuple, Dict


import src.internal.Console as Console
import src.internal.InstanceHandler as InstanceHandler

if TYPE_CHECKING:
    from src.instances.core.CollisionInstance import CollisionInstance


def _is_instance_collidable(instance_id: str) -> bool:
    return (
        getattr(InstanceHandler.instances[instance_id], "is_collidable", None) != None
    )


_instances: List[str] = []
_collidable: Dict[str, List[str]] = {}
_collisions: List[Tuple[str, str]] = []


def register_instance(instance_id: str):
    if not _is_instance_collidable(instance_id):
        Console.log(
            f"{instance_id} cannot be registered as collidable because it is not",
            Console.LogType.ERROR,
        )
        return

    _instances.append(instance_id)
    Console.log(f"{instance_id} was registered as collidable")
    _recompute_collidable_instances()


def unregister_instance(instance_id: str):
    if instance_id not in _instances:
        Console.log(
            f"{instance_id} does not exist as a collidable instance",
            Console.LogType.ERROR,
        )
        return

    _instances.remove(instance_id)
    Console.log(f"{instance_id} was unregistered as collidable")
    _recompute_collidable_instances()


def _update_collisions():
    global _collisions
    new_collisions: List[Tuple[str, str]] = []

    for collision_group, instances in _collidable.items():
        for index, instance1_id in enumerate(instances):
            for instance2_id in instances[index + 1 :]:
                instance1: "CollisionInstance" = InstanceHandler.instances[instance1_id]  # type: ignore
                instance2: "CollisionInstance" = InstanceHandler.instances[instance2_id]  # type: ignore

                if instance1._collision_mask.collides_with(instance2._collision_mask):
                    new_collisions.append((instance1_id, instance2_id))

        # Handle collision end
    for collision in _collisions:
        if collision not in new_collisions:
            instance1: "CollisionInstance" = InstanceHandler.instances[collision[0]]  # type: ignore
            instance2: "CollisionInstance" = InstanceHandler.instances[collision[1]]  # type: ignore
            instance1.on_collision_end.fire(instance2)
            instance2.on_collision_end.fire(instance1)

    # Handle collision start
    for collision in new_collisions:
        if collision not in _collisions:
            instance1: "CollisionInstance" = InstanceHandler.instances[collision[0]]  # type: ignore
            instance2: "CollisionInstance" = InstanceHandler.instances[collision[1]]  # type: ignore
            instance1.on_collision.fire(instance2)
            instance2.on_collision.fire(instance1)

    _collisions = new_collisions


def _recompute_collidable_instances():
    _collidable.clear()

    for instance_id in _instances:
        if not _is_instance_collidable(instance_id):
            continue

        collision_group: str = InstanceHandler.instances[instance_id]._collision_group  # type: ignore

        if collision_group not in _collidable:
            _collidable[collision_group] = []

        _collidable[collision_group].append(instance_id)

    Console.log(
        f"CollisionHandler is handling {sum(len(ids) for ids in _collidable.values())} instances"
    )


__all__ = [
    "_recompute_collidable_instances",
    "_update_collisions",
    "register_instance",
    "unregister_instance",
]
