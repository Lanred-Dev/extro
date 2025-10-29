from typing import TYPE_CHECKING, Callable

import extro.Console as Console

if TYPE_CHECKING:
    from extro.shared.types import EmptyFunction
    import extro.internal.InstanceManager as InstanceManager

    PreRegisterCheck = Callable[[InstanceManager.InstanceID], bool]


class InstanceRegistry:
    __slots__ = ("instances", "_name", "_preregister_check", "_on_list_change")

    instances: "list[InstanceManager.InstanceID]"
    _name: str
    _preregister_check: "PreRegisterCheck | None"
    _on_list_change: "EmptyFunction"

    def __init__(
        self,
        name: str,
        on_list_change: "EmptyFunction" = lambda: None,
        preregister_check: "PreRegisterCheck | None" = None,
    ):
        self.instances = []
        self._name = name
        self._on_list_change = on_list_change
        self._preregister_check = preregister_check

    def register(self, instance_id: "InstanceManager.InstanceID"):
        if instance_id in self.instances:
            Console.log(
                f"{self._name} already has instance {instance_id} registered",
                Console.LogType.WARNING,
            )
            return
        elif self._preregister_check and not self._preregister_check(instance_id):
            Console.log(
                f"{self._name} cannot register instance {instance_id} due to preregister check failure",
                Console.LogType.WARNING,
            )
            return

        self.instances.append(instance_id)
        self._on_list_change()

    def unregister(self, instance_id: "InstanceManager.InstanceID"):
        if instance_id not in self.instances:
            Console.log(
                f"{self._name} does not have instance {instance_id} registered",
                Console.LogType.WARNING,
            )
            return

        self.instances.remove(instance_id)
        self._on_list_change()
