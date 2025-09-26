from typing import TYPE_CHECKING

import extro.internal.services.Identity as IdentityService
import extro.Console as Console

if TYPE_CHECKING:
    from extro.core.Instance import Instance

instances: "dict[int, Instance]" = {}
queued_for_update: "set[int]" = set()


def register(instance: "Instance"):
    id: int = IdentityService.generate_ordered_numeric_id()
    instance._id = id
    instances[id] = instance
    Console.log(f"Registered instance {id}")


def unregister(instance_id: int):
    global instances, queued_for_update

    if instance_id not in instances:
        Console.log(f"{instance_id} is not an instance", Console.LogType.ERROR)
        return

    del instances[instance_id]
    queued_for_update.discard(instance_id)

    Console.log(f"{instance_id} is no longer an instance", Console.LogType.DEBUG)


def update_queued():
    global queued_for_update

    if len(queued_for_update) == 0:
        return

    for instance_id in queued_for_update.copy():
        instances[instance_id]._invalidation_manager.flush()

    queued_for_update.clear()


def queue_for_update(instance_id: int):
    """Queue an instance to be flushed before the next frame. The instance must be registered."""
    global queued_for_update

    if instance_id not in instances or instance_id in queued_for_update:
        return

    queued_for_update.add(instance_id)


def queue_all_for_update():
    global queued_for_update
    queued_for_update = set(instances.keys())
    Console.log("All instances queued for update", Console.LogType.DEBUG)


__all__ = [
    "instances",
    "register",
    "unregister",
    "update_queued",
    "queue_for_update",
    "queue_all_for_update",
]
