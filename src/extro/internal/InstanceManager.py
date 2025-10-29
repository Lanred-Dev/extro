from typing import TYPE_CHECKING

import extro.internal.services.Identity as IdentityService
import extro.Console as Console

if TYPE_CHECKING:
    from extro.instances.core.Instance import Instance

    InstanceID = int

instances: "dict[InstanceID, Instance]" = {}


def register(instance: "Instance"):
    id: "InstanceID" = IdentityService.generate_ordered_numeric_id()
    instance._id = id
    instances[id] = instance
    Console.log(f"Registered instance {id}")


def unregister(instance_id: "InstanceID"):
    global instances

    if instance_id not in instances:
        Console.log(f"{instance_id} is not an instance", Console.LogType.ERROR)
        return

    del instances[instance_id]
    Console.log(f"{instance_id} is no longer an instance", Console.LogType.DEBUG)
