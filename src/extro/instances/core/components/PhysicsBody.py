import extro.Console as Console
from extro.instances.core.components.Component import Component
from extro.shared.Vector2C import Vector2


class PhysicsBody(Component):
    def __init__(
        self,
        mass: float,
        restitution: float = 0.2,
        is_anchored: bool = False,
    ):
        self.mass = mass
        self.restitution = restitution
        self.is_anchored = is_anchored
        self._forces = []
        self.desired_velocity = Vector2(0, 0)
        self._physics_velocity = Vector2(0, 0)
        self._actual_force_velocity = Vector2(0, 0)
        self._actual_velocity = Vector2(0, 0)

    def destroy(self):
        self._forces.clear()

    def apply_force(self, force: Vector2):
        if force.magnitude() == 0:
            Console.log(
                "Applying a force with a magnitude of 0 has no effect",
                Console.LogType.WARNING,
            )
            return

        self._forces.append(force)

    def _recalculate_inverse_mass(self):
        self._inverse_mass = 1 / self._mass if not self._is_anchored else 0

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, mass: float):
        self._mass = mass
        self._recalculate_inverse_mass()

    @property
    def is_anchored(self) -> bool:
        return self._is_anchored

    @is_anchored.setter
    def is_anchored(self, is_anchored: bool):
        self._is_anchored = is_anchored
        self._recalculate_inverse_mass()

        if is_anchored:
            self._actual_velocity = Vector2(0, 0)
            self._forces.clear()
