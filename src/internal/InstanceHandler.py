from typing import TYPE_CHECKING, Dict
from src.internal.IdentityHandler import generate_id
from src.internal.Console import Console, LogType

if TYPE_CHECKING:
    from src.instances.core.Instance import Instance
    from src.shared_types import EmptyFunction


class InstanceHandlerCls:
    """Manages creation, registration, and retrieval of instances."""

    instances: Dict[str, "Instance"]
    _queued_for_update: Dict[str, "EmptyFunction"]

    def __init__(self):
        self.instances = {}
        self._queued_for_update = {}

    def register_instance(self, instance: "Instance"):
        """Register an instance for tracking."""
        instance_id: str = generate_id(10, "i_")
        instance.id = instance_id
        self.instances[instance_id] = instance
        Console.log(f"Registered instance {instance_id}")

    def unregister_instance(self, instance_id: str):
        """Unregister an instance by object or ID."""
        if instance_id not in self.instances:
            Console.log(f"{instance_id} is not an instance", LogType.WARNING)
            return

        self.instances.pop(instance_id, None)
        Console.log(f"{instance_id} is no longer an instance")

    def update_instances(self):
        if len(self._queued_for_update) == 0:
            return

        for flush_instance in self._queued_for_update.values():
            flush_instance()

        self._queued_for_update.clear()

    def queue_instance_for_update(self, instance: "Instance"):
        if instance.id in self._queued_for_update:
            return

        self._queued_for_update[instance.id] = instance.flush


InstanceHandler = InstanceHandlerCls()
__all__ = ["InstanceHandler"]
