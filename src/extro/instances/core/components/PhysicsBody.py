from typing import TYPE_CHECKING

import extro.Console as Console
from extro.instances.core.components.Component import Component
from extro.shared.Vector2 import Vector2
import extro.internal.systems.Physics as PhysicsSystem
import extro.internal.ComponentManager as ComponentManager
import extro.services.Physics as PhysicsService

if TYPE_CHECKING:
    import extro.internal.InstanceManager as InstanceManager


class PhysicsBody(Component):
    __slots__ = Component.__slots__ + (
        "restitution",
        "_mass",
        "_inverse_mass",
        "_is_anchored",
        "_forces",
        "velocity",
        "_body_type",
        "rotational_velocity",
        "_is_dynamic",
    )

    _key = "physics_body"

    restitution: float
    _mass: float
    _inverse_mass: float
    _is_anchored: bool
    _forces: list[tuple[Vector2, Vector2]]
    velocity: Vector2
    rotational_velocity: float
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
        self.velocity = Vector2(0, 0)
        self.rotational_velocity = 0
        self.mass = mass
        self.restitution = restitution
        self._body_type = body_type
        self.is_anchored = is_anchored

    def destroy(self):
        super().destroy()
        self._forces.clear()

    def add_force(self, force: Vector2, point: Vector2 = Vector2(0.5, 0.5)):
        if force.magnitude() == 0:
            Console.log(
                "Applying a force with a magnitude of 0 has no effect",
                Console.LogType.WARNING,
            )
            return

        self._forces.append((force.copy(), Vector2(point.x - 0.5, point.y - 0.5)))

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
            self.velocity = Vector2(0, 0)
            self.rotational_velocity = 0
            self._forces.clear()

    @property
    def is_dynamic(self) -> bool:
        return self._is_dynamic
