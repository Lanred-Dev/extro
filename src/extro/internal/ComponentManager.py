from typing import TYPE_CHECKING, Any
from enum import Enum, auto

import extro.Console as Console

if TYPE_CHECKING:
    import extro.internal.InstanceManager as InstanceManager
    from extro.instances.core.components.Transform import Transform
    from extro.instances.core.components.Collider import Collider
    from extro.instances.core.components.Drawable import Drawable
    from extro.instances.core.components.PhysicsBody import PhysicsBody
    from extro.instances.core.components.Animator import Animator
    from extro.instances.core.components.Hierarchy import Hierarchy


class ComponentType(Enum):
    TRANSFORM = auto()
    COLLIDER = auto()
    DRAWABLE = auto()
    PHYSICS_BODY = auto()
    ANIMATOR = auto()
    HIERARCHY = auto()


transforms: "dict[InstanceManager.InstanceIDType, Transform]" = {}
colliders: "dict[InstanceManager.InstanceIDType, Collider]" = {}
drawables: "dict[InstanceManager.InstanceIDType, Drawable]" = {}
physics_bodies: "dict[InstanceManager.InstanceIDType, PhysicsBody]" = {}
animators: "dict[InstanceManager.InstanceIDType, Animator]" = {}
hierarchies: "dict[InstanceManager.InstanceIDType, Hierarchy]" = {}
component_lists: "dict[ComponentType, dict[InstanceManager.InstanceIDType, Any]]" = {
    ComponentType.TRANSFORM: transforms,
    ComponentType.COLLIDER: colliders,
    ComponentType.DRAWABLE: drawables,
    ComponentType.PHYSICS_BODY: physics_bodies,
    ComponentType.ANIMATOR: animators,
    ComponentType.HIERARCHY: hierarchies,
}


def register(
    instance_id: "InstanceManager.InstanceIDType", type: ComponentType, component
):
    component_lists[type][instance_id] = component
    Console.log(f"Registered component {type.name} for instance {instance_id}")


def unregister(instance_id: "InstanceManager.InstanceIDType"):
    for component_list in component_lists.values():
        if instance_id in component_list:
            component_list[instance_id].destroy()
            del component_list[instance_id]

    Console.log(f"Unregistered instance {instance_id} components")
