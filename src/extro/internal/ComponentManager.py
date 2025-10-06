from typing import TYPE_CHECKING, Any
from enum import Enum, auto

import extro.Console as Console

if TYPE_CHECKING:
    from extro.internal.InstanceManager import InstanceIDType
    from extro.instances.core.components.Transform import Transform
    from extro.instances.core.components.Collider import Collider
    from extro.instances.core.components.Drawable import Drawable
    from extro.instances.core.components.PhysicsBody import PhysicsBody
    from extro.instances.core.components.Animator import Animator


class ComponentType(Enum):
    TRANSFORM = auto()
    COLLIDER = auto()
    DRAWABLE = auto()
    PHYSICS_BODY = auto()
    ANIMATOR = auto()


transforms: "dict[InstanceIDType, Transform]" = {}
colliders: "dict[InstanceIDType, Collider]" = {}
drawables: "dict[InstanceIDType, Drawable]" = {}
physics_bodies: "dict[InstanceIDType, PhysicsBody]" = {}
animators: "dict[InstanceIDType, Animator]" = {}
component_lists: "dict[ComponentType, dict[InstanceIDType, Any]]" = {
    ComponentType.TRANSFORM: transforms,
    ComponentType.COLLIDER: colliders,
    ComponentType.DRAWABLE: drawables,
    ComponentType.PHYSICS_BODY: physics_bodies,
    ComponentType.ANIMATOR: animators,
}


def register(instance_id: "InstanceIDType", type: ComponentType, component):
    component_lists[type][instance_id] = component
    Console.log(f"Registered component {type.name} for instance {instance_id}")


def unregister(instance_id: "InstanceIDType"):
    for component_list in component_lists.values():
        if instance_id in component_list:
            component_list[instance_id].destroy()
            del component_list[instance_id]

    Console.log(f"Unregistered instance {instance_id} components")
