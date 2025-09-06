from typing import TYPE_CHECKING, Dict
from src.internal.IdentityHandler import generate_id
from src.shared_types import EmptyFunction
from src.internal.Console import Console, LogType

if TYPE_CHECKING:
    from src.instances.core.Instance import Instance


class InstanceHandlerCls:
    """Manages creation, registration, and retrieval of instances."""

    instances: Dict[str, "Instance"]
    __queued_for_update: Dict[str, EmptyFunction]

    def __init__(self):
        self.instances = {}
        self.__queued_for_update = {}

    def create_instance_id(self) -> str:
        """Generate a unique ID for a new instance."""
        return generate_id(10, "i_")

    def register_instance(self, instance: "Instance"):
        """Register an instance for tracking."""
        self.instances[instance.id] = instance
        Console.log(f"Registered instance {instance.id}")

    def unregister_instance(self, instance: "Instance | str"):
        """Unregister an instance by object or ID."""
        if isinstance(instance, str):
            instance_id = instance
        elif isinstance(instance, Instance):
            instance_id = instance.id

        if instance_id not in self.instances:
            Console.log(f"{instance_id} is not an instance", LogType.WARNING)
            return

        self.instances.pop(instance_id, None)
        Console.log(f"{instance_id} is no longer an instance")

    def update_instances(self):
        if len(self.__queued_for_update) == 0:
            return

        for recompute_instance in self.__queued_for_update.values():
            recompute_instance()

        self.__queued_for_update.clear()

    def queue_dirty_instance_for_update(self, instance: "Instance"):
        if instance.id in self.__queued_for_update:
            return

        self.__queued_for_update[instance.id] = instance.recompute_if_needed


InstanceHandler = InstanceHandlerCls()
__all__ = ["InstanceHandler"]
