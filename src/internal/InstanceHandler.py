from typing import TYPE_CHECKING, Dict
import src.internal.IdentityHandler as IdentityHandler
import src.internal.Console as Console

if TYPE_CHECKING:
    from src.instances.core.Instance import Instance
    from src.shared_types import EmptyFunction


instances: "Dict[str, Instance]" = {}
_queued_for_update: Dict[str, "EmptyFunction"] = {}


def register_instance(instance: "Instance"):
    instance.id = IdentityHandler.generate_id(10, "i_")
    instances[instance.id] = instance
    Console.log(f"Registered instance {instance.id}")


def unregister_instance(instance_id: str):
    if instance_id not in instances:
        Console.log(f"{instance_id} is not an instance", Console.LogType.ERROR)
        return

    del instances[instance_id]
    del _queued_for_update[instance_id]
    Console.log(f"{instance_id} is no longer an instance")


def _update_instances():
    global _queued_for_update

    if len(_queued_for_update) == 0:
        return

    still_queued: Dict[str, "EmptyFunction"] = {}

    for instance_id, flush_instance in _queued_for_update.items():
        instance: "Instance" = instances[instance_id]

        # Instances depend on a scene when converting their vectors to screen space, so no need to flush if they aren't in one
        if instance._scene is None:
            still_queued[instance_id] = flush_instance
            continue

        flush_instance()

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
    "register_instance",
    "unregister_instance",
    "_update_instances",
    "queue_instance_for_update",
    "_force_update_all_instances",
]
