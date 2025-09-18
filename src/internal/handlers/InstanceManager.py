from typing import TYPE_CHECKING

import src.internal.services.IdentityService as IdentityService
import src.internal.Console as Console

if TYPE_CHECKING:
    from src.instances.core.Instance import Instance
    from src.internal.shared_types import EmptyFunction


instances: "dict[str, Instance]" = {}
_queued_for_update: "dict[str, EmptyFunction]" = {}


def register(instance: "Instance"):
    instance.id = IdentityService.generate_id(10, "i_")
    instances[instance.id] = instance
    Console.log(f"Registered instance {instance.id}")


def unregister(instance_id: str):
    if instance_id not in instances:
        Console.log(f"{instance_id} is not an instance", Console.LogType.ERROR)
        return

    del instances[instance_id]

    if instance_id in _queued_for_update:
        del _queued_for_update[instance_id]

    Console.log(f"{instance_id} is no longer an instance")


def _update():
    global _queued_for_update

    if len(_queued_for_update) == 0:
        return

    still_queued: "dict[str, EmptyFunction]" = {}

    for flush in _queued_for_update.values():
        flush()

    _queued_for_update = still_queued


def queue_instance_for_update(instance: "Instance"):
    if instance.id in _queued_for_update:
        return

    _queued_for_update[instance.id] = instance.flush


def _force_update_all_instances():
    for instance in instances.values():
        instance._recalculate_position()
        instance._recalculate_size()


__all__ = [
    "instances",
    "register",
    "unregister",
    "_update",
    "queue_instance_for_update",
    "_force_update_all_instances",
]
