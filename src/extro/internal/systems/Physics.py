from typing import TYPE_CHECKING
from enum import auto, IntFlag

import extro.internal.ComponentManager as ComponentManager
import extro.services.Physics as PhysicsService
import extro.services.Timing as TimingService
from extro.shared.Vector2C import Vector2
import extro.internal.systems.Transform as TransformSystem


if TYPE_CHECKING:
    import extro.internal.systems.Collision as CollisionSystem

FORCE_MAGNITUDE_THRESHOLD: float = 0.01
PENETRATION_SLOP: float = 0.05


class PhysicsBodyDirtyFlags(IntFlag):
    MASS = auto()


def update():
    TimingService.on_pre_physics.fire()

    decay: float = max(1 - (PhysicsService.dampening * TimingService.delta), 0)

    for instance_id, physics_body in ComponentManager.physics_bodies.items():
        if physics_body.has_flag(PhysicsBodyDirtyFlags.MASS):
            physics_body._inverse_mass = (
                1 / physics_body._mass if not physics_body._is_anchored else 0
            )
            physics_body.remove_flag(PhysicsBodyDirtyFlags.MASS)

        if physics_body.is_anchored:
            continue

        acting_force: Vector2 = Vector2(0, 0)
        acting_rotational_force: float = 0.0

        if len(physics_body._forces) > 0:
            for index, [force, point] in enumerate(physics_body._forces[:]):
                force.x *= decay
                force.y *= decay

                if force.magnitude() <= FORCE_MAGNITUDE_THRESHOLD:
                    physics_body._forces.pop(index)
                else:
                    acting_force += force

                    if point != Vector2(0, 0):
                        torque: float = force.x * point.y - force.y * point.x
                        acting_rotational_force += torque / physics_body._mass

        transform = ComponentManager.transforms[instance_id]

        physics_body.velocity += (
            acting_force * physics_body._inverse_mass * TimingService.delta
        )

        velocity_magnitude: float = physics_body.velocity.magnitude()
        if 0 < velocity_magnitude <= FORCE_MAGNITUDE_THRESHOLD:
            physics_body.velocity = Vector2(0, 0)
            continue
        elif velocity_magnitude > FORCE_MAGNITUDE_THRESHOLD:
            physics_body.velocity *= decay
            x, y = (physics_body.velocity * TimingService.delta).to_tuple()
            transform.position.absolute_x += x
            transform.position.absolute_y += y
            transform.add_flag(TransformSystem.TransformDirtyFlags.POSITION)

        physics_body.rotational_velocity += (
            acting_rotational_force * physics_body._inverse_mass * TimingService.delta
        )

        if abs(physics_body.rotational_velocity) <= FORCE_MAGNITUDE_THRESHOLD:
            physics_body.rotational_velocity = 0
        else:
            physics_body.rotational_velocity *= decay
            transform = ComponentManager.transforms[instance_id]
            transform.rotation += physics_body.rotational_velocity * TimingService.delta
            transform.add_flag(TransformSystem.TransformDirtyFlags.ROTATION)


def resolve_collisions(
    collisions_data: "CollisionSystem.CollisionsData",
):
    for (instance1_id, instance2_id), (
        normal,
        penetration,
        contact_point,
    ) in collisions_data.items():
        if penetration <= PENETRATION_SLOP:
            continue

        penetration -= PENETRATION_SLOP

        instance1_transform = ComponentManager.transforms[instance1_id]
        instance2_transform = ComponentManager.transforms[instance2_id]
        instance1_physics_body = ComponentManager.physics_bodies[instance1_id]
        instance2_physics_body = ComponentManager.physics_bodies[instance2_id]

        total_inverse_mass: float = (
            instance1_physics_body._inverse_mass + instance2_physics_body._inverse_mass
        )

        if total_inverse_mass == 0:
            return

        penetration -= PENETRATION_SLOP
        correction_x: float = normal[0] * penetration
        correction_y: float = normal[1] * penetration

        is_instance1_dynamic: bool = (
            not instance1_physics_body._is_anchored
            and instance1_physics_body._body_type
            == PhysicsService.PhysicsBodyType.DYNAMIC
        )
        is_instance2_dynamic: bool = (
            not instance2_physics_body._is_anchored
            and instance2_physics_body._body_type
            == PhysicsService.PhysicsBodyType.DYNAMIC
        )

        # Its only worth calculating the impulse if at least one body is dynamic
        if is_instance1_dynamic or is_instance2_dynamic:
            relative_velocity: Vector2 = (
                instance2_physics_body.velocity - instance1_physics_body.velocity
            )

        if is_instance1_dynamic:
            mass_correction: float = (
                instance1_physics_body._inverse_mass / total_inverse_mass
            )
            instance1_transform.position.absolute_x += correction_x * mass_correction
            instance1_transform.position.absolute_y += correction_y * mass_correction
            instance1_transform.add_flag(TransformSystem.TransformDirtyFlags.POSITION)

        if is_instance2_dynamic:
            mass_correction: float = (
                instance2_physics_body._inverse_mass / total_inverse_mass
            )
            instance2_transform.position.absolute_x -= correction_x * mass_correction
            instance2_transform.position.absolute_y -= correction_y * mass_correction
            instance2_transform.add_flag(TransformSystem.TransformDirtyFlags.POSITION)
