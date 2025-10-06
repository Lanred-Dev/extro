from typing import TYPE_CHECKING

import extro.internal.services.Identity as IdentityService
import extro.Console as Console
import extro.internal.ComponentManager as ComponentManager

if TYPE_CHECKING:
    from extro.instances.core.Instance import Instance

    InstanceIDType = int

instances: "dict[InstanceIDType, Instance]" = {}


def register(instance: "Instance"):
    id: "InstanceIDType" = IdentityService.generate_ordered_numeric_id()
    instance._id = id
    instances[id] = instance
    Console.log(f"Registered instance {id}")


def unregister(instance_id: "InstanceIDType"):
    global instances

    if instance_id not in instances:
        Console.log(f"{instance_id} is not an instance", Console.LogType.ERROR)
        return

    del instances[instance_id]
    ComponentManager.unregister(instance_id)
    Console.log(f"{instance_id} is no longer an instance", Console.LogType.DEBUG)
