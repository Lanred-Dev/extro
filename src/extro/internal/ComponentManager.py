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
    from extro.instances.core.components.AudioSource import AudioSource


class ComponentType(Enum):
    TRANSFORM = auto()
    COLLIDER = auto()
    DRAWABLE = auto()
    PHYSICS_BODY = auto()
    ANIMATOR = auto()
    HIERARCHY = auto()
    AUDIO_SOURCE = auto()


transforms: "dict[InstanceManager.InstanceID, Transform]" = {}
colliders: "dict[InstanceManager.InstanceID, Collider]" = {}
drawables: "dict[InstanceManager.InstanceID, Drawable]" = {}
physics_bodies: "dict[InstanceManager.InstanceID, PhysicsBody]" = {}
animators: "dict[InstanceManager.InstanceID, Animator]" = {}
hierarchies: "dict[InstanceManager.InstanceID, Hierarchy]" = {}
audio_sources: "dict[InstanceManager.InstanceID, AudioSource]" = {}

component_list_map: "dict[ComponentType, dict[InstanceManager.InstanceID, Any]]" = {
    ComponentType.TRANSFORM: transforms,
    ComponentType.COLLIDER: colliders,
    ComponentType.DRAWABLE: drawables,
    ComponentType.PHYSICS_BODY: physics_bodies,
    ComponentType.ANIMATOR: animators,
    ComponentType.HIERARCHY: hierarchies,
    ComponentType.AUDIO_SOURCE: audio_sources,
}


def register(instance_id: "InstanceManager.InstanceID", type: ComponentType, component):
    component_list_map[type][instance_id] = component
    Console.log(f"Registered component {type.name} for instance {instance_id}")


def unregister(instance_id: "InstanceManager.InstanceID", type: ComponentType):
    component_list = component_list_map[type]

    if instance_id not in component_list:
        Console.log(
            f"Instance {instance_id} has no component {type.name}",
            Console.LogType.ERROR,
        )
        return

    del component_list[instance_id]
    Console.log(f"Unregistered component {type.name} for instance {instance_id}")
