from typing import TYPE_CHECKING
from enum import auto, IntFlag

import extro.internal.ComponentManager as ComponentManager
import extro.services.Physics as PhysicsService
import extro.services.Timing as TimingService
from extro.shared.Vector2 import Vector2
import extro.internal.systems.Transform as TransformSystem
import extro.internal.systems.Physics.PhysicsSolver as PhysicsSolver


if TYPE_CHECKING:
    import extro.internal.systems.Collision as CollisionSystem

FORCE_MAGNITUDE_THRESHOLD: float = 0.01
PENETRATION_CORRECTION: float = 1.0
PENETRATION_SLOP: float = 0.05
ZERO_VECTOR = Vector2(0, 0)
DEFAULT_RESTITUTION: float = 0.5


class PhysicsBodyDirtyFlags(IntFlag):
    MASS = auto()


def update(collisions_data: "CollisionSystem.CollisionsData"):
    TimingService.on_pre_physics.fire()

    if len(collisions_data) > 0:
        resolve_collisions(collisions_data)

    decay: float = max(1 - (PhysicsService.dampening * TimingService.delta), 0)

    for instance_id in list(ComponentManager.physics_bodies.keys()):
        physics_body = ComponentManager.physics_bodies[instance_id]

        if physics_body.has_flag(PhysicsBodyDirtyFlags.MASS):
            physics_body._inverse_mass = (
                1 / physics_body._mass if not physics_body._is_anchored else 0
            )
            physics_body._is_dynamic = (
                not physics_body._is_anchored
                and physics_body._body_type == PhysicsService.PhysicsBodyType.DYNAMIC
            )
            physics_body.remove_flag(PhysicsBodyDirtyFlags.MASS)

        if physics_body.is_anchored:
            continue

        acting_force: Vector2 = ZERO_VECTOR.copy()
        acting_rotational_force: float = 0.0

        if len(physics_body._forces) > 0:
            for index, [force, point] in enumerate(physics_body._forces[:]):
                force.x *= decay
                force.y *= decay

                if force.magnitude() <= FORCE_MAGNITUDE_THRESHOLD:
                    physics_body._forces.pop(index)
                else:
                    acting_force += force

                    if point != ZERO_VECTOR:
                        acting_rotational_force += force.x * point.y - force.y * point.x

        transform = ComponentManager.transforms[instance_id]

        physics_body.velocity += (
            acting_force * physics_body._inverse_mass * TimingService.delta
        )

        if abs(physics_body.velocity.magnitude()) <= FORCE_MAGNITUDE_THRESHOLD:
            physics_body.velocity = Vector2(0, 0)
        else:
            physics_body.velocity *= decay
            vector: Vector2 = physics_body.velocity * TimingService.delta
            transform.position.absolute_x += vector.x
            transform.position.absolute_y += vector.y
            transform.add_flag(TransformSystem.TransformDirtyFlags.POSITION)

        physics_body.rotational_velocity += (
            acting_rotational_force * physics_body._inverse_mass * TimingService.delta
        )

        if abs(physics_body.rotational_velocity) <= FORCE_MAGNITUDE_THRESHOLD:
            physics_body.rotational_velocity = 0
        else:
            physics_body.rotational_velocity *= decay
            transform.rotation += physics_body.rotational_velocity * TimingService.delta
            transform.add_flag(TransformSystem.TransformDirtyFlags.ROTATION)


def resolve_collisions(
    collisions_data: "CollisionSystem.CollisionsData",
):
    for (instance1_id, instance2_id), (
        penetration,
        normal,
        contact_point,
    ) in collisions_data.items():
        if penetration <= PENETRATION_SLOP:
            continue

        instance1_physics_body = ComponentManager.physics_bodies.get(instance1_id)
        instance2_physics_body = ComponentManager.physics_bodies.get(instance2_id)

        if (
            not instance1_physics_body
            or not instance2_physics_body
            or instance1_physics_body._flags != 0
            or instance2_physics_body._flags != 0
        ):
            continue

        is_instance1_dynamic: bool = instance1_physics_body._is_dynamic
        is_instance2_dynamic: bool = instance2_physics_body._is_dynamic

        if not is_instance1_dynamic and not is_instance2_dynamic:
            continue

        total_inverse_mass: float = (
            instance1_physics_body._inverse_mass + instance2_physics_body._inverse_mass
        )

        if total_inverse_mass == 0:
            continue

        instance1_transform = ComponentManager.transforms[instance1_id]
        instance2_transform = ComponentManager.transforms[instance2_id]

        penetration *= PENETRATION_CORRECTION
        correction: Vector2 = normal * penetration

        (
            did_resolve,
            instance1_velocity,
            instance1_rotational_velocity,
            instance2_velocity,
            instance2_rotational_velocity,
        ) = PhysicsSolver.solve_impulse(
            normal,
            contact_point,
            min(
                instance1_physics_body.restitution,
                instance2_physics_body.restitution,
            ),
            total_inverse_mass,
            instance1_transform._bounding,
            instance1_physics_body.velocity,
            is_instance1_dynamic,
            instance1_physics_body.rotational_velocity,
            instance1_physics_body._mass,
            instance2_transform._bounding,
            instance2_physics_body.velocity,
            is_instance2_dynamic,
            instance2_physics_body.rotational_velocity,
            instance2_physics_body._mass,
        )

        if is_instance1_dynamic:
            mass_correction: float = (
                instance1_physics_body._inverse_mass / total_inverse_mass
            )
            instance1_transform._position.absolute_x -= correction.x * mass_correction
            instance1_transform._position.absolute_y -= correction.y * mass_correction
            instance1_transform.add_flag(TransformSystem.TransformDirtyFlags.POSITION)

            if did_resolve:
                instance1_physics_body.velocity.x = instance1_velocity.x
                instance1_physics_body.velocity.y = instance1_velocity.y
                instance1_physics_body.rotational_velocity = (
                    instance1_rotational_velocity
                )

        if is_instance2_dynamic:
            mass_correction: float = (
                instance2_physics_body._inverse_mass / total_inverse_mass
            )
            instance2_transform._position.absolute_x += correction.x * mass_correction
            instance2_transform._position.absolute_y += correction.y * mass_correction
            instance2_transform.add_flag(TransformSystem.TransformDirtyFlags.POSITION)

            if did_resolve:
                instance2_physics_body.velocity.x = instance2_velocity.x
                instance2_physics_body.velocity.y = instance2_velocity.y
                instance2_physics_body.rotational_velocity = (
                    instance2_rotational_velocity
                )
