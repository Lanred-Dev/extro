from typing import TYPE_CHECKING

import extro.Console as Console
from extro.instances.core.components.Component import Component
from extro.shared.Vector2 import Vector2
from extro.shared.Angle import Angle
import extro.internal.systems.Physics as PhysicsSystem
import extro.internal.systems.Physics.PhysicsSolver as PhysicsSolver
import extro.internal.ComponentManager as ComponentManager
import extro.services.Physics as PhysicsService

if TYPE_CHECKING:
    import extro.internal.InstanceManager as InstanceManager


class PhysicsBody(Component):
    __slots__ = Component.__slots__ + (
        "_restitution",
        "_mass",
        "_inverse_mass",
        "_is_anchored",
        "_forces",
        "_impulses",
        "_velocity",
        "_body_type",
        "_angular_velocity",
        "_is_dynamic",
    )

    _key = "physics_body"

    _restitution: float
    _mass: float
    _inverse_mass: float
    _is_anchored: bool
    _forces: list[tuple[Vector2, Vector2]]
    _impulses: list[tuple[Vector2, Vector2]]
    _velocity: Vector2
    _angular_velocity: Angle
    _body_type: PhysicsService.PhysicsBodyType
    _is_dynamic: bool

    def __init__(
        self,
        owner: "InstanceManager.InstanceID",
        mass: float,
        restitution: float = PhysicsSystem.DEFAULT_RESTITUTION,
        is_anchored: bool = False,
        body_type: PhysicsService.PhysicsBodyType = PhysicsService.PhysicsBodyType.DYNAMIC,
    ):
        super().__init__(owner, ComponentManager.ComponentType.PHYSICS_BODY)

        self._forces = []
        self._impulses = []
        self._velocity = Vector2(0, 0)
        self._angular_velocity = Angle(0)
        self.mass = mass
        self._restitution = restitution
        self._body_type = body_type
        self.is_anchored = is_anchored

        transform = ComponentManager.transforms[owner]
        PhysicsSolver.create_physics_body(
            owner,
            transform._actual_size,
            transform._actual_position,
            transform._rotation,
            self._velocity,
            self._angular_velocity,
        )

    def destroy(self):
        super().destroy()

        self._forces.clear()
        PhysicsSolver.destroy_physics_body(self._owner)

    def add_force(self, force: Vector2, point: Vector2 = Vector2(0.5, 0.5)):
        """Applies a continuous force to the physics body."""
        if force.magnitude() == 0:
            Console.log(
                "Applying a force with a magnitude of 0 has no effect",
                Console.LogType.WARNING,
            )
            return

        self._forces.append((force.copy(), Vector2(point.x - 0.5, point.y - 0.5)))

    def add_impulse(self, impulse: Vector2, point: Vector2 = Vector2(0.5, 0.5)):
        """Applies an instantaneous change in velocity to the physics body."""
        if impulse.magnitude() == 0:
            Console.log(
                "Applying an impulse with a magnitude of 0 has no effect",
                Console.LogType.WARNING,
            )
            return

        self._impulses.append((impulse.copy(), Vector2(point.x - 0.5, point.y - 0.5)))

    def clear_forces(self):
        """Clears all forces applied to the physics body."""
        self._forces.clear()

    @property
    def body_type(self) -> PhysicsService.PhysicsBodyType:
        return self._body_type

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, mass: float):
        self._mass = mass
        self.add_flag(PhysicsSystem.PhysicsBodyDirtyFlags.MASS)

    @property
    def is_anchored(self) -> bool:
        return self._is_anchored

    @is_anchored.setter
    def is_anchored(self, is_anchored: bool):
        self._is_anchored = is_anchored
        self.add_flag(PhysicsSystem.PhysicsBodyDirtyFlags.MASS)

        if is_anchored:
            self._velocity.x = 0
            self._velocity.y = 0
            self._angular_velocity.radians = 0
            self.clear_forces()

    @property
    def is_dynamic(self) -> bool:
        return self._is_dynamic

    @property
    def restitution(self) -> float:
        return self._restitution

    @restitution.setter
    def restitution(self, restitution: float):
        self._restitution = restitution
        self.add_flag(PhysicsSystem.PhysicsBodyDirtyFlags.RESTITUTION)

    @property
    def velocity(self) -> Vector2:
        return self._velocity
    
    @velocity.setter
    def velocity(self, velocity: Vector2):
        self._velocity.x = velocity.x
        self._velocity.y = velocity.y
    
    @property
    def angular_velocity(self) -> Angle:
        return self._angular_velocity
    
    @angular_velocity.setter
    def angular_velocity(self, angular_velocity: float):
        self._angular_velocity.degrees = angular_velocity
