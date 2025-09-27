from libc.math cimport fabs

import extro.Console as Console
import extro.internal.Engine as Engine
import extro.internal.InstanceManager as InstanceManager
import extro.services.Physics as PhysicsService
from extro.shared.Vector2 cimport Vector2
from extro.core.components.PhysicsBody cimport PhysicsBody

ctypedef object Instance

cdef float penetration_slop = 0.05
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
    PhysicsService.on_pre_physics.fire()

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

        for index in range(len(physics_body._forces) - 1, -1, -1):
            current_force = physics_body._forces[index]
            total_force = total_force.__cadd__(current_force)
            physics_body._forces[index] = current_force.__cmul_float__(PhysicsService.dampening)

            if fabs(<double>current_force.magnitude()) < 0.01:
                physics_body._forces.pop(index)

        physics_body._actual_force_velocity = physics_body._actual_force_velocity.__cadd__(total_force.__ctruediv_float__(physics_body._actual_mass).__cmul_float__(Engine.delta)).__cmul_float__(force_decay)

        if physics_body._physics_velocity.magnitude() > 0:
            physics_body._physics_velocity = physics_body._physics_velocity.__cmul_float__(force_decay)

        physics_body._actual_velocity = physics_body._physics_velocity.__cadd__(physics_body.desired_velocity).__cadd__(physics_body._actual_force_velocity)

        if physics_body._actual_velocity.magnitude() == 0:
            continue

        # Not using `__cadd__` because `_actual_position` is a python Vector2 object
        instance._actual_position = instance._actual_position.__add__(physics_body._actual_velocity.__cmul_float__(Engine.delta))
        instance._apply_position()

cdef position_correction(Vector2 normal, float penetration, Instance instance1, Instance instance2):
    if penetration <= penetration_slop:
        return

    cdef PhysicsBody physics_body1 = instance1.physics_body
    cdef PhysicsBody physics_body2 = instance2.physics_body
    cdef Vector2 correction = normal.__cmul_float__(penetration - penetration_slop)

    if physics_body1._is_anchored and not physics_body2._is_anchored:
        instance2._actual_position = instance2._actual_position.__add__(correction)
    elif physics_body2._is_anchored and not physics_body1._is_anchored:
        instance1._actual_position = instance1._actual_position.__sub__(correction)
    elif not physics_body1._is_anchored and not physics_body2._is_anchored:
        correction = correction.__cmul_float__(0.5)
        instance1._actual_position = instance1._actual_position.__sub__(correction)
        instance2._actual_position = instance2._actual_position.__add__(correction)


cdef resolve_impulse(Vector2 normal, float penetration, Instance instance1, Instance instance2):
    cdef PhysicsBody physics_body1 = instance1.physics_body
    cdef PhysicsBody physics_body2 = instance2.physics_body

    # Relative velocity along the collision normal
    cdef Vector2 relative_velocity = physics_body2._actual_velocity.__csub__(physics_body1._actual_velocity)
    cdef float velocity_along_normal = relative_velocity.__cdot__(normal)

    if velocity_along_normal > 0:
        return  # moving apart, no impulse needed

    # Effective restitution
    cdef float e = min(physics_body1.restitution, physics_body2.restitution)

    # Skip impulse entirely if one object is anchored and restitution is 0
    if (physics_body1._is_anchored != physics_body2._is_anchored) and e == 0:
        return

    # Impulse scalar
    cdef float j = -(1 + e) * velocity_along_normal

    cdef float instance_velocity_along_normal

    # Apply impulse only to non-anchored bodies
    if not physics_body1._is_anchored:
        physics_body1._physics_velocity = physics_body1._physics_velocity.__csub__(normal.__cmul_float__(j))
        if e == 0:
            # zero out velocity along normal
            instance_velocity_along_normal = physics_body1._physics_velocity.__cdot__(normal)
            if instance_velocity_along_normal > 0:
                physics_body1._physics_velocity = physics_body1._physics_velocity.__csub__(normal.__cmul_float__(instance_velocity_along_normal))

    if not physics_body2._is_anchored:
        physics_body2._physics_velocity = physics_body2._physics_velocity.__cadd__(normal.__cmul_float__(j))
        if e == 0:
            # zero out velocity along normal
            instance_velocity_along_normal = physics_body2._physics_velocity.__cdot__(normal)
            if instance_velocity_along_normal < 0:
                physics_body2._physics_velocity = physics_body2._physics_velocity.__csub__(normal.__cmul_float__(instance_velocity_along_normal))


cpdef resolve_collisions(list[tuple[int, int]] collisions, dict[tuple[int, int], tuple[Vector2, float]] collisions_data):
    cdef Instance instance1
    cdef Instance instance2
    cdef Vector2 normal
    cdef float penetration

    for collision_index in range(len(collisions)):
        instance1_id, instance2_id = collisions[collision_index]

        if instance1_id not in instances or instance2_id not in instances:
            continue

        normal, penetration = collisions_data[(instance1_id, instance2_id)]

        instance1 = InstanceManager.instances[instance1_id]
        instance2 = InstanceManager.instances[instance2_id]
        position_correction(normal, penetration, instance1, instance2)
        resolve_impulse(normal, penetration, instance1, instance2)
