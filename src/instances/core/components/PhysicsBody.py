import src.internal.Console as Console
import src.internal.Engine as Engine
from src.values.Vector2 import Vector2


class PhysicsBody:
    _owner_id: str
    _mass: float
    _forces: list[Vector2]
    velocity: Vector2
    _actual_force_velocity: Vector2
    _actual_velocity: Vector2
    _anchored: bool

    def __init__(self, owner_id: str, mass: float, anchored: bool = False):
        self._mass = mass
        self._forces = []
        self.velocity = Vector2(0, 0)
        self._actual_force_velocity = Vector2(0, 0)
        self._actual_velocity = Vector2(0, 0)
        self._anchored = anchored
        self._owner_id = owner_id

    def destroy(self):
        self._forces.clear()

    def apply_force(self, force: Vector2):
        if force == Vector2(0, 0):
            Console.log(
                "Applying a force with a magnitude of 0 has no effect",
                Console.LogType.WARNING,
            )
            return

        self._forces.append(force)

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, mass: float):
        self._mass = mass

    @property
    def anchored(self) -> bool:
        return self._anchored

    @anchored.setter
    def anchored(self, anchored: bool):
        self._anchored = anchored

        if anchored:
            self._actual_velocity = Vector2(0, 0)
            self._forces.clear()
