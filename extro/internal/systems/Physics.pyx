from libc.math cimport fabs

import extro.Console as Console
import extro.internal.Engine as Engine
import extro.internal.InstanceManager as InstanceManager
import extro.services.Physics as PhysicsService
from extro.shared.Vector2 cimport Vector2
from extro.core.components.PhysicsBody cimport PhysicsBody

ctypedef object Instance

cdef set[int] instances = set()


def register(instance_id: int):
    if instance_id in instances:
        Console.log(
            f"{instance_id} is already registered as a physics body",
            Console.LogType.WARNING,
        )
        return

    instances.add(instance_id)
    Console.log(f"{instance_id} was registered as a physics body")


def unregister(instance_id: int):
    if instance_id not in instances:
        Console.log(
            f"{instance_id} does not exist as a physics body",
            Console.LogType.ERROR,
        )
        return

    instances.remove(instance_id)
    Console.log(f"{instance_id} was unregistered as a physics body")


cpdef update():
    cdef Instance instance
    cdef PhysicsBody physics_body
    cdef Vector2 total_force
    cdef Vector2 current_force
    cdef float force_decay = 1 - (PhysicsService.dampening * Engine.delta)
    cdef int index

    if force_decay < 0:
        force_decay = 0

    for instance_id in instances:
        instance = InstanceManager.instances[instance_id]
        physics_body = instance.physics_body

        if physics_body._is_anchored:
            continue

        total_force = Vector2(0, 0)

        index = 0

        while index < len(physics_body._forces):
            current_force = physics_body._forces[index]
            total_force = total_force.__cadd__(current_force)
            physics_body._forces[index] = current_force.__cmul_float__(PhysicsService.dampening)

            if fabs(<double>current_force.magnitude()) < 0.01:
                physics_body._forces.remove(current_force)
            else:
                index += 1

        physics_body._actual_force_velocity = physics_body._actual_force_velocity.__cadd__(total_force.__ctruediv_float__(physics_body.mass).__cmul_float__(Engine.delta)).__cmul_float__(force_decay)

        physics_body._actual_velocity = physics_body.velocity.__cadd__(physics_body._actual_force_velocity)

        if physics_body._actual_velocity.magnitude() == 0:
            continue

        # Not using `__cadd__` because `_actual_position` is a python Vector2 object
        instance._actual_position = instance._actual_position.__add__(physics_body._actual_velocity.__cmul_float__(Engine.delta))
        instance._apply_position()


def resolve_collisions(collisions: list[tuple[int, int]]):
    for instance1_id, instance2_id in collisions:
        if instance1_id not in instances or instance2_id not in instances:
            continue

        instance1 = InstanceManager.instances[instance1_id]
        physics_body1 = instance1.physics_body

        if not physics_body1._is_anchored:
            physics_body1._actual_velocity = -physics_body1._actual_velocity

        instance2 = InstanceManager.instances[instance2_id]
        physics_body2 = instance2.physics_body

        if not physics_body2._is_anchored:
            physics_body2._actual_velocity = -physics_body2._actual_velocity