import src.internal.Console as Console
import src.internal.handlers.InstanceManager as InstanceManager
from src.values.Vector2 import Vector2
import src.internal.Engine as Engine

# pixels per second^2
force_dampening: float = 0.6
_instances: set[str] = set()


def register(instance_id: str):
    if instance_id in _instances:
        Console.log(
            f"{instance_id} is already registered as a physics body",
            Console.LogType.WARNING,
        )
        return

    _instances.add(instance_id)
    Console.log(f"{instance_id} was registered as a physics body")


def unregister(instance_id: str):
    if instance_id not in _instances:
        Console.log(
            f"{instance_id} does not exist as a physics body",
            Console.LogType.ERROR,
        )
        return

    _instances.remove(instance_id)
    Console.log(f"{instance_id} was unregistered as a physics body")


def _update():
    for instance_id in _instances:
        instance = InstanceManager.instances[instance_id]
        physics_body = instance.physics_body

        if physics_body.anchored:
            continue

        total_force: Vector2 = sum(physics_body._forces, Vector2(0, 0))
        force_decay: float = max(1 - (force_dampening * Engine.delta), 0)

        # Apply friction to the forces so that they dont last forever
        for index in range(len(physics_body._forces)):
            physics_body._forces[index] *= force_decay

            if abs(physics_body._forces[index].magnitude()) < 0.01:
                physics_body._forces.remove(physics_body._forces[index])

        total_force_acceleration: Vector2 = total_force / physics_body.mass
        physics_body._actual_force_velocity += total_force_acceleration * Engine.delta
        physics_body._actual_force_velocity *= force_decay

        physics_body._actual_velocity = (
            physics_body.velocity + physics_body._actual_force_velocity
        )

        if physics_body._actual_velocity.magnitude() == 0:
            continue

        instance._actual_position += physics_body._actual_velocity * Engine.delta
        instance._apply_position()


def _resolve_collisions(collisions: list[tuple[str, str]]):
    for instance1_id, instance2_id in collisions:
        if instance1_id not in _instances or instance2_id not in _instances:
            continue

        instance1 = InstanceManager.instances[instance1_id]
        physics_body1 = instance1.physics_body

        if not physics_body1.anchored:
            physics_body1._actual_velocity = -physics_body1._actual_velocity

        instance2 = InstanceManager.instances[instance2_id]
        physics_body2 = instance2.physics_body

        if not physics_body2.anchored:
            physics_body2._actual_velocity = -physics_body2._actual_velocity


def set_force_dampening(value: float):
    global force_dampening
    force_dampening = value


__all__ = [
    "force_dampening",
    "_update",
    "register",
    "unregister",
    "_resolve_collisions",
    "set_force_dampening",
]
