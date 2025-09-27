import extro.Console as Console
from extro.shared.Vector2 cimport Vector2


cdef class PhysicsBody:
    def __init__(self, owner_id: int, mass: float, restitution: float = 0.2, is_anchored: bool = False):
        self.mass = mass
        self.restitution = restitution
        self._forces = []
        self.desired_velocity = Vector2(0, 0)
        self._physics_velocity = Vector2(0, 0)
        self._actual_force_velocity = Vector2(0, 0)
        self._actual_velocity = Vector2(0, 0)
        self._is_anchored = <bint>is_anchored
        self._owner_id = owner_id

    def destroy(self):
        self._forces.clear()

    cpdef apply_force(self, Vector2 force):
        if force.magnitude() == 0:
            Console.log(
                "Applying a force with a magnitude of 0 has no effect",
                Console.LogType.WARNING,
            )
            return

        self._forces.append(force)

    cdef _recalculate_actual_mass(self):
        self._actual_mass = 1 / self._mass if not self._is_anchored else 0

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, mass: float):
        self._mass = mass
        self._recalculate_actual_mass()

    @property
    def is_anchored(self) -> bint:
        return self._is_anchored

    @is_anchored.setter
    def is_anchored(self, is_anchored: bool):
        self._is_anchored = <bint>is_anchored
        self._recalculate_actual_mass()

        if is_anchored:
            self._actual_velocity = Vector2(0, 0)
            self._forces.clear()