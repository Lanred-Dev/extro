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
    import extro.internal.InstanceManager as InstanceManager

VELOCITY_MAGNITUDE_THRESHOLD: float = 0.01
ANGLULAR_VELOCITY_MAGNITUDE_THRESHOLD: float = 0.001
ZERO_VECTOR = Vector2(0, 0)
DEFAULT_RESTITUTION: float = 0.5


class PhysicsBodyDirtyFlags(IntFlag):
    MASS = auto()
    RESTITUTION = auto()


def update(collisions_data: "CollisionSystem.CollisionsData"):
    TimingService.on_pre_physics.fire()

    decay: float = max(1 - (PhysicsService.dampening * TimingService.delta), 0)
    updates: list = []

    for instance_id in list(ComponentManager.physics_bodies.keys()):
        physics_body = ComponentManager.physics_bodies[instance_id]
        has_flags: bool = not physics_body.is_empty()

        if physics_body.has_flag(PhysicsBodyDirtyFlags.MASS):
            physics_body._inverse_mass = (
                1 / physics_body._mass if not physics_body._is_anchored else 0
            )
            physics_body._is_dynamic = (
                not physics_body._is_anchored
                and physics_body._body_type == PhysicsService.PhysicsBodyType.DYNAMIC
            )

        if has_flags:
            physics_body.clear_flags()
            updates.append(
                (
                    instance_id,
                    physics_body._mass,
                    physics_body._inverse_mass,
                    physics_body._restitution,
                    physics_body._is_dynamic,
                )
            )

        if physics_body.is_anchored:
            continue

        acting_force: Vector2 = ZERO_VECTOR.copy()
        acting_rotational_force: float = 0.0

        if len(physics_body._forces) > 0:
            for force, point in physics_body._forces[:]:
                acting_force += (
                    force / physics_body._inverse_mass
                ) * TimingService.delta

                if point != ZERO_VECTOR:
                    acting_rotational_force += point.x * force.y - point.y * force.x

        if len(physics_body._impulses) > 0:
            for impulse, point in physics_body._impulses[:]:
                acting_force += impulse / physics_body._inverse_mass

                if point != ZERO_VECTOR:
                    acting_rotational_force += point.x * impulse.y - point.y * impulse.x

            physics_body._impulses.clear()

        transform = ComponentManager.transforms[instance_id]

        physics_body._velocity += acting_force

        if abs(physics_body._velocity.magnitude()) <= VELOCITY_MAGNITUDE_THRESHOLD:
            physics_body._velocity.x = 0
            physics_body._velocity.y = 0
        else:
            physics_body._velocity *= decay
            vector: Vector2 = physics_body._velocity * TimingService.delta
            transform.position.absolute_x += vector.x
            transform.position.absolute_y += vector.y
            transform.add_flag(TransformSystem.TransformDirtyFlags.POSITION)

        physics_body._angular_velocity.radians += (
            acting_rotational_force * physics_body._inverse_mass * TimingService.delta
        )

        if (
            abs(physics_body._angular_velocity.radians)
            <= ANGLULAR_VELOCITY_MAGNITUDE_THRESHOLD
        ):
            physics_body._angular_velocity.radians = 0
        else:
            physics_body._angular_velocity.radians *= decay
            transform._rotation.degrees += (
                physics_body._angular_velocity.degrees * TimingService.delta
            )
            transform.add_flag(TransformSystem.TransformDirtyFlags.ROTATION)

    PhysicsSolver.step(updates)

    # This happens at the end of the physics update to ensure all physics bodies have been updated
    if len(collisions_data) > 0:
        resolve_collisions(collisions_data)


def resolve_collisions(
    collisions_data: "CollisionSystem.CollisionsData",
):
    updated_instances: "list[InstanceManager.InstanceID]" = (
        PhysicsSolver.resolve_collisions(collisions_data)
    )

    for instance_id in updated_instances:
        transform = ComponentManager.transforms[instance_id]
        transform.add_flag(TransformSystem.TransformDirtyFlags.POSITION)
